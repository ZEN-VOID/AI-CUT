# Type Package: subject_reference_flow

主体参照流是本技能默认路线。它只负责把 `5-分组` 分镜组转成 LibTV CLI handoff plan；真实画布执行由 `.agents/skills/cli/libTV` 完成。

## Fixed Context

- 基本处理对象：`projects/aigc/<项目名>/5-分组/第N集.md`。
- 每个非连接件分镜组 `## x-y-z` 直接作为一条 LibTV 视频生成任务的剧情主体。
- `5-分组` 是主要信息来源；不得回到 `4-摄影`、`3-Detail` 或更早阶段重写分镜组内容，除非用户显式要求修复上游。
- 分镜组视频 prompt 主体直接采用现有分镜组正文；LLM 只负责裁决提取范围、保真组织、缺口说明和审查，不得扩写或改写剧情事实。
- 组底 fenced YAML 的 `角色 / 场景 / 道具` 是主体参照绑定的默认来源。
- 组底 YAML 同时定义参考数组的 canonical order：`角色` 原顺序 -> `场景` 原顺序 -> `道具` 原顺序。
- 组底 fenced YAML 必须完整保留在 `video_node.params.prompt` 底部；其 `角色 / 场景 / 道具 / 时长估算` 还必须投影为参考绑定、duration 和证据工件。
- 不得用正文泛词、子串或猜测名自动扩展主体列表。
- 画布默认已经存在规范命名的主体参照图；规范名应与 YAML 主体名一致。
- 默认不需要 LibTV 远端提示词优化或镜头压缩；`allow_libtv_prompt_optimization=false`。
- 视频生成必须是参考驱动：只要本组有至少一张可用主体参照图，提交语义必须显式为“全能参考 / 多图主体参考生成视频”，标准字段必须为 `modeType=mixed2video`。

## Subject Binding Table

统一命名为 `主体绑定表`，每行至少包含：

```yaml
- yaml_name: 令狐冲
  category: 角色
  canvas_node_name: CHAR-005-令狐冲.png
  node_key: 5a9b2d1e-eb41-4ae9-a93d-9d0d5a67355c
  url: https://...
  usage: 决战主角之一
```

CLI handoff plan 必须声明：

- handoff plan 和 `video_node.params.prompt` 分层；主体绑定表只用于工具参数与画布节点映射，不进入 prompt。
- `主体绑定表` 是参考绑定唯一真源。
- 最新版 CLI 的稳定引用方式是左侧输入连线 + runtime `{{Image N}}`；`N` 必须来自新建/更新视频节点后查询到的 `data.params.imageList[]` 或等价左侧输入顺序。
- 若计划顺序、UI 排列、节点框体顺序或缩略图顺序与绑定表不一致，以 `stable_subject_id + node_key + assetId/url` 为准；若 runtime `imageList` 与计划顺序不一致，以查询结果生成 `runtime_image_placeholder_map[]` 后再写 prompt。
- `subject_bindings`、`planned_left_input_edges[]`、`source_node_keys`、`source_node_url_mapping` 和计划层 `imageList/mixedList` 必须按 canonical order 的选中子集排列；不得按上传顺序、画布创建时间、本地文件扫描顺序或 `Portrait N` 排列。
- 执行层必须用 `--left` 或 `--left-add` 把主体图节点按 canonical order 逐张连到视频节点左侧；prompt 中只在底部 YAML 主体条目使用已通过 `runtime_image_placeholder_map[]` 登记的 `{{Image N}}` 占位，不使用不可验证的 UI `@` 文本。
- 最终 prompt 必须在 runtime map 之后装配；计划阶段准备主体文本和 YAML，但不把计划顺序中的 `Image N` 当成最终编号。
- 决定性检查点固定在最终节点参数、左侧输入和远端 `--prompt` 都写完之后、`--run` 之前；最终放行依据是这一次查询到的 `data.params.imageList[] + data.params.prompt`，不是本地 prompt 文件或更早查询结果。
- `video_node.params.prompt` 中必须保留原主体名，不得只写图片序号。
- 每个进入 LibTV 的参考图都必须在 handoff plan 中以计划层 `planned_image_index + stable_subject_id + URL + node_key + yaml_name + 用途` 出现，并在运行前补齐 `runtime_image_index + {{Image N}}`，且和 `runtime_image_placeholder_map[] / libtv_images[] / mixedList` 一致。
- 远端消息、submit plan、queue record、manifest 和实际工具入参必须记录同一个标准 `modeType`；主体参照流默认 `mixed2video`。
- 只有用户显式要求远端优化时，`allow_libtv_prompt_optimization` 才可为 `true`，并必须记录到 submit plan、queue 和 report。
- 未 opt-in 时，若查询发现实际节点 prompt 被压缩改写，或混入 `{{Portrait N}}`、执行锁、生成参数、主体绑定表、参考图清单或诊断说明，应先自动清理并重写最终 prompt；只有 CLI 无法写回或远端持续污染时，才记为 `needs_rework / remote_prompt_rewritten_or_polluted`。
- 内部诊断或 fallback 说明不得进入 prompt，例如 `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频`；这些只写入证据工件。
- 不得重复追加 `StyleBible`、`StyleBible_Summary`、音频约束或 `其中，...` 尾部复述；分镜组正文已有内容只出现一次。
- 不得用泛化人物描述替代 YAML 主体绑定。

