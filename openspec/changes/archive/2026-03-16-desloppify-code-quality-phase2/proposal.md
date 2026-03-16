## Why

Following the successful merge of PR #31 (desloppify-code-quality phase 1), the codebase still has **469 open issues** identified by desloppify analysis. While phase 1 fixed 17 issues (unused imports, sys.exit() replacements, subprocess timeouts, MD5 security fix, duplicate function extraction), significant technical debt remains:

- **37 HIGH severity code smells** (silent exception handlers, monster functions, sys.path mutations)
- **360 MEDIUM severity code smells** (loose type annotations, too many optional params, high cyclomatic complexity)
- **27 security issues** (bandit timeout — needs manual verification)
- **178 untested modules** (2.3% test health)
- **24 duplication clusters** (boilerplate and function duplicates)
- **20 subjective dimensions** at 0.0% (require human architectural review)

The strict score is currently **19.9/100** (target: 95.0). This proposal addresses the remaining mechanical issues to achieve a target score of **~50-60/100**.

## What Changes

### Phase 2A: Quick Wins (Priority 1 — < 2h effort)

1. **Remove sys.path mutations** (2 instances)
   - `docs/conf.py:22` — Use proper package installation instead
   - `examples/conversion_coverage_check.py:39` — Import from installed package

2. **Fix hardcoded URLs** (6 instances)
   - Extract to constants in `src/ffbb_api_client_v2/config.py`
   - Update references in scripts

3. **Deduplicate constants** (26 instances)
   - Identify common constants (endpoint URLs, field names, enum values)
   - Extract to `src/ffbb_api_client_v2/constants.py`

4. **Remove trivial function** (1 instance)
   - `examples/field_sets_and_filtering.py:21` — `demo_field_sets()` does nothing

### Phase 2B: Exception Handling (Priority 2 — 4h effort)

5. **Fix silent exception handlers** (12 instances)
   - `docs/conf.py:41` — Log or re-raise `FileNotFoundError`
   - `examples/conversion_coverage_check.py` (4 instances) — Log ValueError/TypeError
   - `examples/extract_contacts.py` (2 instances) — Log and continue with context
   - `scripts/discover_types.py` (3 instances) — Log Exception with context

6. **Fix catch blocks that only log** (9 instances)
   - `docs/conf.py:55` — Re-raise or handle Exception
   - `examples/complete_usage_example.py:191` — Add recovery logic
   - `scripts/audit_api_models.py:921` — Re-raise after logging
   - `scripts/discover_types.py` (5 instances) — Re-raise after logging
   - `scripts/validate_fk_expansion.py:84` — Already fixed in PR #31

7. **Fix remaining sys.exit() calls** (4 instances)
   - `examples/conversion_coverage_check.py:763` — Return exit code
   - `scripts/check_from_dict_compliance.py:169` — Return exit code
   - `scripts/test_explicit_fields.py:324` — Return exit code
   - `scripts/validate_fk_expansion.py:112` — Return exit code

### Phase 2C: Monster Functions (Priority 3 — 8h effort)

8. **Refactor monster functions** (9 instances in 4 files)
   - `examples/extract_contacts.py`:
     - `build()` — 202 LOC → Extract HTML building logic
     - `to_html()` — 335 LOC → Extract section builders
     - `_write_html_club_card()` — 303 LOC → Extract field renderers
     - `_write_leaflet_js()` — 192 LOC → Extract JS template
     - `_write_report_ui_js()` — 334 LOC → Extract UI component builders
     - `main()` — 690 LOC → Extract phase handlers
   - `scripts/discover_types.py`:
     - `main()` — 639 LOC → Extract discovery phases
   - `scripts/phase1_dedup.py`:
     - `main()` — 369 LOC → Extract deduplication steps
   - `scripts/test_meilisearch_features.py`:
     - `main()` — 180 LOC → Extract test runners

### Phase 2D: Test Coverage (Priority 4 — 16h effort)

