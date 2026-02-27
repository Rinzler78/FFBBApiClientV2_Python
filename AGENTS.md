<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so `openspec update` can refresh the instructions.
<!-- OPENSPEC:END -->

<!-- BEGIN:PROJECT_GOVERNANCE_RULES -->
## Project Engineering Rules (Managed)

### Coding Rules
- Apply Clean Code principles: small cohesive units, explicit naming, no dead code.
- Apply SOLID, DRY, and KISS by default.
- Keep clear Clean Architecture boundaries (domain/application/infrastructure).
- Use design patterns only when they reduce complexity and improve maintainability.

### Testing Rules
- Prefer TDD for new behavior (Red -> Green -> Refactor).
- Require automated unit tests for business logic and integration tests for external boundaries.
- Add e2e tests for critical user flows and release-critical paths.
- Keep tests deterministic, isolated, and fast; avoid unstable external services in unit tests.

### Deployment / Release / Tagging Rules
- CI must block merge on failing lint, tests, or security checks.
- Use SemVer and update CHANGELOG for every released change.
- Create annotated Git tags `vMAJOR.MINOR.PATCH` for releases.
- Every deployment change must include rollback instructions and post-deploy verification.

### Control Rules (Any Agent + OpenSpec)
- Any non-trivial change requires an approved OpenSpec proposal before implementation.
- Agent must run pre-commit + tests + static analysis + security checks before finalization.
- No commit/push when quality gates fail.
- Implementation branches must use dedicated linked worktrees.
- For high-risk changes (security/performance/architecture), require explicit review by specialized agents.

### Delivery Sequence (Mandatory)
- After code changes, run validation first (pre-commit, lint, tests, security checks, compliance audit when applicable).
- Commit only when validation is green.
- Push branch and open/update a PR against `develop`.
- Wait for CI/PR checks to finish; do not merge with failing checks.
- If PR checks fail, fix issues on the same branch and repeat validation -> commit -> push until all checks are green.

### Stack-Specific Rules (Python)
- Prefer type hints on public APIs and keep static typing checks active (mypy/pyright).
- Keep format/lint checks enforced (ruff/black/flake8/pylint according to project tooling).
- Use pytest markers and layered tests (`unit`, `integration`, `e2e`) where relevant.
<!-- END:PROJECT_GOVERNANCE_RULES -->

<!-- BEGIN:DELIVERY_SEQUENCE_RULES -->
## Delivery Sequence (Managed)

1. Implement on a dedicated feature/fix branch in a linked worktree.
2. Run local validation (`pre-commit`, lint, tests, security checks, compliance audit as relevant).
3. Commit only if validation is green.
4. Push branch and create/update PR to `develop`.
5. Wait for CI/PR checks.
6. If a check fails, fix on the same branch and loop back to step 2 until all checks are green.
<!-- END:DELIVERY_SEQUENCE_RULES -->

<!-- BEGIN:GLOBAL_USER_RULES -->
## Global User Rules Inheritance (Managed)

- Apply user-level rules from `~/AGENTS.md` when this file exists.
- Apply user-level governance from `~/.claude/CLAUDE.md`.
- Project rules may strengthen global user rules, but must never weaken them.
- If `~/AGENTS.md` defines skills and trigger rules, load only the minimum relevant skills for the current task.
<!-- END:GLOBAL_USER_RULES -->
