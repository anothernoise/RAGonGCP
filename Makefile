.PHONY: help setup test lint run ingest tf-init tf-validate tf-plan docker-build

VENV ?= .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PROFILE ?= bc_real_estate

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install package + dev deps
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test: ## Run unit tests (no GCP creds needed)
	$(VENV)/bin/pytest -q

lint: ## Lint with ruff
	$(VENV)/bin/ruff check src tests

run: ## Run the API locally with the offline fake backend
	RAGONGCP_BACKEND=fake $(VENV)/bin/uvicorn ragongcp.api.main:app --reload --port 8080

ingest: ## Ingest the active profile's sources (needs GCP creds)
	$(PY) -m ragongcp.ingestion.run --profile $(PROFILE)

tf-init: ## terraform init
	cd infra/terraform && terraform init

tf-validate: ## terraform validate
	cd infra/terraform && terraform validate

tf-plan: ## terraform plan
	cd infra/terraform && terraform plan

docker-build: ## Build the container image
	docker build -t ragongcp:local .
