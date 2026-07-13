# Workflow

`workflow` is a Skill 2.0 package for turning livestream teaching material into concise, source-backed instructional video packages.

Default inputs:

- Video material: `projects/素材/`
- Optional learning-step guide, course notes, or brief: `projects/内容/`
- Output: `projects/输出/[任务名]/`

When no guide is provided, the workflow derives learning steps from the source video/audio transcript and visual teaching evidence before selecting clips.

Source material is preprocessed by default:

- live footage uses `speed=1.1` unless explicitly overridden or QA rejects acceleration
- original and derived timestamps remain mapped for evidence, subtitles, and QA
- repeated livestream loops are recognized as full-film source units such as `-1`, `-2`, and `-3`

Core rendered output includes long-form and slice deliverables by default:

- one optimized coherent long-form teaching film with unnecessary pauses, blanks, livestream chatter, repetition, and off-topic material removed
- one maximized coherent teaching slice series under `final/slices/`, where every viable source-backed slice opportunity is output or justified as excluded, and each slice is cut on content boundaries and preserves the core explanation, necessary context, source evidence, and a natural ending
- one combination slice extension under `final/slices/combinations/` when not explicitly exempted: A is the stable first 20%, C is the stable final 10%, B1-B5 are middle intervals with controlled random candidate selection for non-repetitive reuse; random selection is no-replacement-first and only reuses candidates with balanced counts after a pool is exhausted or continuity requires it; when the candidate pool supports it, output at least 10 combinations per source unit and split each long combination into about 10 coherent combination-derived part slices

Final subtitle output is also required by default:

- one semantically corrected long-film SRT matched to the final long-film audio timeline
- matching semantically corrected SRT sidecars for every rendered slice
- display-proofed final cue inputs before visible rendering, so each on-screen subtitle is a complete sentence, clause, or natural short phrase and repair runs record whether rerendering is unnecessary, affected-only, all subtitled videos, or blocked
- visible captions rendered into the final long-film MP4 and every rendered slice MP4, unless the user explicitly asks for sidecar-only output
- subtitle correction artifacts under `04-assets/subtitles/`, including raw subtitle source, timing projection, terminology/correction plan, and subtitle QA evidence

HyperFrames is the primary composition and render route. `video-editing-skill`, `wis`, and `wangjianshuo-perspective` are sibling capabilities loaded only through the peer routing rules in `SKILL.md`.

When the teaching plan needs extra voiceover, subtitle dubbing, or bridge narration, the workflow can load `cli/mmx-cli` to synthesize approved source-backed text into versioned audio files under `projects/素材/`, then use those files as traceable edit assets.

## Directory Tree

```text
workflow/
├── agents/
│   └── openai.yaml
├── CONTEXT/
│   ├── 好的示例.md
│   ├── 坏的示例.md
│   ├── 正向经验.md
│   ├── 负向经验.md
│   └── 重要记忆.md
├── references/
│   └── skill-2.0-package-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── types/
│   ├── type-map.md
│   └── default/
│       └── default.md
├── CHANGELOG.md
├── SKILL.md
├── test-prompts.json
└── README.md
```

## Usage

Invoke `$workflow` when the task is to understand long teaching footage, preprocess it with traceable 1.1x timing, split repeated livestream rounds into source units when present, align it to a supplied course or learning-step guide when available, derive a source-backed teaching outline when it is not available, extract the useful visual/audio moments, and deliver a clean caption-visible teaching long film plus maximized coherent content-boundary teaching slices and A/B1-B5/C combination slices with final-audio-matched corrected subtitles, or a source-backed edit plan when rendering is not in scope.

For process tutorials, the default target shape is result or learner promise, roadmap, step demos, rationale or parameter notes, collapsed repetition, and final proof when source evidence supports those parts.

Generated supplemental audio follows the `Supplemental Audio Material Contract` in `SKILL.md`: the script is LLM-authored from source evidence first, `mmx-cli` only synthesizes the approved text, and the generated audio must be manifested, aligned, mixed, and QA-sampled.

Subtitles and text overlays follow the `Subtitle Style Contract` and `Visible Subtitle Rendering Contract` in `SKILL.md`: narration captions, chapter titles, step labels, parameter callouts, emphasis keywords, resource notes, and final-proof captions are separate categories with fixed font, size, contrast, safe-area, and QA requirements; final MP4s must show visible bottom-aligned narration captions by default at visual 100 px for 1080p output, scaled proportionally as `round(100 * output_height / 1080)` for non-1080p output heights,米黄色 `#FFF1C7`, high-contrast black outline/shadow, with one visual line per cue and long text split into short consecutive semantically complete phrase cues instead of auto-wrapped or mechanically cut mid-phrase.

Subtitle text follows the `Semantic Subtitle Processing Contract` and `Subtitle Display Proofing Contract` in `SKILL.md`: raw ASR is only intermediate evidence; final `.srt` files must be projected to the rendered audio timeline, semantically corrected with source-backed terminology, display-proofed for complete visible cue phrases before rendering, rendered visibly into final MP4s by default, and QA-checked for cue order, overlap, duration, display completeness, visibility, and high-risk term drift.

The runtime truth is `SKILL.md`. README is only a quick entry and directory summary.

## Runtime Spine

- `SKILL.md` owns input routing, business profile, type routing, node map, peer skill routing, review gates, and output contract.
- `CONTEXT/` stores reusable examples and learning only; it does not redefine rules.
- `types/`, `references/`, `review/`, `templates/`, and `scripts/` are authorized detail modules and cannot replace `SKILL.md`.
- Final task artifacts belong under `projects/输出/[任务名]/` by default. User-provided legacy task paths are treated as explicit overrides, not as the current default.
