## 1. Agent Governance Completion (P0)

- [x] 1.1 Update `.claude/agents/api-contract-guardian.md` with full specification: add owner_agent + inherits to frontmatter, add Trigger Conditions, Input Contract, Output Contract, Config Justification, Checks Owned sections
- [x] 1.2 Update `.claude/agents/python-reviewer.md` with full specification (same sections as 1.1)
- [x] 1.3 Update `.claude/agents/release-manager-lite.md` with full specification (same sections as 1.1)
- [x] 1.4 Add agent routing table to `AGENTS.md` mapping user intents to project agents
- [x] 1.5 Create `.claude/AGENTS.md` overlay referencing the 3 project agents with model tier and responsibilities

## 2. Token Optimization Configuration (P1)

- [x] 2.1 Create `.claude/optimization.yml` with context_compression section (rtk_enabled, summarization_threshold, compress_tool_outputs)
- [x] 2.2 Add context_pruning section (max_claude_md_lines, max_agent_prompt_words, prune_stale_results)
- [x] 2.3 Add code_chunking section (max_lines_per_read, context_lines, prefer_ast_extraction)
- [x] 2.4 Add retrieval section (max_files_per_query, prefer_repo_map, search_order)
- [x] 2.5 Add caching section (tool_result_ttl_seconds, invalidation_trigger)
- [x] 2.6 Add tool_first section (enforce: true, preferred_tools list)
- [x] 2.7 Create `.claude/repo-map.yml` with entry_points, modules, tests, config_files sections
- [x] 2.8 Add tool-first strategy section to `.claude/CLAUDE.md`

## 3. Release Governance Fix (P0/P1)

- [x] 3.1 Identify correct commits for v1.3.0 and v1.4.0 from CHANGELOG dates and git history
- [x] 3.2 Create annotated git tag `v1.3.0` at the identified commit
- [x] 3.3 Create annotated git tag `v1.4.0` at the identified commit
- [x] 3.4 Fix CHANGELOG.md comparison links: `[1.3.0]` → `compare/v1.2.0...v1.3.0`, `[1.4.0]` → `compare/v1.3.0...v1.4.0`
- [x] 3.5 Create `RELEASING.md` documenting: prerequisites, cz bump usage, tag push, CI publish trigger, rollback
- [x] 3.6 Update `.claude/CLAUDE.roadmap.md` to mark v1.3.0/v1.4.0 as "released (tag pending push)" or remove stale references

## 4. OpenSpec Quality Fix (P1)

- [x] 4.1 Expand `openspec/project.md` with Domain Context section (FFBB APIs, Directus REST, Meilisearch)
- [x] 4.2 Add Important Constraints section to `openspec/project.md` (backward compat, quality gates, Git Flow)
- [x] 4.3 Add External Dependencies section to `openspec/project.md` (FFBB API, PyPI, GitHub Actions)
- [x] 4.4 Add `depends_on` declarations to `openspec/changes/fix-conversion-mismatch-detection/tasks.md`

## 5. Governance Documentation Cleanup (P2)

- [x] 5.1 Add tool-first retrieval workflow documentation to `.claude/CLAUDE.md` (Glob/Grep/Read preference, retrieval order)
- [x] 5.2 Verify all `.claude/checks/CHK-*.md` files are referenced in agent Checks Owned sections (cross-reference validation)
- [x] 5.3 Run `openspec status` to confirm all artifacts are complete
