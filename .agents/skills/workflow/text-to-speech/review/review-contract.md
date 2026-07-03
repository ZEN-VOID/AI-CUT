# Review Contract

## Default Provider

- Default auxiliary provider: `code-reviewer`
- If higher-priority policy blocks real dispatch, report the degradation source and use local checklist review.

## Review Dimensions

| dimension | checks |
| --- | --- |
| structure | Package tree matches `SKILL.md` `Directory Structure & Detail Routing Contract`; no hidden runtime rule lives outside authorized modules |
| directory_routing | `Directory Structure & Detail Routing Contract` covers package tree, detail owners, forbidden use, and real-file sync |
| context_semantics | `CONTEXT/ File Semantics Contract` defines five context files with represents, write_when, must_not_contain, and promotion_signal |
| business_analysis | `Business Requirement Analysis Contract` defines business_goal, business_object, constraint_profile, success_criteria, complexity_source, and topology_fit |
| runtime_spine | `SKILL.md` can independently run the task through input, type routing, thinking-action nodes, gates, and output |
| quantifiable_execution | execution rules affecting scope, evidence, thresholds, retries, or stop conditions are quantifiable or have fallback evidence |
| attention_governance | attention anchors, transfer rules, drift signals, and re-center entries are defined and actionable |
| checkpoints | high-impact, semantic, validation, and Darwin evaluation checkpoints are defined |
| evaluation_prompts | `test-prompts.json` has 3+ prompt objects with id, prompt, and expected |
| module_triggering | `Module Trigger Matrix` maps task signals and `FAIL-*` codes to authorized module combinations, load phases, and return gates |
| module_authorization | existing optional modules are declared in `Module Loading Matrix` with load_when, authority, forbidden_use, and rework_target |
| types | type packages, selection signals, `type_profile`, and knowledge-base boundary |
| scripts | `scripts/generate_missing_audio.py` exposes dry-run, scoped generation, overwrite guard, balanced voice assignment, title filtering, and manifest output |
| security | No API key is committed or echoed; local mmx path is preferred; source copy files are read-only; existing nonempty audio is protected by default |
| runtime_behavior | Guardrails cover auth/quota/rate-limit stop conditions, retry ceiling, empty-text rejection, and no global mmx installation |
| integration | Script dry-run, Python compile, Skill 2.0 validation, and package smoke test must pass before delivery |
| convergence | Done means missing targets are either generated as nonempty same-stem MP3s or explicitly reported with owner and residual risk |

## Reference Gate Coverage

Each mandatory `references/` file must expose a `Review Gate Mapping` table and every mapped gate/fail code must resolve here or in a more specific review contract.

| reference_file | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `references/skill-2.0-package-contract.md` | Default paths, local mmx path, overwrite guard, title filtering, balanced voices, and manifest ownership remain aligned with `SKILL.md` | `FAIL-PACKAGE-CONTRACT` | `SKILL.md` Core Task Contract / `scripts/generate_missing_audio.py` | package audit, script argument audit, dry-run manifest plan |

## Runtime Review Checklist

| question | pass condition | fail_code | rework_target |
| --- | --- | --- | --- |
| Are text and audio matched only by identical stem? | Every `文案<N>.txt` maps to `文案<N>.mp3` in the audio directory | `FAIL-NAMING-MISMATCH` | `N2-SCAN` |
| Are existing nonempty MP3 files preserved? | Generation plan excludes them unless `--overwrite` is explicit | `FAIL-OVERWRITE-RISK` | `N2-SCAN` |
| Is the bracket title ignored only for TTS input? | First standalone `【...】` line is stripped from temp input and source file is unchanged | `FAIL-TITLE-FILTER` | `N3-PLAN` |
| Are the three BeiYin voices balanced in batch mode? | Voice counts differ by no more than one | `FAIL-VOICE-DISTRIBUTION` | `N3-PLAN` |
| Is the local MiniMax CLI used? | CLI path resolves under `.agents/skills/cli/mmx-cli` | `FAIL-MMX-LOCALITY` | `N1-INTAKE` |
| Are generated audio files usable? | Every generated output exists and has size greater than zero | `FAIL-AUDIO-EMPTY` | `N4-GENERATE` |
| Are secrets kept out of durable artifacts? | `SKILL.md`, scripts, README, manifests, and reports contain no real `sk-` key | `FAIL-SECRET-LEAK` | `N5-CLOSE` |

## Verdict

`pass | pass_with_followups | needs_rework | blocked`
