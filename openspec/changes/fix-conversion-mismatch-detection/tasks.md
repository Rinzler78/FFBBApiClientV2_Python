## 1. Phase 0 — Rename enums to *Enum suffix
<!-- depends_on: none -->

- [ ] 1.1 Rename 29 enum classes in `models/` (class name + file name): `Sexe`->`SexeEnum`, `Code`->`CodeEnum`, `Etat`->`EtatEnum`, `Jour`->`JourEnum`, `Label`->`LabelEnum`, `Niveau`->`NiveauEnum`, `Source`->`SourceEnum`, `Status`->`StatusEnum`, `Echelon`->`EchelonEnum`, `Pratique`->`PratiqueEnum`, `AgeGroup`->`AgeGroupEnum`, `Gender`->`GenderEnum`, `Objectif`->`ObjectifEnum`, `NiveauType`->`NiveauTypeEnum`, `CategorieType`->`CategorieTypeEnum`, `TypeLeague`->`TypeLeagueEnum`, `TypeCompetition`->`TypeCompetitionEnum`, `PhaseCode`->`PhaseCodeEnum`, `CodeFonction`->`CodeFonctionEnum`, `ContactRole`->`ContactRoleEnum`, `CoordonneesType`->`CoordonneesTypeEnum`, `OrganisateurType`->`OrganisateurTypeEnum`, `PublicationInternet`->`PublicationInternetEnum`, `CompetitionType`->`CompetitionTypeEnum`, `HitType`(pratiques)->`PratiquesHitTypeEnum`, `HitType`(tournois)->`TournoisHitTypeEnum`, `Libelle`->`TournoiTypes3x3LibelleEnum`, `CategorieChampionnat3X3Libelle`->`CategorieChampionnat3x3LibelleEnum`, `CompetitionOrigineTypeCompetition`->`CompetitionOrigineTypeCompetitionEnum`
- [ ] 1.2 Rename 2 enum classes in `meilisearch_ffbb/models/`: `Name`->`TerrainsNameEnum`, `Storage`->`TerrainsStorageEnum`
- [ ] 1.3 Update all `__init__.py` files with new imports and `__all__` entries
- [ ] 1.4 Update all importing files across `models/`, `meilisearch_ffbb/`, `directus_ffbb/`, `tests/`, `scripts/`, `examples/`
- [ ] 1.5 Deduplicate cross-API: delete `meilisearch_ffbb/models/terrains_sexe_enum.py`, point `TournoisHit` to global `SexeEnum`. Standardize `MIXED`->`MIXTE`
- [ ] 1.6 Delete orphaned `meilisearch_ffbb/models/tournois_libelle.py`
- [ ] 1.7 Verify: `python -m py_compile` on all changed files + `python -c "from ffbb_api_client_v2 import *"`
- [ ] 1.8 Commit: `refactor(models): rename all enums to *Enum suffix, deduplicate cross-API enums`

## 2. Phase 0.5 — FK expansion validation script
<!-- depends_on: Phase 0 -->

- [ ] 2.1 Create `scripts/validate_fk_expansion.py`: verify `categorie` and `type_competition_generique` return dicts with dot-notation fields
- [ ] 2.2 Run the script and document results
- [ ] 2.3 Commit: `test(scripts): add FK expansion validation script`

## 3. Phase 1 — Model deduplication and merging
<!-- depends_on: Phase 0, Phase 0.5 -->

- [ ] 3.1 Replace `PurpleLogo` with `Logo` everywhere, delete `purple_logo.py`
- [ ] 3.2 Replace `CompetitionIDCategorie` with `Categorie` in `CompetitionID`, delete `competition_id_categorie.py`
- [ ] 3.3 Replace `CompetitionIDTypeCompetitionGenerique` and `CompetitionOrigineTypeCompetitionGenerique` with `TypeCompetitionGenerique`, delete both files
- [ ] 3.4 Replace `TeamEngagement` with `EngagementEquipe`, delete `team_engagement.py`
- [ ] 3.5 Replace `IDEngagementEquipe` with `EngagementEquipe`, delete `id_engagement_equipe.py`
- [ ] 3.6 Replace `OrganismeEquipe` with `IDOrganismeEquipe`, delete `organisme_equipe.py`
- [ ] 3.7 Replace `OrganismeIDPere` with `Organisateur` (after type alignment: `id`/`commune` to `str`), delete `organisme_id_pere.py`
- [ ] 3.8 Delete `OrganismeId` (`organisme_id.py`), update `PhaseEngagement.id_organisme` to `str | None`
- [ ] 3.9 Create `CompetitionBase` (10 shared fields), refactor `CompetitionID` into `Competition(CompetitionBase)` + 5 fields, refactor `CompetitionRef` into `CompetitionDetail(CompetitionBase)` + 4 fields. Delete `competition_id.py` and `competition_ref.py`
- [ ] 3.10 Rename `CompetitionIDTypeCompetition` to `CompetitionTypeFacet` in `competition_type_facet.py`
- [ ] 3.11 Update all `__init__.py` files, remove deleted imports
- [ ] 3.12 Update all importing files across entire codebase
- [ ] 3.13 Verify: compile check + import check
- [ ] 3.14 Commit: `refactor(models): deduplicate models, create CompetitionBase hierarchy`

## 4. Phase 2 — Enum value fixes
<!-- depends_on: Phase 1 -->

