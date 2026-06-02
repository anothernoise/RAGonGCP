# Troubleshooting

Common issues and fixes when running RAGonGCP.

## `make setup` fails

Possible causes:

- unsupported Python version
- `uv` is not installed or too old
- local virtual environment corruption

Try:

```bash
rm -rf .venv
uv --version
make setup
```

Ensure your Python version meets `pyproject.toml` (`>=3.10`).

## API returns `502` on `/query` or `/ingest`

`502` is used to surface backend/config/runtime errors from adapters.

Check:

- `.env` values (`RAGONGCP_PROJECT_ID`, `RAGONGCP_LOCATION`, `RAGONGCP_STAGING_BUCKET`)
- active profile (`RAGONGCP_PROFILE`)
- backend value (`RAGONGCP_BACKEND` or profile `backend`)
- Google ADC auth:

  ```bash
  gcloud auth application-default login
  ```

## Web ingestion blocked by allowlist

Web source only fetches URLs whose host exactly matches the configured
`web_allowlist`.

Fix by adding required hostnames to the profile allowlist, for example both:

- `example.com`
- `www.example.com`

## Ingestion fails due to missing staging bucket

Web and Drive ingestion need `RAGONGCP_STAGING_BUCKET`.

Confirm:

- bucket exists
- runtime identity has access
- env variable is populated

## Tests pass offline but cloud mode fails

Offline tests use the fake backend and validate core behavior only.

For cloud mode validation:

- run ingestion against a real profile
- run `/query` against real corpus data
- validate IAM/API enablement in Terraform state

## Terraform apply errors

Typical causes:

- APIs not enabled yet (eventual consistency)
- insufficient IAM permissions on deployer account
- invalid or non-unique bucket name

Recommended flow:

```bash
terraform validate
terraform plan
terraform apply
```

If an API was just enabled, retry after a short wait.
