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

## Planned architecture

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

See [the model record](docs/model-record.md) for hardware, configuration,
provenance, and known limitations.