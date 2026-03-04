## ADDED Requirements

### Requirement: FK properties receiving scalar IDs MUST use scalar converters
When a Directus FK field returns a scalar value (string ID, integer, or UUID) instead of an expanded dict, the model property SHALL use the appropriate scalar converter (`from_str`, `from_int`, `from_uuid`) and type annotation.

#### Scenario: Logo FK returns UUID
- **WHEN** `EngagementEquipe.logo` receives a UUID string instead of a Logo dict
- **THEN** the type SHALL be `UUID | None` and the converter SHALL be `from_uuid`
- **AND** `to_dict` SHALL serialize with `str(self.logo)` or equivalent

#### Scenario: FK returns string ID
- **WHEN** `Organisateur.organisme_id_pere` receives a string ID
- **THEN** the type SHALL be `str | None` and the converter SHALL be `from_str`

#### Scenario: Competition FK scalar conversions
- **WHEN** `CompetitionBase.logo` receives a UUID, `Competition.competition_origine` receives a string, `CompetitionDetail.saison` and `.organisateur` receive strings
- **THEN** each SHALL use the matching scalar type and converter

#### Scenario: CompetitionRencontre FK conversions
- **WHEN** `CompetitionRencontre` FK fields (`id_organisme_equipe1`, `id_organisme_equipe2`, `gs_id`, `id_engagement_equipe1`, `id_engagement_equipe2`, `salle`) receive strings
- **THEN** all SHALL be `str | None` with `from_str`

#### Scenario: Salle FK conversions
- **WHEN** `Salle.commune` and `Salle.cartographie` receive string IDs
- **THEN** both SHALL be `str | None` with `from_str`

#### Scenario: ExternalRencontre FK conversions
- **WHEN** `ExternalRencontre` FK fields (`competition_id`, `id_organisme_equipe1`, `id_organisme_equipe2`, `salle`, `id_poule`) receive strings
- **THEN** all SHALL be `str | None` with `from_str`

#### Scenario: Live FK conversions
- **WHEN** `Live.external_id`, `.team_engagement_home`, `.team_engagement_out` receive strings
- **THEN** all SHALL be `str | None` with `from_str`

#### Scenario: OrganismeEngagement FK conversions
- **WHEN** `OrganismeEngagement.id_poule` and `.id_competition` receive strings
- **THEN** both SHALL be `str | None` with `from_str`

#### Scenario: PhaseEngagement FK conversion
- **WHEN** `PhaseEngagement.id_organisme` receives a string
- **THEN** it SHALL be `str | None` with `from_str`

#### Scenario: TypeCompetitionGenerique FK conversion
- **WHEN** `TypeCompetitionGenerique.logo` receives a UUID
- **THEN** it SHALL be `UUID | None` with `from_uuid`

### Requirement: Dot-notation expanded FK fields MUST keep model types
When `competition_fields.py` uses dot-notation (e.g., `categorie.id`, `categorie.code`), the API always returns an expanded dict. These properties SHALL keep their model type with `from_obj`.

#### Scenario: CompetitionBase.categorie stays Categorie
- **WHEN** `competition_fields.py` specifies `categorie.id`, `categorie.code`, `categorie.libelle`, `categorie.ordre`
- **THEN** `CompetitionBase.categorie` SHALL remain `Categorie | None` with `from_obj(Categorie.from_dict, ...)`

#### Scenario: CompetitionBase.type_competition_generique stays model
- **WHEN** `competition_fields.py` specifies `typeCompetitionGenerique.id`, `typeCompetitionGenerique.logo`
- **THEN** `CompetitionBase.type_competition_generique` SHALL remain `TypeCompetitionGenerique | None`

### Requirement: Value-type mismatches MUST be corrected
When the API returns a different primitive type than the model expects, the model SHALL be updated to match.

#### Scenario: Commune.commune_id int to str
- **WHEN** `Commune.commune_id` uses `from_int` but the API returns a string
- **THEN** it SHALL be changed to `str | None` with `from_str`

#### Scenario: PratiquesHit.id int to str
- **WHEN** `PratiquesHit.id` uses `from_int` but MeiliSearch returns a string
- **THEN** it SHALL be changed to `str | None` with `from_str`

#### Scenario: TerrainsHit.id int to str
- **WHEN** `TerrainsHit.id` uses `from_int` but MeiliSearch returns a string
- **THEN** it SHALL be changed to `str | None` with `from_str`

#### Scenario: PouleRencontreItemModel.numero int to str
- **WHEN** `PouleRencontreItemModel.numero` receives mixed `str | int` values
- **THEN** it SHALL be `str | None` with `from_str` (single type policy)

### Requirement: Missing enum values MUST be added
When the API returns enum values not present in the Python enum definition, those values SHALL be added.

#### Scenario: TypeCompetitionEnum missing values
- **WHEN** the API returns `"DIV 3x3"` and `"PLAT"` which are not in `TypeCompetitionEnum`
- **THEN** `DIV_3X3 = "DIV 3x3"` and `PLAT = "PLAT"` SHALL be added

#### Scenario: PratiquesHitTypeEnum missing Point
- **WHEN** the API returns `"Point"` which is not in `PratiquesHitTypeEnum`
- **THEN** `POINT = "Point"` SHALL be added

#### Scenario: TournoisHitTypeEnum missing Point
- **WHEN** the API returns `"Point"` which is not in `TournoisHitTypeEnum`
- **THEN** `POINT = "Point"` SHALL be added

### Requirement: Unenumerable value sets MUST use str type
When a field receives a large, open-ended set of values that cannot be reasonably enumerated, the property SHALL use `str | None` instead of an enum.

#### Scenario: DocumentFlyerType to str
- **WHEN** `DocumentFlyer.type` uses `DocumentFlyerType` enum (2 values) but receives 23+ MIME types
- **THEN** the type SHALL be `str | None` with `from_str`
- **AND** `document_flyer_type.py` SHALL be deleted

### Requirement: Missing fields MUST be added to OrganismeFields
Fields present in the API response but absent from `OrganismeFields.get_fields()` SHALL be added.

#### Scenario: Add 8 missing organisme fields
- **WHEN** the API returns `dateAffiliation`, `entreprise`, `handibasket`, `horsAssociation`, `logo_base64`, `omnisport`, `saison_en_cours`, `url_competition`
- **THEN** these 8 fields SHALL be added to `OrganismeFields.get_fields()`
