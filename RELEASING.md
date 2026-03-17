# Release Workflow

## Prerequisites

- All tests passing: `bash scripts/validate-local.sh`
- CI green on `develop` branch
- CHANGELOG.md updated with new version section
- On `develop` branch (or release branch)

## Steps

### 1. Update CHANGELOG

Add a new version section in `CHANGELOG.md` under `[Unreleased]`:

```markdown
## [X.Y.Z] - YYYY-MM-DD
```

Move unreleased items into the new section. Add comparison link at bottom:

```markdown
[X.Y.Z]: https://github.com/Rinzler78/FFBBApiClientV2_Python/compare/vPREV...vX.Y.Z
```

Update `[Unreleased]` link to compare from the new tag.

### 2. Version Bump with Commitizen

```bash
cz bump --dry-run          # preview the version bump
cz bump                     # create version bump commit
```

Commitizen reads `pyproject.toml [tool.commitizen]` and uses `version_provider = "scm"` to derive the next version from git tags and commit history.

### 3. Create Annotated Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z - <brief description>"
```

### 4. Push Tag

```bash
git push origin vX.Y.Z
```

This triggers the CI publish job in `.github/workflows/ci.yml` which:
- Builds the wheel
- Creates a GitHub Release with artifacts
- Publishes to PyPI via twine

### 5. Verify

- Check GitHub Actions: `gh run list --workflow=ci.yml`
- Verify PyPI: `pip install ffbb-api-client-v2==X.Y.Z`
- Verify GitHub Release: `gh release view vX.Y.Z`

## SemVer Rules

| Change Type | Bump | Example |
|-------------|------|---------|
| Breaking API change | MAJOR | Remove public method, change return type |
| New feature (backward compatible) | MINOR | Add endpoint, new model |
| Bug fix | PATCH | Fix parsing, correct field mapping |

## Rollback

If a release has critical issues:

1. **Yank from PyPI** (hides but doesn't delete):
   ```bash
   pip install twine
   twine upload --skip-existing  # re-upload fixed version
   ```

2. **Delete GitHub Release** (if needed):
   ```bash
   gh release delete vX.Y.Z --yes
   git tag -d vX.Y.Z
   git push origin :refs/tags/vX.Y.Z
   ```

3. Create a hotfix branch from the previous tag and follow the normal release flow.
