import pandas as pd
import os

def load_esg_csv(file_path: str = 'data/esg_sample.csv') -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"🚫 File not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        expected_columns = [
            "org_id", "org_name", "sector", "country", 
            "emissions_score", "labor_compliance_score", 
            "governance_index", "esg_flagged", "report_date"
        ]
        
        if not all(col in df.columns for col in expected_columns):
            raise ValueError("🚫 CSV schema mismatch. Please verify column names.")
        
        print(f"✅ Loaded {len(df)} records from {file_path}")
        return df
    
    except Exception as e:
        print(f"🚨 Error loading CSV: {e}")
        raise
