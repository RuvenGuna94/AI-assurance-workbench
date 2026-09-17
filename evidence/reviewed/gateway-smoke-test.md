# Gateway Smoke-Test Record

- Date: `17.09.2026`
- Reviewer: `Ruven Guna`
- Model: `llama3.2:3b-instruct-q4_K_M`
- Ollama version: `0.34.0`
- Gateway binding: `0.0.0.0:8000`
- Docker route: `host.docker.internal:8000`

## Results

| Check | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Windows health | HTTP 200 with `status: ok` |  |  |
| Windows chat | Policy-consistent response |  |  |
| Missing API key | HTTP 401 |  |  |
| Oversized message | HTTP 422 |  |  |
| Docker health | HTTP 200 with `status: ok` |  |  |

## Notes

Record failures, unexpected behavior, troubleshooting performed, and any limitations.