# Output Template

## Output Contract Alignment

| Field | Contract |
| --- | --- |
| Required output | local AIGC mapping, projectSpace/folder evidence, canvas UUID/projectUuid, upload registry, YAML backfill, video node list, runtime image map |
| Output format | JSON manifests, JSON submit plans, JSON queue records, Markdown reports |
| Output path | `projects/aigc/<项目名>/10-画布/libTV画布流/第N集/` |
| Naming convention | `<video_node_instance_id>-subject-reference-manifest.json`, `<video_node_instance_id>-libtv-submit-plan.json`, `<video_node_instance_id>-queue-record.json`, `<video_node_instance_id>-执行报告.md`; `source_group_id` 只写入内容和 registry，不单独作为唯一文件名前缀 |
| Completion gate | final remote query verifies `imageList` order, prompt hygiene, structured execution report evidence, `LibTV Upstream Video Direction Matrix` and no unauthorized run |

## Execution Report Evidence

每个 `<video_node_instance_id>-执行报告.md` 至少包含：

- `Execution Decision Trace`: 记录关键判断、适用规则、输入证据、取舍理由和输出落点，不输出冗长思维链。
- `Reference Execution Matrix`: 逐条记录本轮实际加载或未触发的 `references/`、`types/`、`review/`、`templates/`、`guardrails/`、CLI 文档和项目上下文。
- `Rule Evidence Map`: 将 project space/canvas、YAML backfill、image order、prompt hygiene、multi-storyboard、runtime boundary、upstream direction 和 final query gate 映射到证据文件或远端查询。
- `N/A Justification`: 对未触发的模式、reference 或 gate 说明原因。
- `Repair Log`: 记录 fail code、返工目标、修复结果和残余风险。

## LibTV Upstream Video Direction Matrix

| upstream_context | direction_role | used_as | video_node_decision | remote_evidence_anchor | boundary_check | evidence_map |
| --- | --- | --- | --- | --- | --- | --- |
| `8-分组/第N集.md` | prompt truth | complete_group_source |  | remote prompt / submit plan | no rewrite / no scripted prompt |  |
| `3-主体` / uploaded refs | subject fidelity | image order and UUIDs |  | imageList / mixedList | no guessed binding |  |
| `9-图像` / generated refs | visual reference | optional storyboard/subject evidence |  | manifest / prompt segment | no second truth |  |
| project constraints / LibTV limits | runtime boundary | node settings and run policy |  | queue record / final query | no unauthorized run |  |

## Queue Record Fields

```json
{
  "local_project_root": "projects/aigc/<项目名>",
  "local_episode": "第N集",
  "local_episode_scope": "projects/aigc/<项目名>/第N集",
  "source_file": "projects/aigc/<项目名>/8-分组/第N集.md",
  "evidence_dir": "projects/aigc/<项目名>/10-画布/libTV画布流/第N集",
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
  "upstream_video_direction_matrix_status": "required",
  "runtime_image_placeholder_map": [],
  "queried_runtime_image_map_verified": false,
  "execution_report_evidence_status": "required",
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
  "source_file": "projects/aigc/<项目名>/8-分组/第N集.md",
  "evidence_dir": "projects/aigc/<项目名>/10-画布/libTV画布流/第N集",
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
