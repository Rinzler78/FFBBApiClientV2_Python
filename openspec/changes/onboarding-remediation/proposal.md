## Why

The project onboarding audit (2026-03-17) identified 14 FAIL and 6 WARN across 43 compliance checks. The most impactful gaps are: incomplete agent specifications blocking governance routing, missing optimization configuration blocking 6 token-efficiency checks, untagged releases creating version drift, and missing OpenSpec task dependencies. Remediating now unblocks compliant development workflow and prevents governance debt from compounding.

## What Changes

- Complete all 3 project agent specification files with required sections (Trigger Conditions, Input/Output Contract, Config Justification, Checks Owned, inherits)
- Add agent routing table and governance overlay to project AGENTS.md and .claude/AGENTS.md
- Create `.claude/optimization.yml` and `.claude/repo-map.yml` for token optimization
- Expand `openspec/project.md` with missing Domain Context, Important Constraints, External Dependencies
- Add `depends_on` fields to OpenSpec task files
- Fix release governance: create missing annotated tags (v1.3.0, v1.4.0), fix CHANGELOG comparison links, document release workflow
- Move pyright-lsp plugin from user scope to project scope
- Add tool-first strategy and retrieval workflow documentation to `.claude/CLAUDE.md`
- Update CLAUDE.roadmap.md to remove stale tag references

## Capabilities

### New Capabilities
- `agent-governance-completion`: Complete agent specifications, routing table, check ownership, and .claude/AGENTS.md overlay
- `token-optimization-config`: Create optimization.yml, repo-map.yml, and document tool-first strategy
- `release-governance-fix`: Create missing tags, fix CHANGELOG links, document release workflow
- `openspec-quality-fix`: Expand openspec/project.md and add task dependency declarations

### Modified Capabilities
- `code-quality-standards`: Add tool-first strategy and retrieval workflow docs to existing CLAUDE.md governance

## Impact

- **Governance files**: AGENTS.md, .claude/AGENTS.md (new), .claude/agents/*.md (3 files updated)
- **Optimization files**: .claude/optimization.yml (new), .claude/repo-map.yml (new)
- **Release artifacts**: CHANGELOG.md (link fixes), RELEASING.md (new), git tags (v1.3.0, v1.4.0)
- **OpenSpec files**: openspec/project.md (expanded), openspec/changes/*/tasks.md (depends_on added)
- **Settings**: .claude/settings.local.json (pyright-lsp addition), ~/.claude/settings.json (pyright-lsp removal)
- **Documentation**: .claude/CLAUDE.md (tool-first strategy), CLAUDE.roadmap.md (stale refs removed)
- **No breaking changes** — all modifications are additive governance/configuration
- **SemVer**: No library code changes, no version bump needed
- **Testing**: No test changes required (governance-only change)
