# Tasks: Desloppify Code Quality Phase 2

## Phase 2A: Quick Wins (Estimated: 2h)

- [ ] **2A.1** Remove sys.path mutation from `docs/conf.py`
  - File: `docs/conf.py:22`
  - Action: Delete sys.path insertion, import from installed package
  - Validation: `sphinx-build docs/ docs/_build/` succeeds

- [ ] **2A.2** Remove sys.path mutation from `examples/conversion_coverage_check.py`
  - File: `examples/conversion_coverage_check.py:39`
  - Action: Delete sys.path insertion, import from installed package
  - Validation: Script runs successfully

- [ ] **2A.3** Extract hardcoded URLs to constants
  - Files: `scripts/*.py` (6 instances)
  - Action: Create `src/ffbb_api_client_v2/constants.py`, update imports
  - Validation: All scripts run successfully

- [ ] **2A.4** Deduplicate common constants
  - Files: `src/`, `scripts/` (26 instances)
  - Action: Identify duplicates, extract to `constants.py`
  - Validation: No duplicate string literals > 3 occurrences

- [ ] **2A.5** Remove trivial function `demo_field_sets()`
  - File: `examples/field_sets_and_filtering.py:21`
  - Action: Delete function and calls
  - Validation: Example still runs

## Phase 2B: Exception Handling (Estimated: 4h)

- [ ] **2B.1** Fix silent exception in `docs/conf.py`
  - File: `docs/conf.py:41`
  - Action: Add logging or re-raise
  - Validation: Sphinx build logs warnings appropriately

- [ ] **2B.2** Fix silent exceptions in `examples/conversion_coverage_check.py`
  - File: `examples/conversion_coverage_check.py:238,245,371,422`
  - Action: Add logging with context
  - Validation: Script logs errors appropriately

- [ ] **2B.3** Fix silent exceptions in `examples/extract_contacts.py`
  - File: `examples/extract_contacts.py:4639,4658`
  - Action: Add logging with context
  - Validation: Script logs errors appropriately

- [ ] **2B.4** Fix silent exceptions in `scripts/discover_types.py`
  - File: `scripts/discover_types.py:1653,1773,2146`
  - Action: Add logging with context
  - Validation: Script logs errors appropriately

- [ ] **2B.5** Fix catch-log-only in `docs/conf.py`
  - File: `docs/conf.py:55`
  - Action: Re-raise or add recovery
  - Validation: Sphinx build handles errors appropriately

- [ ] **2B.6** Fix catch-log-only in `examples/complete_usage_example.py`
  - File: `examples/complete_usage_example.py:191`
  - Action: Re-raise or add recovery
  - Validation: Example handles errors appropriately

- [ ] **2B.7** Fix catch-log-only in `scripts/audit_api_models.py`
  - File: `scripts/audit_api_models.py:921`
  - Action: Re-raise after logging
  - Validation: Script fails fast on errors

- [ ] **2B.8** Fix catch-log-only in `scripts/discover_types.py`
  - File: `scripts/discover_types.py:703,1388,1596,1719,2194`
  - Action: Re-raise after logging
  - Validation: Script fails fast on errors

- [ ] **2B.9** Fix remaining sys.exit() calls
  - Files: `examples/conversion_coverage_check.py:763`, `scripts/check_from_dict_compliance.py:169`, `scripts/test_explicit_fields.py:324`, `scripts/validate_fk_expansion.py:112`
  - Action: Convert to return codes with `sys.exit(main())`
  - Validation: Scripts return correct exit codes

## Phase 2C: Monster Functions (Estimated: 8h)

- [ ] **2C.1** Refactor `examples/extract_contacts.py:build()` (202 LOC)
  - Action: Extract HTML building logic
  - Validation: Tests pass, output unchanged

- [ ] **2C.2** Refactor `examples/extract_contacts.py:to_html()` (335 LOC)
  - Action: Extract section builders
  - Validation: Tests pass, output unchanged

- [ ] **2C.3** Refactor `examples/extract_contacts.py:_write_html_club_card()` (303 LOC)
  - Action: Extract field renderers
  - Validation: Tests pass, output unchanged

- [ ] **2C.4** Refactor `examples/extract_contacts.py:_write_leaflet_js()` (192 LOC)
  - Action: Extract JS template builders
  - Validation: Tests pass, output unchanged

- [ ] **2C.5** Refactor `examples/extract_contacts.py:_write_report_ui_js()` (334 LOC)
  - Action: Extract UI component builders
  - Validation: Tests pass, output unchanged

- [ ] **2C.6** Refactor `examples/extract_contacts.py:main()` (690 LOC)
  - Action: Extract phase handlers
  - Validation: Tests pass, output unchanged

