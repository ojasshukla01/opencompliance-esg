from datetime import datetime
import json
import os

def log_ingestion(source: str, record_count: int, status: str, log_file: str = "data/ingestion_log.json"):
    log_entry = {
        "source": source,
        "record_count": record_count,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }

    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)

    print(f"📝 Ingestion log updated in {log_file}")
