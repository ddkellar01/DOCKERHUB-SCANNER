.PHONY: help build scan test clean

help:
	@echo "DOCKERHUB-SCANNER Makefile Commands:"
	@echo "  make build   - Build the local Docker image"
	@echo "  make scan    - Scan a target image (e.g., make scan IMAGE=redis:latest)"
	@echo "  make test    - Run unit test suite"
	@echo "  make clean   - Clean up temporary files and docker caches"

build:
	docker build -t dockerhub-scanner:latest .

scan:
	@if [ -z "$(IMAGE)" ]; then \
		echo "Error: Please specify an image. Usage: make scan IMAGE=library/alpine:latest"; \
		exit 1; \
	fi
	docker run --rm \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-e GEMINI_API_KEY=$(GEMINI_API_KEY) \
		dockerhub-scanner:latest $(IMAGE)

test:
	python -m unittest discover -s tests

clean:
	rm -rf reports/ /tmp/scan_target/
	docker system prune -f
