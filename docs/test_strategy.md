# Test Strategy - FFBBApiClientV2_Python

## 1. Test Pyramid

### Level 1: Unit - Models
Tests for `from_dict`, `to_dict`, round-trips, edge cases (None, empty dict, invalid types).
No network calls, instant execution.

**Location**: `tests/unit/models/` (test_100 to test_123)

### Level 2: Unit - Clients
Tests for `FFBBAPIClientV2`, `ApiFFBBAppClient`, `MeilisearchFFBBClient` with mocked HTTP.

**Location**: `tests/unit/clients/` (test_200 to test_206)

### Level 3: Unit - Utils
Tests for `cache_manager`, `retry_utils`, `secure_logging`, `converter_utils`, `config`, `token_manager`, `input_validation`.

**Location**: `tests/unit/utils/` (test_300 to test_307)

### Level 4: Unit - Helpers
Tests for `http_requests_helper`, `http_requests_utils`.

**Location**: `tests/unit/helpers/` (test_400)

### Level 5: Integration
Real API calls (skipped if tokens not set), raw JSON conversion tests.

**Location**: `tests/integration/` (test_500 to test_506)

### Level 6: E2E
Multi-step user journeys (search -> club -> teams -> calendar).

**Location**: `tests/e2e/` (currently empty, ready for future tests)

---

## 2. Directory Structure

```
tests/
    conftest.py                              # Shared fixtures (cache, env, fixture_loader)
    unit/
        conftest.py
        models/
            test_100_competition_id_categorie.py
            test_101_competition_id_sexe.py
            test_102_competition_id_type_competition.py
            test_103_competition_id_type_competition_generique.py
            test_104_competition_origine_categorie.py
            test_105_competition_origine_type_competition_generique.py
            test_106_competition_origine.py
            test_107_id_engagement_equipe.py
            test_108_id_organisme_equipe.py
            test_109_id_organisme_equipe1_logo.py
            test_110_labellisation.py
            test_111_niveau_class.py
            test_112_purple_logo.py
            test_113_salle.py
            test_114_tournoi_type_class.py
            test_115_type_association_libelle.py
            test_116_type_competition_generique.py
            test_117_organisateur.py
            test_118_competition_id.py
            test_119_terrains_inner_models.py
            test_120_pratiques_inner_models.py
            test_121_to_dict_round_trip.py
            test_122_coverage_gaps.py
            test_123_missing_coverage.py
        clients/
            test_200_api_ffbb_app_client.py
            test_201_unit_tests_core.py
            test_202_meilisearch_client.py
            test_203_meilisearch_client_extension.py
            test_204_ffbb_api_client_v2.py
            test_205_meilisearch_ffbb_client.py
            test_206_coverage_gaps_clients.py
        utils/
            test_300_secure_logging.py
            test_301_input_validation.py
            test_302_retry_utils.py
            test_303_cache_manager.py
            test_304_config.py
            test_305_token_manager.py
            test_306_converter_utils.py
            test_307_coverage_gaps_utils.py
        helpers/
            test_400_http_helpers.py
    integration/
        conftest.py
        test_500_user_journey.py
        test_501_user_journey_v2.py
        test_502_enhanced_integration.py
        test_503_secure_logging.py
        test_504_input_validation.py
        test_505_retry_timeout.py
        test_506_raw_json_model_conversion.py
    e2e/
        conftest.py
    fixtures/
        *.json
```

### Numbering Convention

| Range   | Category         |
|---------|------------------|
| 100-199 | Unit - Models    |
| 200-299 | Unit - Clients   |
| 300-399 | Unit - Utils     |
| 400-499 | Unit - Helpers   |
| 500-599 | Integration      |
| 600-699 | E2E              |

---

## 3. File Inventory

### Unit - Models (tests/unit/models/)

