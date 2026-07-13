# Review Contract

## Default Provider

- Default auxiliary provider: local checklist review.
- If a higher-priority policy blocks real render or helper dispatch, report the degradation source and use source-backed manual review.

## Review Dimensions

| dimension | checks |
| --- | --- |
| structure | `SKILL.md` contains runtime spine, node map, peer routing, gates, output contract, and no unresolved scaffold markers |
| directory_routing | `Directory Structure & Detail Routing Contract` covers package tree, detail owners, forbidden use, and real-file sync |
| context_semantics | `CONTEXT/ File Semantics Contract` defines five context files with represents, write_when, must_not_contain, and promotion_signal |
| business_analysis | Business profile defines goal, object, constraints, success criteria, complexity source, and topology fit |
| runtime_spine | Node map can run from source intake to one output or to a plan-only close |
| quantifiable_execution | Scope, evidence count, thresholds, retries, and fallback evidence are explicit |
| attention_governance | Anchors, transfer rules, drift signals, and re-center entries are actionable |
| source_preprocessing | Source material defaults to 1.1x or records an explicit exception; original and derived timestamps are mapped; livestream loop rounds are checked and repeated rounds become `-1/-2/-3` source units rather than an untracked pooled timeline |
| source_derived_guide | When no guide is supplied, derived learning steps are backed by transcript/audio/video evidence before clip selection |
| teaching_shape | Process tutorials preserve a source-supported outcome hook, roadmap, step demos, rationale or parameter notes, repetition-collapse rationale, and final proof |
| dual_output | Full render mode produces optimized long film/full-film unit output(s), a teaching slice series, and required combination-slice evidence; slices are not contextless highlights, are not average-duration/fixed-length chunks, and each contains core explanation, source evidence, necessary context, content-boundary start/end rationale, and a natural ending |
| slice_quantity | Each source unit has a slice opportunity inventory; coherent source-backed slice opportunities are output or entered into combination pools unless excluded with a defensible reason; slice count is not capped by convenience |
| combination_slices | Combination slices use semantic A, B1-B5, and C bands; each B interval has 3-5 viable candidates or a documented reason; random selections or order-preserving recombination choices, seed/selection method, non-repetition, incompatible combinations, and QA are recorded; a linear prerequisite order is not an automatic exemption, and must first be handled as order-preserving recombination unless the user explicitly exempts it or evidence shows recombination is blocked; random selection is no-replacement-first, repeats only after a B pool is exhausted or continuity requires it, repeat counts are balanced and documented, whole B1-B5 paths do not repeat; when viable pools support it, each source unit outputs at least 10 combinations rather than a tiny sample, and long combination outputs are further split into about 10 coherent sequential part slices |
| subtitle_processing | Final long-film and slice subtitles match the final audio timelines, are not raw ASR, have LLM-approved semantic correction/terminology evidence, pass cue order/overlap/duration checks, and are rendered visibly into final MP4s unless an explicit sidecar-only exception is recorded |
| subtitle_display_proofing | Final visible subtitle cues are proofed after semantic correction and final-timeline projection but before rendering; each cue preserves a complete sentence, clause, or natural short phrase; split/merge/time-shift decisions and risky cues are recorded; combination and short-slice subtitles are proofed on the recomposed final timeline; rerender scope is justified as none, affected-only, all-subtitled-videos, or blocked |
| generated_audio | Supplemental audio is used only after source-backed script approval; mmx output is versioned under `projects/素材/`, manifested, aligned, mixed, and QA-sampled |
| subtitle_style | Text overlays are categorized, font/size/contrast/position/safe-area choices follow `Subtitle Style Contract`; default narration captions use visual 100 px at 1080p and scale by `round(100 * output_height / 1080)` for other output heights,米黄色 `#FFF1C7`, high-contrast black outline/shadow, and bottom safe-area placement unless an exact user override or stronger brand rule is recorded; renderer-specific nominal font sizes must be calibrated and recorded with output resolution and computed font size; required narration captions are visible in final MP4s, bottom-aligned, single-line per cue, semantically complete at phrase level, and sampled frames record readability plus any operation/result obstruction risk |
| checkpoints | Scope, semantic, validation, and evaluation checkpoints are defined |
| evaluation_prompts | `test-prompts.json` has 3+ prompt objects with id, prompt, and expected behavior |
| module_triggering | `Module Trigger Matrix` maps task signals and fail codes to authorized module combinations |
| module_authorization | Existing optional modules are declared in `Module Loading Matrix` with load_when, authority, forbidden_use, and rework_target |
| peer_skill_routing | HyperFrames is primary for composition; helper skills are loaded only through the peer routing table |
| types | Type packages support teaching-cut, source-derived-guide, material-audit, render-only, repair-review, and ambiguous-batch modes |
| scripts | Scripts are mechanical only and do not write teaching truth |
| security | Existing source files are read-only; versioned generated supplemental audio under `projects/素材/` is manifested; secrets, mmx credentials, and personal config are not copied; output overwrite is explicit or versioned |
| runtime_behavior | Guardrails, forbidden actions, and escalation protocol are present |
| integration | HyperFrames evidence or documented fallback exists for full render mode; caption-visible optimized long film, content-boundary slice series, corrected subtitle set, and output contract are complete |
| convergence | Final package has one canonical output root and residual risks are named |

## Reference Gate Coverage

Each mandatory `references/` file must expose a `Review Gate Mapping` table and every mapped gate/fail code must resolve here or in `SKILL.md`.

| reference_file | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `references/skill-2.0-package-contract.md` | Reference must remain subordinate to `SKILL.md` | `FAIL-MODULE-DRIFT` | `SKILL.md Module Loading Matrix` | Reference diff and section owner |
| `references/skill-2.0-package-contract.md` | Sibling skills must route through peer matrix | `FAIL-PEER-ROUTING` | `SKILL.md Peer Skill Routing Matrix` | Peer skill load trace |

## Verdict

`pass | pass_with_followups | needs_rework | blocked`
