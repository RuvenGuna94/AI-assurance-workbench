# Evaluation Evidence

This directory contains reviewed evidence produced while testing the AI Assurance Workbench. The evidence demonstrates how ASQI Engineer, Garak, the FastAPI gateway, and the local Ollama-backed model were configured, executed, and reviewed.

The workbooks may contain adversarial prompts and model-generated hostile language created during security testing. They contain no production customer data.

## Directory policy

- `local/` contains raw, temporary, or unreviewed test output and is excluded from Git.
- `reviewed/` contains sanitised evidence selected for version control.
- Raw output must be manually reviewed before it is copied into `reviewed/`.
- Production data, real credentials, customer or third-party personal information, authorization headers, API keys, and model binaries must never be committed. Project-author and reviewer attribution may be retained for provenance.
- A reviewed evidence artifact should remain traceable to its application commit, configuration, model, runtime, and evaluation execution.
- Detailed model output should be published only when it has been inspected for sensitive information and unnecessary local environment details.

## Evidence workflow

Evaluation evidence moves through the following stages:

1. ASQI Engineer executes the configured evaluation suite.
2. Garak submits adversarial prompts to the application and records detector results.
3. Raw results are stored under `local/`.
4. Detector signals and model outputs are manually reviewed.
5. Relevant attempts are reproduced when confirmation is required.
6. Sensitive or environment-specific information is removed.
7. Sanitised summaries and review workbooks are copied into `reviewed/`.
8. Confirmed findings, limitations, mitigations, and retest outcomes are recorded in [`docs/findings.md`](../docs/findings.md).

A detector signal is an investigation lead. It is not automatically a confirmed vulnerability.

## Evidence requirements

Each reviewed test record should identify:

- Execution date.
- Reviewer.
- Evaluated Git commit hash.
- ASQI workflow or execution identifier.
- Application and evaluation configuration.
- Model tag, quantisation, and runtime version.
- ASQI Engineer and Garak versions.
- Test-container image and digest where available.
- Commands or test suite executed.
- Expected outcome.
- Observed outcome.
- Review classification.
- Severity where a finding has been assessed.
- Relevant risk IDs.
- Reproduction result where confirmation was attempted.
- Known limitations, deviations, and residual uncertainty.

A successful command, container, ASQI workflow, or Garak execution means that the evaluation infrastructure completed its work. It does not mean that the evaluated application passed the security assessment.

## Understanding the review workbooks

Detailed review workbooks contain three worksheets.

### Probe Summary

`Probe Summary` provides aggregate results by Garak probe and detector.

It records:

- Risk ID.
- Source result file.
- Garak run ID.
- Number of generations.
- Probe and detector.
- Passed attempts.
- Total attempts.
- Number of detector signals requiring review.
- Automated pass rate.

The pass rate is an automated Garak measurement. It must not be presented as a general security score or proof that the application is safe.

### Signals

`Signals` is the investigation queue. It contains detector results that met the configured review threshold.

For the published workbooks, a detector score of `0.5` or greater was selected for review.

This worksheet records:

- The relevant risk ID.
- Garak run and attempt identifiers.
- Probe and detector.
- Detector score.
- Prompt submitted during the test.
- Model-generated output.
- Detector trigger and probe goal.
- Manual-review classification.
- Grouped finding identifier.
- Reviewer notes.

Rows in this worksheet require human interpretation. A detector may fire because the model followed an adversarial instruction, but it may also fire because the model repeated the trigger while refusing the request.

### All Attempts

`All Attempts` contains the complete detector-level evaluation record, including attempts that did not produce a review signal.

This worksheet supports:

- Confirmation that the expected tests ran.
- Review of successful and unsuccessful model responses.
- Investigation of suspicious responses below the selected threshold.
- Comparison across probes, prompts, and detectors.
- Traceability between aggregate results and individual attempts.
- Independent review of the evaluation conclusions.

Only rows producing review signals receive classifications. Blank classification fields in `All Attempts` normally indicate that the corresponding detector result did not enter the manual-review queue.

One Garak attempt may be evaluated by multiple detectors. The same prompt and response may therefore appear in more than one detector-level row.

## Classification taxonomy

| Classification | Meaning |
| --- | --- |
| `Confirmed` | The observed policy failure was manually reproduced under the recorded application, model, and runtime configuration. |
| `Not reproduced` | The original detector signal did not repeat during the documented reproduction attempts. |
| `False positive` | The detector fired, but manual review found that the output did not exhibit the assessed policy failure. |
| `Needs review` | The output appears relevant to a potential failure, but further investigation or reproduction is required. |
| `Environmental failure` | The result was caused by an infrastructure, connectivity, resource, or runtime problem. |
| `Configuration failure` | The evaluation configuration was invalid or incompatible with the installed tools. |
| `Not applicable` | The detector result does not apply to the assessed risk or intended use. |

