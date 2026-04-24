# Request Distillation Contract

## Scope

本文件承接原 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` 的完整版蒸馏方法，并按 `B.分镜故事板` 的融合包边界重写为可执行细则。

目标是从 `projects/aigc/<项目名>/3-Detail/第N集.json` 中唯一锁定一个 `分镜组ID`，把该组转成一条多格 storyboard image-request JSON；本文件只拥有 request 蒸馏规则，不拥有参照绑定、provider handoff 或真实图片生成。

## Mandatory Inputs

- canonical detail root: `projects/aigc/<项目名>/3-Detail/第N集.json`
- canonical detail schema: `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`
- runtime adapter: `.agents/skills/aigc/_shared/detail_root_adapter.py`
- shared template: `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
- target group: 唯一 `分镜组ID`

可选补证输入只允许用于人工核对，不得覆盖 canonical detail root：

- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`
- `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`
- `projects/aigc/<项目名>/4-Design/` 下角色、场景、道具参考，仅登记到 request 的参照槽位或交给后续绑定阶段。

## Source Priority

1. 第一事实源固定为 `3-Detail/第N集.json` 中的 `meta + groups[].global/detail.分镜列表`。
2. `水月 / 镜花` sidecar 只补解释力，不改写第一事实源。
3. 旧式 `组间设计 / 正文切分参考[] / 正文回指 / 分镜明细[]` 只允许由 runtime compat projection 派生。
4. `4-Design/` 只提供资产候选或命名证据，不允许补写镜头事实。
5. provider 参数不得进入 prompt 正文。

## Readiness Gate

进入蒸馏前必须确认：

1. canonical detail root 经 adapter 判定为 `detail_in_progress | ready`。
2. `groups[]` 存在，并能唯一命中目标 `分镜组ID`。
3. 目标组具备 `global` 与 `detail` 结构。
4. 目标组至少可回链：
   - `分镜组ID`
   - `global.剧本正文`
   - `global.全局风格`
   - `global.类型元素`
   - `global.导演意图`
   - `detail.分镜数`
   - `detail.分镜列表`
5. `detail.分镜列表` 顺序稳定，且每个组内镜头至少可回链：
   - `分镜ID`
   - `时间`
   - `剧本正文` 或等价画面事实
   - `主体锚定`
   - `角色表现`
   - `运动表现`
   - `氛围表现`
   - `分镜构图`
   - `摄影表现` 或 `摄影美学`
   - `运镜手法`
   - `转场特效`
6. 可选镜头字段存在时应优先消费：`景别`、`镜头视角`、`镜头速度`、`视觉强化`。
7. 兼容字段存在时只作 fallback 或人工核对：`角色背景面`、`角色站位走位`、`道具及状态`、`分镜表现`、`正文回指`。

全局缺口必须阻断；局部缺口可保守留空并进入 `partial` 路由，但不得虚构。

## Distillation Topology

在 `B.分镜故事板` 中，旧叶子的 `N0-N6` 被消化为 `S0-S4`：

| new node | absorbed old nodes | responsibility |
| --- | --- | --- |
| `S0-intake-lock` | `N0 + N1` | 锁定对象、输出模式、source readiness 与非目标 |
| `S1-group-lock` | `N2` | 唯一定位分镜组，收集有序 `source_shot_ids` |
| `S2-storyboard-distill` | `N3 + N4` | LLM 生成 `固定英文前缀 + 组级设计块 + 多镜融写列` |
| `S3-template-map` | `N5` | 将 prompt 与组信息映射到共享 image request 模板 |
| `S4-request-land` | `N6` | 写 `第N集.json`，按需写 `_manifest.json`，执行 request gate |

`S1` 不直接写 prompt；它必须把完整、有序、可回链的组事实交给 `S2`。真正的完整版蒸馏方法从 `S2` 开始执行。

## Prompt Assembly Method

### Authorship

- 组级 storyboard prompt 正文、组级设计块、多镜融写列、多格画面节奏与审美裁决必须由 LLM 直接完成。
- 脚本只允许读取、归一、投影、校验或 dry-run；不得把脚本输出作为 canonical creative truth。
- 若使用旧 `generate_episode_packets.py`，只能投影既有 LLM 真源或校验模板字段。

### Fixed Prefix

prompt 必须逐字以以下三行开头：

```text
Create a multi-panel storyboard based on the following shot breakdown.
Add the shot sequence number in the bottom-left corner of each panel (no other text).
Auto-adapt the panel layout grid based on the total number of shots.
```

固定前缀之后直接进入 `storyboard_group` 内容块，中间不得插入解释说明、provider 参数或任务指令。

### Group Design Block

组级设计块用于统一空间、角色、氛围、构图逻辑和画面风格。它必须覆盖目标组的稳定组级事实：

| source field | usage |
| --- | --- |
| `分镜组ID` | 仅作结构化回链或组级锚点，不写成冗长字段标题 |
| `global.剧本正文` | 作为理解整组叙事的来源，不独立整段粘贴进 prompt |
| `global.全局风格` | 写成统一画面风格 |
| `global.类型元素` | 写成类型元素或情绪机制 |
| `global.导演意图` | 写成视觉重点和叙事意图 |
| `出场角色及穿搭` | 有则写入角色与穿搭连续性；无则保守留空 |

推荐句式：

- `全局风格统一为{全局风格}`
- `本组类型元素为{类型元素}`
- `本组导演意图聚焦{导演意图}`
- `角色与穿搭连续性保持{出场角色及穿搭}`

这些句式是蒸馏框架，不是脚本主创模板；LLM 可以在不改变事实的前提下做自然融写。

### Multi-Shot Rows

多镜融写列必须按 `source_shot_ids` 的原顺序覆盖每个镜头。每镜开头固定为：

```text
{time_range}｜分镜{shot_index}：
```

要求：

1. `shot_index` 使用组内序号，不使用完整四段式 `分镜ID`。
2. 完整四段式 `分镜ID` 只保留在 `meta.source_shot_ids` 等结构化字段。
3. 除镜级序号标签外，不在 prompt 中暴露字段标题。
4. 每镜必须消费真实上游事实，不得把整组剧情压成单段摘要。
5. 镜头事实应优先从 branch-owned 字段取值；legacy 字段只作 fallback。

### Shot Field Consumption

每镜按以下优先级组织内容：

| priority | field group | fields |
| --- | --- | --- |
| P0 | script bridge | `剧本正文`，必要时用 compat `正文回指` 辅助定位 |
| P0 | visual action | `运动表现`、`角色表现`、`主体锚定` |
| P1 | camera grammar | `景别`、`镜头视角`、`分镜构图`、`运镜手法`、`镜头速度` |
| P1 | atmosphere and texture | `氛围表现`、`摄影表现` / `摄影美学`、`视觉强化` |
| P2 | transition | `转场特效` |
| fallback | legacy visual helpers | `角色背景面`、`角色站位走位`、`道具及状态`、`分镜表现` |

若某字段缺失：

- 不补写未知事实。
- 不删除该镜头行。
- 用已有字段完成可回链的保守描述。
- 若缺口影响生成消费，在 `_manifest.json` 或调用侧闭环中记录 `exception_note`。

### Compression Levels

当 prompt 过长时，按以下顺序收缩，不得打乱镜头顺序：

| level | usage |
| --- | --- |
| `full` | 保留剧本桥接、运动、角色、氛围、摄影、视觉强化、转场 |
| `normal` | 保留剧本桥接、运动、角色、氛围，摄影可作为 fallback |
| `tight` | 保留剧本桥接、运动、角色、关键构图/运镜短语 |
| `ultra` | 只保留每镜最关键动作、角色状态和必要构图，不删除镜头 |

收缩时优先压缩子句，不允许把多镜合并为一段剧情摘要。

## Request Object Requirements

request JSON 至少包含：

- `meta.project`
- `meta.episode`
- `meta.group_id`
- `meta.source_tranche = "分镜故事板"`
- `meta.shot_level = "storyboard_group"`
- `meta.source_shot_ids`
- `prompt_style.type`
- `prompt_style.language`
- `prompt_style.char_limit`
- `model.model_version`
- `model.ratio`
- `model.image_size`
- `model.output_format`
- `model.num_images`
- `model.reference_images`
- `model.image_markers`
- `prompt`
- `prompt_char_count`

`model.reference_images` 与 `model.image_markers` 缺图时也必须保留空槽位；真实绑定由后续 `S5-S6` 负责。

## Landing And Manifest

唯一 request 业务真源：

- `projects/aigc/<项目名>/5-Image/分镜故事板/第N集/第N集.json`

条件侧车：

- `projects/aigc/<项目名>/5-Image/分镜故事板/第N集/_manifest.json`，仅当 `full_trace`。

`_manifest.json` 最低字段：

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `group_count`
6. `groups[].group_id`
7. `groups[].source_shot_ids`
8. `groups[].prompt_char_count`
9. `groups[].has_reference_slots`
10. `groups[].exception_note`

可选字段：

- `groups[].thinking_process_summary`
- `groups[].backtrack_note`

思考过程默认留在调用侧摘要；`full_trace` 时只允许浓缩为可复核摘要，不写成长篇草稿。

## Request Gate

通过 request 蒸馏必须同时满足：

1. source request 或 `分镜组ID` 唯一可追溯。
2. `source_shot_ids` 顺序与 `detail.分镜列表` 一致。
3. prompt 以固定英文前缀开头。
4. prompt 继续组织为组级设计块与完整多镜融写列。
5. prompt 没有独立粘贴整组 `global.剧本正文` 作为长段摘要。
6. 每个镜头行都可回链对应上游镜头事实。
7. `prompt_char_count` 与实际 prompt 一致。
8. request JSON 保持共享模板骨架完整。
9. `reference_images / image_markers` 不被删除或伪造。
10. 输出路径仍落在兼容 runtime 槽位。

## Failure And Rework

| fail signal | rework node |
| --- | --- |
| 对象其实是单帧或漫画页 | `S0` reroute |
| canonical `groups[]` 缺失或 adapter readiness 不成立 | `S0` block |
| `group_id` 不唯一或镜头顺序不稳定 | `S1` |
| 组级设计块漏掉核心组字段 | `S2` |
| 多镜融写列缺镜头、乱序或摘要化 | `S2` |
| 固定前缀漂移 | `S2` |
| request 模板字段缺失 | `S3` |
| `第N集.json` / `_manifest.json` 不可追溯 | `S4` |

## Legacy Script Boundary

旧脚本 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/scripts/generate_episode_packets.py` 只能用于：

- 读取或投影既有 LLM 真源。
- dry-run 校验模板字段。
- 兼容旧产物结构。

它不得作为默认 prompt 主创执行器。若必须启用旧式脚本主创，只能在显式 legacy guard 下执行，且不得写回默认工作流。
