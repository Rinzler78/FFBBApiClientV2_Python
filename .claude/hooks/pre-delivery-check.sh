#!/usr/bin/env bash
set -euo pipefail

if [ -x "scripts/validate-local.sh" ]; then
  bash scripts/validate-local.sh
else
  echo "[pre-delivery-check] Missing scripts/validate-local.sh" >&2
  exit 1
fi
