You are a focused subagent reviewer for a single holistic investigation batch.

Repository root: /Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python-phase2
Blind packet: /Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python-phase2/.desloppify/review_packet_blind.json
Batch index: 17
Batch name: design_coherence
Batch rationale: design_coherence review

DIMENSION TO EVALUATE:

## design_coherence
Are structural design decisions sound — functions focused, abstractions earned, patterns consistent?
Look for:
- Functions doing too many things — multiple distinct responsibilities in one body
- Parameter lists that should be config/context objects — many related params passed together
- Files accumulating issues across many dimensions — likely mixing unrelated concerns
- Deep nesting that could be flattened with early returns or extraction
- Repeated structural patterns that should be data-driven
Skip:
- Functions that are long but have a single coherent responsibility
- Parameter lists where grouping would obscure meaning — do NOT recommend config/context objects or dependency injection wrappers just to reduce parameter count; only group when the grouping has independent semantic meaning
- Files that are large because their domain is genuinely complex, not because they mix concerns
- Nesting that is inherent to the problem (e.g., recursive tree processing)
- Do NOT recommend extracting callable parameters or injecting dependencies for 'testability' — direct function calls are simpler and preferred unless there is a concrete decoupling need

YOUR TASK: Read the code for this batch's dimension. Judge how well the codebase serves a developer from that perspective. The dimension rubric above defines what good looks like. Cite specific observations that explain your judgment.

Mechanical scan evidence — navigation aid, not scoring evidence:
The blind packet contains `holistic_context.scan_evidence` with aggregated signals from all mechanical detectors — including complexity hotspots, error hotspots, signal density index, boundary violations, and systemic patterns. Use these as starting points for where to look beyond the seed files.

Mechanical concern signals — investigate and adjudicate:
Overview (48 signals):
  design_concern: 20 — docs/conf.py, examples/basketball_dashboard.py, ...
  duplication_design: 14 — scripts/discover_meilisearch_indexes.py, scripts/phase0_enum_rename.py, ...
  mixed_responsibilities: 12 — examples/complete_usage_example.py, examples/conversion_coverage_check.py, ...
  interface_design: 1 — scripts/discover_types.py
  structural_complexity: 1 — src/ffbb_api_client_v2/models/categorie_code.py

