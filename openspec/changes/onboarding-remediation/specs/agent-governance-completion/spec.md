## ADDED Requirements

### Requirement: Agent specification completeness
Each project agent file in `.claude/agents/` SHALL contain all sections required by the agent specification standard: YAML frontmatter (name, description, model, color, owner_agent, inherits), Trigger Conditions, Input Contract, Output Contract, Config Justification, and Checks Owned.

#### Scenario: api-contract-guardian fully specified
- **WHEN** reading `.claude/agents/api-contract-guardian.md`
- **THEN** the file SHALL contain all 5 required sections with non-empty content and `inherits: api-contract-guardian` in frontmatter

#### Scenario: python-reviewer fully specified
- **WHEN** reading `.claude/agents/python-reviewer.md`
- **THEN** the file SHALL contain all 5 required sections with non-empty content and `inherits: python-reviewer` in frontmatter

#### Scenario: release-manager-lite fully specified
- **WHEN** reading `.claude/agents/release-manager-lite.md`
- **THEN** the file SHALL contain all 5 required sections with non-empty content and `inherits: release-manager` in frontmatter

### Requirement: Agent routing table in AGENTS.md
The project root `AGENTS.md` SHALL contain a routing table mapping user intents to the 3 project agents, following the format: `| User Intent | Route To | Context to Pass |`.

#### Scenario: Routing table present and complete
- **WHEN** reading `AGENTS.md`
- **THEN** a table with columns "User Intent", "Route To", "Context to Pass" SHALL exist with at least 3 rows mapping to api-contract-guardian, python-reviewer, and release-manager-lite

### Requirement: Agent check ownership declarations
Each project agent SHALL declare ownership of its assigned project-level checks (CHK-*.md files) in its `## Checks Owned` section.

#### Scenario: Check ownership cross-reference
- **WHEN** listing all `.claude/checks/CHK-*.md` files
- **THEN** every check SHALL be referenced in exactly one agent's Checks Owned section

### Requirement: Claude AGENTS overlay
A `.claude/AGENTS.md` file SHALL exist as the project-level Claude governance overlay, referencing the 3 project agents and their routing.

#### Scenario: Overlay file exists with agent references
- **WHEN** reading `.claude/AGENTS.md`
- **THEN** the file SHALL reference api-contract-guardian, python-reviewer, and release-manager-lite with their model tier and responsibility summary
