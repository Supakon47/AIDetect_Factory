import os
import csv
from datetime import datetime
from typing import Dict, Any

def ensure_logs_dir(log_dir: str):
    os.makedirs(log_dir, exist_ok=True)

def append_log_csv(log_path: str, row: Dict[str, Any]):
    file_exists = os.path.exists(log_path)

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def now_iso():
    return datetime.now().isoformat(timespec="seconds")