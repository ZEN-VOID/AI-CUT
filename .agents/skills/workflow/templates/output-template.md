# Output Template

## Output Contract Alignment

- Required output: one canonical task package containing source preprocessing evidence, caption-visible optimized long teaching video(s) for usable full-film source units, a maximized coherent sequential teaching slice series cut on content boundaries, required A/B1-B5/C combination slices, combination-derived sequential part slices when combination outputs are long, and semantically corrected plus display-proofed subtitles matched to final audio, or a plan-only audit package when rendering is not in scope.
- Output format: `projects/输出/[任务名]/` with phase folders, manifests, QA report, and final report.
- Output path: default `projects/输出/[任务名]/`; user-provided paths, including legacy English-root task paths, are explicit overrides recorded in manifest and report.
- Naming convention: kebab-case or pinyin-safe task slug; optimized long video `final/[任务名].mp4` with visible captions by default; semantically corrected long-video subtitles `final/[任务名].srt`; slice videos `final/slices/[NN]-[slice-slug].mp4` with visible captions by default; semantically corrected slice subtitles use matching `.srt`; slice index `final/slices/index.json` or `final/slices/index.md`; subtitle correction artifacts under `04-assets/subtitles/`; report `final/report.md`; manifest `final/manifest.json`.
- Completion gate: final report names mode, guide mode, paths, preprocessing status, 1.1x policy or exception, round/source-unit map, peer skills, supplied or derived guide coverage, teaching-shape status, generated-audio status when used, subtitle-processing status, subtitle-display-proofing status, rerender scope, subtitle-render mode, subtitle-style status when text overlays exist, visible-caption QA status, source-backed segment map, slice opportunity inventory summary, sequential slice map/index with content-boundary rationale, candidate/output/excluded counts, excluded-slice rationale, combination slice map/index with A/B1-B5/C coverage, random selection evidence, combination output count rationale, combination-derived part-slice index, render or plan-only status, long-film QA result, slice QA result, slice quantity QA result, combination-slice QA result, subtitle QA result, subtitle display QA result, validation status, residual blockers, and exact artifact paths.
- Module trigger evidence: cite the `Module Trigger Matrix` row when internal modules were loaded; write `none` when no optional modules were loaded.
- Business analysis evidence: summarize business_profile and topology_fit status.
- Quant criteria evidence: summarize action_scope, evidence_count, pass_threshold, retry_limit, and fallback_evidence status.
- Attention evidence: summarize attention anchor, drift signals, and any recenter handling.
- Checkpoint evidence: summarize CHK-SCOPE, CHK-SEMANTIC, CHK-VALIDATION, and CHK-DARWIN status.
- Prompt eval evidence: summarize test-prompts ids and eval_mode when evaluation was run.

## Final Output

Use this structure in `final/report.md`:

