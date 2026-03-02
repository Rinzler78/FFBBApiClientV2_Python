---
id: CHK-MCP-012
type: configuration
title: "MCP policy compliance"
description: "Verify no global MCP duplication in project config."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: ["AGENTS.md"]
evidence:
  all_of:
    - file: ".claude/CLAUDE.md"
      contains_all: ["Do not duplicate global MCP"]
recommendations:
  - key: no_global_mcp_duplication
    summary: "Do not duplicate filesystem, MCP_DOCKER, context7, byterover-mcp, serena in project MCP config"
    source: "global MCP policy"
    target_files: [".claude/CLAUDE.md", ".mcp.json"]
validation_criteria:
  required:
    - "No global MCP duplication in project .mcp.json"
  ci_expected: []
tags: ["configuration", "mcp"]
owner: "project"
version: 1
---

## Intent
Prevent MCP confusion and resource duplication by keeping global MCPs at user scope only.
