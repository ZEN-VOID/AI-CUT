# Output Template

## Output Contract Alignment

| Field | Contract |
| --- | --- |
| Required output | local AIGC mapping, projectSpace/folder evidence, canvas UUID/projectUuid, upload registry, YAML backfill, video node list, runtime image map |
| Output format | JSON manifests, JSON submit plans, JSON queue records, Markdown reports |
| Output path | `projects/aigc/<项目名>/13-画布/libTV画布流/第N集/` |
| Naming convention | `<video_node_instance_id>-subject-reference-manifest.json`, `<video_node_instance_id>-libtv-submit-plan.json`, `<video_node_instance_id>-queue-record.json`, `<video_node_instance_id>-执行报告.md`; `source_group_id` 只写入内容和 registry，不单独作为唯一文件名前缀 |
| Completion gate | final remote query verifies `imageList` order, prompt hygiene and no unauthorized run |

## Queue Record Fields

```json
{
  "local_project_root": "projects/aigc/<项目名>",
  "local_episode": "第N集",
  "local_episode_scope": "projects/aigc/<项目名>/第N集",
  "source_file": "projects/aigc/<项目名>/10-分组/第N集.md",
  "evidence_dir": "projects/aigc/<项目名>/13-画布/libTV画布流/第N集",
  "projectSpaceId": null,
  "folderId": null,
  "project_space_name": "",
  "project_space_resolution": "resolved_from_project_list",
  "projectUuid": "",
  "canvas_name": "",
  "source_group_id": "",
  "video_node_instance_id": "vid__1-1-1__b001__r00__v001",
  "parent_video_node_instance_id": null,
  "batch_no": "b001",
  "revision_no": "r00",
  "variant_no": "v001",
  "operation": "initial_batch",
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

## Active Registry Shape

```json
{
  "local_project_root": "projects/aigc/<项目名>",
  "local_episode": "第N集",
  "local_episode_scope": "projects/aigc/<项目名>/第N集",
  "source_file": "projects/aigc/<项目名>/10-分组/第N集.md",
  "evidence_dir": "projects/aigc/<项目名>/13-画布/libTV画布流/第N集",
  "projectSpaceId": null,
  "folderId": null,
  "project_space_name": "",
  "project_space_resolution": "resolved_from_project_list",
  "projectUuid": "",
  "canvas_name": "",
  "groups": {
    "1-1-1": {
      "source_group_id": "1-1-1",
      "active_instance_id": "vid__1-1-1__b002__r00__v001",
      "instances": [
        {
          "video_node_instance_id": "vid__1-1-1__b001__r00__v001",
          "video_node_key": "",
          "queue_status": "video_node_created_not_run"
        },
        {
          "video_node_instance_id": "vid__1-1-1__b002__r00__v001",
          "video_node_key": "",
          "parent_video_node_instance_id": null,
          "queue_status": "video_node_created_not_run"
        }
      ]
    }
  }
}
```
