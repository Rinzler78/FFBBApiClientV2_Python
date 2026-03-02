---
id: CHK-SECURITY-004
type: security
title: "Secrets detection"
description: "Verify gitleaks is configured in CI and local validation."
enabled: true
default_severity: critical
applies_when:
  stacks: [python]
  paths_exist_any: [".github/workflows/quality-gates.yml"]
evidence:
  all_of:
    - file: ".github/workflows/quality-gates.yml"
      contains_all: ["gitleaks"]
    - file: "scripts/validate-local.sh"
      contains_all: ["gitleaks"]
recommendations:
  - key: secret_scanning_enforced
    summary: "Ensure gitleaks runs in CI and local validation to prevent secret leaks"
    source: "global security baseline"
    target_files: [".github/workflows/quality-gates.yml", "scripts/validate-local.sh"]
validation_criteria:
  required:
    - "gitleaks detect --source . --no-banner --redact exits 0"
  ci_expected:
    - "security"
tags: ["security", "secrets", "gitleaks"]
owner: "project"
version: 1
---

## Intent
Prevent accidental secret commits via automated scanning in both local and CI pipelines.
