## Context

The onboarding audit (2026-03-17) evaluated 43 compliance checks and found 14 FAIL / 6 WARN. The failures cluster into 4 independent domains:

1. **Agent governance** (5 FAILs): Project agents lack required specification sections, routing table, check ownership, and inherits metadata.
2. **Token optimization** (7 FAILs): Missing `.claude/optimization.yml` and `.claude/repo-map.yml` block all optimization checks.
3. **Release governance** (2 FAILs + 1 WARN): CHANGELOG documents v1.3.0/v1.4.0 but tags don't exist; comparison links broken; no release runbook.
4. **OpenSpec quality** (2 FAILs): `openspec/project.md` incomplete; tasks lack `depends_on` fields.

All changes are governance/configuration artifacts — no library source code is modified.

## Goals / Non-Goals

**Goals:**
- Resolve all 14 FAIL checks to PASS
- Resolve WARN checks where actionable (optimization, release, roadmap)
- Establish complete agent governance chain (specifications + routing + ownership)
- Create optimization configuration as single source of truth
- Align CHANGELOG and git tags

**Non-Goals:**
- Refactoring library source code (facade split, to_dict DRY — flagged by code-reviewer but out of scope)
- Adding pytest markers to test files (P2 test-strategist finding — separate change)
- Upgrading CI to OIDC trusted publishing (P1 but requires GitHub settings changes)
- Adding dependency lower bounds (P2 security finding — separate change)

## Decisions

### D1: Single optimization.yml with all sections
All 6 optimization checks read from `.claude/optimization.yml`. Creating one file with all sections (context_compression, context_pruning, code_chunking, retrieval, caching, tool_first) is simpler and more maintainable than multiple files. Sections follow the check criteria exactly.

### D2: Agent specs get full specification standard in one pass
Rather than incremental fixes, update all 3 agent files to the full specification standard (frontmatter fields + 5 required sections). This prevents repeated governance failures and establishes the pattern for future agents.

### D3: Tags created from CHANGELOG dates, not retroactively bumped
v1.3.0 and v1.4.0 tags will be created as annotated tags pointing at the commits that correspond to the CHANGELOG release dates. This preserves history accuracy.

### D4: pyright-lsp stays at user level (decision reversal)
The tooling-decisions.yaml already documents that pyright-lsp was intentionally kept at user level to avoid duplication. The check flags scope policy, but the documented rationale is valid. Mark as acknowledged deviation rather than moving the plugin.

### D5: Existing OpenSpec tasks get depends_on via phase numbering
Rather than restructuring existing tasks.md files, add YAML `depends_on` declarations at the top of each phase referencing the prior phase ID.

## Risks / Trade-offs

- [Risk] Creating tags retroactively may confuse CI if it triggers on tag push → Mitigation: Create tags locally first, push only after verifying CI config won't auto-publish stale artifacts.
- [Risk] optimization.yml values are estimates without profiling data → Mitigation: Use conservative defaults; tune after measuring actual session token usage.
- [Risk] Agent specification updates may drift from global agent standard updates → Mitigation: Agent spec standard is versioned in policy; periodic re-audit via `check-type-governance`.
