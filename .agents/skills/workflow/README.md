# Workflow

Workflow is a HyperFrames-native workflow for legacy F1/F2-style reference-rhythm video creation.

Use workflow when the user wants a script/voiceover/media/reference package turned into a previewable, validated, and finally rendered HyperFrames video, with captions, overlays, PiP, transitions, BGM and final validation handled through `.agents/skills/hyperframes/`.

Default video aspect ratio is `16:9` (`1920x1080`). Use another ratio only when the user explicitly asks for it, a named platform/spec requires it, or the project source of truth has already locked that format.

## Runtime Boundary

- workflow uses Codex/LLM for video understanding, storyboard decisions, subtitle cue review, visual matching and creative judgment.
- workflow uses HyperFrames for composition authoring, media tracks, captions, overlays, animation, preview, validation and render.
- workflow does not depend on F1 scripts, MoviePy, or an ffmpeg filter graph as its primary renderer. It may ingest `workflow/video-to-manifest` output only as optional source evidence before building workflow-native `asset_evidence.json`.

## Directory Tree

```text
workflow/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT/
│   ├── 重要记忆.md
│   ├── 负向经验.md
│   ├── 正向经验.md
│   ├── 好的示例.md
│   └── 坏的示例.md
├── README.md
├── references/
│   └── legacy-migration-matrix.md
├── review/
│   └── review-contract.md
├── scripts/
│   ├── README.md
│   ├── update_asset_usage_monitor.py
│   ├── validate_dialogue_sync.py
│   └── validate_visual_contract.py
├── SKILL.md
├── templates/
│   ├── execution-report.md
│   ├── output-template.md
│   └── prp.md
├── test-prompts.json
├── types/
    ├── default/
    │   └── default.md
    └── type-map.md
└── video-to-manifest/
    ├── agents/
    │   └── openai.yaml
    ├── CHANGELOG.md
    ├── CONTEXT.md
    ├── README.md
    ├── SKILL.md
    ├── scripts/
    │   ├── README.md
    │   ├── inspect_video_material.py
    │   └── validate_video_manifest.py
    ├── templates/
    │   ├── manifest-template.yaml
    │   └── output-template.md
    └── test-prompts.json
```

Runtime experience and reusable lessons live in the five-file `CONTEXT/` structure required by Skill 2.0:

- `重要记忆.md`: durable boundaries, Context Health and writeback policy.
- `负向经验.md`: failure modes, root causes and repair playbook.
- `正向经验.md`: reusable heuristics and successful patterns.
- `好的示例.md`: short examples that can be copied as execution patterns.
- `坏的示例.md`: counterexamples tied to fail codes.

## Typical Outputs

- `workflow_intake.json`
- `asset_evidence.json`
- `projects/素材使用监控.csv` as the global four-column material usage monitor
- `dialogue_alignment.json`
- `dialogue_sync_validation.json`
- `reference_rhythm.json`
- `STORYBOARD.md`
- `workflow_composition_plan.json`
- HyperFrames project files such as `index.html` and adopted assets
- snapshots / render logs
- `<work-root>/renders/<project-slug>_workflow_final.mp4` for single workflow tasks
- `projects/output/<日期>/<project-slug>_workflow_final.mp4` as the canonical final path for single workflow tasks
- `projects/output/<日期>/成片/<project-slug>_workflow_final.mp4` as the canonical final collection path for batch tasks
- default final dimensions: `1920x1080` unless an explicit non-16:9 exception is recorded
- `reports/workflow-execution-report-YYYYMMDD-HHMM.md`

## Default Paths

- No target path: `projects/output/<日期>/过程/<project-slug>/`
- Single final path: `projects/output/<日期>/<project-slug>_workflow_final.mp4`
- Batch work root: `projects/output/<日期>/过程/<batch-id>/`
- Batch final collection: `projects/output/<日期>/成片/`
- User `result_dir`: process files under `<result_dir>/<日期>/过程/<project-slug>/` or `<result_dir>/<日期>/过程/<batch-id>/`; final files under `<result_dir>/<日期>/` or `<result_dir>/<日期>/成片/`
- Shared cumulative assets: `projects/素材/` and `projects/示例/` are read-only source pools, not daily output roots.