- [ ] **2C.7** Refactor `scripts/discover_types.py:main()` (639 LOC)
  - Action: Extract discovery phases
  - Validation: Tests pass, output unchanged

- [ ] **2C.8** Refactor `scripts/phase1_dedup.py:main()` (369 LOC)
  - Action: Extract deduplication steps
  - Validation: Tests pass, output unchanged

- [ ] **2C.9** Refactor `scripts/test_meilisearch_features.py:main()` (180 LOC)
  - Action: Extract test runners
  - Validation: Tests pass, output unchanged

## Phase 2D: Test Coverage (Estimated: 16h)

- [ ] **2D.1** Write tests for `retry_utils.py`
  - File: `tests/unit/utils/test_retry_utils.py`
  - Coverage target: > 95%
  - Validation: `pytest tests/unit/utils/test_retry_utils.py --cov=retry_utils`

- [ ] **2D.2** Write tests for `input_validation.py`
  - File: `tests/unit/utils/test_input_validation.py`
  - Coverage target: > 95%
  - Validation: `pytest tests/unit/utils/test_input_validation.py --cov=input_validation`

- [ ] **2D.3** Write tests for `cartographie.py`
  - File: `tests/unit/models/test_cartographie.py`
  - Coverage target: > 90%
  - Validation: `pytest tests/unit/models/test_cartographie.py --cov=cartographie`

- [ ] **2D.4** Write tests for Meilisearch models (priority: high-importer files)
  - Files: `tests/unit/meilisearch_ffbb/models/`
  - Coverage target: > 80%
  - Validation: `pytest tests/unit/meilisearch_ffbb/ --cov=meilisearch_ffbb`

- [ ] **2D.5** Write tests for Directus models (priority: high-importer files)
  - Files: `tests/unit/directus_ffbb/models/`
  - Coverage target: > 80%
  - Validation: `pytest tests/unit/directus_ffbb/ --cov=directus_ffbb`

## Phase 2E: Security Audit (Estimated: 2h)

- [ ] **2E.1** Run bandit manually
  - Command: `bandit -r src/ scripts/ -f json --quiet > bandit-results.json`
  - Validation: Results file generated

- [ ] **2E.2** Review HIGH severity issues
  - Action: Fix or document false positives
  - Validation: No unmitigated HIGH issues

- [ ] **2E.3** Review MEDIUM severity issues
  - Action: Fix or document false positives
  - Validation: No unmitigated MEDIUM issues

- [ ] **2E.4** Create `.bandit-ignore` if needed
  - Action: Document known false positives
  - Validation: Bandit scan passes

## Phase 2F: Subjective Review (Estimated: 8h)

- [ ] **2F.1** Review abstraction_fitness dimension
  - Command: `desloppify review --prepare --dimensions abstraction_fitness`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.2** Review api_surface_coherence dimension
  - Command: `desloppify review --prepare --dimensions api_surface_coherence`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.3** Review contract_coherence dimension
  - Command: `desloppify review --prepare --dimensions contract_coherence`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.4** Review design_coherence dimension
  - Command: `desloppify review --prepare --dimensions design_coherence`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.5** Review type_safety dimension
  - Command: `desloppify review --prepare --dimensions type_safety`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.6** Review error_consistency dimension
  - Command: `desloppify review --prepare --dimensions error_consistency`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.7** Review naming_quality dimension
  - Command: `desloppify review --prepare --dimensions naming_quality`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.8** Review logic_clarity dimension
  - Command: `desloppify review --prepare --dimensions logic_clarity`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.9** Review dependency_health dimension
  - Command: `desloppify review --prepare --dimensions dependency_health`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.10** Review package_organization dimension
  - Command: `desloppify review --prepare --dimensions package_organization`
  - Action: Launch subagent, import results
  - Validation: Dimension scored

- [ ] **2F.11** Review remaining 10 dimensions
  - Action: Complete reviews for all 20 dimensions
  - Validation: All dimensions scored

## Summary

| Phase | Tasks | Estimated Hours | Priority |
|-------|-------|-----------------|----------|
| 2A: Quick Wins | 5 | 2h | 🔴 Critical |
| 2B: Exception Handling | 9 | 4h | 🔴 Critical |
| 2C: Monster Functions | 9 | 8h | 🟠 High |
| 2D: Test Coverage | 5 | 16h | 🟠 High |
| 2E: Security Audit | 4 | 2h | 🔴 Critical |
| 2F: Subjective Review | 11 | 8h | 🟡 Medium |
| **Total** | **43** | **40h** | |

## Completion Criteria

- [ ] All 43 tasks completed
- [ ] Desloppify strict score ≥ 50.0/100
- [ ] All pre-commit hooks pass
- [ ] Tox tests pass with > 96% coverage
- [ ] No HIGH/MEDIUM security issues
- [ ] PR created and merged to develop