`Needs review` must not be reported as `Confirmed`. Confirmation requires sufficient evidence, including reproduction where the review method requires it.

## Grouping findings

Multiple detector signals can represent variations of the same underlying control weakness. The evidence therefore distinguishes:

- Individual detector signals.
- Individual reproduction attempts.
- Grouped findings representing an underlying application weakness.

Grouped finding identifiers such as `F-001` or `FT-001` prevent repeated prompt variations from being reported as separate vulnerabilities when they demonstrate the same root cause.

The total number of detector signals must not be presented as the total number of confirmed vulnerabilities.

## Interpreting the results

Review conclusions must consider the application’s intended use and actual capabilities.

The evaluated application:

- Uses a fictional retailer-support policy.
- Has no access to real customer accounts.
- Has no access to orders, payment systems, or production data.
- Cannot issue refunds, cancel orders, or delete accounts.
- Does not have external action-taking tools.

A prompt-injection failure can still demonstrate that the application abandoned its intended role or restrictions. However, its impact should not be overstated as customer harm, sensitive-data disclosure, or external-system compromise unless the evaluation actually demonstrates those outcomes.

Passing selected probes does not establish general resistance to prompt injection, encoded instructions, jailbreaks, prompt extraction, hallucination, privacy risks, denial of service, or business-policy failures.

Results apply only to the recorded application code, system prompt, model, quantisation, runtime, inference settings, ASQI version, Garak version, container image, probes, detectors, and concurrency settings.

## Sanitisation checks

Before an artifact is added to `reviewed/`, check it for:

- Passwords, API keys, tokens, and authorization headers.
- Customer or third-party personal information and usernames. Project-author and reviewer attribution may be retained when required for provenance.
- Customer, payment, or production data.
- Absolute local filesystem paths.
- Environment variables and local configuration values.
- Hidden worksheets or columns containing unreviewed data.
- Comments, document properties, external links, or formulas containing local information.
- Unexpectedly sensitive or harmful model output.
- Duplicate evidence that may confuse the evaluation record.

Sanitisation must not alter the meaning of the reviewed result. If text must be removed or replaced, document that the evidence was sanitised.

## Published workbooks

GitHub does not render `.xlsx` workbook contents. Each published workbook therefore has an accompanying Markdown summary describing its scope, results, review state, and limitations.

The published workbooks contain:

- The smoke assessment classification and detailed-attempt review.
- The focused assessment’s row-level prompt, response, detector, and classification records.
- The provisional baseline scorecard and its source JSON.

Result counts and assessment conclusions are maintained in the corresponding run summaries and the [findings register](../docs/findings.md). This file defines how evidence is handled; it is not a second assessment report.

Representative reproduction material remains in `evidence/local/` and has not been published. Its summarised conclusions are recorded in reviewed documentation, but the workbook must not be committed unless it is separately reviewed, sanitised, and deliberately selected for publication.

## Reviewed evidence

- [Local environment record](reviewed/environment-record.md)
- [Garak smoke assessment summary — 2026-09-27](reviewed/garak-smoke-assessment-2026-09-27.md)
- [Garak smoke assessment review workbook — 2026-09-27](reviewed/garak-smoke-review-2026-09-27.xlsx)
- [Garak smoke detailed-attempt review workbook — 2026-09-27](reviewed/garak-smoke-detailed-review-2026-09-27.xlsx)
- [Focused Garak baseline — 2026-10-01](reviewed/garak-focused-2026-10-01/summary.md)
- [Focused Garak assessment — 2026-10-02](reviewed/garak-focused-2026-10-02/summary.md)
- [Focused Garak detailed-review workbook — reviewed 2026-10-04](reviewed/garak-focused-2026-10-02/detailed-review-2026-10-04.xlsx)
- [Provisional ASQI baseline scorecard — 2026-10-04](reviewed/baseline-scorecard-2026-10-04/summary.md)
- [Reviewed ASQI baseline scorecard JSON — 2026-10-04](reviewed/baseline-scorecard-2026-10-04/baseline-scorecard-results.json)

## Related documentation

- [Evaluation findings](../docs/findings.md)
- [Threat model](../docs/threat-model.md)
- [System card](../docs/system-card.md)
- [Model record](../docs/model-record.md)
- [Tool and runtime versions](../docs/tool-versions.md)
