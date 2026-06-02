.PHONY: help setup test test-e2e lint run ingest demo-chainlit tf-init tf-validate tf-plan docker-build

VENV ?= .venv
UV ?= uv
PROFILE ?= bc_real_estate

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Create .venv and install deps via uv
	$(UV) sync --extra dev

test: ## Run unit tests (no GCP creds needed)
	$(UV) run pytest -q

test-e2e: ## Run offline end-to-end API tests
	$(UV) run pytest -q tests/e2e

lint: ## Lint with ruff
	$(UV) run ruff check src tests

run: ## Run the API locally with the offline fake backend
	RAGONGCP_BACKEND=fake $(UV) run uvicorn ragongcp.api.main:app --reload --port 8080

ingest: ## Ingest the active profile's sources (needs GCP creds)
	$(UV) run python -m ragongcp.ingestion.run --profile $(PROFILE)

demo-chainlit: ## Run Chainlit demo UI against the API
	$(UV) run --extra demo chainlit run examples/chainlit_app.py --watch

tf-init: ## terraform init
	cd infra/terraform && terraform init

tf-validate: ## terraform validate
	cd infra/terraform && terraform validate

tf-plan: ## terraform plan
	cd infra/terraform && terraform plan

docker-build: ## Build the container image
	docker build -t ragongcp:local .
