#!/usr/bin/env bash
set -e

IMAGE_NAME="dockerhub-scanner:latest"

case "$1" in
  build)
    echo "[*] Building Docker Image..."
    docker build -t $IMAGE_NAME .
    ;;
  scan)
    echo "[*] Running Scanner on Local Container..."
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
      -e GEMINI_API_KEY=$GEMINI_API_KEY \
      $IMAGE_NAME ${2:-"library/alpine:latest"}
    ;;
  clean)
    echo "[*] Cleaning local containers and dangling images..."
    docker system prune -f
    ;;
  *)
    echo "Usage: ./manage.sh {build|scan <target_image>|clean}"
    exit 1
    ;;
esac
