# Tool Layer Video Material Manifest

Date: 2026-06-21

## Purpose

`projects/测试/素材/视频` already contained AIGC-content-focused clips. This batch adds tool-layer display material cut directly from `projects/测试/示例`, covering product UI, prompt/script workflow, character and scene generation, editing timeline, export/import, and asset proof screens.

## Inputs

| source | duration | role |
| --- | ---: | --- |
| `projects/测试/示例/微信视频2026-06-20_230344_729.mp4` | 42.28s | tool entry, prompt-to-script, character board/export |
| `projects/测试/示例/微信视频2026-06-20_230409_530.mp4` | 48.50s | dashboard, generation workflow, editing timeline |
| `projects/测试/示例/微信视频2026-06-20_230418_487.mp4` | 60.60s | style/model selection, one-click generation workflow |
| `projects/测试/示例/微信视频2026-06-20_230437_789.mp4` | 52.45s | Jianying import workflow, asset/document proof |

## New Materials

| output | source range | duration | content focus |
| --- | --- | ---: | --- |
| `projects/测试/素材/视频/tool-01-ai-tool-entry.mp4` | `230344_729` 00:06.000-00:12.200 | 6.2s | AI tool entry and visual asset intake |
| `projects/测试/素材/视频/tool-02-prompt-script-workflow.mp4` | `230344_729` 00:12.000-00:18.400 | 6.4s | prompt/script simplification |
| `projects/测试/素材/视频/tool-03-character-board-export.mp4` | `230344_729` 00:24.000-00:31.600 | 7.6s | character board and export action |
| `projects/测试/素材/视频/tool-04-dashboard-generation.mp4` | `230409_530` 00:00.000-00:06.200 | 6.2s | AIGC production dashboard |
| `projects/测试/素材/视频/tool-05-character-scene-generation.mp4` | `230409_530` 00:12.000-00:21.800 | 9.8s | character and scene generation |
| `projects/测试/素材/视频/tool-06-editing-timeline.mp4` | `230409_530` 00:30.000-00:37.400 | 7.4s | editing timeline and post workflow |
| `projects/测试/素材/视频/tool-07-style-model-workflow.mp4` | `230418_487` 00:12.000-00:21.800 | 9.8s | style selection and AI model workflow |
| `projects/测试/素材/视频/tool-08-one-click-generation.mp4` | `230418_487` 00:24.000-00:36.800 | 12.8s | one-click character/location/video generation |
| `projects/测试/素材/视频/tool-09-jianying-import-workflow.mp4` | `230437_789` 00:09.000-00:21.800 | 12.8s | script assets to Jianying import flow |
| `projects/测试/素材/视频/tool-10-asset-proof-interface.mp4` | `230437_789` 00:36.000-00:48.600 | 12.6s | generated assets and supporting document interface |

## Processing

- Output canvas: 1280x720.
- Frame rate: 30 fps.
- Video codec: H.264.
- Audio codec: AAC, source audio retained where present.
- Source files in `projects/测试/示例` were not modified.
- Existing files in `projects/测试/素材/视频` were not modified.

## Verification

| check | result | evidence |
| --- | --- | --- |
| ffprobe media parameters | pass | all new clips report video + audio streams, 1280x720, 30 fps |
| full decode | pass | `ffmpeg -i <clip> -f null -` completed for all 10 clips |
| visual spot check | pass | `projects/测试/结果/auto-edit/edit/tool_material_selection/verify/tool_layer_new_assets_sheet.jpg` |

## Source Sync Check

No source-layer contract, skill, template, script, route, or registry change was needed. This was a project asset augmentation task under the user's explicit instruction to cut tool-layer display material from `projects/测试/示例`.
