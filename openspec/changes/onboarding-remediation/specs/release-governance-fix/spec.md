## ADDED Requirements

### Requirement: CHANGELOG and git tags alignment
Every version documented in CHANGELOG.md SHALL have a corresponding annotated git tag. CHANGELOG comparison links SHALL point to correct tag ranges.

#### Scenario: v1.3.0 tag exists
- **WHEN** running `git tag -l v1.3.0`
- **THEN** the tag SHALL exist as an annotated tag

#### Scenario: v1.4.0 tag exists
- **WHEN** running `git tag -l v1.4.0`
- **THEN** the tag SHALL exist as an annotated tag

#### Scenario: Comparison links are correct
- **WHEN** reading CHANGELOG.md footer links
- **THEN** `[1.3.0]` SHALL point to `compare/v1.2.0...v1.3.0` and `[1.4.0]` SHALL point to `compare/v1.3.0...v1.4.0`

### Requirement: Release workflow documentation
A `RELEASING.md` file SHALL exist documenting the tag creation and publishing workflow.

#### Scenario: Release runbook present
- **WHEN** reading `RELEASING.md`
- **THEN** the file SHALL document: prerequisites, `cz bump` usage, tag push procedure, CI publish trigger, and rollback steps

### Requirement: Roadmap stale reference cleanup
`CLAUDE.roadmap.md` SHALL NOT reference git tags that do not exist in the repository.

#### Scenario: No stale tag references
- **WHEN** reading `.claude/CLAUDE.roadmap.md`
- **THEN** all version references SHALL correspond to existing git tags or be marked as "planned"
