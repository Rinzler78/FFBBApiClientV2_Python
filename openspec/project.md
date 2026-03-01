# Project Context

## Purpose
Modern Python client library for the FFBB (French Basketball Federation) APIs. Provides a dual-backend facade over Directus REST and Meilisearch endpoints with type-safe models, flexible field selection, and comprehensive testing.

## Tech Stack
- Python 3.10+
- requests / requests-cache (HTTP + caching)
- python-dateutil, python-dotenv (utilities)
- Directus REST API backend
- Meilisearch search backend
- pytest, tox, pre-commit (dev tooling)

## Project Conventions

### Code Style
FFBBApiClientV2_Python enforces Clean Code, SOLID, DRY, and KISS through pre-commit and CI quality gates.

### Architecture Patterns
Dual-backend facade pattern: each FFBB entity can be queried via Directus REST or Meilisearch. Use explicit architecture boundaries (Clean Architecture) and documented design patterns per module.

### Testing Strategy
Use TDD by default for new behavior and keep unit/integration/e2e coverage aligned with risk. Contract tests validate API response schemas.

### Git Workflow
Git Flow with master/develop, feature branches in dedicated worktrees, and Conventional Commits.

## Domain Context
FFBB basketball domain entities: organismes, clubs, salles, terrains, competitions, engagements, rencontres, joueurs, entraineurs, saisons. The client exposes typed models for each entity and supports dual-backend queries (Directus for structured data, Meilisearch for full-text search).

## Important Constraints
Preserve backward compatibility of the public API surface. Enforce quality/security gates and follow Git Flow/worktree policy. Both API backends may evolve independently.

## External Dependencies
- FFBB Directus REST API (primary structured data source)
- FFBB Meilisearch instance (full-text search)
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
