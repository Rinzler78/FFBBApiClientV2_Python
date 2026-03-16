## ADDED Requirements

### Requirement: Exception Handling Standards
All scripts and examples SHALL follow consistent exception handling patterns:
1. Never silently suppress exceptions (no bare `pass` or `continue` in except blocks)
2. Log exceptions with context before re-raising or continuing
3. Use specific exception types instead of bare `Exception` where possible
4. CLI entry points SHALL return exit codes instead of calling `sys.exit()` directly

#### Scenario: Silent exception handler in docs/conf.py
- **Given** `docs/conf.py` has `except FileNotFoundError: pass`
- **When** the file is not found
- **Then** the error should be logged with context
- **And** the build should fail gracefully or use a default

#### Scenario: sys.exit() in library code
- **Given** a script with `sys.exit(1)` in library code (not `if __name__ == "__main__"`)
- **When** an error occurs
- **Then** the function should raise an exception or return an error code
- **And** `main()` should call `sys.exit(main())`

### Requirement: Constant Deduplication
Common constants (URLs, endpoints, field names) SHALL be centralized in `src/ffbb_api_client_v2/constants.py` to avoid duplication across scripts and source files.

#### Scenario: Hardcoded URL in script
- **Given** a script with hardcoded URL like `"https://meilisearch-prod.ffbb.app/"`
- **When** the script is written
- **Then** the URL should be imported from `constants.py`
- **And** no duplicate URL strings should exist in multiple files

### Requirement: Function Size Limits
Functions exceeding 150 LOC SHALL be refactored into smaller, focused units with single responsibilities.

#### Scenario: Monster function in extract_contacts.py
- **Given** `main()` function with 690 LOC in `examples/extract_contacts.py`
- **When** the function is refactored
- **Then** it should be split into phase handlers (< 100 LOC each)
- **And** each phase handler should be independently testable

### Requirement: Critical Module Coverage
Modules with high blast radius (many importers) SHALL have unit tests with > 90% coverage.

#### Scenario: retry_utils.py without tests
- **Given** `src/ffbb_api_client_v2/utils/retry_utils.py` has 9 importers
- **When** tests are added
- **Then** `tests/unit/utils/test_retry_utils.py` must exist
- **And** coverage must be > 95%
- **And** all public functions must be tested

#### Scenario: input_validation.py without tests
- **Given** `src/ffbb_api_client_v2/utils/input_validation.py` has 2 importers
- **When** tests are added
- **Then** `tests/unit/utils/test_input_validation.py` must exist
- **And** coverage must be > 95%

### Requirement: Security Audit
All security issues identified by bandit SHALL be reviewed and resolved (fixed or documented as false positives).

#### Scenario: Bandit HIGH severity issue
- **Given** bandit reports a HIGH severity issue
- **When** the issue is reviewed
- **Then** it must be either fixed or documented as false positive
- **And** no unmitigated HIGH issues remain

## ADDED Requirements

### Requirement: Script Error Handling
Scripts MUST use exceptions for error propagation in library functions and return exit codes from main() functions.

#### Scenario: Replace sys.exit with exception
- **Given** a script function calls `sys.exit(1)` directly
- **When** the function is refactored
- **Then** it should raise `RuntimeError` instead
- **And** `main()` should return an exit code

#### Scenario: Replace silent except with logging
- **Given** a script has `except Exception: continue`
- **When** the handler is refactored
- **Then** it should log the exception with context
- **And** either re-raise or explicitly continue

### Requirement: Documentation Build Configuration
`docs/conf.py` MUST import from installed package without sys.path mutation.

#### Scenario: Remove sys.path insertion
- **Given** `docs/conf.py` inserts src/ into sys.path
- **When** the configuration is updated
- **Then** sys.path insertion should be removed
- **And** Sphinx should find the package via installation
