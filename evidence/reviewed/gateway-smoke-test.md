# Gateway Smoke-Test Records

## Run: 2026-09-17

- Reviewer: `Ruven Guna`
- Git commit: `01150e46a54bf7da297712610c2b547602c994d7`
- Model: `llama3.2:3b-instruct-q4_K_M`
- Ollama version: `0.34.0`

### Results

Existing results table goes here.

### Notes

Existing notes go here.

---

## Run: 2026-09-19

- Reviewer: `Ruven Guna`
- Git commit: `1dc0af36eb5acf2829ce52b194372e3ceb351eee`
- Model: `llama3.2:3b-instruct-q4_K_M`
- Ollama version: `0.34.0`

### Automated results

| Check | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Ruff linting | No linting errors | No linting errors reported | Pass |
| Mypy type checking | No type errors | Record the actual output | Pending |
| Pytest | Six tests pass | Record the actual output | Pending |

### Integration results

| Check | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Windows health | HTTP 200 with `status: ok` | Record the actual result | Pending |
| Windows chat | Policy-consistent response | Record the actual result | Pending |
| Missing API key | HTTP 401 | Request rejected with HTTP 401 | Pass |
| Oversized message | HTTP 422 | Request containing 8,001 characters rejected with HTTP 422 | Pass |
| Docker health | HTTP 200 with `status: ok` | Record the actual result | Pending |

### Notes

The pytest run may report a Starlette/AnyIO dependency deprecation warning. This warning does not represent a failed application test.