```markdown
# [任务名]

Mode: teaching-cut | source-derived-guide | material-audit | render-only | repair-review
Guide mode: supplied-guide | source-derived-guide
Output root: projects/输出/[任务名]/
Optimized long video: final/[任务名].mp4 or not rendered in plan-only mode
Slice series: final/slices/ or not rendered in plan-only mode
Combination slices: final/slices/combinations/ or explicit exception

## Source And Guide
- Material:
- Preprocessing: speed=1.1 | original-speed-override | blocked
- Timestamp mapping:
- Round/source units:
- Supplied guide:
- Derived learning steps:
- Generated supplemental audio:
- Peer skills loaded:

## Teaching Coverage
- Covered steps:
- Long-film coverage:
- Slice coverage:
- Slice quantity summary:
- Excluded slice rationale:
- Combination coverage:
- Source gaps:
- Dropped material rationale:

## Combination Slices
- A band:
- B1 candidates:
- B2 candidates:
- B3 candidates:
- B4 candidates:
- B5 candidates:
- C band:
- Random seed:
- Selection manifest:
- Non-repetition status:
- Minimum-repeat policy: no-replacement-first per B pool; repeat only after a pool is exhausted or continuity requires it; include candidate usage counts and confirm no full B1-B5 path repeats.
- Incompatible combinations:
- Combination QA:
- Combination-derived part slices:
- Part-slice index:

## Teaching Shape
- Outcome hook / learner promise:
- Roadmap:
- Step demos:
- Rationale or parameter notes:
- Repetition collapse:
- Final proof:

## Supplemental Audio
- Need / rationale:
- Source-backed voiceover script:
- MMX route:
- Output audio file:
- Generated audio manifest:
- Audio-text alignment:
- Mix decision:
- QA result:

## Subtitle Processing
- Raw subtitle source:
- Timing projection:
- Semantic correction plan:
- Domain glossary / correction table:
- Long-film subtitle:
- Slice subtitles:
- Subtitle QA:
- Residual subtitle risks:

## Subtitle Display Proofing
- Display-proofing status: passed | passed_with_risks | blocked | not_applicable_explicit
- Display-proofing plan:
- Display-proofed subtitle inputs:
- Cue split/merge/time-shift summary:
- Semantic completeness risks:
- Combination/short-slice final-timeline proofing:
- Rerender scope: none | affected-only | all-subtitled-videos | blocked
- Rerender scope rationale:
- Subtitle display QA:

## Subtitle Rendering
- Render mode: burned-in | visible-overlay | sidecar-only-explicit | blocked
- Long-film visible captions:
- Slice visible captions:
- Sampled-frame QA:
- Obstruction/readability notes:
- Sidecar-only exception:

## Subtitle Style
- Output resolution:
- Font stack:
- User style overrides:
- Narration captions: default visual 100 px at 1080p; computed font size is `round(100 * output_height / 1080)` for non-1080p output heights; 米黄色 `#FFF1C7`, high-contrast black outline/shadow unless an exact user override or stronger brand rule is recorded
- Renderer calibration: record output resolution, computed narration-caption size, and nominal renderer settings used to achieve that visual size
- Narration line policy: single-line per cue; long text split into consecutive cues, not renderer-wrapped
- Cue semantic completeness policy: each visible cue preserves a complete sentence, clause, or natural short phrase; no mechanical mid-term or mid-phrase splits
- Bottom position / safe margin:
- Chapter titles:
- Step labels:
- Parameter callouts:
- Emphasis keywords:
- Resource notes:
- Final-proof captions:
- Readability / overlap QA:
- Spec artifact:

## Artifacts
- Source manifest:
- Source preprocess plan:
- Round/source-unit map:
- Teaching cut plan:
- Slice opportunity inventory:
- Slice plan:
- Excluded slice rationale:
- Combination slice plan:
- Combination slice manifest:
- Subtitle correction plan:
- Subtitle timing map:
- Subtitle display-proofing plan:
- Subtitle display QA:
- Visible-caption QA:
- Voiceover script:
- Generated audio manifest:
- Subtitle style spec:
- Asset manifest:
- HyperFrames composition:
- QA report:
- Final manifest:

## Validation
- Render status:
- Long-film QA status:
- Slice QA status:
- Slice quantity QA status:
- Combination-slice QA status:
- Subtitle QA status:
- Visible-caption QA status:
- Prompt eval mode:
- Residual blockers:
```

## Evidence

Every selected long-film segment should include source file, source unit id, original start/end, 1.1x derived start/end or exception, supplied or derived guide step id, segment role, transcript excerpt or approved voiceover text, final subtitle cue evidence, and visual rationale. Every sequential slice should include title, learning goal, source ranges, covered guide steps, core explanation, necessary context, independent-coherence rationale, content-boundary start/end rationale, natural ending, and matching subtitle path. Every source unit should include candidate_count, sequential_output_count, combination_candidate_count, combination_output_count, excluded_count, and excluded-slice rationale so the report can show quantity was maximized under coherence constraints. Every combination slice should include A range, selected B1-B5 candidate ids, C range, random seed, non-repetition status, compatibility rationale, source evidence, and matching subtitle path. Segment role should use one of: `outcome-hook`, `roadmap`, `step-demo`, `rationale`, `parameter-note`, `repetition-collapse`, `resource-note`, `final-proof`, or `bridge`. Any generated supplemental audio on the segment or slice should cite source backing, generated audio path, alignment timing, and mix decision. Any final subtitle set should cite raw source, timing projection, semantic correction method, display-proofing status, rerender scope, domain glossary, sample fixes, subtitle render mode, visible-caption QA, subtitle display QA, and subtitle QA status. Any caption or text overlay on the segment or slice should cite one subtitle category from `Subtitle Style Contract` and note whether it passed sampled-frame visibility, readability, and overlap QA.

## Review Result

`pass | pass_with_followups | needs_rework | blocked`