For each concern, read the source code and report your verdict in issues[]:
  - Confirm → full issue object with concern_verdict: "confirmed"
  - Dismiss → minimal object: {concern_verdict: "dismissed", concern_fingerprint: "<hash>"}
    (only these 2 fields required — add optional reasoning/concern_type/concern_file)
  - Unsure → skip it (will be re-evaluated next review)

  - [design_concern] docs/conf.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (281 LOC): zero importers, not an entry point
    fingerprint: 48b387d9a5fc9db1
  - [design_concern] examples/basketball_dashboard.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (461 LOC): zero importers, not an entry point
    fingerprint: 25d755cb8b2ae531
  - [design_concern] examples/cross_api_workflows.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (251 LOC): zero importers, not an entry point
    fingerprint: 028bd041bf678bcc
  - [design_concern] examples/quick_start.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (108 LOC): zero importers, not an entry point
    fingerprint: 00a275b48aa141a1
  - [design_concern] examples/team_ranking_analysis.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (234 LOC): zero importers, not an entry point
    fingerprint: f7a2af1628f0ac26
  - [design_concern] scripts/analyze_test_structure.py
    summary: Design signals from smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells
    evidence: [smells] 5x Loose type annotation — use specific types
    fingerprint: 5dbced4acfe5a603
  - [design_concern] scripts/check_from_dict_compliance.py
    summary: Design signals from smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells
    evidence: [smells] 1x sys.exit() outside CLI entry point — use exceptions
    fingerprint: b595b7ce1c28504d
  - [design_concern] scripts/discover_meilisearch_settings.py
    summary: Design signals from signature, smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: signature, smells
    evidence: [signature] 'get_index_settings' has 2 different signatures across 3 files
    fingerprint: b74d3b21b2214f94
  - [design_concern] scripts/phase3_rename.py
    summary: Design signals from smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells
    evidence: [smells] 4x Loose type annotation — use specific types
    fingerprint: 0315bb3ba9ccc1ec
  - [design_concern] scripts/validate_fk_expansion.py
    summary: Design signals from smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells
    evidence: [smells] 1x sys.exit() outside CLI entry point — use exceptions
    fingerprint: 70bf7708610fec95
  - [design_concern] src/ffbb_api_client_v2/_http/client.py
    summary: Design signals from smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells
    evidence: [smells] 1x Catch block that only logs (swallowed error)
    fingerprint: 242bf6bbbe343f14
  - [design_concern] src/ffbb_api_client_v2/directus/client.py
    summary: Design signals from signature, smells
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: signature, smells
    evidence: [signature] 'get_fields' has 2 different signatures across 15 files
    fingerprint: abf3e03f7824a69d
  - [design_concern] src/ffbb_api_client_v2/directus_ffbb/client.py
    summary: Design signals from smells, structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells, structural
    evidence: File size: 1066 lines
    fingerprint: 63ceb3861433bd56
  - [design_concern] src/ffbb_api_client_v2/directus_ffbb/models/get_communes_response.py
    summary: Design signals from signature
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: signature
    evidence: [signature] 'from_dict' has 2 different signatures across 91 files
    fingerprint: e1115246b2d02d6a
  - [design_concern] src/ffbb_api_client_v2/directus_ffbb/models/live.py
    summary: Design signals from smells, structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells, structural
    evidence: File size: 173 lines
    fingerprint: 48907483774570b7
  - [design_concern] src/ffbb_api_client_v2/meilisearch_ffbb/client.py
    summary: Design signals from smells, structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells, structural
    evidence: File size: 945 lines
    fingerprint: a7522fb7134bb6f2
  - [design_concern] src/ffbb_api_client_v2/meilisearch_ffbb/models/competitions_hit.py
    summary: Design signals from smells, structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: smells, structural
    evidence: File size: 268 lines
    fingerprint: 12a9547b8b38a8b3
  - [design_concern] src/ffbb_api_client_v2/meilisearch_ffbb/models/pratiques_hit.py
    summary: Design signals from structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: structural
    evidence: File size: 311 lines
    fingerprint: 1c050e85dabf235b
  - [design_concern] src/ffbb_api_client_v2/models/__init__.py
    summary: Design signals from facade, structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: facade, structural
    evidence: File size: 212 lines
    fingerprint: 0637f71447081ea3
  - [design_concern] src/ffbb_api_client_v2/models/team_ranking.py
    summary: Design signals from dict_keys, structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: dict_keys, structural
    evidence: File size: 110 lines
    fingerprint: 4b769ed679e58d99
  - [duplication_design] scripts/discover_meilisearch_indexes.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication, smells
    evidence: [smells] 1x High cyclomatic complexity (>12 decision points)
    fingerprint: 2ffc9f7f9b6c804e
  - [duplication_design] scripts/phase0_enum_rename.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication, smells
    evidence: [smells] 4x Loose type annotation — use specific types
    fingerprint: 0f52d73ac8737451
  - [duplication_design] src/ffbb_api_client_v2/directus_ffbb/models/get_salles_response.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication
    evidence: [boilerplate_duplication] Boilerplate block repeated across 2 files (window 8 lines): src/ffbb_api_client_v2/directus_ffbb/models/get_salles_response.py:21, src/ffbb_api_client_v2/directus_ffbb/models/get_terrains_response.py:28
    fingerprint: c0f077da3fc62f79
  - [duplication_design] src/ffbb_api_client_v2/directus_ffbb/models/salles_fields.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication
    evidence: [boilerplate_duplication] Boilerplate block repeated across 3 files (window 14 lines): src/ffbb_api_client_v2/directus_ffbb/models/salles_fields.py:43, src/ffbb_api_client_v2/directus_ffbb/models/terrains_fields.py:47, src/ffbb_api_client_v2/directus_ffbb/models/tournois_fields.py:68
    fingerprint: f6353dfb8fce6eab
  - [duplication_design] src/ffbb_api_client_v2/meilisearch_ffbb/models/competitions_multi_search_query.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication, smells
    evidence: [smells] 1x Loose type annotation — use specific types
    fingerprint: 322eae570879f47e
  - [duplication_design] src/ffbb_api_client_v2/meilisearch_ffbb/models/engagements_hit.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication, structural
    evidence: File size: 191 lines
    fingerprint: dfecc06cb0ecce59
  - [duplication_design] src/ffbb_api_client_v2/meilisearch_ffbb/models/formation_session.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication
    evidence: [boilerplate_duplication] Boilerplate block repeated across 2 files (window 10 lines): src/ffbb_api_client_v2/meilisearch_ffbb/models/formation_session.py:37, src/ffbb_api_client_v2/models/offre_pratique.py:26
    fingerprint: c861fc1176a52d9f
  - [duplication_design] src/ffbb_api_client_v2/meilisearch_ffbb/models/rencontres_hit.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Can the nesting be reduced with early returns, guard clauses, or extraction into helper functions? Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication, structural
    evidence: File size: 316 lines
    fingerprint: c8e42c722810d8f2
  - [duplication_design] src/ffbb_api_client_v2/meilisearch_ffbb/models/salles_hit.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication
    evidence: [boilerplate_duplication] Boilerplate block repeated across 2 files (window 8 lines): src/ffbb_api_client_v2/meilisearch_ffbb/models/salles_hit.py:120, src/ffbb_api_client_v2/meilisearch_ffbb/models/terrains_hit.py:109
    fingerprint: 4a030dd95b4c9396
  - [duplication_design] src/ffbb_api_client_v2/meilisearch_ffbb/models/tournois_hit.py
    summary: Duplication pattern — assess if extraction is warranted
    question: Is the duplication worth extracting into a shared utility, or is it intentional variation?
    evidence: Flagged by: boilerplate_duplication, structural
    evidence: File size: 226 lines
    fingerprint: 9c06fc6f415eaf31
  (+18 more — use `desloppify show <detector> --no-budget` to explore)

