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