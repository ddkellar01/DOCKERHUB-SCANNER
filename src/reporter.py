import os
import json
from datetime import datetime
from config import config

def save_report(image_name: str, ai_assessment: str, trivy_data: dict, file_scan_summary: dict):
    os.makedirs(config.reports_dir, exist_ok=True)
    safe_name = image_name.replace("/", "_").replace(":", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(config.reports_dir, f"{safe_name}_{timestamp}.json")

    report_payload = {
        "image": image_name,
        "timestamp": timestamp,
        "ai_assessment": ai_assessment,
        "trivy_summary": trivy_data.get("Metadata", {}),
        "clamav_summary": file_scan_summary
    }

    with open(report_path, "w") as f:
        json.dump(report_payload, f, indent=4)
    print(f"[*] Audit report securely persisted to: {report_path}")
