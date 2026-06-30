# Scripts

Scripts in `video-to-manifest` are mechanical helpers only.

## `inspect_video_material.py`

Discovers video files, runs `ffprobe`, extracts sample frames, and writes a `material-evidence.json` packet. For videos longer than 60 seconds, it also writes evidence-only `analysis_slices[]` windows by default, each no longer than 60 seconds. It may also write a non-final skeleton YAML with mechanical fields and `needs_llm` placeholders.

For project-standard directories, it records a mechanical `directory_category_hint`:

- `操作展示/` -> `operation_demo`
- `工具使用/` -> `tool_display`
- `影像内容/` -> `aigc_content`

Useful long-material options:

- `--pre-slice-threshold-sec`: duration threshold for generating `analysis_slices[]`; default `60`.
- `--max-analysis-slice-sec`: maximum duration for each analysis slice; default `60`.
- `--slice-sample-count`: minimum sample frames per analysis slice; default `3`.
- `--write-analysis-clips`: additionally write physical proxy clips under `<work_dir>/analysis_clips/`.
- `--analysis-clips-dir`: override the proxy clip output directory.

Physical proxy clips are only generated when explicitly requested. They are written under the work directory, linked back through `analysis_slices[].proxy_clip`, and must not move, overwrite, or replace the original source videos.

It must not author final semantic fields such as `visual_summary`, `semantic_tags`, `semantic_vector`, `trigger_profile`, `visual_signature`, `variation_profile`, `tool_state`, `best_for`, `avoid_for`, or `splice_notes`.

## `validate_video_manifest.py`

Validates `视频说明.yaml` structure, shared workflow fields, media paths, media duration tolerance, segment ranges, directory-category consistency, and category-specific evidence. It returns fatal errors for schema or media contradictions and warnings for quality risks such as missing `operation_state` in `operation_demo` segments, missing `tool_state` in `tool_display` segments, missing `analysis_slices[]` for long videos, shallow `semantic_tags`, or missing workflow batch-diversity fields.

Validation passing means the manifest is structurally consumable by a downstream workflow profile. It does not replace frame-level semantic review, workflow EDL decisions, or workflow `asset_evidence.json` rebuilds.
