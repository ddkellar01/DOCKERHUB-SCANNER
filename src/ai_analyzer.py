import os
import json
from google import genai
from google.genai import types

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

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
        )
    )

    return response.text
