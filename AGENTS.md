# AGENTS.md - FFBB API Client V2

## Build/Lint/Test Commands

**Run all tests:** `python -m unittest discover tests`
**Run tests with coverage:** `coverage run -m unittest discover tests`
**Run single test:** `python -m unittest tests.test_000_api_ffbb_app_client.Test000ApiFfbbAppClient.test_lives`
**Lint code:** `pre-commit run --all-files` or `tox -e lint`
**Build package:** `python -m build` or `tox -e build`

## Code Style Guidelines

### Formatting & Linting
- **Black formatting:** max line length 88, compatible with flake8
- **isort imports:** profile=black, known_first_party=ffbb_api_client_v2
- **flake8 linting:** max_line_length=88, extend_ignore=E203,W503
- **autoflake:** remove unused imports and variables
- **pyupgrade:** Python 3.9+ compatibility

### Type Hints & Imports
- Use `from __future__ import annotations` for forward references
- Comprehensive type hints on all public methods
- Import sorting: stdlib → third-party → local (isort)

### Naming Conventions
- Classes: PascalCase (ApiFFBBAppClient, GetCompetitionResponse)
- Methods/functions: snake_case (get_lives, get_saisons)
- Variables: snake_case (bearer_token, cached_session)
- Constants: UPPER_CASE (not extensively used)

### Error Handling
- Raise ValueError for invalid inputs with descriptive messages
- Use try/except blocks for external API calls
- Return None or empty collections for missing data

### Documentation
- Google-style docstrings for all public methods
- Args/Returns sections in docstrings
- Type hints in docstrings when complex

### Testing
- unittest framework with setUp methods
- Test classes inherit from unittest.TestCase
- Environment variables loaded via python-dotenv
- Assert methods: assertIsNotNone, assertIsInstance, etc.

### Project Structure
- src/ layout with namespace packages
- Clear separation: clients/, helpers/, models/, utils/
- __init__.py files for proper imports
