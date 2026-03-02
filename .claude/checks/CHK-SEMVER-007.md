---
id: CHK-SEMVER-007
type: process
title: "Conventional commits + SemVer"
description: "Verify CHANGELOG follows Keep a Changelog format and tags match SemVer."
enabled: true
default_severity: medium
applies_when:
  stacks: [python]
  paths_exist_any: ["CHANGELOG.md"]
evidence:
  all_of:
    - file: "CHANGELOG.md"
      exists: true
    - file: "CHANGELOG.md"
      contains_all: ["Unreleased", "Added", "Changed"]
recommendations:
  - key: semver_changelog_aligned
    summary: "Ensure latest CHANGELOG entry matches latest git tag"
    source: "AGENTS.md deployment rules"
    target_files: ["CHANGELOG.md"]
validation_criteria:
  required:
    - "Latest CHANGELOG version matches latest annotated git tag"
  ci_expected: []
tags: ["process", "semver", "changelog"]
owner: "project"
version: 1
---

## Intent
Maintain release traceability between CHANGELOG entries and git tags.
