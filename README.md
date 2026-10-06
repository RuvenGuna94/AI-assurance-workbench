# AI Assurance Workbench

This repository demonstrates the evaluation of a locally hosted, model-backed application using ASQI Engineer and Garak.

The application is a fictional customer-support assistant powered by an open-weight Llama model distributed under the Llama Community License and running locally through Ollama. A FastAPI gateway provides an OpenAI-compatible interface and applies the application's support policy. ASQI Engineer orchestrates containerized Garak security tests against that interface.

## Project goals

- Run an open-weight language model locally with Ollama.
- Build a small OpenAI-compatible application using FastAPI.
- Define an explicit system boundary and threat model.
- Use ASQI Engineer to orchestrate model evaluations.
- Use Garak to test selected prompt-injection and encoded-instruction risks.
- Convert technical results into an ASQI scorecard.
- Preserve reviewed, reproducible evidence without overstating assurance.

## Data notice

This is a portfolio and learning project. It contains no production systems, production credentials, real customer records, customer personal data, or payment data. Reviewed evidence may include the project author's name for assessment provenance.

The retailer, policies, users, prompts, API keys, and test scenarios are fictional or synthetic. Raw evaluation outputs must be reviewed and sanitized before they are committed.

## Architecture

```text
ASQI Engineer
        |
        v
Garak test container
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
## Why ASQI Engineer and Garak

ASQI Engineer provides the orchestration layer for validating configuration, executing the pinned containerized test framework, preserving workflow metadata and applying an explicit scorecard to the results.

Garak was selected to provide targeted adversarial evidence for the risks defined in the threat model. The assessment deliberately uses selected prompt-injection and encoded-instruction probes rather than claiming comprehensive red-team coverage.

The evaluation targets the FastAPI gateway rather than Ollama directly. This includes the application's trusted system prompt, authentication boundary and request controls within the evaluated system.

## Model

This project uses `llama3.2:3b-instruct-q4_K_M` through Ollama.

See [the model record](docs/model-record.md) for hardware, configuration, provenance, and known limitations.

## Current assessment outcome

The [AI assurance report](docs/assurance-report.md) provides the complete assessment scope, method, results, findings, scorecard decision, limitations and retest triggers.

- The current assurance status is **PROVISIONAL**. R1 remains open because `F-001` is a confirmed and reproducible prompt-injection policy override. R2 has limited evidence, R3 through R5 are not assessed, and no mitigation or equivalent retest has been completed.
- The [initial Garak smoke assessment](evidence/reviewed/garak-smoke-assessment-2026-09-27.md) documents execution status, manual classifications, limitations, and the first grouped R1 prompt-injection finding.
- The [focused Garak assessment](evidence/reviewed/garak-focused-2026-10-02/summary.md) expands the configured R1 and R2 coverage and records a representative reproduction sample. Unsampled detector signals remain unconfirmed.
- [Findings and triage notes](docs/findings.md) preserve the risk mapping, evidence references, reproduction status, and residual limitations.
- The [scoring method](docs/scoring-method.md) explains how execution, detector signals, manual review, and risk status are converted into decision support.
- The [baseline scorecard](evidence/reviewed/baseline-scorecard-2026-10-04/summary.md) records the current ASQI-managed release judgment.
- The [evidence index](evidence/README.md) distinguishes local raw output from reviewed evidence suitable for version control.

These results demonstrate selected evaluation workflows, not complete security coverage or certification.

## Local authentication boundary

The published `local-lab-key` is a development-only accidental-traffic guard. It is intentionally not treated as a secret and is not a meaningful authentication or authorization control for production or untrusted networks. Replace the mechanism before any non-local deployment.

## Testing

See [TESTING.md](TESTING.md) for local setup, smoke-test commands, expected results, and manual security checks.