- [ ] 4.1 Add `DIV_3X3 = "DIV 3x3"` and `PLAT = "PLAT"` to `TypeCompetitionEnum`
- [ ] 4.2 Add `POINT = "Point"` to `PratiquesHitTypeEnum`
- [ ] 4.3 Add `POINT = "Point"` to `TournoisHitTypeEnum`
- [ ] 4.4 Convert `DocumentFlyer.type` from `DocumentFlyerType | None` to `str | None`, delete `document_flyer_type.py`
- [ ] 4.5 Check `TournoiTypes3x3LibelleEnum` for missing values, add if needed
- [ ] 4.6 Update `__init__.py` for deleted `document_flyer_type.py`
- [ ] 4.7 Verify: compile check
- [ ] 4.8 Commit: `fix(models): add missing enum values, convert DocumentFlyerType to str`

## 5. Phase 3 — Model renaming
<!-- depends_on: Phase 1, Phase 2 -->

- [ ] 5.1 Rename `ExternalCompetitionID` to `ExternalCompetition` (`external_competition.py`)
- [ ] 5.2 Rename `ExternalID` to `ExternalRencontre` (`external_rencontre.py`)
- [ ] 5.3 Rename `IDOrganismeEquipe` to `OrganismeEquipe` (`organisme_equipe.py`)
- [ ] 5.4 Rename `IDPoule` to `Poule` (`poule.py`)
- [ ] 5.5 Rename `SexeClass` to `SexeFacet` (`sexe_facet.py`), `NiveauClass` to `NiveauFacet` (`niveau_facet.py`), `TypeClass` to `TypeFacet` (`type_facet.py`), `TournoiTypeClass` to `TournoiTypeFacet` (`tournoi_type_facet.py`), `PratiquesTypeClass` to `PratiquesTypeFacet` (`pratiques_type_facet.py`)
- [ ] 5.6 Update all `__init__.py` files with new imports
- [ ] 5.7 Update all importing files across entire codebase (models, meilisearch, directus, tests, scripts, examples)
- [ ] 5.8 Verify: compile check + import check
- [ ] 5.9 Commit: `refactor(models): rename ID/Class-suffixed models to descriptive names`

## 6. Phase 4 — FK from_obj to scalar converter fixes
<!-- depends_on: Phase 3 -->

- [ ] 6.1 Fix Competition models: `CompetitionBase.logo`->`UUID`, `Competition.competition_origine`->`str`, `CompetitionDetail.saison`/`.organisateur`->`str`
- [ ] 6.2 Fix `CompetitionRencontre`: `id_organisme_equipe1/2`, `gs_id`, `id_engagement_equipe1/2`, `salle` -> `str`
- [ ] 6.3 Fix Engagement/Organisme: `EngagementEquipe.logo`->`UUID`, `OrganismeEquipe.logo`->`UUID`, `Organisateur.organisme_id_pere`->`str`, `OrganismeEngagement.id_poule`/`.id_competition`->`str`, `PhaseEngagement.id_organisme`->`str`, `TypeCompetitionGenerique.logo`->`UUID`
- [ ] 6.4 Fix Salle: `commune`->`str`, `cartographie`->`str`
- [ ] 6.5 Fix `ExternalRencontre`: `competition_id`, `id_organisme_equipe1/2`, `salle`, `id_poule` -> `str`
- [ ] 6.6 Fix `Live`: `external_id`, `team_engagement_home`, `team_engagement_out` -> `str`
- [ ] 6.7 Update `to_dict()` methods for all changed properties
- [ ] 6.8 Verify: compile check
- [ ] 6.9 Commit: `fix(models): convert FK from_obj to scalar converters for Directus FK fields`

## 7. Phase 5 — Value type fixes
<!-- depends_on: Phase 4 -->

- [ ] 7.1 Fix `Commune.commune_id`: `int | None` -> `str | None` with `from_str`
- [ ] 7.2 Fix `PratiquesHit.id`: `int | None` -> `str | None` with `from_str`
- [ ] 7.3 Fix `TerrainsHit.id`: `int | None` -> `str | None` with `from_str`
- [ ] 7.4 Fix `PouleRencontreItemModel.numero`: `int | None` -> `str | None` with `from_str`
- [ ] 7.5 Verify: compile check
- [ ] 7.6 Commit: `fix(models): correct value type mismatches (int -> str)`

## 8. Phase 6 — Missing OrganismeFields
<!-- depends_on: Phase 5 -->

- [ ] 8.1 Add 8 fields to `OrganismeFields.get_fields()`: `dateAffiliation`, `entreprise`, `handibasket`, `horsAssociation`, `logo_base64`, `omnisport`, `saison_en_cours`, `url_competition`
- [ ] 8.2 Verify: compile check
- [ ] 8.3 Commit: `fix(models): add 8 missing fields to OrganismeFields`

## 9. Phase 7 — Tests, scripts, examples update
<!-- depends_on: Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6 -->

- [ ] 9.1 Update all test files in `tests/` for renamed classes/modules
- [ ] 9.2 Update `scripts/discover_types.py` and other scripts for renamed classes
- [ ] 9.3 Update all files in `examples/` for renamed classes
- [ ] 9.4 Run `python -m pytest tests/` — all tests must pass
- [ ] 9.5 Commit: `refactor(tests): update tests, scripts, examples for model renames`

## 10. Phase 8 — Final cleanup and verification
<!-- depends_on: Phase 7 -->

- [ ] 10.1 Verify no orphaned model files remain (grep for old class names)
- [ ] 10.2 Verify all `__init__.py` exports are consistent
- [ ] 10.3 Verify class name <-> module name consistency (PascalCase <-> snake_case)
- [ ] 10.4 Run full verification: `python -m py_compile`, `python -m pytest tests/`, `python -c "from ffbb_api_client_v2 import *"`
- [ ] 10.5 Run `scripts/discover_types.py` and verify Tier 1/2/3 counts decreased
- [ ] 10.6 Run `scripts/validate_fk_expansion.py` and confirm results
- [ ] 10.7 Commit any remaining fixes: `chore: final cleanup after model restructuring`
