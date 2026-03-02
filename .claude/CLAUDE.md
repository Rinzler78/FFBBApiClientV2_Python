# Project AI Governance

## Scope
Python API client library.

## Required Workflow
- Git flow with master as production branch
- Conventional commits
- Contract tests + unit tests required for API changes

## MCP Policy
- Project MCP allowed: sequential-thinking
- Use global byterover-mcp for durable memory; do not add project-local memory MCP

- `byterover-mcp`: durable cross-project memory.
- `context7`: external documentation retrieval only (no persistent memory).
- `serena`: semantic code navigation/editing only (memory tools disabled in project config).
- Do not duplicate global MCP (`filesystem`, `MCP_DOCKER`, `context7`, `byterover-mcp`, `serena`) in project MCP config.

- Shared memory/MCP policy: `~/.claude/policies/memory-bank-strategy.md`.

## Specialized Agents
- api-contract-guardian (sonnet)
- python-reviewer (sonnet)
- release-manager-lite (haiku)

## Model Policy
- haiku for maintenance/docs
- sonnet for code and tests
- opus only for high-risk refactors

## Serena Project Setup
- This project must keep `.serena/project.yml` up to date.
- Serena MCP runs globally with `--project-from-cwd`.
- Activate Serena project context at session start when needed.