## Reference Resolution

- 同一 LibTV `projectUuid/projectID` 画布内，已经按同一 YAML 主体名成功上传并登记为 active 的主体图 URL 可直接复用。
- active registry 固定为 `projects/aigc/<项目名>/8-视频/libTV画布流/libtv-canvas-active-registry.json`，主键为 `projectUuid::category::yaml_name`。
- 只有缺少 active URL、同名登记歧义、图片被调整/更换或用户明确要求“替换/更新/重新上传”时，才检查本地生成目录并生成上传计划。
- 本地查找目录固定为：
  - `projects/aigc/<项目名>/6-设计/角色/3-生成`
  - `projects/aigc/<项目名>/6-设计/场景/3-生成`
  - `projects/aigc/<项目名>/6-设计/道具/3-生成`
- 需要新上传时，多视图优先，没有多视图就主图，都没有就空着并从参照图片数组中移除。
- 名称命中多个候选图片时，先把候选图发送到当前窗口作为可加载上下文执行视觉消歧；无法唯一判定才进入 `ambiguous`。
- 本地图片路径、候选集合和消歧证据只写入 manifest / submit plan，不写进 prompt 正文。

## Evidence Artifacts

- `libtv-canvas-active-registry.json`：项目级画布主体 active registry。
- `<分镜组ID>-subject-reference-manifest.json`：组级主体绑定、候选、消歧和预算真源。
- `<分镜组ID>-libtv-submit-plan.json`：组级提交计划，必须记录 `allow_libtv_prompt_optimization` 和 `cli_handoff`。
- `<分镜组ID>-queue-record.json`：组级提交状态，必须记录 `executor_skill`、`projectUuid`、`groupNodeKey`、`video_node_key`、`runtime_image_placeholder_map[]`、`queried_runtime_image_map_verified`、下载状态和阻断原因。

## Reference Budget

- 单组进入 `images[]` / `mixedList` 的图片最多 9 张。
- 同一 YAML 主体默认只提交一张主体参照图；除非用户显式要求多视图或多版本对比，不得为同一主体在同一视频任务中重复提交两张同义主体图。
- 超过时角色和场景优先，先排除道具，其次排除重复、不必要或可由源文本保留的次要主体。
- 被排除项必须在 manifest / submit plan 记录为 `excluded_from_libtv_images` 或 `excluded_due_to_budget`。
- 无法合理压缩到 9 张以内时状态为 `needs_rework / reference_budget_unresolved`，不得提交。
- 若可用参考图在 LibTV/Seedance 预处理或审核中失败，状态为 `needs_rework / reference_asset_review_failed`；不得自动把该组降级为无参考图纯文生视频，除非用户当前轮显式授权。

## Duration Rule

- `4 < 时长估算 < 15`：使用估算时长。
- `时长估算 >= 15`：使用 15 秒。
- `时长估算 <= 4`：使用 4 秒。
- 缺少 YAML `时长估算` 时，按组内 `分镜明细` 秒数求和估算，区间时长优先取上限；仍无法确定时回退 15 秒并记录 `duration_source=fallback_default`。
- 每组必须形成 `duration_estimate_seconds` 和最终 `duration`。

## Default Video Spec

- `resolution`: `720p`
- `ratio`: `16:9`
- `download`: `false`

用户显式指定其他规格时，按用户要求传递给 LibTV。