## Shared Asset Taxonomy

`projects/素材/` may contain preprocessing folders that guide later material filling and workflow selection:

- Visual material branches: `开头素材/`, `收益素材/`, `漫剧素材/`, `大字报/`, `工作流素材/`, `引流素材/`, `资产图/`, `转场素材/`
- Keyword branch: `核心关键词/`
- Legacy raw inputs: historical raw pools should live under `旧/` or another explicitly marked archive.

Empty taxonomy folders are placeholders only. workflow must still use real files, manifests and visual evidence before selecting assets.

`projects/内容/` contains the current content truth and audio-clock pools:

- `文案/` for batch `.txt` scripts.
- `音频/` for same-stem voiceover audio; `BGM.*` under `音频/` is only a background music candidate.

When both `projects/内容/文案/文案N.txt` and `projects/内容/音频/文案N.mp3` exist, workflow should treat the shared stem as the stable batch item key and must not randomly cross-pair scripts and audio.

`projects/素材使用监控.csv` is the global usage monitor for shared material pools. It must keep exactly four columns: `素材名`, `文件路径`, `使用次数`, `使用程度`; `使用程度` is either `全片` or `部分切片`. Detailed per-output segment evidence stays in `asset_usage_ledger.json`; the CSV is updated only after a local final MP4 has passed verification.

## Layered Assembly Model

workflow videos should be planned as a rhythm structure before assets are placed. For social ads, viral openings and batch videos, the default structure is:

- `hook_opening`: viral opening material that establishes the first 3-5 seconds.
- `content_body`: the main content, with comic-drama, tool/workflow and revenue/proof material all covered or explicitly marked unavailable.
- `private_traffic_cta`: private-domain or next-action traffic segment.

Each segment must declare four visual layers in `workflow_composition_plan.json`:

- `background_video`: a continuous background throughline, usually from `projects/素材/漫剧素材/纯漫剧素材/`, with `mask: none` and `opacity: 1`.
- `semantic_pip`: cue-bound picture-in-picture evidence matched to the script.
- `dialogue_caption`: subtitle cues following the script/audio clock.
- `editorial_overlay`: one core word or short sentence summarizing the segment.

The plan should expose `background_throughline` and `timeline_segments` so `validate_visual_contract.py --strict-social-ad` can check that the video is not just random script-driven asset rotation.

## Validation

For actual projects, run the HyperFrames checks that apply to the generated project:

```bash
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final <project-root> --write-report <project-root>/dialogue_sync_validation.json
python3 .agents/skills/workflow/scripts/validate_visual_contract.py <project-root> --write-report <project-root>/visual_contract_validation.json
python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py <batch-or-output-root>
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect
npx hyperframes snapshot
npx hyperframes render
```

Render is required by default for ordinary workflow tasks. Only explicit plan-only, audit-only, asset-evidence-only, no-render requests, or dependency blockers may stop before final MP4, and the report must state the exception.
Browser/page preview is not a final output; ordinary workflow tasks must produce a local canonical MP4 under the configured output root.

For dialogue-caption projects, final render cannot pass only on `manual_script_audio_duration`, equal-split timing, preview cue notes, or visually plausible but shuffled subtitle text. `dialogue_sync_validation.json` must be pass, including cue timing, sortable script order, per-cue audio anchors, and HTML `data-cue-id` / timing / text alignment, or the route returns to `repair_dialogue_timing`.
For current `projects/内容/文案/` + `projects/内容/音频/` routes, run the dialogue validator with `--require-script-audio-pair` and record `source_script`, `source_audio`, and the shared stem.
