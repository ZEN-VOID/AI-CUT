# Output Template

## Output Contract Alignment

| Field | Contract |
| --- | --- |
| Required output | project UUID, upload registry, YAML backfill, video node list, runtime image map |
| Output format | JSON manifests, JSON submit plans, JSON queue records, Markdown reports |
| Output path | `projects/aigc/<项目名>/8-视频/libTV画布流/第N集/` |
| Naming convention | `<group_id>-subject-reference-manifest.json`, `<group_id>-libtv-submit-plan.json`, `<group_id>-queue-record.json`, `<group_id>-执行报告.md` |
| Completion gate | final remote query verifies `imageList` order, prompt hygiene and no unauthorized run |

## Queue Record Fields

```json
{
  "projectUuid": "",
  "canvas_project_name": "",
  "source_file": "",
  "group_id": "",
  "video_node_key": "",
  "model": "star-video2",
  "modeType": "mixed2video",
  "ratio": "16:9",
  "resolution": "720p",
  "duration": 15,
  "subject_bindings": [],
  "runtime_image_placeholder_map": [],
  "queried_runtime_image_map_verified": false,
  "run_executed": false,
  "queue_status": "video_node_created_not_run"
}
```
