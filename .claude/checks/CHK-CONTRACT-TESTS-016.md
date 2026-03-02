---
id: CHK-CONTRACT-TESTS-016
type: quality
title: "API contract tests"
description: "Verify contract tests exist for FFBB API endpoint methods."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: ["tests/"]
evidence:
  all_of:
    - file: "tests/"
      exists: true
recommendations:
  - key: contract_tests_present
    summary: "Ensure contract tests validate API response models match upstream FFBB API contracts"
    source: ".claude/CLAUDE.md contract testing requirement"
    target_files: ["tests/"]
validation_criteria:
  required:
    - "Contract tests exist for each endpoint method in DirectusFfbb and MeilisearchFfbb"
  ci_expected:
    - "test"
tags: ["quality", "testing", "api-contract", "python"]
owner: "project"
version: 1
---

## Intent
Ensure API client methods produce responses matching the upstream FFBB API contract structure.
