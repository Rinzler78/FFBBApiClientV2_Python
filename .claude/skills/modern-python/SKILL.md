# Modern Python

Apply modern Python 3.10+ best practices for safe, performant, and maintainable code.

Inspired by [Trail of Bits](https://blog.trailofbits.com/) Python guidance.

## When to Activate
- Writing new Python modules or refactoring existing ones.
- Reviewing Python code for modernization opportunities.
- Setting up or updating Python tooling configuration.

## Rules

### Type Safety
- Use type annotations on all public functions and methods.
- Prefer `X | Y` union syntax over `Union[X, Y]` (Python 3.10+).
- Use `TypeAlias` for complex type expressions.
- Run pyright in strict mode for library code.
- Avoid `Any` unless interfacing with untyped external APIs.

### Modern Idioms
- Use `match`/`case` for multi-branch dispatch where clearer than if/elif.
- Prefer `dataclasses` or `NamedTuple` over plain dicts for structured data.
- Use `pathlib.Path` over `os.path` for file operations.
- Use f-strings over `str.format()` or `%` formatting.
- Use `from __future__ import annotations` for forward references.

### Safety
- Never use dynamic code execution or unsafe deserialization on untrusted data.
- Validate and sanitize all external inputs at system boundaries.
- Use `secrets` module for cryptographic randomness, not `random`.
- Prefer `subprocess.run` with explicit args list over shell=True.
- Never hardcode secrets; use environment variables via `python-dotenv`.
- Prefer JSON serialization over binary formats for data interchange.

### Testing
- Write pytest tests with clear arrange/act/assert structure.
- Use `responses` library to mock HTTP calls (never hit live APIs in unit tests).
- Prefer parametrize over copy-paste test methods.
- Aim for branch coverage, not just line coverage.
- Use fixtures for shared setup; keep test files focused on one module.

### Dependencies
- Pin direct dependencies with version ranges in `setup.cfg` or `pyproject.toml`.
- Use `tox` for reproducible multi-environment testing.
- Keep dev dependencies separate from runtime dependencies.
- Run `pip-audit` or equivalent for vulnerability checking.

### Formatting and Linting
- Format with black (line length 140 for this project).
- Sort imports with isort (black-compatible profile).
- Lint with flake8 + pylint (errors and warnings).
- Auto-clean with autoflake (remove unused imports) and pyupgrade.
