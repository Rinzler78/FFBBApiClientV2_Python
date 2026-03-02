---
id: CHK-STATIC-002
type: quality
title: "Static analysis (lint + type check)"
description: "Verify pylint, pyright, and flake8 are configured and passing."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: ["pyproject.toml"]
evidence:
  all_of:
    - file: "pyproject.toml"
      contains_all: ["tool.pyright", "tool.pylint"]
    - file: ".pre-commit-config.yaml"
      contains_all: ["pylint", "pyright", "flake8"]
recommendations:
  - key: static_analysis_configured
    summary: "Ensure pyright, pylint, and flake8 are all configured in pyproject.toml and pre-commit"
    source: "AGENTS.md quality gates"
    target_files: ["pyproject.toml", ".pre-commit-config.yaml"]
validation_criteria:
  required:
    - "pre-commit run pylint --all-files exits 0"
    - "pre-commit run pyright --all-files exits 0"
    - "pre-commit run flake8 --all-files exits 0"
  ci_expected:
    - "quality"
tags: ["quality", "lint", "type-check", "python"]
owner: "project"
version: 1
---

## Intent
Catch type errors, code smells, and style issues before code reaches CI.
