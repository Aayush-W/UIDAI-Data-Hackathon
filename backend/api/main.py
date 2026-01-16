"""
FastAPI Backend for UIDAI Dashboard
Provides REST API endpoints for data retrieval and analytics
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="UIDAI Aadhaar Lifecycle Risk API",
    description="Backend API for district-level risk analytics",
    version="1.0.0"
)

# CORS middleware for Streamlit connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class DistrictMetrics(BaseModel):
    district_id: str
    district_name: str
    state: str
    population: int
    ehi: float
    dsi: float
    bci: float
    alhs: float
    low_child_compliance: int
    infra_stress: int
    catchup_spike: int
    future_surge: int
    flags_count: int
    risk_category: str
    last_updated: str


class SummaryStats(BaseModel):
    total_districts: int
    critical_districts: int
    high_risk_districts: int
    medium_risk_districts: int
    low_risk_districts: int
    avg_alhs: float
    total_flags: int
    total_population: int


class StateStats(BaseModel):
    state: str
    district_count: int
    avg_alhs: float
    total_flags: int
    population: int
    critical_count: int


# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load district metrics from CSV"""
    data_path = os.getenv('DATA_PATH', './data/processed/district_metrics.csv')
    
    if not Path(data_path).exists():
        raise FileNotFoundError(
            f"Data file not found at {data_path}. "
            "Run 'python data/sample_generator.py' first."
        )
    
    df = pd.read_csv(data_path)
    return df


# Cache data in memory (in production, use Redis or similar)
_data_cache = None

def get_data():
    """Get cached data or load from file"""
    global _data_cache
    if _data_cache is None:
        _data_cache = load_data()
    return _data_cache


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "UIDAI Risk Analytics API",
        "version": "1.0.0"
    }


@app.get("/api/summary", response_model=SummaryStats)
async def get_summary_stats():
    """Get national-level summary statistics"""
    df = get_data()
    
    return SummaryStats(
        total_districts=len(df),
        critical_districts=len(df[df['risk_category'] == 'Critical']),
        high_risk_districts=len(df[df['risk_category'] == 'High']),
        medium_risk_districts=len(df[df['risk_category'] == 'Medium']),
        low_risk_districts=len(df[df['risk_category'] == 'Low']),
        avg_alhs=round(df['alhs'].mean(), 2),
        total_flags=int(df['flags_count'].sum()),
        total_population=int(df['population'].sum())
    )


@app.get("/api/districts", response_model=List[DistrictMetrics])
async def get_districts(
    state: Optional[str] = Query(None, description="Filter by state"),
    risk_category: Optional[str] = Query(None, description="Filter by risk category"),
    min_alhs: Optional[float] = Query(None, description="Minimum ALHS score"),
    limit: Optional[int] = Query(None, description="Limit number of results")
):
    """Get district-level metrics with optional filters"""
    df = get_data()
    
    # Apply filters
    if state:
        df = df[df['state'] == state]
    
    if risk_category:
        df = df[df['risk_category'] == risk_category]
    
    if min_alhs:
        df = df[df['alhs'] >= min_alhs]
    
    # Sort by ALHS descending
    df = df.sort_values('alhs', ascending=False)
    
    # Limit results
    if limit:
        df = df.head(limit)
    
    return df.to_dict('records')


@app.get("/api/districts/{district_id}", response_model=DistrictMetrics)
async def get_district_by_id(district_id: str):
    """Get metrics for a specific district"""
    df = get_data()
    
    district = df[df['district_id'] == district_id]
    
    if district.empty:
        raise HTTPException(status_code=404, detail="District not found")
    
    return district.iloc[0].to_dict()


@app.get("/api/states", response_model=List[StateStats])
async def get_state_stats():
    """Get aggregated statistics by state"""
    df = get_data()
    
    state_stats = df.groupby('state').agg({
        'district_id': 'count',
        'alhs': 'mean',
        'flags_count': 'sum',
        'population': 'sum'
    }).reset_index()
    
    state_stats.columns = ['state', 'district_count', 'avg_alhs', 'total_flags', 'population']
    state_stats['avg_alhs'] = state_stats['avg_alhs'].round(2)
    
    # Count critical districts per state
    critical_counts = df[df['risk_category'] == 'Critical'].groupby('state').size()
    state_stats['critical_count'] = state_stats['state'].map(critical_counts).fillna(0).astype(int)
    
    # Sort by average ALHS descending
    state_stats = state_stats.sort_values('avg_alhs', ascending=False)
    
    return state_stats.to_dict('records')


@app.get("/api/top-risk-districts")
async def get_top_risk_districts(limit: int = Query(10, ge=1, le=50)):
    """Get top N districts by ALHS score"""
    df = get_data()
    
    top_districts = df.nlargest(limit, 'alhs')[[
        'district_id', 'district_name', 'state', 'alhs', 
        'flags_count', 'population', 'risk_category'
    ]]
    
    return {
        "count": len(top_districts),
        "districts": top_districts.to_dict('records')
    }


