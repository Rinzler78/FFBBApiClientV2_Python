## ADDED Requirements

### Requirement: Enum classes MUST use the Enum suffix
All Python `Enum` classes in the library SHALL be named with the `Enum` suffix (e.g., `SexeEnum`, `TypeCompetitionEnum`). The module file SHALL be named `snake_case` of the class name (e.g., `sexe_enum.py`).

#### Scenario: Rename existing enum without Enum suffix
- **WHEN** an enum class `Sexe` exists in `models/sexe.py`
- **THEN** it SHALL be renamed to `SexeEnum` in `models/sexe_enum.py`
- **AND** all imports across the codebase SHALL reference the new name and module

#### Scenario: Resolve HitType name collision
- **WHEN** two different enums share the name `HitType` in `pratiques_hit_type.py` and `tournois_hit_type.py`
- **THEN** they SHALL be renamed to `PratiquesHitTypeEnum` and `TournoisHitTypeEnum` respectively

#### Scenario: Resolve Libelle name collision
- **WHEN** `Libelle` exists in both `models/tournoi_types_3x3_libelle_enum.py` and `meilisearch_ffbb/models/tournois_libelle.py`
- **THEN** the models/ version SHALL be renamed `TournoiTypes3x3LibelleEnum`
- **AND** the meilisearch orphan SHALL be deleted

### Requirement: Facet-count dataclasses MUST use the Facet suffix
Dataclasses that represent MeiliSearch facet distribution counts (fields mapping enum labels to `int` counts) SHALL use the `Facet` suffix instead of `Class`.

#### Scenario: Rename SexeClass to SexeFacet
- **WHEN** a facet-count dataclass `SexeClass` exists in `models/sexe_class.py`
- **THEN** it SHALL be renamed to `SexeFacet` in `models/sexe_facet.py`

#### Scenario: All Class-suffixed facet models renamed
- **WHEN** facet models `NiveauClass`, `TypeClass`, `TournoiTypeClass`, `PratiquesTypeClass` exist
- **THEN** they SHALL be renamed to `NiveauFacet`, `TypeFacet`, `TournoiTypeFacet`, `PratiquesTypeFacet`

### Requirement: Models MUST NOT use ID, Class, or Ref suffixes
Dataclass model names SHALL NOT contain `ID`, `Class`, or `Ref` as suffixes. Names SHALL describe the model's domain concept.

#### Scenario: Rename ID-suffixed models
- **WHEN** models `ExternalCompetitionID`, `ExternalID`, `IDOrganismeEquipe`, `IDPoule` exist
- **THEN** they SHALL be renamed to `ExternalCompetition`, `ExternalRencontre`, `OrganismeEquipe`, `Poule`

#### Scenario: Rename CompetitionRef
- **WHEN** `CompetitionRef` exists
- **THEN** it SHALL be renamed to `CompetitionDetail`

### Requirement: Class names MUST match module names
Every class `FooBar` SHALL live in a module named `foo_bar.py`. PascalCase for classes, snake_case for modules.

#### Scenario: Verify class-module name consistency
- **WHEN** a class is renamed
- **THEN** the module file SHALL also be renamed to match `snake_case(ClassName)`
- **AND** `__init__.py` exports SHALL be updated accordingly

### Requirement: Cross-API enum deduplication
When an identical enum exists in both `models/` and `meilisearch_ffbb/models/`, the global `models/` version SHALL be the single source of truth.

#### Scenario: Deduplicate SexeEnum
- **WHEN** `SexeEnum` exists in both `models/` (values: Feminin, Masculin, Mixte) and `meilisearch_ffbb/models/terrains_sexe_enum.py` (same values)
- **THEN** the meilisearch file SHALL be deleted
- **AND** `TournoisHit` SHALL import `SexeEnum` from the global `models/`
- **AND** the Python attribute `MIXED` SHALL be standardized to `MIXTE`

#### Scenario: Delete orphaned meilisearch enum
- **WHEN** `meilisearch_ffbb/models/tournois_libelle.py` is imported nowhere
- **THEN** it SHALL be deleted

### Requirement: All consumers MUST be updated after renames
Tests, scripts, and examples SHALL be updated to use new class and module names.

#### Scenario: Update test imports
- **WHEN** a model or enum is renamed
- **THEN** all test files in `tests/` that import the old name SHALL be updated

#### Scenario: Update script imports
- **WHEN** a model or enum is renamed
- **THEN** all script files in `scripts/` that reference the old name SHALL be updated

#### Scenario: Update example imports
- **WHEN** a model or enum is renamed
- **THEN** all example files in `examples/` that reference the old name SHALL be updated
