import subprocess
import os
from config import config

def generate_cyclonedx_sbom(image_name: str) -> str:
    """
    Generates a CycloneDX JSON SBOM report for the target image.
    """
    os.makedirs(config.reports_dir, exist_ok=True)
    safe_name = image_name.replace("/", "_").replace(":", "_")
    sbom_path = os.path.join(config.reports_dir, f"sbom_{safe_name}.json")

    print(f"[*] Generating CycloneDX SBOM for {image_name}...")
    cmd = [
        "trivy", "image", 
        "--format", "cyclonedx", 
        "--output", sbom_path, 
        image_name
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"[*] SBOM successfully saved to: {sbom_path}")
        return sbom_path
    else:
        print(f"[Warning] SBOM generation encountered issues: {result.stderr}")
        return ""
