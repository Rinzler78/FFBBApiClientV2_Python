## ADDED Requirements

### Requirement: OpenSpec project context completeness
The `openspec/project.md` file SHALL contain all 5 required sections: Purpose, Tech Stack, Domain Context, Important Constraints, and External Dependencies.

#### Scenario: All sections present
- **WHEN** reading `openspec/project.md`
- **THEN** sections for Purpose, Tech Stack, Domain Context, Important Constraints, and External Dependencies SHALL exist with non-placeholder content

#### Scenario: Domain Context describes FFBB APIs
- **WHEN** reading the Domain Context section
- **THEN** it SHALL describe the FFBB federation API landscape (Directus REST + Meilisearch search) and the client library's role

### Requirement: OpenSpec task dependency declarations
Every task in OpenSpec `tasks.md` files SHALL declare explicit `depends_on` fields when inter-task dependencies exist.

#### Scenario: Tasks have depends_on fields
- **WHEN** reading `openspec/changes/fix-conversion-mismatch-detection/tasks.md`
- **THEN** each phase beyond Phase 0 SHALL declare `depends_on` referencing its prerequisite phase(s)

#### Scenario: No circular dependencies
- **WHEN** parsing all `depends_on` declarations in a tasks.md file
- **THEN** the dependency graph SHALL be acyclic (no task depends transitively on itself)
