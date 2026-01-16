from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import uvicorn

app = FastAPI(title="UIDAI Risk Engine API", version="2.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Data Store
class DataStore:
    df = None

@app.on_event("startup")
def load_data():
    """Load and preprocess data on server startup"""
    try:
        # 1. Load the dataset
        df = pd.read_csv("UIDAI_Final_Dashboard_Dataset.csv")
        
        # 2. Rename columns to match Frontend expectations
        column_mapping = {
            'district': 'District',
            'state': 'State',
            'enrol_total_enrolments': 'Total_Enrolment',
            'bio_total_bio_updates': 'Pending_Biometrics', 
            
            # Risk Flags
            'bio_FUTURE_SURGE_RISK': 'Flag_Future_Surge_Risk',
            'bio_INFRA_STRESS': 'Flag_Infra_Stress',
            'bio_LOW_CHILD_COMPLIANCE': 'Flag_Low_Child_Compliance',
            'bio_ADULT_SPIKE': 'Flag_Catch_Up_Spike',
            
            # Raw Metrics
            'enrol_saturation_index': 'Enrolment_Health_Index', 
            'demo_persistent_friction_score': 'Demographic_Stability_Index',
            'bio_Bio_Stress_Index': 'Biometric_Compliance_Index', 
            'Friction_Intensity_Score': 'ALHS_Score' 
        }
        
        existing_cols = [c for c in column_mapping.keys() if c in df.columns]
        df = df[existing_cols].rename(columns=column_mapping)
        df.fillna(0, inplace=True)
        
        # 3. Clean and Normalize Data
        flag_cols = ['Flag_Future_Surge_Risk', 'Flag_Infra_Stress', 'Flag_Low_Child_Compliance', 'Flag_Catch_Up_Spike']
        for col in flag_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).map({'True': 1, 'False': 0, '1': 1, '0': 0, '1.0': 1, '0.0': 0}).fillna(0).astype(int)

        def normalize(series):
            if series.max() == series.min(): return 0
            return (series - series.min()) / (series.max() - series.min())

        # Normalize Scores to 0-1 range for Radar Charts
        if 'ALHS_Score' in df.columns: df['ALHS_Score'] = normalize(df['ALHS_Score'])
        if 'Enrolment_Health_Index' in df.columns: df['Enrolment_Health_Index'] = normalize(df['Enrolment_Health_Index'])
        
        # Invert specific metrics where "High Score" in CSV meant "Bad Performance"
        # We want 1.0 = Good Health for Radar Charts
        if 'Demographic_Stability_Index' in df.columns: df['Demographic_Stability_Index'] = 1 - normalize(df['Demographic_Stability_Index'])
        if 'Biometric_Compliance_Index' in df.columns: df['Biometric_Compliance_Index'] = 1 - normalize(df['Biometric_Compliance_Index'])

        DataStore.df = df
        print("✅ Data Loaded & Processed Successfully")
        print(f"📊 Total Records: {len(df)}")
        print(f"🌍 States: {df['State'].nunique()}")
        print(f"🏙️ Districts: {df['District'].nunique()}")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        # Dummy Fallback
        DataStore.df = pd.DataFrame()

@app.get("/")
def health_check():
    return {
        "status": "active", 
        "system": "UIDAI Lifecycle Intelligence",
        "version": "2.0",
        "records": len(DataStore.df) if DataStore.df is not None else 0
    }

@app.get("/api/summary")
def get_summary(state: str = "All India"):
    df = DataStore.df
    if df is None or df.empty: 
        return {
            "critical_districts": 0,
            "avg_compliance": 0,
            "pending_updates": 0,
            "system_health": 0,
            "high_risk_districts": 0,
            "moderate_risk_districts": 0,
            "total_districts": 0
        }
    
    if state != "All India": 
        df = df[df['State'] == state]
    
    # Enhanced metrics
    high_risk = df[df['ALHS_Score'] > 0.7].shape[0]
    moderate_risk = df[(df['ALHS_Score'] > 0.4) & (df['ALHS_Score'] <= 0.7)].shape[0]
    
    return {
        "critical_districts": int(high_risk),
        "avg_compliance": round(float(df['Biometric_Compliance_Index'].mean()), 4),
        "pending_updates": int(df['Pending_Biometrics'].sum()),
        "system_health": round(float(1 - df['ALHS_Score'].mean()), 3),
        "high_risk_districts": int(high_risk),
        "moderate_risk_districts": int(moderate_risk),
        "total_districts": int(len(df))
    }

@app.get("/api/dataset")
def get_dataset(state: str = "All India"):
    df = DataStore.df
    if df is None or df.empty: return []
    if state != "All India": df = df[df['State'] == state]
    return df.to_dict(orient="records")

@app.get("/api/states")
def get_states():
    """Get list of all states"""
    df = DataStore.df
    if df is None or df.empty: return []
    return sorted(df['State'].unique().tolist())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)