# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-02-10

### Added
- 2 new Meilisearch indexes: `ffbbserver_engagements` (~105k hits), `ffbbserver_formations` (~90 hits)
- `EngagementsHit`, `FormationsHit`, `MeilisearchIndexSettings` and associated models (facets, stats, multi-search queries)
- `filter`, `sort`, `limit` parameters on all 18 search methods
- `FieldSet.WILDCARD` for Directus queries with all fields
- `MeilisearchClient.get_index_settings()` to retrieve index settings
- Discovery scripts: `discover_meilisearch_indexes.py`, `discover_meilisearch_settings.py`, `discover_api_fields.py`
- Analytics notebooks: `simple_rating_notebook.ipynb`, `projection_notebook.ipynb`
- Interactive Streamlit dashboard: `basketball_dashboard.py`
- API model audit script: `audit_api_models.py`
- Automated developer setup: `setup_dev.sh`, `requirements.txt`
- Tests: `test_207` to `test_209` (clients), `test_124` to `test_127` (models)

### Changed (Breaking)
- **BREAKING**: `fields` parameter removed from 5 Directus methods, only `field_set: FieldSet` remains (default `FieldSet.DETAILED`)
- **BREAKING**: `FieldSet.MINIMAL` removed (never handled by QueryFieldsManager)
- **BREAKING**: `deep_limit` renamed to `deep_rencontres_limit` (int) in `get_competition()`
- **BREAKING**: `get_poule()` now exposes explicit deep parameters (`deep_rencontres_limit`, `deep_rencontres_filter_saison_actif`, `deep_rencontres_sort`, `deep_classements_limit`)
- `validate_deep_limit` max increased from 10000 to 100000
- Completed facets for competitions, salles, terrains indexes

### Fixed
- Swapped `TerrainsHit` and `TournoisHit` models (fields matched the wrong index)
- Phantom `horaire` field removed from `RencontresHit`
- `TournoisMultiSearchQuery`: missing sort propagation

### Removed
- `GradientColor` model (unused)
- Old example scripts (`complete_usage_example.py`, `quick_start.py`, `team_ranking_analysis.py`)

## [1.2.0] - 2025-02-05

### Added
- **NEW**: `TokenManager` class for automatic token resolution
  - Fetches tokens from environment variables or FFBB API
  - Uses HTTP-level caching via `CacheManager` for configuration requests
  - `FFBBTokens` dataclass for type-safe token handling
- **NEW**: Centralized configuration module (`config.py`)
  - `API_FFBB_BASE_URL`, `MEILISEARCH_BASE_URL` constants
  - `DEFAULT_USER_AGENT` constant
  - `ENV_API_TOKEN`, `ENV_MEILISEARCH_TOKEN` environment variable names
  - API endpoint path constants (`ENDPOINT_CONFIGURATION`, `ENDPOINT_LIVES`, etc.)
  - Meilisearch endpoint path constants (`MEILISEARCH_ENDPOINT_MULTI_SEARCH`)
- New tests: `test_019_config.py`, `test_020_token_manager.py`

### Changed
- **BREAKING**: `TokenManager.get_tokens()` signature changed: `use_cache` parameter replaced by `cache_config`
- API clients now use centralized endpoint constants from `config.py`
- Simplified Quick Start examples using TokenManager
- Updated all example scripts to demonstrate TokenManager usage

### Removed
- `TokenManager.clear_cache()` method (use `get_cache_manager().clear()` instead)
- `TokenManager._cached_tokens` class variable (HTTP caching is now used)

### Improved
- No more manual token management required for basic usage
- Environment variable handling is now optional (tokens can be auto-fetched)

## [1.1.1] - 2025-09-16

### Fixed
- Fixed flake8 line length errors that prevented CI workflow from completing
- Updated maximum line length configuration to be compatible with Black formatting
- Improved code formatting consistency across the codebase

## [1.1.0] - 2025-09-16

### Added
- Comprehensive data models with automatic validation (`GetOrganismeResponse`, `GetCompetitionResponse`, `GetSaisonsResponse`, `GetPouleResponse`)
- Centralized query fields management with `QueryFieldsManager` and `FieldSet` enums
- 28 comprehensive unit tests with 100% pass rate
- Enhanced integration tests with real API validation
- Automatic environment variable loading from `.env` files
- Pre-commit hooks for code quality enforcement (Black, Flake8, isort)
- Advanced usage examples in documentation
- API reference documentation
- **NEW**: Team ranking analysis example (`examples/team_ranking_analysis.py`)
- **NEW**: Input validation utilities with secure token handling
- **NEW**: Retry mechanisms with exponential backoff for improved reliability
- **NEW**: Caching system for performance optimization

### Changed
- **BREAKING**: API methods now return strongly-typed model objects instead of dictionaries
- **BREAKING**: Field management now uses centralized `QueryFieldsManager` class
- All API methods use default fields automatically when fields parameter is None
- Improved error handling with automatic invalid data filtering
- Enhanced documentation with comprehensive examples
- Better API response parsing with `{"data": {...}}` wrapper handling
- **SECURITY**: Enhanced secure token logging and validation
- **PERFORMANCE**: Modernized Python code to use Python 3.9+ features (union operators, improved type hints)
- **QUALITY**: Applied comprehensive code formatting (Black, isort, pyupgrade) and linting (flake8)

### Fixed
- API response parsing issues with nested data structures
- Environment variable loading in test environments
- **CLEANUP**: Removed development scripts, temporary files, and redundant documentation
- **CONSISTENCY**: Consolidated CHANGELOG files (removed duplicate .rst version)

### Removed
- Temporary development scripts (`analyze_senas_ranking.py`, `find_pelissanne_*.py`, etc.)
- Cache files and temporary directories (`http_cache/`, `http_cache.db`, etc.)
- Redundant documentation files (Pelissanne analysis docs, duplicate parameters files)
- Duplicate CHANGELOG.rst file in favor of unified CHANGELOG.md
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
