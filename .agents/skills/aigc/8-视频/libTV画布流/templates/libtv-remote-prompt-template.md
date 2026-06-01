# LibTV Video Prompt And CLI Handoff Template

本模板区分两层内容：

- `cli_handoff_plan`：交给 `.agents/skills/cli/libTV` 的执行计划，包含项目、分组、节点、模型、参数和参考图绑定。
- `video_node.params.prompt`：视频节点真正使用的创作提示词，只能是原样分镜正文、完整 fenced YAML，以及插在 YAML 主体条目后的已验证 `{{Image N}}` 图片占位。

不得把 `cli_handoff_plan` 中的执行参数、参考图清单、主体绑定诊断、missing/excluded 原因、文件路径或审计说明复制进 `video_node.params.prompt`。允许进入 prompt 的参考信息只有最新版 CLI 支持的 `{{Image N}}` 占位，且只能位于底部 YAML 主体条目后。

## CLI Handoff Plan

```yaml
cli_handoff_plan:
  executor_skill: ".agents/skills/cli/libTV"
  auth_check:
    command: "libtv account info"
  project:
    projectUuid: "{projectUuid}"
    projectName: "{projectName}"
  target_group:
    name: "{episode_or_batch_group_name}"
    key: "{groupNodeKey}"
  video_node:
    name: "{group_id}"
    type: "video"
    modeType: "{modeType}"
    duration: "{duration}"
    resolution: "{resolution}"
    ratio: "{ratio}"
    download: false
    allow_libtv_prompt_optimization: false
    params_prompt_source: "projects/aigc/<项目名>/5-分组/第N集.md::{group_id}"
  reference_bindings_for_tool_params_only:
{selected_reference_bindings_yaml}
  planned_left_input_edges:
    - planned_image_index: 1
      stable_subject_id: "{stable_subject_id}"
      yaml_name: "{yaml_name}"
      category: "{角色|场景|道具}"
      node_key: "{image_node_key}"
      assetId: "{assetId}"
      url: "{url}"
      connect_command: "libtv node \"{group_id}\" -p \"{projectUuid}\" -g \"{groupNodeKey}\" --left-add \"{image_node_key}\""
  runtime_image_placeholder_map:
    - image_index: 1
      placeholder: "{{Image 1}}"
      stable_subject_id: "{stable_subject_id}"
      yaml_name: "{yaml_name}"
      node_key: "{image_node_key}"
      assetId: "{assetId}"
      url: "{url}"
      verified_by: "queried data.params.imageList"
  queried_runtime_image_map_verified: false
  prompt_lock:
    params_prompt_must_equal_video_prompt: true
    no_rewrite_no_summary_no_extra_shots: true
    no_execution_metadata_in_prompt: true
  expected_evidence:
    - video_node_key
    - queried_video_node_params
    - queried_runtime_imageList
    - runtime_image_placeholder_map
    - node_key_url_mapping
    - queue_record
```

## Video Prompt

`video_node.params.prompt` 必须严格等于：

```text
{clean_video_prompt}
```

## Assembly Rules

- `clean_video_prompt` 由两部分组成：`## x-y-z` 下的分镜组正文 + 底部完整 fenced YAML 内容；已绑定主体的 `{{Image N}}` 只允许插入底部 YAML 的 `角色 / 场景 / 道具` 条目主体名后。
- `clean_video_prompt` 不包含执行锁、生成参数、`YAML主体清单`、`主体绑定表`、`参照图绑定`、参考图清单、missing/excluded 诊断、manifest 路径、submit plan 字段或 `{{Portrait N}}` 历史占位。
- 底部 YAML 必须完整保留原字段和值，包括 `字数统计`、`时长估算`、`角色`、`场景`、`道具` 等；不得只摘要成主体清单。
- 每个已绑定 YAML 主体必须能通过 `reference_bindings_for_tool_params_only`、`planned_left_input_edges[]` 和 `runtime_image_placeholder_map[]` 回指 `canvas_node_name / node_key / assetId / URL`。
- 最新版 CLI 的稳定引用方式是左侧输入连线 + runtime `{{Image N}}`：执行层必须用 `--left` 或 `--left-add` 连接主体图节点，创建/更新视频节点后先查询 `data.params.imageList[]`，再用 `node_key + assetId/url` 生成 `runtime_image_placeholder_map[]`；`{{Image N}}` 的 N 必须等于该主体在 runtime `imageList` 中的 1-based 顺序。
- 最终 prompt 不能在 runtime map 生成前定稿；先用 draft prompt 建节点和连图，查询 runtime 编号后，再按 `runtime_image_placeholder_map[]` 写入最终 `clean_video_prompt`。
- 每个已绑定 YAML 主体只在底部 fenced YAML 的 `角色 / 场景 / 道具` 条目主体名后插入对应占位，例如 `- 令狐冲 {{Image 1}}`；分镜组正文中的主体名不插入占位。
- 参考数组构造前必须先生成 `canonical_reference_order`：`YAML.角色[] -> YAML.场景[] -> YAML.道具[]`，保留各列表内原顺序。
- `subject_bindings`、`selected_reference_bindings_yaml`、`planned_left_input_edges[]`、`source_node_keys`、`source_node_url_mapping` 和计划层 `imageList/mixedList` 都按 canonical order 的选中子集排列。
- 如果 runtime `data.params.imageList[]` 顺序与计划顺序或主体出现顺序不同，必须以查询结果、`runtime_image_placeholder_map[]` 和绑定表为准重写 prompt；不得把第 N 张图默认绑定给第 N 个主体。
- 决定性检查点只有一个：最终节点参数、左侧输入和 `--prompt` 都写完之后，`--run` 之前，查询一次远端视频节点，以该次返回的 `data.params.imageList[] + data.params.prompt` 作为唯一放行真源。
- 决定性检查不通过时，先自动修复可控项：按 runtime map 重写 prompt、清理污染字段或重建左侧输入；只有不可自动修复时，本次执行状态才为 `needs_rework`，不得进入 `--run`。
- 最终放行 `--run` 前，必须直接检查远端 `data.params.prompt`，确认没有 `{{Portrait N}}`、绑定表、参考图清单、执行锁、路径或诊断文本。
- 插入引用属于 transport-only 参照绑定，且只作用于 YAML 主体条目；不得改变正文原文措辞、句序、镜头顺序、台词、动作结果或风格描述。
- 同一 YAML 主体默认只提交一张主体参照图；除非用户显式要求多视图或多版本对比，不得为同一主体在同一视频任务中重复提交两张同义主体图。
- 参照图超过 9 张时，预算裁决只影响 `imageList/mixedList` 和 evidence artifacts；被排除主体仍保留在底部 YAML 原文中，但不得在 prompt 中写入缺图原因或排除原因。
- 不得追加 `StyleBible`、`StyleBible_Summary` 或 `其中，...` 尾部复述。
- 不得出现 `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频`、`角色与道具按原文生成` 等执行诊断或泛化主体替代句。
