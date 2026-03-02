---
id: CHK-TESTS-003
type: quality
title: "Unit tests + coverage"
description: "Verify pytest runs with branch coverage via tox."
enabled: true
default_severity: high
applies_when:
  stacks: [python]
  paths_exist_any: ["tox.ini", "pyproject.toml"]
evidence:
  all_of:
    - file: "tox.ini"
      exists: true
    - file: "tox.ini"
      contains_all: ["pytest", "--cov", "--cov-branch"]
    - file: "pytest.ini"
      contains_all: ["testpaths"]
recommendations:
  - key: test_coverage_enforced
    summary: "Ensure tox runs pytest with branch coverage on src/ffbb_api_client_v2. Test config lives in pytest.ini (canonical source)."
    source: "AGENTS.md testing rules"
    target_files: ["tox.ini", "pytest.ini"]
validation_criteria:
  required:
    - "tox -e py310 exits 0 with branch coverage reported"
  ci_expected:
    - "test"
tags: ["quality", "testing", "coverage", "python"]
owner: "project"
version: 2
---

## Intent
Ensure automated tests with branch coverage are enforced for all code changes.
