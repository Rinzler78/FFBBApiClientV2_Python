---
id: CHK-GITFLOW-008
type: process
title: "Git Flow + worktree policy"
description: "Verify Git Flow branching model and worktree usage for implementation branches."
enabled: true
default_severity: medium
applies_when:
  stacks: [python]
  paths_exist_any: ["AGENTS.md"]
evidence:
  all_of:
    - file: "AGENTS.md"
      contains_all: ["worktree", "develop", "master"]
    - file: ".github/workflows/quality-gates.yml"
      contains_all: ["develop", "master"]
recommendations:
  - key: gitflow_worktree_enforced
    summary: "Ensure branch naming follows Git Flow and implementation uses linked worktrees"
    source: "global governance git-worktree-strategy"
    target_files: ["AGENTS.md"]
validation_criteria:
  required:
    - "Branch naming follows feature/fix/release/hotfix convention"
    - "Implementation branches use dedicated linked worktrees"
  ci_expected:
    - "quality"
tags: ["process", "git-flow", "worktree"]
owner: "project"
version: 1
---

## Intent
Enforce Git Flow branching model with worktree isolation for parallel development safety.
