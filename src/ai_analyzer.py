import os
import json
from google import genai
from google.genai import types

# Google has been churning model names (2.5-pro-preview -> 2.0-flash -> 3-flash,
# each 404ing in turn, and the API's own "use X instead" advice keeps being
# wrong). So: try candidates in order, skip the ones the API rejects.
MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-3-flash",
    "gemini-flash-latest",
]

def analyze_security_findings(image_name: str, trivy_report: dict, file_scan_summary: dict) -> str:
    """
    Sends container artifacts and scan telemetry to Gemini for
    advanced adversarial reasoning.
    """
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
    You are an elite container security expert and malware reversing analyst. Evaluate the telemetry for Docker Hub image: '{image_name}'.

    ### 1. Vulnerability & SBOM Findings (Trivy):
    {json.dumps(trivy_report, indent=2)}

    ### 2. Static Malware/Virus Scan (ClamAV):
    {json.dumps(file_scan_summary, indent=2)}

    ### Instructions:
    Perform a meticulous threat assessment. Examine for hidden spyware signatures, ransomware triggers, obfuscated shell scripts, unauthorized privilege escalation vectors, or supply chain compromises.
    Format your response precisely as follows:
    1. **Threat Verdict:** [SAFE / SUSPICIOUS / MALICIOUS]
    2. **Risk Analysis:** Core vulnerabilities or threat vectors identified.
    3. **Behavioral Heuristics:** Evaluation of hidden layers or suspicious binary signatures.
    4. **Recommendation:** Final approval or block directive.
    """

    config = types.GenerateContentConfig(temperature=0.1)

    last_err = None
    for model in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as e:
            # Model doesn't exist (anymore) -> try the next candidate.
            # Anything else (bad key, quota, ...) -> fail fast, retrying won't help.
            if "404" in str(e) or "NOT_FOUND" in str(e):
                last_err = e
                continue
            raise

    raise RuntimeError(
        f"No working Gemini model from candidates {MODEL_CANDIDATES}. Last error: {last_err}"
    )
