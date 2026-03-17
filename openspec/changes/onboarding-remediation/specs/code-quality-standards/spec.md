## MODIFIED Requirements

### Requirement: Tool-first retrieval strategy
The project governance documentation SHALL include a tool-first strategy section instructing all agents to prefer dedicated tools (Glob, Grep, Read, Serena) over LLM-based reasoning for code navigation and search tasks.

#### Scenario: CLAUDE.md documents tool-first approach
- **WHEN** an agent needs to find code or read files
- **THEN** the `.claude/CLAUDE.md` governance file SHALL instruct the agent to use Glob for file search, Grep for content search, Read for file reading, and Serena for symbolic navigation before attempting LLM-based approaches

#### Scenario: Retrieval workflow documented
- **WHEN** an agent begins a code investigation task
- **THEN** the governance documentation SHALL specify the retrieval order: repo-map.yml lookup first, then targeted tool use, then broader search only if needed
