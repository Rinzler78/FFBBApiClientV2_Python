---
id: CHK-PRECOMMIT-001
type: quality
title: "Pre-commit configuration"
description: "Verify pre-commit hooks are configured with required quality gates."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: [".pre-commit-config.yaml"]
evidence:
  all_of:
    - file: ".pre-commit-config.yaml"
      exists: true
    - file: ".pre-commit-config.yaml"
      contains_all: ["black", "flake8", "isort", "pylint", "pyright", "pyupgrade", "autoflake"]
recommendations:
  - key: precommit_hooks_complete
    summary: "Ensure all required hooks are present: trailing-whitespace, check-ast, black, flake8, isort, pylint, pyright, pyupgrade, autoflake"
    source: "AGENTS.md quality gates"
    target_files: [".pre-commit-config.yaml"]
validation_criteria:
  required:
    - "pre-commit run --all-files exits 0"
  ci_expected:
    - "quality"
tags: ["quality", "pre-commit", "python"]
owner: "project"
version: 1
---

## Intent
Ensure all Python quality hooks are enforced locally before any commit reaches CI.
