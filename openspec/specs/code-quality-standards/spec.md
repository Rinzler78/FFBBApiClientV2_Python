# code-quality-standards Specification

## Purpose
TBD - created by archiving change desloppify-code-quality-phase2. Update Purpose after archive.
## Requirements
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
