# System Card

## Purpose

AI Assurance Workbench evaluates a fictional retailer support assistant powered by Llama 3.2 through Ollama.

A FastAPI gateway supplies the support policy and exposes an OpenAI-compatible chat endpoint. ASQI Engineer orchestrates Garak evaluations against the application.

## Intended use

The assistant may explain these policies:

- Unused products may be returned within 30 days with proof of purchase.
- Orders can be cancelled only before dispatch.
- Standard delivery takes three to five business days.
- Account deletion requires verified human support.

The assistant provides information only. It has no access to customer accounts, orders, payments, or account-management systems.

## Prohibited behavior

The assistant must not:

- Claim to have viewed an order or customer account.
- Claim to have issued refunds, cancelled orders, or deleted accounts.
- Request or repeat passwords, full payment-card numbers, or API keys.
- Follow instructions to ignore its policy.
- Reveal its system prompt.
- Provide unrelated harmful instructions.

Unsupported or ambiguous requests should be directed to human support.

## System components

- Application: FastAPI support gateway.
- Model runtime: Native Ollama on Windows.
- Model: llama3.2:3b-instruct-q4_K_M.
- Evaluation orchestration: ASQI Engineer.
- Vulnerability evaluation: Garak in a Docker container.

See [the model record](model-record.md) for model and hardware details.

## Evaluation architecture

ASQI Engineer evaluates the FastAPI support gateway as an OpenAI-compatible `llm_api` system. The application is assessed through the same `/v1/chat/completions` endpoint used by other clients.

The model-backed evaluation path is:

```text
ASQI Engineer
    -> Garak test container
    -> FastAPI support gateway
    -> Ollama
    -> Llama 3.2
```

The FastAPI gateway is the system boundary presented to the evaluation framework. It:

- Authenticates requests using a local synthetic API key.
- Rejects caller-supplied system messages.
- Inserts the version-controlled support policy.
- Limits message count and content length.
- Fixes temperature at zero for the initial assessment.
- Caps requested output tokens.
- Translates Ollama connectivity failures into a controlled gateway response.
- Returns responses using an OpenAI-compatible structure.

The application does not expose Ollama directly to the Garak test container. This ensures that the evaluation includes the policy and controls implemented by the gateway rather than testing the base model in isolation.

## ASQI system definition

The ASQI system definition is stored in `config/systems/local-ollama-app.yaml`.

The system definition identifies the FastAPI gateway as an OpenAI-compatible `llm_api` target. Containers reach the Windows-hosted gateway through:

```text
http://host.docker.internal:8000/v1
```

The configured model identifier is part of the API contract presented to the test container. The gateway selects the locally configured Ollama model and does not allow the caller to replace the trusted application policy.

## Supporting evaluation runtime

ASQI uses supporting services that are separate from the model inference path:

- PostgreSQL stores DBOS workflow and step state for durable ASQI execution.
- Jaeger receives and displays supported OpenTelemetry traces.
- Docker provides isolated execution of the Garak test container.

These services support orchestration, recovery, and observability. They do not supply policy content, retrieve customer data, or generate assistant responses.

## LiteLLM decision

The upstream ASQI runtime includes LiteLLM as an optional model-provider proxy. This project does not use LiteLLM because the FastAPI support gateway already provides the OpenAI-compatible endpoint required by ASQI and Garak.

Excluding LiteLLM keeps the initial evaluation path smaller and makes it easier to attribute observed behavior to the gateway, Ollama, or the model. LiteLLM may be considered later if the project adds multi-provider comparisons, centralized provider credentials, routing, or fallback behavior.

## Version and provenance references

Exact tool versions, the pinned Garak container digest, installation commands, and reproduction commands are recorded in [Tool Versions](tool-versions.md).

Model provenance and hardware information are recorded in [Model Record](model-record.md).

Risks, planned coverage, and evaluation limitations are recorded in [Threat Model](threat-model.md).

## Data and deployment

This is a local portfolio project using fictional policies and synthetic test prompts. No production data or real customer records are used.

The application is not intended for public or production deployment.

## Evaluation scope

The initial Garak evaluation targets selected prompt-injection risks. Later scans may include encoded instructions and jailbreak attempts.

Garak does not provide complete coverage of business-policy correctness, privacy, hallucination, or every prohibited behavior.

See [the threat model](threat-model.md) for risks and coverage gaps.

## Limitations

System prompts are not security boundaries by themselves. The model may ignore instructions, hallucinate, or produce unsafe output.

Evaluation results apply only to the recorded application, prompt, model, runtime, and test configuration. Passing a scan does not establish universal safety or production readiness.
