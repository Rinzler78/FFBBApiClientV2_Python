## Why

The `discover_types.py` script identified **60 Tier 1** (type-level mismatches where `from_obj` receives scalars), **10 Tier 2** (enum value mismatches), **11 Tier 3** (value-level type mismatches), and **49 missing model fields**. Additionally, the model layer has accumulated significant technical debt: duplicate models representing the same JSON structures, inconsistent naming conventions (`*ID`, `*Class`, `*Ref` suffixes), name collisions across API-specific modules, and enum classes that shadow dataclass names.

## What Changes

- **BREAKING**: Rename all 30+ enum classes to `*Enum` suffix (e.g., `Sexe` → `SexeEnum`, `HitType` → `PratiquesHitTypeEnum`)
- **BREAKING**: Deduplicate ~10 model classes by merging subsets into their supersets (e.g., `PurpleLogo` → `Logo`, `TeamEngagement` → `EngagementEquipe`, `OrganismeIDPere` → `Organisateur`)
- **BREAKING**: Restructure `CompetitionID` + `CompetitionRef` into `CompetitionBase` + `Competition` + `CompetitionDetail` with shared base class
- **BREAKING**: Rename models to remove `ID`/`Class`/`Ref` suffixes (e.g., `ExternalID` → `ExternalRencontre`, `SexeClass` → `SexeFacet`, `IDPoule` → `Poule`)
- Fix ~20 FK properties using `from_obj` that receive scalar IDs → convert to `from_str`/`from_uuid`
- Fix 5 value-type mismatches (e.g., `int | None` → `str | None` where API returns strings)
- Add missing enum values to `TypeCompetition`, `PratiquesHitType`, `TournoisHitType`
- Convert `DocumentFlyerType` enum to `str | None` (23+ MIME types, not enumerable)
- Add 8 missing fields to `OrganismeFields`
- Deduplicate cross-API enums (`SexeEnum` exists identically in both `models/` and `meilisearch_ffbb/models/`)
- Delete orphaned file `meilisearch_ffbb/models/tournois_libelle.py`
- Create validation script to confirm dot-notation FK fields (`categorie`, `type_competition_generique`) always return expanded dicts
- Update all tests, scripts, and examples to reflect renames

## Capabilities

### New Capabilities
- `model-naming-conventions`: Enforce consistent naming across the model layer — `*Enum` for enums, `*Facet` for facet-count dataclasses, PascalCase classes matching snake_case module names, no `ID`/`Class`/`Ref` suffixes
- `model-deduplication`: Eliminate duplicate model classes by merging subsets into supersets, creating shared base classes where distinct variants exist
- `converter-type-fixes`: Fix type mismatches in `from_dict` converters — FK scalars use `from_str`/`from_uuid`, value types match API reality
- `fk-validation-script`: Validation script confirming dot-notation FK expansion behavior

### Modified Capabilities

## Impact

- **Models** (`src/ffbb_api_client_v2/models/`): ~50 files renamed/modified/deleted. All enum and dataclass names change.
- **MeiliSearch models** (`src/ffbb_api_client_v2/meilisearch_ffbb/models/`): ~10 files updated for import changes + 3 files deleted (duplicate enum, orphaned file)
- **Directus models** (`src/ffbb_api_client_v2/directus_ffbb/models/`): ~15 files updated for import changes + field additions
- **Public API**: All re-exports in `__init__.py` files change. This is a **major breaking change** for consumers importing model classes.
- **Tests/Scripts/Examples**: All files referencing model names must be updated.
- **SemVer**: Requires a **major version bump** due to breaking public API changes.
