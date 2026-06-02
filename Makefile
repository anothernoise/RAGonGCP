.PHONY: help setup test lint run ingest tf-init tf-validate tf-plan docker-build

VENV ?= .venv
UV ?= uv
PROFILE ?= bc_real_estate

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Create .venv and install deps via uv
	$(UV) sync --extra dev

test: ## Run unit tests (no GCP creds needed)
	$(UV) run pytest -q

lint: ## Lint with ruff
	$(UV) run ruff check src tests

run: ## Run the API locally with the offline fake backend
	RAGONGCP_BACKEND=fake $(UV) run uvicorn ragongcp.api.main:app --reload --port 8080

ingest: ## Ingest the active profile's sources (needs GCP creds)
	$(UV) run python -m ragongcp.ingestion.run --profile $(PROFILE)

tf-init: ## terraform init
	cd infra/terraform && terraform init

tf-validate: ## terraform validate
	cd infra/terraform && terraform validate

tf-plan: ## terraform plan
	cd infra/terraform && terraform plan

docker-build: ## Build the container image
	docker build -t ragongcp:local .
