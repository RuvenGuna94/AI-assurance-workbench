# AI Assurance Workbench

This repository demonstrates the evaluation of a locally hosted, model-backed application using ASQI Engineer and Garak.

The application is a fictional customer-support assistant powered by an open-source Llama model running locally through Ollama. A FastAPI gateway provides an OpenAI-compatible interface and applies the application's support policy. ASQI Engineer orchestrates containerized Garak security tests against that interface.

## Project goals

- Run an open-source language model locally with Ollama.
- Build a small OpenAI-compatible application using FastAPI.
- Define an explicit system boundary and threat model.
- Use ASQI Engineer to orchestrate model evaluations.
- Use Garak to test selected prompt-injection and encoded-instruction risks.
- Convert technical results into an ASQI scorecard.
- Preserve reviewed, reproducible evidence without overstating assurance.

## Data notice

This is a portfolio and learning project. It contains no production systems, production credentials, real customer records, or personal data.

The retailer, policies, users, prompts, API keys, and test scenarios are fictional or synthetic. Raw evaluation outputs must be reviewed and sanitized before they are committed.

## Architecture

```text
Garak test container
        |
        v
ASQI Engineer
        |
        v
FastAPI support gateway
        |
        v
Ollama
        |
        v
Llama 3.2 3B Instruct
```

## Model

This project uses `llama3.2:3b-instruct-q4_K_M` through Ollama.

See [the model record](docs/model-record.md) for hardware, configuration, provenance, and known limitations.

## Current results

- The [initial Garak smoke assessment](evidence/reviewed/garak-smoke-assessment-2026-09-27.md) documents execution status, manual classifications, limitations, and the first grouped R1 prompt-injection finding.
- The [focused Garak assessment](evidence/reviewed/garak-focused-2026-10-02/summary.md) expands the configured R1 and R2 coverage and records a representative reproduction sample. Unsampled detector signals remain unconfirmed.
- [Findings and triage notes](docs/findings.md) preserve the risk mapping, evidence references, reproduction status, and residual limitations.

These results demonstrate selected evaluation workflows, not complete security coverage or certification.

## Local authentication boundary

The published `local-lab-key` is a development-only accidental-traffic guard. It is intentionally not treated as a secret and is not a meaningful authentication or authorization control for production or untrusted networks. Replace the mechanism before any non-local deployment.

## Testing

See [TESTING.md](TESTING.md) for local setup, smoke-test commands, expected results, and manual security checks.
