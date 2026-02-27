# OpenSpec Instructions

## Workflow
1. Use `openspec list` and `openspec list --specs` to inspect current state.
2. For non-trivial changes, create a proposal under `openspec/changes/<change-id>/`.
3. Validate proposals: `openspec validate <change-id> --strict`.
4. Implement only after approval.
5. Archive completed changes with `openspec archive <change-id> --yes`.
