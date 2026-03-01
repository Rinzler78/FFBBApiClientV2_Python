# Project Context

## Purpose
Modern Python client library for FFBB APIs, exposing a typed dual-backend facade over Directus REST and Meilisearch.

## Tech Stack
- Python 3.10+
- requests, requests-cache
- python-dateutil, python-dotenv
- pytest, tox, pre-commit
- Directus REST API and Meilisearch API backends

## Project Conventions

### Code Style
FFBBApiClientV2_Python enforces Clean Code, SOLID, DRY, and KISS through pre-commit and CI quality gates.

### Architecture Patterns
Use explicit architecture boundaries (Clean Architecture) and a dual-backend facade pattern (Directus + Meilisearch) per domain entity.

### Testing Strategy
Use TDD by default for new behavior and keep unit/integration/e2e coverage aligned with risk.

### Git Workflow
Git Flow with master/develop, feature branches in dedicated worktrees, and Conventional Commits.

## Domain Context
FFBB basketball entities: organismes, clubs, salles, terrains, competitions, engagements, rencontres, joueurs, entraineurs, and saisons.

## Important Constraints
Preserve backward compatibility of the public client API, enforce quality/security gates, and follow Git Flow with linked worktrees.

## External Dependencies
- FFBB Directus REST API
- FFBB Meilisearch API
- PyPI dependencies: requests, requests-cache, python-dateutil, python-dotenv

<!-- BEGIN:OPENSPEC_DELIVERY_RULES -->
## Delivery Rules (Managed)

### Coding & Architecture
- Apply Clean Code + SOLID + DRY + KISS in all implementation tasks.
- Keep Clean Architecture boundaries explicit and preserve separation of concerns.
- Prefer documented and justified design patterns when complexity requires them.

### Testing & Quality
- Default to TDD for new behavior and bug fixes when feasible.
- Require automated unit, integration, and (when relevant) e2e tests.
- Require lint, static analysis, and test execution in CI as blocking gates.
- Maintain coverage targets and no untested bugfix policy.

### Deployment, Release, Tagging
- Define deployment checks and rollback steps for operational changes.
- Maintain SemVer discipline with CHANGELOG updates per release.
- Require annotated Git tags `vMAJOR.MINOR.PATCH` on released versions.

### Agent Controls
- OpenSpec proposal approval is required before non-trivial implementation.
- Agent finalization requires passing pre-commit + CI + security checks.
- Commit only after successful local validation.
- Push branch and open/update PR, then wait for CI checks.
- If PR checks fail, fix and repeat validation -> commit -> push until green.
- Reject completion if governance checks are missing or failing.
<!-- END:OPENSPEC_DELIVERY_RULES -->
