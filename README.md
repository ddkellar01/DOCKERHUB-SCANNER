# DOCKERHUB-SCANNER

Enterprise-grade automated container security framework designed to intercept, extract, analyze, and vet Docker Hub container images for malware, spyware, ransomware, and structural vulnerabilities before allowing local deployment or installation. Powered by **Trivy**, **ClamAV**, and **Gemini Pro Thinking**.

## Features
- **Deep Layer Extraction:** Pulls and unpacks container file systems into isolated inspection sandboxes.
- **Multi-Engine Static Scanning:** Combines Trivy (SBOM, secrets, CVE vulnerability scanner) with ClamAV (malware & virus signature engine).
- **Gemini Pro Thinking Heuristics:** Employs advanced reasoning budgets to analyze telemetry for zero-day supply chain compromises, obfuscated backdoor scripts, and suspicious configuration anomalies.
- **Automated Enforcement:** Instantly blocks deployment if high-risk malware signatures or malicious verdicts are returned.