@app.get("/api/flags/summary")
async def get_flag_summary():
    """Get summary of early-warning flags"""
    df = get_data()
    
    return {
        "low_child_compliance": int(df['low_child_compliance'].sum()),
        "infra_stress": int(df['infra_stress'].sum()),
        "catchup_spike": int(df['catchup_spike'].sum()),
        "future_surge": int(df['future_surge'].sum()),
        "total_flags": int(df['flags_count'].sum()),
        "districts_with_multiple_flags": len(df[df['flags_count'] >= 2])
    }


@app.get("/api/risk-distribution")
async def get_risk_distribution():
    """Get distribution of districts by risk category"""
    df = get_data()
    
    distribution = df['risk_category'].value_counts().to_dict()
    
    return {
        "distribution": distribution,
        "percentages": {
            k: round(v / len(df) * 100, 2) 
            for k, v in distribution.items()
        }
    }


@app.get("/api/correlation-matrix")
async def get_correlation_matrix():
    """Get correlation matrix for key metrics"""
    df = get_data()
    
    metrics = ['ehi', 'dsi', 'bci', 'alhs']
    corr = df[metrics].corr()
    
    return {
        "metrics": metrics,
        "correlation_matrix": corr.to_dict()
    }


@app.post("/api/refresh-data")
async def refresh_data():
    """Refresh cached data (reload from file)"""
    global _data_cache
    _data_cache = None
    df = get_data()
    
    return {
        "status": "success",
        "message": "Data cache refreshed",
        "records_loaded": len(df)
    }


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    try:
        df = get_data()
        print(f"✅ Data loaded: {len(df)} districts")
    except FileNotFoundError as e:
        print(f"⚠️  Warning: {str(e)}")
        print("   Run 'python data/sample_generator.py' to generate sample data")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down API server...")


# ============================================================================
# RUN SERVER (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('BACKEND_HOST', 'localhost')
    port = int(os.getenv('BACKEND_PORT', 8000))
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║  UIDAI Aadhaar Lifecycle Risk API                         ║
    ║  Backend Server Starting...                                ║
    ╚════════════════════════════════════════════════════════════╝
    
    📡 API URL: http://{host}:{port}
    📚 Docs: http://{host}:{port}/docs
    🔧 ReDoc: http://{host}:{port}/redoc
    
    Press Ctrl+C to stop
    """)
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
"""
FastAPI Backend for UIDAI Dashboard
Provides REST API endpoints for data retrieval and analytics
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="UIDAI Aadhaar Lifecycle Risk API",
    description="Backend API for district-level risk analytics",
    version="1.0.0"
)

# CORS middleware for Streamlit connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class DistrictMetrics(BaseModel):
    district_id: str
    district_name: str
    state: str
    population: int
    ehi: float
    dsi: float
    bci: float
    alhs: float
    low_child_compliance: int
    infra_stress: int
    catchup_spike: int
    future_surge: int
    flags_count: int
    risk_category: str
    last_updated: str


class SummaryStats(BaseModel):
    total_districts: int
    critical_districts: int
    high_risk_districts: int
    medium_risk_districts: int
    low_risk_districts: int
    avg_alhs: float
    total_flags: int
    total_population: int


class StateStats(BaseModel):
    state: str
    district_count: int
    avg_alhs: float
    total_flags: int
    population: int
    critical_count: int


# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load district metrics from CSV"""
    data_path = os.getenv('DATA_PATH', './data/processed/district_metrics.csv')
    
    if not Path(data_path).exists():
        raise FileNotFoundError(
            f"Data file not found at {data_path}. "
            "Run 'python data/sample_generator.py' first."
        )
    
    df = pd.read_csv(data_path)
    return df


# Cache data in memory (in production, use Redis or similar)
_data_cache = None

def get_data():
    """Get cached data or load from file"""
    global _data_cache
    if _data_cache is None:
        _data_cache = load_data()
    return _data_cache


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "UIDAI Risk Analytics API",
        "version": "1.0.0"
    }


@app.get("/api/summary", response_model=SummaryStats)
async def get_summary_stats():
    """Get national-level summary statistics"""
    df = get_data()
    
    return SummaryStats(
        total_districts=len(df),
        critical_districts=len(df[df['risk_category'] == 'Critical']),
        high_risk_districts=len(df[df['risk_category'] == 'High']),
        medium_risk_districts=len(df[df['risk_category'] == 'Medium']),
        low_risk_districts=len(df[df['risk_category'] == 'Low']),
        avg_alhs=round(df['alhs'].mean(), 2),
        total_flags=int(df['flags_count'].sum()),
        total_population=int(df['population'].sum())
    )


