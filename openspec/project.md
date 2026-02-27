# Project Context

## Purpose
FFBBApiClientV2_Python is a python project.

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
Domain context for FFBBApiClientV2_Python; refine with business-specific details.

## Important Constraints
Preserve backward compatibility, enforce quality/security gates, and follow Git Flow/worktree policy.

## External Dependencies
External APIs/services and third-party dependencies used by FFBBApiClientV2_Python.

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
