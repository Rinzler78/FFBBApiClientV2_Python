# Worktree Init

Create a linked worktree for an implementation branch: $ARGUMENTS

## Instructions

### Step 1: Validate Environment

1. Verify git repository: `git rev-parse --is-inside-work-tree`
2. Get repo root: `git rev-parse --show-toplevel`
3. Ensure working tree is clean: `git status --porcelain`
4. Fetch latest: `git fetch origin`

### Step 2: Parse Arguments

Parse the branch description from `$ARGUMENTS`.
If empty, ask the user for a task description.

Determine branch type and name:
- Features: `feature/<kebab-case-name>`
- Bug fixes: `fix/<kebab-case-name>` or `hotfix/<kebab-case-name>`
- Chores: `chore/<kebab-case-name>`
- Docs: `docs/<kebab-case-name>`
- Refactors: `refactor/<kebab-case-name>`

Generate worktree directory path: `.claude/worktrees/<kebab-case-name>`

### Step 3: Determine Base Branch

- Default base: `develop`
- For hotfix branches: base from `master`
- User can override with `--base <branch>`

### Step 4: Create Worktree

```bash
git worktree add -b <branch-name> .claude/worktrees/<name> <base-branch>
```

### Step 5: Output Summary

Display:
```
| Field | Value |
|-------|-------|
| Branch | <branch-name> |
| Worktree | .claude/worktrees/<name> |
| Base | <base-branch> |
```

Remind the user:
- Work in the worktree directory for all changes
- Run `bash scripts/validate-local.sh` before committing
- Use `/worktree-deliver` when ready to push and create PR
- Target PR to `develop` (or `master` for hotfixes)