@app.get("/api/districts", response_model=List[DistrictMetrics])
async def get_districts(
    state: Optional[str] = Query(None, description="Filter by state"),
    risk_category: Optional[str] = Query(None, description="Filter by risk category"),
    min_alhs: Optional[float] = Query(None, description="Minimum ALHS score"),
    limit: Optional[int] = Query(None, description="Limit number of results")
):
    """Get district-level metrics with optional filters"""
    df = get_data()
    
    # Apply filters
    if state:
        df = df[df['state'] == state]
    
    if risk_category:
        df = df[df['risk_category'] == risk_category]
    
    if min_alhs:
        df = df[df['alhs'] >= min_alhs]
    
    # Sort by ALHS descending
    df = df.sort_values('alhs', ascending=False)
    
    # Limit results
    if limit:
        df = df.head(limit)
    
    return df.to_dict('records')


@app.get("/api/districts/{district_id}", response_model=DistrictMetrics)
async def get_district_by_id(district_id: str):
    """Get metrics for a specific district"""
    df = get_data()
    
    district = df[df['district_id'] == district_id]
    
    if district.empty:
        raise HTTPException(status_code=404, detail="District not found")
    
    return district.iloc[0].to_dict()


@app.get("/api/states", response_model=List[StateStats])
async def get_state_stats():
    """Get aggregated statistics by state"""
    df = get_data()
    
    state_stats = df.groupby('state').agg({
        'district_id': 'count',
        'alhs': 'mean',
        'flags_count': 'sum',
        'population': 'sum'
    }).reset_index()
    
    state_stats.columns = ['state', 'district_count', 'avg_alhs', 'total_flags', 'population']
    state_stats['avg_alhs'] = state_stats['avg_alhs'].round(2)
    
    # Count critical districts per state
    critical_counts = df[df['risk_category'] == 'Critical'].groupby('state').size()
    state_stats['critical_count'] = state_stats['state'].map(critical_counts).fillna(0).astype(int)
    
    # Sort by average ALHS descending
    state_stats = state_stats.sort_values('avg_alhs', ascending=False)
    
    return state_stats.to_dict('records')


@app.get("/api/top-risk-districts")
async def get_top_risk_districts(limit: int = Query(10, ge=1, le=50)):
    """Get top N districts by ALHS score"""
    df = get_data()
    
    top_districts = df.nlargest(limit, 'alhs')[[
        'district_id', 'district_name', 'state', 'alhs', 
        'flags_count', 'population', 'risk_category'
    ]]
    
    return {
        "count": len(top_districts),
        "districts": top_districts.to_dict('records')
    }


@app.get("/api/flags/summary")
async def get_flag_summary():
    """Get summary of early-warning flags"""
    df = get_data()
    
    return {
        "low_child_compliance": int(df['low_child_compliance'].sum()),
        "infra_stress": int(df['infra_stress'].sum()),
        "catchup_spike": int(df['catchup_spike'].sum()),
        "future_surge": int(df['future_surge'].sum()),
        "total_flags": int(df['flags_count'].sum()),
        "districts_with_multiple_flags": len(df[df['flags_count'] >= 2])
    }


@app.get("/api/risk-distribution")
async def get_risk_distribution():
    """Get distribution of districts by risk category"""
    df = get_data()
    
    distribution = df['risk_category'].value_counts().to_dict()
    
    return {
        "distribution": distribution,
        "percentages": {
            k: round(v / len(df) * 100, 2) 
            for k, v in distribution.items()
        }
    }


@app.get("/api/correlation-matrix")
async def get_correlation_matrix():
    """Get correlation matrix for key metrics"""
    df = get_data()
    
    metrics = ['ehi', 'dsi', 'bci', 'alhs']
    corr = df[metrics].corr()
    
    return {
        "metrics": metrics,
        "correlation_matrix": corr.to_dict()
    }


@app.post("/api/refresh-data")
async def refresh_data():
    """Refresh cached data (reload from file)"""
    global _data_cache
    _data_cache = None
    df = get_data()
    
    return {
        "status": "success",
        "message": "Data cache refreshed",
        "records_loaded": len(df)
    }


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    try:
        df = get_data()
        print(f"✅ Data loaded: {len(df)} districts")
    except FileNotFoundError as e:
        print(f"⚠️  Warning: {str(e)}")
        print("   Run 'python data/sample_generator.py' to generate sample data")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down API server...")


# ============================================================================
# RUN SERVER (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('BACKEND_HOST', 'localhost')
    port = int(os.getenv('BACKEND_PORT', 8000))
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║  UIDAI Aadhaar Lifecycle Risk API                         ║
    ║  Backend Server Starting...                                ║
    ╚════════════════════════════════════════════════════════════╝
    
    📡 API URL: http://{host}:{port}
    📚 Docs: http://{host}:{port}/docs
    🔧 ReDoc: http://{host}:{port}/redoc
    
    Press Ctrl+C to stop
    """)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )