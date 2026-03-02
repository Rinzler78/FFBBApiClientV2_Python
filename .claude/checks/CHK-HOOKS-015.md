---
id: CHK-HOOKS-015
type: quality
title: "Post-edit hook (auto-format)"
description: "Verify PostToolUse hook auto-formats .py files on Write/Edit."
enabled: true
default_severity: low
applies_when:
  stacks: [python]
  paths_exist_any: [".claude/settings.local.json"]
evidence:
  all_of:
    - file: ".claude/settings.local.json"
      contains_all: ["PostToolUse", "ruff", "black", ".py"]
recommendations:
  - key: auto_format_hook_active
    summary: "Ensure PostToolUse hook runs ruff or black on .py files after Write/Edit/MultiEdit"
    source: "project quality baseline"
    target_files: [".claude/settings.local.json"]
validation_criteria:
  required:
    - "Hook fires on .py edit and formats without error"
  ci_expected: []
tags: ["quality", "hooks", "formatting"]
owner: "project"
version: 1
---

## Intent
Prevent formatting drift by auto-formatting Python files after every AI-assisted edit.
