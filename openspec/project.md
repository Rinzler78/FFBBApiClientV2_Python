# Project Context

## Purpose
Python client library for the FFBB (Federation Francaise de Basketball) API v2. Provides a unified facade over Directus REST API (14 collections) and Meilisearch full-text search (9 indexes) for accessing French basketball data: clubs, teams, competitions, matches, venues, coaches, tournaments, and more.

## Tech Stack
- python

## Project Conventions

### Code Style
FFBBApiClientV2_Python enforces Clean Code, SOLID, DRY, and KISS through pre-commit and CI quality gates.

### Architecture Patterns
Use explicit architecture boundaries (Clean Architecture) and documented design patterns per module.

### Testing Strategy
Use TDD by default for new behavior and keep unit/integration/e2e coverage aligned with risk.

### Git Workflow
Git Flow with master/develop, feature branches in dedicated worktrees, and Conventional Commits.

## Domain Context
French basketball federation data ecosystem. The API serves club management, competition tracking, match scheduling, venue/court geolocation, coach/official registries, 3x3 tournaments, and training/formation catalogs. Data is accessed via dual backends: Directus (relational, FK-based) and Meilisearch (denormalized, full-text + geo-spatial search). Token-based authentication with automatic token management via TokenManager.

## Important Constraints
Preserve backward compatibility, enforce quality/security gates, and follow Git Flow/worktree policy.

## External Dependencies
FFBB Directus REST API (https://api.ffbb.app/), FFBB Meilisearch instance, requests, requests-cache (HTTP caching), python-dateutil, python-dotenv.

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
