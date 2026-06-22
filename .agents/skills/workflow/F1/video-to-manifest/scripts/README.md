# Scripts

Scripts in `video-to-manifest` are mechanical helpers only.

## `inspect_video_material.py`

Discovers video files, runs `ffprobe`, extracts sample frames, and writes a `material-evidence.json` packet. It may also write a non-final skeleton YAML with mechanical fields and `needs_llm` placeholders.

For project-standard directories, it records a mechanical `directory_category_hint`:

- `操作展示/` -> `operation_demo`
- `工具使用/` -> `tool_display`
- `影像内容/` -> `aigc_content`

It must not author final semantic fields such as `visual_summary`, `semantic_tags`, `tool_state`, `best_for`, `avoid_for`, or `splice_notes`.

## `validate_video_manifest.py`

Validates `视频说明.yaml` structure, required F1 fields, media paths, media duration tolerance, segment ranges, directory-category consistency, and category-specific evidence. It returns fatal errors for schema or media contradictions and warnings for quality risks such as missing `operation_state` in `operation_demo` segments or missing `tool_state` in `tool_display` segments.

Validation passing means the manifest is structurally consumable by F1. It does not replace frame-level semantic review.
