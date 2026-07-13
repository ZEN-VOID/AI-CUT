# Changelog

## 2026-07-08

- Changed the normative default workflow output root to `projects/输出/[任务名]/` so the package matches the repository's Chinese directory convention. User-provided legacy task paths remain accepted as explicit overrides.

## 2026-07-07

- Initialized `workflow` as a Skill 2.0 runtime-spine package.
- Defined the livestream teaching video pipeline: default inputs `projects/素材/` and `projects/内容/`, primary HyperFrames delivery, optional sibling skill routing, and a single task output root.
- Added delivery prompts, review gates, type routing, output template, and package metadata.
- Recorded legacy compatibility: prior reference-rhythm / social-ad workflow semantics are not current defaults and require explicit future migration if needed.
- Added `source-derived-guide` routing: when no teaching-step guide is provided, the workflow derives learning steps from source video/audio understanding, semantically optimizes the teaching order, and requires evidence-backed segment mapping before editing.
- Added target teaching-shape rules from the 2026-07-06 WeChat AI comics tutorial example: outcome hook, roadmap, step demos, rationale/parameter notes, repetition collapse, and final proof are now source-backed planning and QA checks for process tutorials.
- Added `Subtitle Style Contract` for narration captions, chapter titles, step labels, parameter callouts, emphasis keywords, resource notes, and final-proof captions, including font stack, size ranges, safe areas, sampled-frame QA, and `FAIL-SUBTITLE-STYLE`.
- Added `Supplemental Audio Material Contract`: when N3 determines that extra voiceover, subtitle dubbing, or bridge narration is needed, N4 may route to `../cli/mmx-cli/SKILL.md` to synthesize versioned audio under `projects/素材/`, then manifest, align, mix, and QA it with `FAIL-GENERATED-AUDIO`.
- Added `Dual Output Contract`: full render mode must deliver both an optimized coherent long-form teaching film and a coherent teaching slice series under `final/slices/`; slice plans, slice indexes, slice QA, and `FAIL-DUAL-OUTPUT` are now part of the default completion gate.
- Added `Semantic Subtitle Processing Contract`: full render mode must deliver final-audio-matched, semantically corrected subtitles for the long film and every slice; raw ASR is now only intermediate evidence, with subtitle correction plans, timing maps, subtitle QA, and `FAIL-SUBTITLE-PROCESSING` added to the default completion gate.
- Added `Visible Subtitle Rendering Contract`: full render mode must render visible captions into the final long-film MP4 and every slice MP4 by default; `.srt` sidecars remain required evidence but no longer satisfy visible-subtitle delivery by themselves.
- Tightened visible subtitle style: narration captions must be bottom-aligned, match the default or explicitly overridden size, and single-line per cue; long captions must be split into consecutive cue fragments rather than relying on renderer wrapping.
- Added explicit user subtitle-style override handling for subtitle rendering; exact user-specified values such as font size and color must be honored and recorded in style spec, manifest, and QA.
- Tightened slice planning and QA so slice starts/ends must follow teaching content boundaries rather than average duration, fixed chunks, or arbitrary time splits.
- Promoted the user-confirmed visible narration caption default to 100 px at 1080p in the `Subtitle Style Contract`; long text must be split more aggressively and sampled-frame QA must record readability and obstruction risk.
- Added `Source Material Preprocessing Contract`: source material defaults to 1.1x processing with original/derived timestamp mapping, repeated livestream loops must be recognized, and each loop becomes a full-film source unit such as `-1/-2/-3`.
- Added `Combination Slice Utilization Contract`: beyond sequential slices, full render mode now plans A/B1-B5/C combination slices with semantic bands, 3-5 B candidates per interval where viable, controlled random selection, non-repetition tracking, manifest evidence, and QA.
- Added `Slice Quantity Maximization Contract`: every source-unit round must inventory coherent slice opportunities and maximize output quantity under continuity, coherence, source-evidence, and QA gates; omitted viable slices require explicit exclusion rationale.
- Tightened post-run repair defaults from `ai-manju-asset-image-practice`: narration captions now require visual 100 px,米黄色 `#FFF1C7`, high-contrast black outline/shadow, bottom placement, and renderer calibration evidence; combination outputs must not stop at tiny samples such as 3 when 10+ coherent combinations are viable; long combination outputs must also be split into about 10 coherent combination-derived part slices.
- Tightened controlled-random combination selection: B candidates must be selected no-replacement-first, repeated only after a pool is exhausted or continuity requires it, reused with balanced counts, and checked so no full B1-B5 path repeats.
- Tightened narration caption segmentation: visible subtitle cues must preserve semantic sentence/clause/phrase completeness and must not be mechanically cut mid-term or mid-phrase just to satisfy a character limit.
- Added `Subtitle Display Proofing Contract`: final SRT/ASS cues must be proofed as complete visible display units before rendering, display-proofed inputs and subtitle display QA are required evidence, and repair runs must justify rerender scope instead of blindly rerendering all short slices.
- Synchronized narration-caption sizing: 1080p output uses visual 100 px, and other output heights must use `round(100 * output_height / 1080)` with the computed size recorded in style spec, manifest, and sampled-frame QA.
