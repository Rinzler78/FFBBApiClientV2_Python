---
id: CHK-LOCALVAL-006
type: process
title: "Local validation script"
description: "Verify validate-local.sh exists and covers pre-commit, tests, and security."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: ["scripts/validate-local.sh"]
evidence:
  all_of:
    - file: "scripts/validate-local.sh"
      exists: true
    - file: "scripts/validate-local.sh"
      contains_all: ["pre-commit", "tox", "gitleaks"]
recommendations:
  - key: local_validation_complete
    summary: "Ensure validate-local.sh runs pre-commit, tox tests, and gitleaks before delivery"
    source: "AGENTS.md mandatory local validation"
    target_files: ["scripts/validate-local.sh"]
validation_criteria:
  required:
    - "bash scripts/validate-local.sh exits 0"
  ci_expected: []
tags: ["process", "validation", "local"]
owner: "project"
version: 1
---

## Intent
Ensure a comprehensive local validation script exists and is used before every commit.
