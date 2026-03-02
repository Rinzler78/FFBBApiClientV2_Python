---
id: CHK-AGENTS-014
type: quality
title: "Agent definitions quality"
description: "Verify agent definitions contain domain-specific prompts with actionable instructions."
enabled: true
default_severity: low
applies_when:
  stacks: [python]
  paths_exist_any: [".claude/agents"]
evidence:
  all_of:
    - file: ".claude/agents/api-contract-guardian.md"
      exists: true
    - file: ".claude/agents/python-reviewer.md"
      exists: true
recommendations:
  - key: agent_definitions_enriched
    summary: "Each agent file should be >10 lines with domain-specific prompts, tool restrictions, and operational procedures"
    source: "project governance agent optimization"
    target_files: [".claude/agents/api-contract-guardian.md", ".claude/agents/python-reviewer.md", ".claude/agents/release-manager-lite.md", ".claude/agents/project-orchestrator.md", ".claude/agents/project-code-reviewer.md", ".claude/agents/project-test-guardian.md", ".claude/agents/project-cost-optimizer.md"]
validation_criteria:
  required:
    - "Each agent file is >10 lines with actionable instructions"
  ci_expected: []
tags: ["quality", "agents"]
owner: "project"
version: 1
---

## Intent
Ensure agent definitions provide enough domain context for effective, token-efficient execution.