RELEVANT FINDINGS — explore with CLI:
These detectors found patterns related to this dimension. Explore the findings,
then read the actual source code.

  desloppify show boilerplate_duplication --no-budget      # 24 findings
  desloppify show dict_keys --no-budget      # 2 findings
  desloppify show dupes --no-budget      # 19 findings
  desloppify show facade --no-budget      # 1 findings
  desloppify show global_mutable_config --no-budget      # 1 findings
  desloppify show orphaned --no-budget      # 9 findings
  desloppify show props --no-budget      # 1 findings
  desloppify show responsibility_cohesion --no-budget      # 1 findings
  desloppify show signature --no-budget      # 5 findings
  desloppify show smells --no-budget      # 122 findings
  desloppify show structural --no-budget      # 20 findings
  desloppify show uncalled_functions --no-budget      # 1 findings
  desloppify show unused_enums --no-budget      # 1 findings

Report actionable issues in issues[]. Use concern_verdict and concern_fingerprint
for findings you want to confirm or dismiss.

Phase 1 — Observe:
1. Read the blind packet's `system_prompt` — scoring rules and calibration.
2. Study the dimension rubric (description, look_for, skip).
3. Review the existing characteristics list — which are settled? Which are positive? What needs updating?
4. Explore the codebase freely. Use scan evidence, historical issues, and mechanical findings as navigation aids.
5. Adjudicate mechanical concern signals (confirm/dismiss with fingerprint).
6. Augment the characteristics list via context_updates: positive patterns (positive: true), neutral characteristics, design insights.
7. Collect defects for issues[].
8. Respect scope controls: exclude files/directories marked by `exclude`, `suppress`, or non-production zone overrides.
9. Output a Phase 1 summary: list ALL characteristics for this dimension (existing + new, mark [+] for positive) and all defects collected. This is your consolidated reference for Phase 2.

