---
id: CHK-SERENA-MEM-011
type: configuration
title: "Serena memory tools exclusion"
description: "Verify Serena memory tools are excluded to avoid overlap with byterover-mcp."
enabled: true
default_severity: medium
applies_when:
  stacks: [python]
  paths_exist_any: [".serena/project.yml"]
evidence:
  all_of:
    - file: ".serena/project.yml"
      contains_all: ["excluded_tools", "write_memory", "read_memory", "list_memories", "delete_memory"]
recommendations:
  - key: exclude_serena_memory
    summary: "Add write_memory, read_memory, list_memories, delete_memory to excluded_tools"
    source: "global MCP baseline / memory-bank-strategy"
    target_files: [".serena/project.yml"]
validation_criteria:
  required:
    - "excluded_tools list includes write_memory, read_memory, list_memories, delete_memory"
  ci_expected: []
tags: ["configuration", "serena", "memory", "mcp"]
owner: "project"
version: 1
---

## Intent
Keep byterover-mcp as the single durable memory source; prevent Serena memory overlap.
