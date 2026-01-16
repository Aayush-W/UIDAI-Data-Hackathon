"""
Sample Data Generator for UIDAI Dashboard
Generates realistic district-level metrics for demonstration
"""

import pandas as pd
import numpy as np
from pathlib import Path

def generate_district_data(n_districts=100, seed=42):
    """Generate sample district-level Aadhaar metrics"""
    
    np.random.seed(seed)
    
    # Indian states for realistic data
    states = [
        'Uttar Pradesh', 'Maharashtra', 'Bihar', 'West Bengal', 'Madhya Pradesh',
        'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Andhra Pradesh',
        'Odisha', 'Telangana', 'Kerala', 'Jharkhand', 'Assam',
        'Punjab', 'Chhattisgarh', 'Haryana', 'Delhi', 'Jammu and Kashmir'
    ]
    
    data = []
    
    for i in range(n_districts):
        # Generate correlated metrics (reflecting real propagation patterns)
        base_risk = np.random.beta(2, 5)  # Skewed toward lower values
        
        # EHI - Enrolment Health Index
        ehi = base_risk * 100 + np.random.normal(0, 10)
        ehi = np.clip(ehi, 0, 100)
        
        # DSI - Demographic Stability Index (correlated with EHI)
        dsi = ehi * 0.7 + np.random.normal(20, 15)
        dsi = np.clip(dsi, 0, 100)
        
        # BCI - Biometric Compliance Index (affected by both)
        bci = (ehi * 0.4 + dsi * 0.4) + np.random.normal(10, 12)
        bci = np.clip(bci, 0, 100)
        
        # ALHS - Composite score
        alhs = ehi * 0.3 + dsi * 0.3 + bci * 0.4
        
        # Generate flags based on thresholds
        low_child_compliance = (bci > 55 and np.random.random() > 0.6)
        infra_stress = (alhs > 50 and np.random.random() > 0.65)
        catchup_spike = (dsi > 60 and np.random.random() > 0.7)
        future_surge = (ehi > 65 and np.random.random() > 0.65)
        
        flags_count = sum([
            low_child_compliance, 
            infra_stress, 
            catchup_spike, 
            future_surge
        ])
        
        # Population distribution
        population = int(np.random.lognormal(12.5, 0.8))  # Realistic population distribution
        
        data.append({
            'district_id': f'DIS_{i:04d}',
            'district_name': f'District_{chr(65 + i % 26)}{i:03d}',
            'state': np.random.choice(states),
            'population': population,
            'ehi': round(ehi, 2),
            'dsi': round(dsi, 2),
            'bci': round(bci, 2),
            'alhs': round(alhs, 2),
            'low_child_compliance': int(low_child_compliance),
            'infra_stress': int(infra_stress),
            'catchup_spike': int(catchup_spike),
            'future_surge': int(future_surge),
            'flags_count': flags_count,
            'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(data)
    
    # Add risk category
    df['risk_category'] = pd.cut(
        df['alhs'], 
        bins=[0, 40, 60, 75, 100],
        labels=['Low', 'Medium', 'High', 'Critical']
    )
    
    return df


def generate_time_series_data(df, months=12):
    """Generate historical monthly data for trend analysis"""
    
    time_series = []
    
    for _, district in df.iterrows():
        for month in range(months):
            date = pd.Timestamp.now() - pd.DateOffset(months=months-month)
            
            # Add temporal variation
            trend = month / months * 10  # Gradual increase
            noise = np.random.normal(0, 5)
            
            time_series.append({
                'district_id': district['district_id'],
                'month': date.strftime('%Y-%m'),
                'ehi': district['ehi'] + trend + noise,
                'dsi': district['dsi'] + trend + noise,
                'bci': district['bci'] + trend + noise,
                'alhs': district['alhs'] + trend + noise
            })
    
    return pd.DataFrame(time_series)


def main():
    """Generate and save sample data"""
    
    # Create directories
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    
    print("Generating district-level metrics...")
    df_districts = generate_district_data(n_districts=150)
    
    print("Generating time-series data...")
    df_timeseries = generate_time_series_data(df_districts, months=12)
    
    # Save data
    district_file = 'data/processed/district_metrics.csv'
    timeseries_file = 'data/processed/timeseries_metrics.csv'
    
    df_districts.to_csv(district_file, index=False)
    df_timeseries.to_csv(timeseries_file, index=False)
    
    print(f"\n✅ Data generation complete!")
    print(f"   - Districts: {len(df_districts)} records → {district_file}")
    print(f"   - Time series: {len(df_timeseries)} records → {timeseries_file}")
    print(f"\n📊 Summary Statistics:")
    print(f"   - Critical districts: {len(df_districts[df_districts['risk_category'] == 'Critical'])}")
    print(f"   - High risk districts: {len(df_districts[df_districts['risk_category'] == 'High'])}")
    print(f"   - Total flags: {df_districts['flags_count'].sum()}")
    print(f"   - Avg ALHS: {df_districts['alhs'].mean():.2f}")


if __name__ == "__main__":
    main()