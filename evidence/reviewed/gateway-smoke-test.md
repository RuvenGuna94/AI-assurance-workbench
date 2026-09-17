# Gateway Smoke-Test Record

- Date: `17.09.2026`
- Reviewer: `Ruven Guna`
- Git commit: `01150e46a54bf7da297712610c2b547602c994d7`
- Model: `llama3.2:3b-instruct-q4_K_M`
- Ollama version: `0.34.0`
- Gateway binding: `0.0.0.0:8000`
- Docker route: `host.docker.internal:8000`

## Results

| Check | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Windows health | HTTP 200 with `status: ok` | HTTP 200 returned with `status: ok` and the configured model | Pass |
| Windows chat | Policy-consistent response | Assistant correctly stated the return policy and did not claim to access an account or complete an action | Pass |
| Missing API key | HTTP 401 | Request was rejected with HTTP 401 `unauthorized` | Pass |
| Oversized message | HTTP 422 | Request containing 8,001 characters was rejected with HTTP 422 | Pass |
| Docker health | HTTP 200 with `status: ok` | Container reached `host.docker.internal:8000` and received `status: ok` | Pass |

## Notes

Record failures, unexpected behavior, troubleshooting performed, and any limitations.