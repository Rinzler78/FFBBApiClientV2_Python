## ADDED Requirements

### Requirement: Optimization configuration file
A `.claude/optimization.yml` file SHALL exist containing all 6 optimization sections: context_compression, context_pruning, code_chunking, retrieval, caching, tool_first.

#### Scenario: All optimization sections present
- **WHEN** reading `.claude/optimization.yml`
- **THEN** the file SHALL contain keys for context_compression, context_pruning, code_chunking, retrieval, caching, and tool_first with non-empty values

#### Scenario: Context compression configured
- **WHEN** evaluating optimization_context_compression_config check
- **THEN** the context_compression section SHALL specify rtk_enabled, summarization_threshold, and compress_tool_outputs fields

#### Scenario: Context pruning configured
- **WHEN** evaluating optimization_context_pruning_policy check
- **THEN** the context_pruning section SHALL specify max_claude_md_lines, max_agent_prompt_words, and prune_stale_results fields

#### Scenario: Tool-first strategy configured
- **WHEN** evaluating optimization_tool_first_strategy check
- **THEN** the tool_first section SHALL specify enforce: true and document Glob/Grep/Read preference over LLM search

### Requirement: Repository map file
A `.claude/repo-map.yml` file SHALL exist with navigation anchors for the project's source structure.

#### Scenario: Repo map covers source modules
- **WHEN** reading `.claude/repo-map.yml`
- **THEN** the file SHALL contain entry_points, modules, tests, and config_files sections listing the project's key paths

### Requirement: Tool-first strategy in CLAUDE.md
The `.claude/CLAUDE.md` file SHALL document tool-first retrieval strategy instructing agents to prefer Glob/Grep/Read over LLM-based search.

#### Scenario: CLAUDE.md contains tool-first guidance
- **WHEN** reading `.claude/CLAUDE.md`
- **THEN** a section referencing tool-first strategy SHALL exist with explicit mention of Glob, Grep, and Read tools
