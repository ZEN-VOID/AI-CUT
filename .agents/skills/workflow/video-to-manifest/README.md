# Video To Manifest

`video-to-manifest` 是 workflow 共享卫星技能，用于从指定视频或视频目录生成、更新、修复或校验 workflow 等视频工作流可消费的 `视频说明.yaml`。

## Directory Tree

```text
video-to-manifest/
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── inspect_video_material.py
│   ├── validate_video_manifest.py
│   └── README.md
├── templates/
│   ├── manifest-template.yaml
│   └── output-template.md
├── CHANGELOG.md
└── README.md
```

## Quick Use

Use `$video-to-manifest` when the user wants to:

- generate `视频说明.yaml` for one video;
- update a directory-level `视频说明.yaml`;
- repair a manifest that a downstream workflow cannot consume;
- validate an existing manifest before workflow asset-evidence ingestion.

The runtime spine is in `SKILL.md`. Scripts only do mechanical media inspection, frame extraction, skeleton support, and YAML validation. Video semantics, tags, tool screen state, subtitle-safe-zone judgment, and final segment selection must be authored by LLM/operator observation from evidence. The default semantic pass is 逐视频精读: every written video needs per-video visual evidence and observation notes; directory-level overview sheets are only intake aids.

Project-standard video directories map to shared material categories:

- `操作展示/` -> `operation_demo`
- `工具使用/` -> `tool_display`
- `影像内容/` -> `aigc_content`

`operation_demo` requires operation/action-state evidence, `tool_display` requires screen-state evidence, and `aigc_content` requires semantic/visual rhythm evidence for downstream selection. Workflow may use the manifest only as optional input evidence before rebuilding `asset_evidence.json`.

## Helper Commands

```bash
python3 scripts/inspect_video_material.py <video-or-dir> --work-dir <work-dir>
python3 scripts/validate_video_manifest.py <path/to/视频说明.yaml> --report <work-dir>/video-manifest-validation.json
```

Default output is one canonical `视频说明.yaml` in the source video directory unless the user provides another `manifest_path`.
