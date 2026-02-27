#!/usr/bin/env bash
set -euo pipefail

echo "[validate-local] Running full local validation..."

if command -v pre-commit >/dev/null 2>&1 && [ -f .pre-commit-config.yaml ]; then
  if command -v python >/dev/null 2>&1 && [ -f setup.cfg ]; then
    python -m pip install -e .
  fi
  pre-commit run --all-files --show-diff-on-failure
fi

if [ -f tox.ini ] && command -v tox >/dev/null 2>&1; then
  if tox -av 2>/dev/null | grep -Eq '(^|[[:space:]])py310($|[[:space:]])'; then
    tox -e py310
  elif tox -av 2>/dev/null | grep -Eq '(^|[[:space:]])py($|[[:space:]])'; then
    tox -e py
  else
    tox
  fi
elif [ -f pyproject.toml ] && command -v pytest >/dev/null 2>&1; then
  pytest -q
fi

echo "[validate-local] Validation completed successfully."
