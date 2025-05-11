import sys
import os

# Ensure project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion.load_csv import load_esg_csv
from ingestion.log_metadata import log_ingestion
from validation.schema import ESGRecord
from pydantic import ValidationError


def main():
    source = "data/esg_sample.csv"
    status = "Success"
    
    try:
        df = load_esg_csv(source)
        valid_records = 0
        
        for i, row in df.iterrows():
            try:
                ESGRecord(**row.to_dict())
                valid_records += 1
            except ValidationError as ve:
                print(f"❌ Record {i} validation error: {ve}")
        
        print(f"✅ {valid_records} valid records out of {len(df)}")
        log_ingestion(source, valid_records, status)
    
    except Exception as e:
        print(f"🚨 Pipeline failed: {e}")
        log_ingestion(source, 0, "Failed")

if __name__ == "__main__":
    main()