| File | Scope | Tests |
|------|-------|:-----:|
| `test_100_competition_id_categorie.py` | CompetitionIDCategorie round-trip | 2 |
| `test_101_competition_id_sexe.py` | CompetitionIDSexe round-trip | 2 |
| `test_102_competition_id_type_competition.py` | CompetitionIDTypeCompetition round-trip | 2 |
| `test_103_competition_id_type_competition_generique.py` | CompetitionIDTypeCompetitionGenerique round-trip | 2 |
| `test_104_competition_origine_categorie.py` | CompetitionOrigineCategorie round-trip | 2 |
| `test_105_competition_origine_type_competition_generique.py` | CompetitionOrigineTypeCompetitionGenerique round-trip | 2 |
| `test_106_competition_origine.py` | CompetitionOrigine round-trip | 2 |
| `test_107_id_engagement_equipe.py` | IDEngagementEquipe round-trip | 2 |
| `test_108_id_organisme_equipe.py` | IDOrganismeEquipe round-trip | 2 |
| `test_109_id_organisme_equipe1_logo.py` | IDOrganismeEquipe1Logo round-trip | 2 |
| `test_110_labellisation.py` | Labellisation round-trip | 2 |
| `test_111_niveau_class.py` | NiveauClass round-trip | 2 |
| `test_112_purple_logo.py` | PurpleLogo round-trip | 2 |
| `test_113_salle.py` | Salle round-trip | 2 |
| `test_114_tournoi_type_class.py` | TournoiTypeClass round-trip | 2 |
| `test_115_type_association_libelle.py` | TypeAssociationLibelle round-trip | 2 |
| `test_116_type_competition_generique.py` | TypeCompetitionGenerique round-trip | 2 |
| `test_117_organisateur.py` | Organisateur round-trip | 2 |
| `test_118_competition_id.py` | CompetitionID round-trip | 2 |
| `test_119_terrains_inner_models.py` | Terrains inner models (nested) | 6 |
| `test_120_pratiques_inner_models.py` | Pratiques inner models (nested) | 8 |
| `test_121_to_dict_round_trip.py` | Double round-trip from_dict/to_dict | 38 |
| `test_122_coverage_gaps.py` | Model to_dict branches, MultiSearch, FacetDistribution | 46 |
| `test_123_missing_coverage.py` | Enums, FacetStats/Distribution subclasses, model edge cases | 45 |

### Unit - Clients (tests/unit/clients/)

| File | Scope | Tests |
|------|-------|:-----:|
| `test_200_api_ffbb_app_client.py` | ApiFFBBAppClient REST client | varies |
| `test_201_unit_tests_core.py` | Core unit tests | varies |
| `test_202_meilisearch_client.py` | MeilisearchClient | varies |
| `test_203_meilisearch_client_extension.py` | MeilisearchClient extension | varies |
| `test_204_ffbb_api_client_v2.py` | FFBBAPIClientV2 facade | varies |
| `test_205_meilisearch_ffbb_client.py` | MeilisearchFFBBClient (mocked) | 21 |
| `test_206_coverage_gaps_clients.py` | FFBBAPIClientV2 search/delegation branches | 5 |

### Unit - Utils (tests/unit/utils/)

| File | Scope | Tests |
|------|-------|:-----:|
| `test_300_secure_logging.py` | SecureLogger | varies |
| `test_301_input_validation.py` | Input validation | varies |
| `test_302_retry_utils.py` | RetryUtils | varies |
| `test_303_cache_manager.py` | CacheManager | varies |
| `test_304_config.py` | Config | varies |
| `test_305_token_manager.py` | TokenManager | varies |
| `test_306_converter_utils.py` | from_TYPE helpers | 54 |
| `test_307_coverage_gaps_utils.py` | SecureLogging, RetryUtils, CacheManager, __init__, converter_utils edge cases | 30 |

### Unit - Helpers (tests/unit/helpers/)

