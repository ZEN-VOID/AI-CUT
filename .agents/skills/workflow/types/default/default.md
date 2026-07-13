# Live Teaching Default Type Package

## Purpose

Provide fixed context for the default `workflow` task: convert long livestream or screen-recorded teaching material into a concise instructional video package aligned with a supplied learning-step guide, or with source-derived learning steps when no guide is provided.

## Match Signals

- Source material is a livestream, lecture, workshop, screen demo, or AIGC creation teaching recording.
- The guide is a step-by-step learning outline, course notes, article draft, or project instruction under `projects/内容/`, or no guide is present and the source material itself must provide the teaching structure.
- The requested output is a clean teaching package: a caption-visible optimized long film plus content-boundary coherent teaching slices with final-audio-matched corrected subtitles, not a viral clip, product promo, plain subtitle job, or average-duration chunking job.
- The source material may be a long livestream that repeats the same teaching loop; repeated loops should be recognized as full-film source units instead of pooled together.

## Fixed Context

- Teaching completeness outranks short-video excitement.
- Source material defaults to `speed=1.1` with original and derived timestamp mapping unless the user explicitly requests original speed or QA rejects the acceleration.
- Repeated livestream rounds become source units named `-1/-2/-3`; each unit can produce its own optimized long film or be documented as partial/combination-only.
- The long film and slice series are both default core deliverables in full render mode.
- For every source unit, slice output quantity should be maximized after coherence, continuity, source evidence, and QA gates pass; viable slice opportunities need output, combination-pool inclusion, or an exclusion rationale.
- Combination slices are a default extension in full render mode: A is the first semantic 20%, C is the final semantic 10%, and the middle 70% is split into B1-B5 with 3-5 candidate clips each for controlled random recombination. Random recombination is no-replacement-first: avoid repeating B candidates until a pool is exhausted, then reuse with balanced counts and no repeated whole B1-B5 path. When viable pools support it, output at least 10 combinations per source unit rather than a tiny sample; long combination outputs are further split into about 10 coherent sequential part slices.
- Semantically corrected and display-proofed subtitles matched to the final long-film and slice audio timelines are default core deliverables in full render mode, and final MP4s show visible bottom-aligned captions by default; narration captions default to visual 100 px at 1080p and scale by `round(100 * output_height / 1080)` for other output heights,米黄色 `#FFF1C7`, high-contrast black outline/shadow, one visual line per cue, and long text split into consecutive semantically complete phrase cues instead of wrapping or mechanically cutting mid-phrase.
- Slices must preserve core explanation, standalone coherence, content-driven starts/ends, and natural closure; they are not contextless highlights or fixed-length chunks.
- Source-backed audio/text and visible demo evidence outrank decorative visuals.
- Raw ASR is evidence, not final subtitle copy; final subtitles need terminology correction, timing validation, display proofing, visible-caption rendering, and residual-risk notes. Subtitle repair starts by proofing cue display and rerender scope; it does not blindly rerender every short slice before affected files are identified.
- Source-derived learning steps must come from transcript, audio semantics, and visible demo evidence; they are not invented curriculum.
- HyperFrames is the preferred final composition route.
- Scripts and sibling skills may process media, but cannot decide teaching truth.

## Replacement Gate

Create a more specific type package only when a recurring subtype has materially different routing or gates, such as multicam class editing, formal certification-course packaging, or multi-output short-clip segmentation.
