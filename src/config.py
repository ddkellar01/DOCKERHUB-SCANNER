import os
from pydantic import BaseModel

class ScannerConfig(BaseModel):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    scan_target_dir: str = os.getenv("SCAN_TARGET_DIR", "/tmp/scan_target")
    reports_dir: str = os.getenv("REPORTS_DIR", "/app/reports")
    trivy_severity: str = os.getenv("TRIVY_SEVERITY", "HIGH,CRITICAL")
    block_on_malware: bool = True
    block_on_critical_vulns: bool = True

config = ScannerConfig()
