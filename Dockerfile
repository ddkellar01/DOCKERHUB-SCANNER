FROM python:3.11-slim

# Install system dependencies: Docker CLI, Trivy, ClamAV, and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    lsb-release \
    apt-transport-https \
    ca-certificates \
    clamav \
    clamav-daemon \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Trivy vulnerability scanner
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Update ClamAV virus signatures
RUN freshclam || true

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "src/scanner.py"]
