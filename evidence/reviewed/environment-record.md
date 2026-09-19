# Environment Record

## Record details

- Recorded date: `2026-09-19`
- Recorded commit: `037faae950ffba2ed151bbc47840cf5011769a65`
- Environment purpose: Local ASQI Engineer and Garak evaluation lab

## Windows host

- Operating system: Windows
- Docker Desktop: `4.90.0`
- Ollama: `0.34.0`
- GPU: `NVIDIA GeForce RTX 3070 Laptop GPU`
- GPU memory: `8192 MiB`
- NVIDIA driver: `616.92`

## Ubuntu WSL environment

- Distribution: `Ubuntu 26.04.1 LTS`
- Architecture: `x86_64`
- System Python: `3.14.4`
- uv: `0.12.17`
- ASQI Engineer: `0.5.9`
- ASQI runtime Python: `3.12.14`
- Docker Engine: `29.7.2`
- Docker Compose: `5.5.1`
- Docker platform: `Docker Desktop 4.90.0 (238679)`
- Container architecture: `amd64`

## Application environment

- Application runtime: Windows Python `3.12.14`
- Model runtime: Native Ollama on Windows
- Model: `llama3.2:3b-instruct-q4_K_M`
- Model quantization: `Q4_K_M`
- Gateway address from Windows: `http://localhost:8000`
- Gateway address from Docker: `http://host.docker.internal:8000`
- ASQI container backend: Docker

## Runtime separation

Ubuntu's system Python and the ASQI Engineer runtime use separate Python installations. The Ubuntu system command `python3` reports Python 3.14.4, while ASQI Engineer runs in an isolated uv tool environment using Python 3.12.14.

The FastAPI application runs in a separate Windows uv environment using Python 3.12.14. Ollama runs natively on Windows. ASQI Engineer runs from Ubuntu WSL and launches test containers through Docker Desktop.

## Verification commands

```bash
date -I
cat /etc/os-release
uname -m
python3 --version
uv --version
uv tool run --from asqi-engineer python --version
asqi --version
docker version
docker compose version
docker run --rm hello-world
git rev-parse HEAD