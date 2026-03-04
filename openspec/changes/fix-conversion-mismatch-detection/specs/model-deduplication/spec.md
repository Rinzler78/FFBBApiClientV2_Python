## ADDED Requirements

### Requirement: Subset models MUST be merged into their supersets
When a model's fields are a strict subset of another model mapping to the same JSON keys, the subset model SHALL be eliminated and replaced by the superset model everywhere.

#### Scenario: Merge PurpleLogo into Logo
- **WHEN** `PurpleLogo` (1 field: `id`) is a subset of `Logo` (2 fields: `id`, `gradient_color`)
- **THEN** `PurpleLogo` SHALL be replaced by `Logo` in all usages
- **AND** `purple_logo.py` SHALL be deleted

#### Scenario: Merge CompetitionIDCategorie into Categorie
- **WHEN** `CompetitionIDCategorie` (3 fields) is a subset of `Categorie` (6 fields)
- **THEN** `CompetitionIDCategorie` SHALL be replaced by `Categorie`
- **AND** `competition_id_categorie.py` SHALL be deleted

#### Scenario: Merge single-field TypeCompetitionGenerique variants
- **WHEN** `CompetitionIDTypeCompetitionGenerique` and `CompetitionOrigineTypeCompetitionGenerique` both have only `logo`
- **AND** `TypeCompetitionGenerique` has `id` + `logo`
- **THEN** both variants SHALL be replaced by `TypeCompetitionGenerique`
- **AND** both variant files SHALL be deleted

#### Scenario: Merge TeamEngagement into EngagementEquipe
- **WHEN** `TeamEngagement` (4 fields) is a subset of `EngagementEquipe` (6 fields)
- **THEN** `TeamEngagement` SHALL be replaced by `EngagementEquipe`
- **AND** `team_engagement.py` SHALL be deleted

#### Scenario: Merge IDEngagementEquipe into EngagementEquipe
- **WHEN** `IDEngagementEquipe` (3 fields) is a subset of `EngagementEquipe` (6 fields)
- **THEN** `IDEngagementEquipe` SHALL be replaced by `EngagementEquipe`
- **AND** `id_engagement_equipe.py` SHALL be deleted

#### Scenario: Merge OrganismeEquipe into IDOrganismeEquipe
- **WHEN** `OrganismeEquipe` (1 field: `logo`) is a subset of `IDOrganismeEquipe` (6 fields)
- **THEN** `OrganismeEquipe` SHALL be replaced by `IDOrganismeEquipe`
- **AND** `organisme_equipe.py` SHALL be deleted
- **AND** `IDOrganismeEquipe` SHALL be renamed to `OrganismeEquipe`

#### Scenario: Merge OrganismeIDPere into Organisateur
- **WHEN** `OrganismeIDPere` has 0 unique fields vs `Organisateur`
- **AND** type differences (`id`: int vs str, `commune`: int vs str) are resolved to `str | None`
- **THEN** `OrganismeIDPere` SHALL be replaced by `Organisateur`
- **AND** `organisme_id_pere.py` SHALL be deleted

### Requirement: Single-field wrapper models MUST be eliminated when the field becomes scalar
When a model wraps a single FK field and that field is converted to a scalar type, the wrapper model SHALL be deleted.

#### Scenario: Delete OrganismeId
- **WHEN** `OrganismeId` has only `id: str | None`
- **AND** `PhaseEngagement.id_organisme` is converted to `str | None`
- **THEN** `OrganismeId` SHALL be deleted
- **AND** `organisme_id.py` SHALL be deleted

### Requirement: Competition models MUST use base class inheritance
`CompetitionID` and `CompetitionRef` SHALL be restructured into a base class with two specialized subclasses.

#### Scenario: Create CompetitionBase with shared fields
- **WHEN** `CompetitionID` and `CompetitionRef` share 10 JSON keys
- **THEN** a `CompetitionBase` dataclass SHALL be created with those 10 fields
- **AND** `Competition` SHALL inherit from `CompetitionBase` with 5 additional fields (ex-`CompetitionID` unique fields)
- **AND** `CompetitionDetail` SHALL inherit from `CompetitionBase` with 4 additional fields (ex-`CompetitionRef` unique fields)

#### Scenario: Type alignment on shared competition_origine field
- **WHEN** `competition_origine` is `CompetitionOrigine | None` in CompetitionID but `str | None` in CompetitionRef
- **THEN** `CompetitionBase.competition_origine` SHALL use a single consistent type determined by the FK expansion context

### Requirement: Facet-count models MUST be renamed
Models containing facet distribution counts (e.g., `CompetitionIDTypeCompetition` with `championnat`, `coupe` fields) SHALL be renamed with the `Facet` suffix.

#### Scenario: Rename CompetitionIDTypeCompetition
- **WHEN** `CompetitionIDTypeCompetition` contains facet counts
- **THEN** it SHALL be renamed to `CompetitionTypeFacet` in `competition_type_facet.py`

### Requirement: Deleted model files MUST be removed from __init__.py
When a model file is deleted, its import and `__all__` entry in the parent `__init__.py` SHALL be removed.

#### Scenario: Clean up __init__.py after deletion
- **WHEN** `purple_logo.py` is deleted
- **THEN** `from .purple_logo import PurpleLogo` SHALL be removed from `__init__.py`
- **AND** `"PurpleLogo"` SHALL be removed from `__all__`
