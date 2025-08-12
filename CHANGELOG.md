# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - Unreleased

### Added
- Comprehensive data models with automatic validation (`GetOrganismeResponse`, `GetCompetitionResponse`, `GetSaisonsResponse`, `GetPouleResponse`)
- Centralized query fields management with `QueryFieldsManager` and `FieldSet` enums
- 28 comprehensive unit tests with 100% pass rate
- Enhanced integration tests with real API validation
- Automatic environment variable loading from `.env` files
- Pre-commit hooks for code quality enforcement (Black, Flake8, isort)
- Advanced usage examples in documentation
- API reference documentation

### Changed
- **BREAKING**: API methods now return strongly-typed model objects instead of dictionaries
- **BREAKING**: Field management now uses centralized `QueryFieldsManager` class
- All API methods use default fields automatically when fields parameter is None
- Improved error handling with automatic invalid data filtering
- Enhanced documentation with comprehensive examples
- Better API response parsing with `{"data": {...}}` wrapper handling

### Fixed
- API response parsing issues with nested data structures
- Environment variable loading in test environments
- Field parameter handling in API method calls
- Pre-commit hook configuration issues
- Import statements and module organization
- Test reliability and deterministic behavior

### Improved
- Code quality with strict Python standards adherence
- Type hints throughout the codebase
- Performance with smart field selection
- Request caching for better performance
- Documentation with real-world usage scenarios

## [1.0.1] - 2025-08-12

### Added
- Basic integration tests and enhanced testing framework
- Improved API client functionality

### Fixed
- Various bug fixes and stability improvements

## [1.0.0.1] - Previous Release

### Added
- Basic FFBB API client functionality
- Search capabilities across multiple resource types
- Request caching support
- Meilisearch integration for search functionality
- Multi-search across all resource types

### Features
- Access to FFBB API endpoints (competitions, organismes, lives, etc.)
- Search functionality for clubs, competitions, matches, venues
- Basic data models and response handling
- PyScaffold-based project structure
- Apache 2.0 licensing

---

## Migration Guide

### From v1.0.x to v1.1.0

**API Response Changes:**
```python
# Before
organisme = client.get_organisme(123)
name = organisme['nom']  # Dictionary access

# After
organisme = client.get_organisme(123)
name = organisme.nom  # Object attribute access
```

**Field Selection:**
```python
# Before
fields = ["id", "nom", "code"]

# After
from ffbb_api_client_v2.models.query_fields import QueryFieldsManager, FieldSet
fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
```

**Error Handling:**
```python
# After - Automatic error handling
organisme = client.get_organisme(999999)
if organisme is None:
    print("Organization not found or error occurred")
```
