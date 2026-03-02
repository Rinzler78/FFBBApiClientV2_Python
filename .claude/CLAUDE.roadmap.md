# Release Management Roadmap

Pending tag and release tasks that must be performed on `master` by a maintainer.

## Missing Annotated Tags

Tags v1.3.0 and v1.4.0 were never created. They must be created as annotated tags on the correct merge commits in `master`.

```bash
# After merging the release containing v1.3.0 changes:
git checkout master
git log --oneline  # identify the correct commit
git tag -a v1.3.0 <commit-sha> -m "Release v1.3.0"
git push origin v1.3.0

# Same for v1.4.0:
git tag -a v1.4.0 <commit-sha> -m "Release v1.4.0"
git push origin v1.4.0
```

Once tags exist, update CHANGELOG.md comparison links:
- `[1.4.0]` -> `compare/v1.3.0...v1.4.0`
- `[1.3.0]` -> `compare/v1.2.0...v1.3.0`
- `[Unreleased]` -> `compare/v1.4.0...HEAD`

## Lightweight Tag v1.1.1

Tag `v1.1.1` is lightweight (no annotation). Converting to annotated requires deleting and recreating, which may break existing clones. Evaluate risk before proceeding:

```bash
git tag -d v1.1.1
git push origin :refs/tags/v1.1.1
git tag -a v1.1.1 <commit-sha> -m "Release v1.1.1"
git push origin v1.1.1
```

## Non-SemVer Tags

Legacy tags with 4 segments (`v0.0.0.2`, `v1.0.0.1`, etc.) do not conform to SemVer. They are historical and should not be removed, but new releases must use strict 3-segment format (`vMAJOR.MINOR.PATCH`).

## Future Improvements (Separate PRs)

| Item | Priority | Notes |
|------|----------|-------|
| OIDC trusted publishing for PyPI | High | Replaces PYPI_TOKEN secret with keyless auth |
| Expand test matrix (3.11, 3.12) | Medium | Currently only 3.10 in CI |
| Migrate Sphinx to MkDocs | Low | Large effort, evaluate ROI first |