| File | Scope | Tests |
|------|-------|:-----:|
| `test_400_http_helpers.py` | HTTP helpers (catch_result, etc.) | 18 |

### Integration (tests/integration/)

| File | Scope | Tests |
|------|-------|:-----:|
| `test_500_user_journey.py` | E2E user journey (requires tokens) | varies |
| `test_501_user_journey_v2.py` | E2E user journey v2 (requires tokens) | varies |
| `test_502_enhanced_integration.py` | Enhanced integration tests | varies |
| `test_503_secure_logging.py` | SecureLogging integration | varies |
| `test_504_input_validation.py` | Input validation integration | varies |
| `test_505_retry_timeout.py` | Retry/timeout integration | varies |
| `test_506_raw_json_model_conversion.py` | Raw JSON API responses -> from_dict | 32 |

---

## 4. Coverage

### Current Status
- **Global coverage**: **96%+** (branch coverage enabled)
- **Per-module minimum**: **>=90%**
- **Total tests**: **1700+** (all passing, 0 skipped)

### Coverage Targets

| Category | Minimum | Target |
|----------|---------|--------|
| Models (`from_dict`/`to_dict`) | 90% | 100% |
| Clients | 90% | 95% |
| Utils | 90% | 95% |
| Global | 90% | 97%+ |

### Coverage History
| Milestone | Coverage | Tests |
|-----------|:--------:|:-----:|
| Baseline | 62% | 172 |
| + test_021 (raw JSON) | 64% | 204 |
| + test_022 (round-trip) | 81% | 242 |
| + test_023 to test_045 | 92% | 346 |
| + test_046 (converter_utils) | 95% | 450 |
| + test_047 + test_048 + dead code removal | **97%** | **532** |
| + docstrings, search, batch helpers, coverage audit | **96%+** | **1700+** |

### Bugs Fixed During Coverage Work
1. `facet_stats.py`: `raise NotImplementedError` -> `assert False` (from_union catches AssertionError)
2. `id_engagement_equipe.py`: to_dict used `Logo.from_dict` instead of `to_class(Logo, x)`

---

## 5. CI/CD Recommendations

### pytest Markers

```ini
markers =
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    slow: marks tests as slow running
    e2e: marks tests as end-to-end tests
```

### Recommended Pipelines

| Pipeline | Command | Frequency | Time |
|----------|---------|-----------|------|
| Unit (fast) | `pytest tests/unit/ -x -q -n auto` | Every push | ~15s |
| Integration | `pytest tests/integration/ -q` | Nightly / pre-release | ~40s |
| Full suite | `pytest tests/ -x -q -n auto` | Nightly | ~60s |
| Coverage | `pytest tests/ --cov=ffbb_api_client_v2 --cov-branch -q` | Nightly | ~80s |

### Required Environment Variables
- `API_FFBB_APP_BEARER_TOKEN`: Token for api.ffbb.app
- `MEILISEARCH_BEARER_TOKEN`: Token for meilisearch-prod.ffbb.app

Integration tests are automatically skipped if tokens are not set (`@unittest.skipUnless`).

---

## 6. Test Conventions

Full conventions documented in `docs/testing_conventions.md`. Key points:

- **Style**: `unittest.TestCase` mandatory (no bare pytest classes)
- **Runner**: pytest + pytest-xdist for parallel execution
- **Naming**: `test_{XXX}_{module}.py` with numbered ranges by category
- **Quality**: AAA pattern, one act per test, deterministic, no logic in tests
- **Branch coverage**: `--cov-branch` required

---

## 7. Future Recommendations

### A. JSON Fixtures (Level 2)
Capture real API responses in `tests/fixtures/` for offline testing with complete field coverage.

### B. Snapshot Testing
Use `pytest-snapshot` to detect API structure changes automatically.

### C. Contract Testing
Validate API responses contain expected fields, detect new/removed fields.

### D. VCR Pattern
Consider `vcrpy` for recording/replaying API responses in integration tests.
