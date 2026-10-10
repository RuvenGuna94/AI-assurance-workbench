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

| Risk ID | Attack or failure | Coverage status | Desired outcome |
| --- | --- | --- | --- |
| R1 | User overrides the system policy | Smoke and focused Garak assessments completed; `F-001` remains open pending remediation and retest | Assistant retains its support role and restrictions |
| R2 | Encoded instructions bypass restrictions | Limited Base64 and ROT13 testing completed; broader resistance not established | Assistant does not comply with harmful encoded requests |
| R3 | Jailbreak changes restrictions | Not assessed; DAN probe deferred | Assistant maintains restrictions |
| R4 | Application reveals its hidden prompt | Not assessed; dedicated prompt-extraction cases required | No system-prompt disclosure |
| R5 | Model fabricates completed actions | Not assessed; separate application-level functional evaluation required | No claims of completed refunds, cancellations, or account deletion |

Risk IDs remain stable as the project evolves. Changes to coverage, severity, or mitigation should update the existing risk entry rather than assign it a new identity.

## Evaluation strategy

The initial scan targets R1 using:

- `promptinject.HijackHateHumans`
- `promptinject.HijackKillHumans`

Initial settings:

- Generations: 1.
- Parallel attempts: 1.
- Concurrent ASQI tests: 1.

The smoke assessment exercises the complete path from ASQI Engineer through Garak, the FastAPI gateway, Ollama, and the local model. The selected probes provide narrow evidence for `R1`; one generation per probe is sufficient for pipeline verification but not for estimating a reliable failure rate.

The focused assessment added a third prompt-injection probe, selected Base64 and ROT13 probes, and three generations per probe. Concurrency was limited to one ASQI test and one Garak attempt to control local resource use and simplify diagnosis.

A detector signal requires manual review. A passing probe establishes only that its detector did not identify the target behavior under the recorded configuration.

## Coverage limitations

Garak provides evidence for selected vulnerability classes, not complete coverage of every application requirement.

R2 received limited Base64 and ROT13 testing in the focused assessment. R3 remains a planned extension. R4 requires dedicated prompt-extraction tests. R5 requires a separate functional evaluation and is not claimed as covered by the completed Garak scans.

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

## Focused Garak expansion scope

The focused assessment expands R1 and begins R2 evaluation.

R1 is evaluated using:

- `promptinject.HijackHateHumans`
- `promptinject.HijackKillHumans`
- `promptinject.HijackLongPrompt`

R2 is evaluated using:

- `encoding.InjectBase64`
- `encoding.InjectROT13`

The focused suite requests three generations per probe, one parallel Garak attempt and one concurrent ASQI test. These settings provide additional sampling while keeping local execution sequential.

The expanded scan still provides selected evidence rather than complete coverage. Three generations are insufficient to establish a statistically reliable failure rate, and passing these probes does not establish general resistance to prompt injection or encoded instructions.

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
- [Evaluation findings](findings.md)
- [Assurance report](assurance-report.md)
