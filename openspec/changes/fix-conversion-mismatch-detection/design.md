## Context

The FFBB API client library (`ffbb_api_client_v2`) wraps two APIs — Directus REST and MeiliSearch — into Python dataclass models with typed converters (`from_dict`/`to_dict`). Over time, model definitions drifted from actual API responses: FK fields typed as objects receive scalar IDs, enum values are incomplete, duplicate models exist for the same JSON structures, and naming is inconsistent.

The `discover_types.py` script (recently fixed to use library-defined fields with sampling) produced a comprehensive mismatch report that drives this change.

**Current state:**
- 52 dataclasses, 32 enums, 2 str subclasses in `models/`
- 9 Hit models, 7 FacetDistribution models in `meilisearch_ffbb/models/`
- 15 Response + 12 Fields models in `directus_ffbb/models/`
- ~10 duplicate model pairs (subsets of each other)
- Inconsistent suffixes: `*ID`, `*Class`, `*Ref` with no clear convention

## Goals / Non-Goals

**Goals:**
- Eliminate all confirmed type mismatches (Tier 1 FK scalars, Tier 2 enum gaps, Tier 3 value types)
- Remove duplicate models by merging subsets into supersets
- Establish consistent naming: `*Enum` for enums, `*Facet` for facet counts, no arbitrary suffixes
- Ensure PascalCase class names match snake_case module names
- Deduplicate cross-API enums (single source of truth in `models/`)
- Update all consumers (tests, scripts, examples)

**Non-Goals:**
- Refactoring the converter utility functions (`from_obj`, `from_str`, etc.)
- Adding new API endpoints or capabilities
- Changing the MeiliSearch Hit model architecture (expanded objects are correct there)
- Modifying FacetDistribution dataclass patterns (confirmed correct)
- Full backward compatibility — this is a breaking major version change

## Decisions

### D1: Phased execution order (enum rename -> dedup -> model rename -> type fixes)

**Decision**: Execute renames before type fixes to avoid dealing with stale class names during converter changes.

**Rationale**: Renaming enums first (Phase 0) frees base names. Deduplication (Phase 1) reduces the number of models to fix. Model renames (Phase 3) establish final names. Only then do type fixes (Phase 4-5) apply to the final model structure.

**Alternative considered**: Fix types first, rename later. Rejected because it would require fixing types on models that get deleted during dedup, wasting effort.

### D2: Merge subsets into supersets (not the reverse)

**Decision**: When two models overlap, keep the one with more fields and delete the smaller one. Extra fields will simply be `None` when not populated.

**Rationale**: The superset model is always correct (extra fields default to `None`). The subset model loses data when used in contexts that provide more fields.

**Examples**: `PurpleLogo` (1 field) -> `Logo` (2 fields), `TeamEngagement` (4 fields) -> `EngagementEquipe` (6 fields).

### D3: CompetitionBase inheritance for Competition variants

**Decision**: Create `CompetitionBase` with 10 shared fields, `Competition` (ex-CompetitionID, +5 fields) and `CompetitionDetail` (ex-CompetitionRef, +4 fields) inheriting from it.

**Rationale**: The two models share 10 JSON keys but have different extra fields and are used in different API contexts. A base class avoids code duplication while preserving distinct types.

**Alternative considered**: Single `Competition` model with all 19 fields. Rejected because the two contexts never provide all fields simultaneously — a unified model would mislead consumers.

### D4: Keep `categorie` and `type_competition_generique` as model types in Competition

**Decision**: Keep `Categorie | None` and `TypeCompetitionGenerique | None` (not `str | None`).

**Rationale**: `competition_fields.py` uses dot-notation (`categorie.id`, `categorie.code`...), so Directus always returns expanded dicts. The Tier 1 mismatches for these fields come from Wave 3 FK chain sampling (different context). A validation script will confirm.

### D5: One commit per phase

**Decision**: Each phase produces a separate conventional commit.

**Rationale**: Keeps changes reviewable and revertable. If a phase introduces issues, it can be reverted independently.

### D6: Module naming follows class naming

**Decision**: Every renamed class gets a renamed module file matching `snake_case(ClassName)`.

**Rationale**: Convention enforcement — `SexeEnum` lives in `sexe_enum.py`, `SexeFacet` in `sexe_facet.py`. Makes imports predictable.

## Risks / Trade-offs

**[Risk] Mass rename breaks downstream consumers** -> This is a library; any consumer importing model classes will break. Mitigation: major version bump, complete changelog documenting every rename.

**[Risk] Enum dedup across APIs may miss subtle value differences** -> `SexeEnum` in models/ uses `MIXED` while meilisearch uses `MIXTE` for the same value `"Mixte"`. Mitigation: standardize on `MIXTE` (matches the French string value).

**[Risk] Competition base class inheritance may affect dataclass behavior** -> Mitigation: these models use `@dataclass` with `from_dict`/`to_dict`. The inheritance is straightforward with no metaclass conflicts.

**[Risk] Validation script may reveal unexpected API behavior** -> If `categorie`/`type_competition_generique` sometimes return scalars despite dot-notation fields, we'll need a dual-mode converter. Mitigation: run validation script early (Phase 0.5) before committing to the approach.

**[Trade-off] Extra `None` fields from subset merges** -> When `EngagementEquipe` (6 fields) replaces `IDEngagementEquipe` (3 fields), 3 fields will always be `None` in contexts that previously used the smaller model. Acceptable because `None` is the default for all optional fields.
