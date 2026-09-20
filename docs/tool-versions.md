# Tool Versions

These versions define the local toolchain used to execute the AI Assurance Workbench evaluation. The reviewed machine-specific record is available in the [environment record](../evidence/reviewed/environment-record.md).

## Recorded toolchain

- Recorded date: `2026-09-19`
- Operating environment: Ubuntu `26.04.1 LTS` under WSL 2
- Architecture: `x86_64`
- Ubuntu system Python: `3.14.4`
- ASQI runtime Python: `3.12.14`
- uv: `0.12.17`
- ASQI Engineer: `0.5.9`
- Docker Engine: `29.7.2`
- Docker Desktop: `4.90.0`
- Docker Compose: `5.5.1`
- Ollama: `0.34.0`

## ASQI Engineer installation

ASQI Engineer is installed as an isolated uv command-line tool using Python 3.12. Ubuntu's system Python is not used to run ASQI Engineer.

```bash
uv python install 3.12
uv tool install --python 3.12 "asqi-engineer==0.5.9"
```

Verify the installation:

```bash
uv tool run --from asqi-engineer python --version
asqi --version
```

Expected versions:

```text
Python 3.12.14
asqi-engineer version 0.5.9
```

## Reproducing the ASQI installation

To reproduce the recorded ASQI environment, install the pinned version rather than automatically selecting the latest release:

```bash
uv python install 3.12
uv tool install --python 3.12 "asqi-engineer==0.5.9"
```

If ASQI Engineer is already installed at another version, inspect it before changing the environment:

```bash
uv tool list
asqi --version
```

An intentional upgrade should update this document, the environment record, and any evaluation evidence affected by the change.

## Docker verification

ASQI Engineer uses Docker Desktop as its local container backend. Confirm that Ubuntu WSL can reach the Docker engine:

```bash
docker version
docker compose version
docker run --rm hello-world
```

A successful `hello-world` run confirms that the Docker client can contact the Docker daemon and execute a Linux container.

## Ollama placement

Ollama runs natively on Windows rather than inside Ubuntu WSL or Docker. The FastAPI gateway also runs on Windows and connects to Ollama at:

```text
http://localhost:11434/v1
```

ASQI test containers reach the FastAPI gateway through:

```text
http://host.docker.internal:8000
```

## Execution authority

The schemas, commands, and examples packaged with ASQI Engineer `0.5.9` are treated as the execution authority for this evaluation. Differences between this installed version and newer online documentation must be reviewed and documented before changing the evaluation configuration.

## Version-check commands

```bash
date -I
cat /etc/os-release
uname -m
python3 --version
uv --version
uv tool run --from asqi-engineer python --version
uv tool list
asqi --version
docker version
docker compose version
```

## ASQI Garak test container

The Garak test framework is executed through the ASQI Engineer test container.

- Image tag: `asqiengineer/test-container:garak-latest`
- Pinned image: `asqiengineer/test-container@sha256:93b291ecbafa182af24460a587b403591b0e502abd64638a5dcca97b409274d5`
- Garak framework version: `0.12.0`
- Image creation timestamp: `2026-07-20T09:10:52.426904507Z`
- Image pull date: `2026-09-20`
- Local displayed image size: `2.65 GB`

The mutable `garak-latest` tag is retained for readability and discovery. The immutable digest identifies the exact container image used for the recorded evaluation.

Evaluation suite configurations should reference the immutable image:

```yaml
image: asqiengineer/test-container@sha256:93b291ecbafa182af24460a587b403591b0e502abd64638a5dcca97b409274d5
```

Retrieve the current tagged image:

```bash
docker pull asqiengineer/test-container:garak-latest
```

Display its repository digest:

```bash
docker image inspect \
  asqiengineer/test-container:garak-latest \
  --format '{{index .RepoDigests 0}}'
```

Inspect its creation timestamp and uncompressed Docker size:

```bash
docker image inspect \
  asqiengineer/test-container:garak-latest \
  --format 'Created={{.Created}} Size={{.Size}}'
```

Inspect its configured entry point:

```bash
docker image inspect \
  asqiengineer/test-container:garak-latest \
  --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'
```

Verify the Garak package version inside the container:

```bash
docker run --rm \
  --entrypoint python \
  asqiengineer/test-container:garak-latest \
  -c "import importlib.metadata; print(importlib.metadata.version('garak'))"
```

Pull the exact recorded image independently of any later movement of the `garak-latest` tag:

```bash
docker pull \
  asqiengineer/test-container@sha256:93b291ecbafa182af24460a587b403591b0e502abd64638a5dcca97b409274d5
```

The container image itself is stored in Docker Desktop and is not committed to this repository. Only its provenance, version, digest, and retrieval commands are committed.