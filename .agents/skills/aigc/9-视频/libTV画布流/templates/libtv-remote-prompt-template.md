# LibTV Video Prompt And CLI Handoff Template

本模板区分两层内容：

- `cli_handoff_plan`：交给 `.agents/skills/cli/libTV` 的执行计划，包含项目、分组、节点、模型、参数和参考图绑定。
- `video_node.params.prompt`：视频节点真正使用的创作提示词，只能是干净创作正文和已验证 `{{Image N}}` 图片占位。

不得把 `cli_handoff_plan` 中的执行参数、参考图清单、主体绑定诊断、missing/excluded 原因、文件路径或审计说明复制进 `video_node.params.prompt`。允许进入 prompt 的参考信息只有最新版 CLI 支持的 `{{Image N}}` 占位。

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
    params_prompt_source: "projects/aigc/<项目名>/6-分组/第N集.md::{group_id}"
  reference_bindings_for_tool_params_only:
{selected_reference_bindings_yaml}
  left_input_edges:
    - image_index: 1
      placeholder: "{{Image 1}}"
      yaml_name: "{yaml_name}"
      category: "{角色|场景|道具}"
      node_key: "{image_node_key}"
      url: "{url}"
      connect_command: "libtv node \"{group_id}\" -p \"{projectUuid}\" -g \"{groupNodeKey}\" --left-add \"{image_node_key}\""
  image_placeholder_map:
    - image_index: 1
      placeholder: "{{Image 1}}"
      yaml_name: "{yaml_name}"
      node_key: "{image_node_key}"
      verified_by: "queried left input order"
  prompt_lock:
    params_prompt_must_equal_video_prompt: true
    no_rewrite_no_summary_no_extra_shots: true
    no_execution_metadata_in_prompt: true
  expected_evidence:
    - video_node_key
    - queried_video_node_params
    - queried_left_input_order
    - node_key_url_mapping
    - queue_record
```

## Video Prompt

`video_node.params.prompt` 必须严格等于：

```text
{clean_video_prompt}
```

## Assembly Rules

- `clean_video_prompt` 由两部分组成：`## x-y-z` 下的分镜组正文 + 底部完整 fenced YAML 内容；已绑定主体可插入对应 `{{Image N}}`。
- `clean_video_prompt` 不包含执行锁、生成参数、`YAML主体清单`、`主体绑定表`、参考图清单、missing/excluded 诊断、manifest 路径或 submit plan 字段。
- 底部 YAML 必须完整保留原字段和值，包括 `字数统计`、`时长估算`、`角色`、`场景`、`道具` 等；不得只摘要成主体清单。
- 每个已绑定 YAML 主体必须能通过 `reference_bindings_for_tool_params_only`、`left_input_edges[]` 和 `image_placeholder_map[]` 回指 `canvas_node_name / node_key / URL`。
- 最新版 CLI 的稳定引用方式是左侧输入连线 + `{{Image N}}`：执行层必须用 `--left` 或 `--left-add` 连接主体图节点，并查询视频节点确认左侧输入顺序；`{{Image N}}` 的 N 必须等于该主体在左侧输入中的 1-based 顺序。
- 每个已绑定 YAML 主体在分镜组正文第一次出现时，在主体名后插入对应占位，例如 `令狐冲 {{Image 1}}`；底部 YAML 中对应主体名后也插入同一占位。
- 参考数组构造前必须先生成 `canonical_reference_order`：`YAML.角色[] -> YAML.场景[] -> YAML.道具[]`，保留各列表内原顺序。
- `subject_bindings`、`selected_reference_bindings_yaml`、`left_input_edges[]`、`image_placeholder_map[]`、`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 都按 canonical order 的选中子集排列。
- 如果 `imageList` 顺序与主体出现顺序不同，仍以左侧输入查询结果、`image_placeholder_map[]` 和绑定表为准；不得把第 N 张图默认绑定给第 N 个主体。
- 插入引用属于 transport-only 参照绑定，不得改变原文措辞、句序、镜头顺序、台词、动作结果或风格描述。
- 同一 YAML 主体默认只提交一张主体参照图；除非用户显式要求多视图或多版本对比，不得为同一主体在同一视频任务中重复提交两张同义主体图。
- 参照图超过 9 张时，预算裁决只影响 `imageList/mixedList` 和 evidence artifacts；被排除主体仍保留在底部 YAML 原文中，但不得在 prompt 中写入缺图原因或排除原因。
- 不得追加 `StyleBible`、`StyleBible_Summary` 或 `其中，...` 尾部复述。
- 不得出现 `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频`、`角色与道具按原文生成` 等执行诊断或泛化主体替代句。
