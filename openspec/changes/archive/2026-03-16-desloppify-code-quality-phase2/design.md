# Design: Desloppify Code Quality Phase 2

## Overview

This design document details the technical approach for addressing remaining desloppify issues after phase 1 (PR #31).

## Architecture

### Phase 2A: Quick Wins

#### 2A.1: Remove sys.path mutations

**Current state:**
```python
# docs/conf.py
_SCRIPT_DIR = Path(__file__).resolve().parent
_SRC_DIR = str(_SCRIPT_DIR.parent / "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)
```

**Target state:**
```python
# docs/conf.py
# Remove sys.path mutation entirely
# Sphinx should find the package via installed version or PYTHONPATH
import ffbb_api_client_v2  # Import from installed package
```

**Validation:**
- Sphinx build succeeds without sys.path mutation
- CI documentation build passes

#### 2A.2: Extract Hardcoded URLs

**Current state:**
```python
# scripts/discover_types.py
MEILISEARCH_URL = "https://meilisearch-prod.ffbb.app/"
API_BASE_URL = "https://api.ffbb.com/"
```

**Target state:**
```python
# src/ffbb_api_client_v2/constants.py
MEILISEARCH_PROD_URL = "https://meilisearch-prod.ffbb.app/"
API_PROD_URL = "https://api.ffbb.com/"

# scripts/discover_types.py
from ffbb_api_client_v2.constants import MEILISEARCH_PROD_URL, API_PROD_URL
```

#### 2A.3: Deduplicate Constants

**Pattern identification:**
```bash
# Find duplicate string literals
grep -roh '"[^"]*"' src/ scripts/ | sort | uniq -c | sort -rn | head -30
```

**Extraction strategy:**
- Endpoint names → `ENDPOINT_*` constants
- Field names → `FIELD_*` constants
- Common values → `VALUE_*` constants

### Phase 2B: Exception Handling

#### 2B.1: Silent Exception Handlers

**Current state:**
```python
try:
    process_item(item)
except (ValueError, TypeError):
    pass  # Silent suppression
```

**Target state:**
```python
try:
    process_item(item)
except (ValueError, TypeError) as e:
    logger.warning("Failed to process item %s: %s", item.id, e)
    continue  # Explicit continuation with logging
```

#### 2B.2: Catch-Log-Only Handlers

**Current state:**
```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed: %s", e)
    # No re-raise, no recovery
```

**Target state (option 1 — re-raise):**
```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed: %s", e)
    raise  # Re-raise for caller to handle
```

**Target state (option 2 — recovery):**
```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed: %s", e)
    return default_value()  # Graceful degradation
```

### Phase 2C: Monster Functions

#### 2C.1: extract_contacts.py Refactoring

**Current structure:**
```
main() [690 LOC]
├── Phase 1: Fetch data
├── Phase 2: Process clubs
├── Phase 3: Generate HTML
├── Phase 4: Generate JS
└── Phase 5: Write output
```

**Target structure:**
```
main() [50 LOC]
├── _fetch_all_data() [100 LOC]
├── _process_clubs() [150 LOC]
├── _generate_html() [80 LOC]
├── _generate_javascript() [80 LOC]
└── _write_outputs() [60 LOC]

# Extracted builders
_build_club_card_html() [150 LOC] → from to_html()
_build_leaflet_map_js() [120 LOC] → from _write_leaflet_js()
_build_report_ui_js() [180 LOC] → from _write_report_ui_js()
```

**Testing strategy:**
- Unit tests for each extracted function
- Integration test for main() end-to-end
- Snapshot tests for HTML/JS output

### Phase 2D: Test Coverage

#### 2D.1: retry_utils.py Tests

```python
# tests/unit/utils/test_retry_utils.py
class TestRetryConfig:
    def test_default_values(self): ...
    def test_custom_values(self): ...

class TestTimeoutConfig:
    def test_default_values(self): ...
    def test_custom_values(self): ...

class TestRetryWrapper:
    @pytest.mark.parametrize("exception,retry_count", [...])
    def test_retry_on_exception(self, exception, retry_count): ...

    def test_no_retry_on_success(self): ...
    def test_max_retries_exceeded(self): ...
```

#### 2D.2: input_validation.py Tests

```python
# tests/unit/utils/test_input_validation.py
class TestValidateToken:
    def test_valid_token(self): ...
    def test_none_token(self): ...
    def test_empty_token(self): ...
    def test_short_token(self): ...
    def test_invalid_characters(self): ...

class TestValidateDebug:
    def test_valid_values(self): ...
    def test_invalid_type(self): ...
```

### Phase 2E: Security Audit

#### Bandit Manual Run

```bash
# Run bandit manually
bandit -r src/ scripts/ -f json --quiet > bandit-results.json

# Parse results
python3 -c "
import json
with open('bandit-results.json') as f:
    data = json.load(f)
for issue in data.get('results', []):
    if issue['issue_severity'] in ['HIGH', 'MEDIUM']:
        print(f\"[{issue['issue_severity']}] {issue['test_id']}: {issue['filename']}:{issue['line_number']}\")
"
```

#### Expected Issues

Based on phase 1 findings:
- B324: MD5 hash usage (already fixed with `usedforsecurity=False`)
- B603/B607: subprocess calls (mitigated with `timeout=30`)
- B101: assert statements (test code only)
- B112: except-continue (being fixed in phase 2B)

### Phase 2F: Subjective Review

#### Review Process

```bash
# For each dimension:
desloppify review --prepare --dimensions <dimension_name>

# Review generated prompts
# Launch subagent for investigation
# Import results
desloppify review --import-run <run-dir> --scan-after-import
```

#### Dimensions to Review

1. **abstraction_fitness** — Are abstractions appropriate?
2. **api_surface_coherence** — Consistent API design?
3. **contract_coherence** — Functions honor their contracts?
4. **design_coherence** — Sound structural decisions?
5. **type_safety** — Proper type annotations?
6. **error_consistency** — Consistent error handling?
7. **naming_quality** — Clear, consistent naming?
8. **logic_clarity** — Clear control flow?
9. **dependency_health** — Healthy dependency graph?
10. **package_organization** — Logical file placement?

## File Structure Changes

```
src/ffbb_api_client_v2/
├── constants.py              # NEW: Centralized constants
├── config.py                 # MODIFIED: Move URL constants here
└── utils/
    ├── retry_utils.py        # TESTED: Add unit tests
    └── input_validation.py   # TESTED: Add unit tests

tests/unit/
├── utils/
│   ├── test_retry_utils.py        # NEW
│   └── test_input_validation.py   # NEW
└── models/
    └── test_cartographie.py       # NEW

examples/
├── conversion_coverage_check.py   # MODIFIED: Exception handling
├── extract_contacts.py            # REFACTORED: Monster functions
└── field_sets_and_filtering.py    # MODIFIED: Remove trivial function

scripts/
├── audit_api_models.py            # MODIFIED: Exception handling
├── check_from_dict_compliance.py  # MODIFIED: sys.exit() → return
├── discover_types.py              # MODIFIED: Exception handling + refactoring
├── test_explicit_fields.py        # MODIFIED: sys.exit() → return
└── validate_fk_expansion.py       # MODIFIED: sys.exit() → return

docs/
└── conf.py                        # MODIFIED: Remove sys.path, fix exceptions
```

## Testing Strategy

### Unit Tests (Priority 1)
- Test all extracted functions from monster functions
- Test exception handling paths
- Test constant values

### Integration Tests (Priority 2)
- Test script end-to-end execution
- Test with mocked API responses
- Test error scenarios

### Coverage Targets
- `retry_utils.py`: > 95%
- `input_validation.py`: > 95%
- `cartographie.py`: > 90%
- Extracted functions: > 85%

## Validation Checklist

- [ ] Pre-commit hooks pass (black, isort, flake8, pylint, pyright)
- [ ] Tox tests pass (`tox -e py310`)
- [ ] Coverage > 96%
- [ ] Bandit security scan passes (no HIGH/MEDIUM)
- [ ] Desloppify scan shows improvement
- [ ] No breaking changes to public API
- [ ] Documentation builds successfully
