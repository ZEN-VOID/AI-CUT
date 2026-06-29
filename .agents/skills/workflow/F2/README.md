# F2

F2 is a HyperFrames-native workflow for F1-style reference-rhythm video creation.

Use F2 when the user wants a script/voiceover/media/reference package turned into a previewable, validated, and finally rendered HyperFrames video, with captions, overlays, PiP, transitions, BGM and final validation handled through `.agents/skills/hyperframes/`.

Default video aspect ratio is `16:9` (`1920x1080`). Use another ratio only when the user explicitly asks for it, a named platform/spec requires it, or the project source of truth has already locked that format.

## Runtime Boundary

- F2 uses Codex/LLM for video understanding, storyboard decisions, subtitle cue review, visual matching and creative judgment.
- F2 uses HyperFrames for composition authoring, media tracks, captions, overlays, animation, preview, validation and render.
- F2 does not depend on F1 scripts, MoviePy, or an ffmpeg filter graph as its primary renderer. It may ingest `workflow/_shared/video-to-manifest` output only as optional source evidence before building F2-native `asset_evidence.json`.

## Directory Tree

```text
F2/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── references/
│   └── f1-to-f2-migration-matrix.md
├── review/
│   └── review-contract.md
├── scripts/
│   ├── README.md
│   └── validate_dialogue_sync.py
├── SKILL.md
├── templates/
│   ├── execution-report.md
│   ├── output-template.md
│   └── prp.md
├── test-prompts.json
└── types/
    ├── default/
    │   └── default.md
    └── type-map.md
```

## Typical Outputs

- `f2_intake.json`
- `asset_evidence.json`
- `dialogue_alignment.json`
- `dialogue_sync_validation.json`
- `reference_rhythm.json`
- `STORYBOARD.md`
- `f2_composition_plan.json`
- HyperFrames project files such as `index.html` and adopted assets
- snapshots / render logs
- `renders/<project-slug>_f2_final.mp4` by default for ordinary F2 tasks
- default final dimensions: `1920x1080` unless an explicit non-16:9 exception is recorded
- `reports/F2-execution-report-YYYYMMDD-HHMM.md`

## Default Paths

- User `result_dir`: `<result_dir>/f2-hyperframes/<project-slug>/`
- AIGC project: `projects/aigc/<项目名>/workflow/F2/<run_id>/`
- No target path: `videos/<project-slug>/`

## Validation

For actual projects, run the HyperFrames checks that apply to the generated project:

```bash
python3 .agents/skills/workflow/F2/scripts/validate_dialogue_sync.py --strict-final <project-root> --write-report <project-root>/dialogue_sync_validation.json
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect
npx hyperframes snapshot
npx hyperframes render
```

Render is required by default for ordinary F2 tasks. Only explicit plan-only, audit-only, asset-evidence-only, no-render requests, or dependency blockers may stop before final MP4, and the report must state the exception.

For dialogue-caption projects, final render cannot pass only on `manual_script_audio_duration`, equal-split timing, or preview cue notes. `dialogue_sync_validation.json` must be pass, or the route returns to `repair_dialogue_timing`.
