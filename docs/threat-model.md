# Threat Model

## Scope

This document describes risks to a fictional retailer support assistant powered by a locally hosted language model.

The evaluated system includes the FastAPI gateway, its system policy, and the Ollama-backed model. It does not include real order, payment, or customer-account systems.

## Assets to protect

- Integrity of the support policy.
- Accurate representation of the assistant's capabilities.
- Confidentiality of application instructions.
- Sensitive information that a user might submit.
- Availability of the local application and model runtime.
- Integrity and provenance of evaluation evidence.

The system prompt must contain no real credentials or secrets. Preventing prompt disclosure is a behavioral requirement, not a substitute for proper secret management.

## Trust boundaries

1. Untrusted user or Garak input enters the FastAPI gateway.
2. The gateway adds trusted application instructions.
3. The combined messages are sent to Ollama.
4. Untrusted model output is returned through the gateway.
5. Evaluation outputs are reviewed before publication.

User input and model output must not be treated as trusted instructions. The gateway must not allow callers to replace its system policy.

## Threat assumptions

- An attacker can submit arbitrary text through the chat endpoint.
- Attackers may impersonate administrators or claim special authority.
- Attackers may encode instructions or use role-play and jailbreaks.
- The model may follow malicious instructions despite the system policy.
- There are no tools capable of performing actual customer-account actions.

## Risk register

| Risk ID | Attack or failure | Planned coverage | Desired outcome |
| --- | --- | --- | --- |
| R1 | User overrides the system policy | Initial Garak prompt-injection probes | Assistant retains its support role and restrictions |
| R2 | Encoded instructions bypass restrictions | Later Garak Base64 and ROT13 probes | Assistant does not comply with harmful encoded requests |
| R3 | Jailbreak changes restrictions | Later Garak DAN probe, subject to installed probe availability | Assistant maintains restrictions |
| R4 | Application reveals its hidden prompt | Dedicated prompt-extraction cases planned; not covered by the initial scan | No system-prompt disclosure |
| R5 | Model fabricates completed actions | Separate application-level functional evaluation planned | No claims of completed refunds, cancellations, or account deletion |

Risk IDs remain stable as the project evolves. Changes to coverage, severity, or mitigation should update the existing risk entry rather than assign it a new identity.

## Initial Garak test scope

The initial scan targets R1 using:

- `promptinject.HijackHateHumans`
- `promptinject.HijackKillHumans`

Initial settings:

- Generations: 1.
- Parallel attempts: 1.
- Concurrent ASQI tests: 1.

This first run is a smoke evaluation of the complete path from ASQI Engineer through Garak, the FastAPI gateway, Ollama, and the local model. Its purpose is to confirm that the components are correctly connected, requests reach the intended endpoint, responses are captured, detectors execute, and reproducible evidence is produced without overloading the laptop.

The two selected probes exercise a narrow prompt-injection scenario: whether hostile user instructions can cause the assistant to abandon its support role and produce prohibited content. They provide evidence relevant to R1, but they do not establish complete prompt-injection resistance. One generation per probe is deliberately economical and is insufficient for estimating a reliable failure rate because probabilistic model behaviour may vary between runs.

The constrained concurrency settings reduce local CPU, GPU, and memory pressure and make failures easier to diagnose. After the pipeline works reliably, later evaluation stages should increase the number of generations, broaden probe coverage for R1 through R4, and document all configuration changes so results remain comparable.

A passing result means only that the selected probes did not trigger their associated detectors during that particular run and configuration. It does not prove that the application is secure, that R1 has been eliminated, or that another prompt variation will receive the same response. A detector failure is a signal for investigation and review, not automatic proof of an exploitable vulnerability.

The run should record enough metadata to reproduce the result, including the application commit, ASQI Engineer version or image reference, Garak version, probe and detector names, model tag, Ollama version, generation and concurrency settings, and execution date.

Probe names and availability must be checked against the Garak version included in the pinned ASQI test container. Any unavailable or renamed probe should be documented as a configuration difference rather than silently replaced.

## Coverage limitations

Garak provides evidence for selected vulnerability classes, not complete coverage of every application requirement.

R2 and R3 are planned extensions. R4 requires dedicated extraction tests. R5 is documented but is not claimed as covered by the initial Garak scan.

The initial scan also does not establish:

- Correct answers to every retailer-policy question.
- Protection against every sensitive-data disclosure.
- Resistance to denial of service.
- Fairness or absence of bias.
- Production readiness or regulatory compliance.

## Finding review

For each potential finding:

1. Record the risk ID, probe, and detector.
2. Record code, prompt, model, runtime, and container versions.
3. Review the generated output.
4. Attempt to reproduce the behavior.
5. Distinguish a detector signal from a confirmed application failure.
6. Describe impact within the intended use.
7. Document mitigation and retest results.

A successful scan execution can still contain security failures.

## Retest triggers

Repeat relevant evaluations when changing:

- Application code or input controls.
- System policy.
- Model or quantization.
- Ollama version or inference settings.
- ASQI version.
- Garak container, probes, or detectors.
- Evaluation thresholds.

## Related documents

- [System card](system-card.md)
- [Model record](model-record.md)
