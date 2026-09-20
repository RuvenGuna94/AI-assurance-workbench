# ASQI Runtime

This directory contains the reviewed local runtime configuration used by the AI Assurance Workbench.

The runtime provides the supporting services required for ASQI Engineer’s durable workflow execution and optional observability. It does not contain the application, Ollama, the language model, or the Garak test container.

## Provenance

- Source repository: [asqi-engineer/asqi-engineer](https://github.com/asqi-engineer/asqi-engineer)
- Source commit: `54576b0d50fe8e54d8b60572e17848910ef21fbb`
- ASQI Engineer version: `0.5.9`
- Review date: `2026-09-20`

The upstream runtime configuration was reviewed before the required services were adapted for this project. The source commit identifies the exact upstream configuration used as the reference.

## Architecture

The initial evaluation uses the following request path:

```text
ASQI Engineer
    -> Garak test container
    -> FastAPI support gateway
    -> Ollama
    -> Llama 3.2
```

The supporting runtime path is:

```text
ASQI Engineer
    -> PostgreSQL for DBOS workflow state
    -> Jaeger for supported OpenTelemetry traces
```

## Services

### PostgreSQL

The `db` service provides PostgreSQL for DBOS workflow and step state. This allows ASQI to persist execution progress and support durable workflow behavior.

The upstream runtime uses a pgvector-enabled PostgreSQL image. The initial Garak evaluation does not use vector storage or similarity search; PostgreSQL is used for ordinary DBOS workflow persistence.

PostgreSQL is exposed locally on port `5432`.

### Jaeger

The `jaeger` service receives and displays supported OpenTelemetry traces from ASQI workflows.

The Jaeger web interface is exposed locally on port `16686`. Its OpenTelemetry receivers are exposed on ports `4317` and `4318`.

Tracing is operational evidence and does not replace ASQI or Garak evaluation results.

## LiteLLM decision

The upstream ASQI runtime includes LiteLLM as an optional OpenAI-compatible model-provider proxy. This project does not use LiteLLM because the FastAPI support gateway already exposes the OpenAI-compatible endpoint required by ASQI and Garak.

LiteLLM may be considered in a later extension involving multiple providers, centralized provider credentials, model routing, or fallback behavior.

## Prerequisites

The following must be available before starting the runtime:

- Ubuntu WSL.
- Docker Desktop with Ubuntu WSL integration enabled.
- Docker Compose.
- ASQI Engineer installed in Ubuntu WSL.
- The project repository available through its mounted Windows path.

Verify Docker access from Ubuntu:

```bash
docker version
docker compose version
```

Both commands should return version information without a Docker daemon connection error.

## Local configuration

Run the following commands from the `infra/asqi` directory.

Create the local environment file from the committed example:

```bash
cp .env.example .env
```

Review it before loading it:

```bash
less .env
```

The local `.env` file must remain untracked. It must not contain production credentials, personal data, real customer information, or other secrets intended for publication.

Confirm that Git ignores it:

```bash
git check-ignore -v .env
```

The command should identify the matching `.env` rule from the repository’s `.gitignore`.

Confirm that the safe example remains trackable:

```bash
git check-ignore -v .env.example
```

This command should produce no output.

## Environment variables

The initial runtime uses:

- `DBOS_DATABASE_URL`: Connects ASQI and DBOS to the local PostgreSQL database.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: Sends supported workflow traces to the local Jaeger collector.

The local `.env` should contain values equivalent to:

```dotenv
DBOS_DATABASE_URL=postgresql://postgres:asqi@localhost:5432/asqi_starter
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
```

These credentials are for the isolated local lab and must not be reused in a production environment.

Load the reviewed values into the current Ubuntu shell:

```bash
set -a
source .env
set +a
```

Confirm that the database URL is available:

```bash
printf '%s\n' "$DBOS_DATABASE_URL"
```

Expected result:

```text
postgresql://postgres:asqi@localhost:5432/asqi_starter
```

The variables remain available only in the current shell session. Load them again after opening a new Ubuntu terminal.

## Validate the configuration

Before starting the services, validate the Docker Compose configuration:

```bash
docker compose --env-file .env config --quiet
```

A successful validation produces no output and returns exit code `0`.

Check the exit code:

```bash
echo $?
```

Expected result:

```text
0
```

The resolved configuration should contain only the required `db` and `jaeger` services.

## Pull the container images

Download the images required by the runtime:

```bash
docker compose pull db jaeger
```

This downloads the images but does not start the services.

## Start the services

Start PostgreSQL and Jaeger in the background:

```bash
docker compose up -d db jaeger
```

Check their state:

```bash
docker compose ps
```

Both services should be running. The `litellm` service should not be present.

## Verify PostgreSQL

Check whether PostgreSQL is ready to accept connections:

```bash
docker compose exec db pg_isready -U postgres -d asqi_starter
```

Expected result includes:

```text
accepting connections
```

If PostgreSQL is still starting, wait several seconds and repeat the command.

## Verify Jaeger

Check whether the Jaeger web interface responds:

```bash
curl -I http://localhost:16686
```

Expected result includes:

```text
HTTP/1.1 200 OK
```

Open the Jaeger interface in a Windows browser at [http://localhost:16686](http://localhost:16686).

The interface may contain no ASQI traces until an evaluation workflow has been executed.

## View service logs

View recent PostgreSQL logs:

```bash
docker compose logs --tail=50 db
```

View recent Jaeger logs:

```bash
docker compose logs --tail=50 jaeger
```

Follow logs in real time:

```bash
docker compose logs --follow db jaeger
```

Press `Ctrl+C` to stop following the logs. This does not stop the containers.

## Stop the services

Stop the containers without removing them:

```bash
docker compose stop
```

Restart stopped containers:

```bash
docker compose start
```

Alternatively, remove the containers and Docker network while retaining the PostgreSQL volume:

```bash
docker compose down
```

Do not run the following command unless intentionally deleting the PostgreSQL volume and its stored workflow state:

```bash
docker compose down -v
```

## Data persistence

PostgreSQL data is stored in a named Docker volume. The data remains available after `docker compose stop` and normally remains available after `docker compose down`.

Docker images, containers, networks, and volumes are managed by Docker Desktop and are not committed to this repository.

## Security boundaries

This runtime is intended only for local development and evaluation.

- The database credentials are local lab values, not production credentials.
- The services must not be exposed on an untrusted or public network.
- The local `.env` must not be committed.
- Evaluation inputs must not contain production data, real customer records, passwords, full payment-card numbers, or real API keys.
- Reviewed and sanitized evidence may be committed under `evidence/reviewed/`.
- Raw or temporary evidence must remain under the ignored `evidence/local/` directory.

## Reproducibility limitations

The upstream ASQI runtime configuration was reviewed at the Git commit recorded in the provenance section. The local runtime was adapted to include only PostgreSQL and Jaeger.

The container images are referenced by tags rather than immutable image digests:

- `pgvector/pgvector:pg16` is a moving PostgreSQL 16 tag.
- `jaegertracing/jaeger:2.9.0` is versioned but is not pinned by immutable digest.

The source configuration and ASQI Engineer version are recorded, but the runtime should not be described as fully immutable until its container images are pinned by digest.

## Initial scope

This runtime supports the initial ASQI Engineer and Garak evaluation of the Northstar Support Gateway. It does not establish production readiness, complete security coverage, regulatory compliance, or suitability for handling production data.