Phase 2 — Judge (after Phase 1 is complete):
10. Keep issues and scoring scoped to this batch's dimension.
11. Return 0-10 issues for this batch (empty array allowed).
12. For design_coherence, use evidence from `holistic_context.scan_evidence.signal_density` — files where multiple mechanical detectors fired. Investigate what design change would address multiple signals simultaneously. Check `scan_evidence.complexity_hotspots` for files with high responsibility cluster counts.
13. Workflow integrity checks: when reviewing orchestration/queue/review flows,
14. xplicitly look for loop-prone patterns and blind spots:
15. - repeated stale/reopen churn without clear exit criteria or gating,
16. - packet/batch data being generated but dropped before prompt execution,
17. - ranking/triage logic that can starve target-improving work,
18. - reruns happening before existing open review work is drained.
19. If found, propose concrete guardrails and where to implement them.
20. Complete `dimension_judgment`: write dimension_character (synthesizing characteristics and defects) then score_rationale. Set the score LAST.
21. Output context_updates with your Phase 1 observations. Use `add` with a clear header (5-10 words) and description (1-3 sentences focused on WHY, not WHAT). Positive patterns get `positive: true`. New insights can be `settled: true` when confident. Use `settle` to promote existing unsettled insights. Use `remove` for insights no longer true. Omit context_updates if no changes.
22. Do not edit repository files.
23. Return ONLY valid JSON, no markdown fences.

Scope enums:
- impact_scope: "local" | "module" | "subsystem" | "codebase"
- fix_scope: "single_edit" | "multi_file_refactor" | "architectural_change"

Output schema:
{
  "batch": "design_coherence",
  "batch_index": 17,
  "assessments": {"<dimension>": <0-100 with one decimal place>},
  "dimension_notes": {
    "<dimension>": {
      "evidence": ["specific code observations"],
      "impact_scope": "local|module|subsystem|codebase",
      "fix_scope": "single_edit|multi_file_refactor|architectural_change",
      "confidence": "high|medium|low",
      "issues_preventing_higher_score": "required when score >85.0",
      "sub_axes": {"abstraction_leverage": 0-100, "indirection_cost": 0-100, "interface_honesty": 0-100, "delegation_density": 0-100, "definition_directness": 0-100, "type_discipline": 0-100}  // required for abstraction_fitness when evidence supports it; all one decimal place
    }
  },
  "dimension_judgment": {
    "<dimension>": {
      "dimension_character": "2-3 sentences characterizing the overall nature of this dimension, synthesizing both positive characteristics and defects",
      "score_rationale": "2-3 sentences explaining the score, referencing global anchors"
    }  // required for every assessed dimension; do not omit
  },
  "issues": [{
    "dimension": "<dimension>",
    "identifier": "short_id",
    "summary": "one-line defect summary",
    "related_files": ["relative/path.py"],
    "evidence": ["specific code observation"],
    "suggestion": "concrete fix recommendation",
    "confidence": "high|medium|low",
    "impact_scope": "local|module|subsystem|codebase",
    "fix_scope": "single_edit|multi_file_refactor|architectural_change",
    "root_cause_cluster": "optional_cluster_name_when_supported_by_history",
    "concern_verdict": "confirmed|dismissed  // for concern signals only",
    "concern_fingerprint": "abc123  // required when dismissed; copy from signal fingerprint",
    "reasoning": "why dismissed  // optional, for dismissed only"
  }],
  "retrospective": {
    "root_causes": ["optional: concise root-cause hypotheses"],
    "likely_symptoms": ["optional: identifiers that look symptom-level"],
    "possible_false_positives": ["optional: prior concept keys likely mis-scoped"]
  },
  "context_updates": {
    "<dimension>": {
      "add": [{"header": "short label", "description": "why this is the way it is", "settled": true|false, "positive": true|false}],
      "remove": ["header of insight to remove"],
      "settle": ["header of insight to mark as settled"],
      "unsettle": ["header of insight to unsettle"]
    }  // omit context_updates entirely if no changes
  }
}

// context_updates example:
{
  "naming_quality": {
    "add": [
      {
        "header": "Short utility names in base/file_paths.py",
        "description": "rel(), loc() are deliberately terse \u2014 high-frequency helpers where brevity aids readability at call sites. Full names would add noise without improving clarity.",
        "settled": true,
        "positive": true
      }
    ],
    "settle": [
      "Snake case convention"
    ]
  }
}
