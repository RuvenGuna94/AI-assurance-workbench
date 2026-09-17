# Evaluation Evidence

This directory contains reviewed evidence produced while testing the AI Assurance Workbench.

## Directory policy

- `local/` contains raw or temporary test output and is excluded from Git.
- `reviewed/` contains sanitised evidence selected for version control.
- Raw outputs must be reviewed before they are copied into `reviewed/`.
- Production data, real credentials, personal information, and model binaries must never be committed.

## Evidence requirements

Each reviewed test record should identify:

- Execution date.
- Reviewer.
- Git commit hash.
- Application and evaluation configuration.
- Model tag and runtime version.
- Commands or test suite executed.
- Expected outcome.
- Observed outcome.
- Pass, fail, or needs-review status.
- Relevant risk IDs.
- Known limitations or deviations.

A successful command execution does not necessarily mean that the evaluated behavior passed.