# Project Agent Overlay (Claude)

This file is the Claude-specific governance overlay for FFBBApiClientV2_Python.
It complements the project root `AGENTS.md` with Claude runtime agent routing.

## Project Agents

| Agent | Model | Inherits | Responsibility |
|-------|-------|----------|----------------|
| api-contract-guardian | sonnet | api-contract-guardian (global) | API contract stability, model validation, backward compatibility |
| python-reviewer | sonnet | python-reviewer (global) | Code quality, type annotations, pattern compliance, regression detection |
| release-manager-lite | haiku | release-manager (global) | Release readiness, SemVer, CHANGELOG, CI status verification |

## Routing Priority

1. Project agents take priority over global counterparts for domain-specific work.
2. Global system agents (orchestrator-planner, security-auditor, etc.) handle cross-cutting concerns.
3. When both match, prefer the project agent — it delegates to global as needed.

## Check Ownership

| Agent | Checks Owned |
|-------|-------------|
| api-contract-guardian | CHK-CONTRACT-TESTS-016, CHK-AGENTS-014 |
| python-reviewer | CHK-PRECOMMIT-001, CHK-STATIC-002, CHK-TESTS-003, CHK-LOCALVAL-006, CHK-HOOKS-015 |
| release-manager-lite | CHK-SEMVER-007, CHK-GITFLOW-008, CHK-CI-005, CHK-SECURITY-004, CHK-OPENSPEC-009, CHK-SERENA-010, CHK-SERENA-MEM-011, CHK-MCP-012 |
