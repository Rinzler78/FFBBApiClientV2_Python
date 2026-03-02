# Worktree Deliver

Validate, push, and create a PR from the current worktree: $ARGUMENTS

## Instructions

### Step 1: Validate Environment

1. Verify this is a worktree: `git worktree list` (should show multiple entries)
2. Get current branch: `git branch --show-current`
3. Verify branch follows convention (feature/, fix/, hotfix/, chore/, docs/, refactor/)

### Step 2: Review Changes

1. Show all changes: `git diff --stat` and `git status --short`
2. Show commit log since divergence from base: `git log --oneline develop..HEAD`
3. If no changes exist, inform user and stop

### Step 3: Run Validation

Run the mandatory local validation:
```bash
bash scripts/validate-local.sh
```

If validation fails, stop and report the failures. Do not proceed to push.

### Step 4: Stage and Commit (if needed)

If there are uncommitted changes:
1. Show the user what will be committed
2. Ask for confirmation
3. Stage relevant files: `git add <files>`
4. Generate a conventional commit message based on the diff
5. Commit with co-author trailer

### Step 5: Push

```bash
git push -u origin HEAD
```

### Step 6: Create Pull Request

Determine PR target:
- `hotfix/*` branches -> target `master`
- All others -> target `develop`

```bash
gh pr create --base <target> --title "<title>" --body "$(cat <<'EOF'
## Summary
<bullet points from commit messages>

## Validation
- [x] pre-commit passed
- [x] tox tests passed
- [x] gitleaks passed
- [ ] CI checks pending

EOF
)"
```

### Step 7: Output

Display the PR URL and remind the user:
- Wait for CI checks to pass before merging
- After merge, clean up worktree: `git worktree remove .claude/worktrees/<name>`
