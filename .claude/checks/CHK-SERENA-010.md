---
id: CHK-SERENA-010
type: configuration
title: "Serena project configuration"
description: "Verify .serena/project.yml exists with correct language and settings."
enabled: true
default_severity: medium
applies_when:
  stacks: [python]
  paths_exist_any: [".serena/project.yml"]
evidence:
  all_of:
    - file: ".serena/project.yml"
      exists: true
    - file: ".serena/project.yml"
      contains_all: ["python", "read_only: false"]
recommendations:
  - key: serena_config_valid
    summary: "Ensure Serena project config specifies python language and is not read-only"
    source: "global Serena project setup policy"
    target_files: [".serena/project.yml"]
validation_criteria:
  required:
    - "Serena activates project without error"
  ci_expected: []
tags: ["configuration", "serena"]
owner: "project"
version: 1
---

## Intent
Ensure Serena semantic code analysis is properly configured for this Python project.
