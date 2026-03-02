---
id: CHK-CI-005
type: quality
title: "CI workflows"
description: "Verify CI workflows exist for quality gates and test pipeline."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: [".github/workflows/ci.yml"]
evidence:
  all_of:
    - file: ".github/workflows/ci.yml"
      exists: true
    - file: ".github/workflows/quality-gates.yml"
      exists: true
recommendations:
  - key: ci_workflows_present
    summary: "Ensure ci.yml and quality-gates.yml cover prepare/test/finalize/publish and quality/security"
    source: "AGENTS.md deployment rules"
    target_files: [".github/workflows/ci.yml", ".github/workflows/quality-gates.yml"]
validation_criteria:
  required:
    - "CI workflows exist and trigger on push/PR to develop/master"
  ci_expected:
    - "quality"
    - "test"
tags: ["quality", "ci", "github-actions"]
owner: "project"
version: 1
---

## Intent
Ensure CI pipelines block merge on failing quality/security/test checks.
