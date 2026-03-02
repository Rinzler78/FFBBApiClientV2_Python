---
id: CHK-OPENSPEC-009
type: process
title: "OpenSpec methodology"
description: "Verify OpenSpec directory structure, config, and skills are present."
enabled: true
default_severity: medium
applies_when:
  stacks: [python]
  paths_exist_any: ["openspec/config.yaml"]
evidence:
  all_of:
    - file: "openspec/config.yaml"
      exists: true
    - file: "openspec/project.md"
      exists: true
    - file: "openspec/AGENTS.md"
      exists: true
recommendations:
  - key: openspec_structure_complete
    summary: "Ensure OpenSpec directory has config.yaml, project.md, and AGENTS.md"
    source: "global governance openspec-methodology"
    target_files: ["openspec/config.yaml", "openspec/project.md", "openspec/AGENTS.md"]
validation_criteria:
  required:
    - "OpenSpec directory structure complete and skills registered"
  ci_expected: []
tags: ["process", "openspec"]
owner: "project"
version: 1
---

## Intent
Ensure non-trivial changes follow the OpenSpec proposal workflow before implementation.
