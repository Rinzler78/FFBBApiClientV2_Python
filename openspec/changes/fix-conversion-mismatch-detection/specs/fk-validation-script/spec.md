## ADDED Requirements

### Requirement: A validation script MUST confirm dot-notation FK expansion
A script `scripts/validate_fk_expansion.py` SHALL verify that FK fields using dot-notation in `competition_fields.py` always return expanded dicts from the Directus API.

#### Scenario: Validate categorie returns dict
- **WHEN** the script requests a competition with fields including `categorie.id`, `categorie.code`, `categorie.libelle`, `categorie.ordre`
- **THEN** the `categorie` field in the response SHALL be a `dict` (not a scalar)
- **AND** the script SHALL report success

#### Scenario: Validate type_competition_generique returns dict
- **WHEN** the script requests a competition with fields including `typeCompetitionGenerique.id`, `typeCompetitionGenerique.logo`
- **THEN** the `typeCompetitionGenerique` field in the response SHALL be a `dict` (not a scalar)
- **AND** the script SHALL report success

#### Scenario: Handle API unavailability
- **WHEN** the Directus API is unreachable or authentication fails
- **THEN** the script SHALL exit with a clear error message and non-zero exit code

#### Scenario: Report unexpected scalar values
- **WHEN** any checked FK field returns a scalar instead of a dict
- **THEN** the script SHALL report a warning with the field name, expected type, and actual value
- **AND** exit with non-zero exit code
