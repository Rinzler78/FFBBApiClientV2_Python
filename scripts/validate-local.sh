#!/usr/bin/env bash
set -euo pipefail

echo "[validate-local] Running full local validation..."

if command -v pre-commit >/dev/null 2>&1 && [ -f .pre-commit-config.yaml ]; then
  pre-commit run --all-files --show-diff-on-failure
fi

# Keep local parity with CI for Python projects:
# - ensure project deps are available for system lint/type hooks
# - run tox clean/build when available
# - run tests via tox using built wheel when available
if command -v python >/dev/null 2>&1 && { [ -f pyproject.toml ] || [ -f setup.py ] || [ -f setup.cfg ]; }; then
  python -m pip install -e .
fi

if [ -f tox.ini ] && command -v tox >/dev/null 2>&1; then
  if tox -av 2>/dev/null | grep -Eq '(^|[[:space:]])clean($|[[:space:]])'; then
    if tox -av 2>/dev/null | grep -Eq '(^|[[:space:]])build($|[[:space:]])'; then
      tox -e clean,build
    else
      tox -e clean
    fi
  fi

  wheel_file=""
  if ls dist/*.whl >/dev/null 2>&1; then
    wheel_file="$(ls dist/*.whl 2>/dev/null | head -n 1)"
  fi

  if [ -n "$wheel_file" ]; then
    tox --installpkg "$wheel_file"
  elif tox -av 2>/dev/null | grep -Eq '(^|[[:space:]])py310($|[[:space:]])'; then
    tox -e py310
  elif tox -av 2>/dev/null | grep -Eq '(^|[[:space:]])py($|[[:space:]])'; then
    tox -e py
  else
    tox
  fi
elif [ -f pyproject.toml ] && command -v pytest >/dev/null 2>&1; then
  pytest -q
fi

# Security gate parity with CI (mandatory when CI has security scanning).
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --source . --no-banner --redact
else
  echo "[validate-local] Missing gitleaks in PATH. Install gitleaks to satisfy local/CI security parity." >&2
  exit 1
fi

echo "[validate-local] Validation completed successfully."