9. **Add tests for critical untested modules**
   - `src/ffbb_api_client_v2/utils/retry_utils.py` (332 LOC, 9 importers) — HIGH priority
   - `src/ffbb_api_client_v2/utils/input_validation.py` (355 LOC, 2 importers) — HIGH priority
   - `src/ffbb_api_client_v2/models/cartographie.py` (83 LOC, 12 importers) — HIGH priority
   - Meilisearch model files (~50 files, 200-300 LOC each) — MEDIUM priority
   - Directus model files (~30 files) — MEDIUM priority

### Phase 2E: Security Review (Priority 5 — 2h effort)

10. **Manual security audit** (bandit timeout workaround)
    - Run `bandit -r src/ scripts/ -f json --quiet` manually
    - Review and fix any HIGH/MEDIUM severity issues
    - Document false positives in `.bandit-ignore` if needed

### Phase 2F: Subjective Review (Priority 6 — 8h effort)

11. **Complete subjective reviews** (20 dimensions)
    - Run `desloppify review --prepare --dimensions <name>` for each dimension
    - Review and document findings
    - Fix identified architectural issues where actionable

## Capabilities

### New Capabilities
- `exception-handling-standards`: Consistent exception handling across scripts and examples — log with context, re-raise when appropriate, never silently suppress
- `constant-deduplication`: Centralized constants for URLs, endpoints, field names — single source of truth
- `monster-function-refactoring`: Large functions decomposed into focused, testable units with clear responsibilities
- `test-coverage-critical-paths`: Unit tests for utility modules with high blast radius (retry_utils, input_validation)
- `security-audit-process`: Manual bandit review when automated scanning times out

### Modified Capabilities
- `script-error-handling`: Enhanced from phase 1 — scripts now use proper exception propagation and logging

## Impact

### Files Modified (estimated)
- **docs/conf.py** — Exception handling, sys.path removal
- **examples/*.py** (6 files) — Exception handling, sys.exit() fixes, monster function refactoring
- **scripts/*.py** (8 files) — Exception handling, sys.exit() fixes, monster function refactoring
- **src/ffbb_api_client_v2/config.py** — New constants
- **src/ffbb_api_client_v2/constants.py** — New file for deduplicated constants
- **tests/unit/utils/test_retry_utils.py** — New test file
- **tests/unit/utils/test_input_validation.py** — New test file
- **tests/unit/models/test_cartographie.py** — New test file

### Breaking Changes
- **None expected** — All changes are internal refactoring and test additions

### SemVer Impact
- **Patch version** — No public API changes, only internal improvements

## Success Criteria

### Quantitative Metrics
| Metric | Before | Target | Stretch |
|--------|--------|--------|---------|
| Strict Score | 19.9/100 | 50.0/100 | 60.0/100 |
| Code Smells (HIGH) | 37 | < 10 | < 5 |
| Code Smells (MEDIUM) | 360 | < 200 | < 100 |
| Test Health | 2.3% | 15% | 25% |
| Security Issues | 27 (unverified) | 0 verified | 0 |
| Duplication Clusters | 24 | < 15 | < 10 |

### Qualitative Metrics
- [ ] All exception handlers either log with context or re-raise
- [ ] No sys.path mutations outside of documented edge cases
- [ ] All constants extracted to centralized location
- [ ] Monster functions decomposed into testable units
- [ ] Critical utility modules have > 90% test coverage
- [ ] Security audit completed with no HIGH/MEDIUM issues
- [ ] Subjective review dimensions assessed and documented

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Monster function refactoring introduces bugs | HIGH | Comprehensive tests before/after, incremental refactoring |
| Test coverage additions require API tokens | MEDIUM | Use mocks/fixtures, mark integration tests appropriately |
| Security audit reveals critical issues | HIGH | Address immediately, may require hotfix |
| Subjective review identifies architectural debt | MEDIUM | Document and create follow-up proposals |

## Dependencies

- ✅ Phase 1 complete (PR #31 merged)
- ⏳ Bandit security scanner availability
- ⏳ Test infrastructure (pytest, coverage)
- ⏳ CI/CD pipeline for validation

## Rollback Plan

If issues are discovered:
1. Revert individual PRs as needed (each phase is independent)
2. No database migrations or data changes to rollback
3. Test coverage additions are additive — safe to keep even if other changes revert
