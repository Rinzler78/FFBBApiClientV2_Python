---
id: CHK-HOOKS-015
type: quality
title: "Post-edit hook (auto-format)"
description: "Verify PostToolUse hook auto-formats .py files on Write/Edit. Hook may live at project or global scope."
enabled: true
default_severity: low
applies_when:
  stacks: [python]
  paths_exist_any: [".claude/settings.local.json"]
evidence:
  any_of:
    - file: ".claude/settings.local.json"
      contains_all: ["PostToolUse", "ruff", "black", ".py"]
    - runtime_check: "global ~/.claude/settings.json contains PostToolUse hook with ruff/black auto-format for .py files (scope delegation)"
recommendations:
  - key: auto_format_hook_active
    summary: "Ensure PostToolUse hook runs ruff or black on .py files after Write/Edit/MultiEdit. Hook may be defined at project scope (.claude/settings.local.json) or global scope (~/.claude/settings.json). If delegated to global, document in .claude/tooling-decisions.yaml."
    source: "project quality baseline + quality_hooks_scope_delegation"
    target_files: [".claude/settings.local.json", ".claude/tooling-decisions.yaml"]
validation_criteria:
  required:
    - "Hook fires on .py edit and formats without error"
    - "Hook exists at project or global scope (not both)"
  ci_expected: []
tags: ["quality", "hooks", "formatting", "scope-delegation"]
owner: "project"
version: 2
---

## Intent
Prevent formatting drift by auto-formatting Python files after every AI-assisted edit. The hook may be defined at global scope to avoid duplication across projects; in that case, project settings.local.json hooks can be empty if documented in tooling-decisions.yaml.
