import os
import requests

def send_security_alert(image_name: str, verdict: str, summary: str):
    """
    Sends structured webhook alerts to Slack or Discord if configured.
    """
    webhook_url = os.getenv("SECURITY_WEBHOOK_URL")
    if not webhook_url:
        return

    is_malicious = "MALICIOUS" in verdict or "SUSPICIOUS" in verdict
    color = "#FF0000" if is_malicious else "#2EB67D"

    payload = {
        "text": f":shield: *DOCKERHUB-SCANNER Audit Complete*",
        "attachments": [
            {
                "color": color,
                "fields": [
                    {"title": "Target Image", "value": image_name, "short": False},
                    {"title": "Threat Verdict", "value": verdict, "short": True},
                    {"title": "Analysis Summary", "value": summary[:1500], "short": False}
                ],
                "footer": "Automated Container Security Pipeline"
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("[*] Security alert webhook dispatched successfully.")
        else:
            print(f"[Warning] Webhook dispatch returned status code {response.status_code}")
    except Exception as e:
        print(f"[Warning] Failed to send webhook alert: {e}")
