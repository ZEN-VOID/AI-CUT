# Request Distillation Contract

## Purpose

把 `projects/aigc/<项目名>/3-Detail/第N集.json` 中唯一 `分镜ID` 蒸馏为单帧 image-request JSON。

本文件是 `A.分镜画面` 对旧 `1-提示词蒸馏/分镜帧` 蒸馏方法的完整消化层。旧叶子仍保留为兼容入口、旧 runner 和历史追溯源；新执行默认以本文件与 `steps/frame-image-workflow.md` 为蒸馏段真源。

## Absorbed Source Map

| old source | absorbed meaning | new owner |
| --- | --- | --- |
| `分镜帧/SKILL.md` input gate | 只处理单一四段式 `分镜ID`，拒绝故事板、漫画页和多镜合并 | 本文件 `Readiness Gate` + `steps/F0-F1` |
| `分镜帧/SKILL.md` node network | 输入门、唯一锁镜、上下文包、内容蒸馏、prompt 组装、模板填充、审计、写回 | `steps/frame-image-workflow.md` |
| `分镜帧/SKILL.md` prompt rules | 固定英文前缀 + 组级设计块 + 单镜融写行 | 本文件 `Prompt Assembly Method` |
| `分镜帧/prompt-assembly-spec.md` syntax | 前缀、组级字段、镜级字段顺序、压缩等级、字段标题禁用 | 本文件 `Prompt Assembly Method` |
| `分镜帧/CONTEXT.md` heuristics | 对象边界、脚本主创阻断、正文桥接、模板骨架保留 | 本文件 gates + 本包 `CONTEXT.md` |

## Mandatory Inputs

- canonical detail root: `projects/aigc/<项目名>/3-Detail/第N集.json`
- shared template: `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
- unique shot id: 四段式 `episode-scene-group-frame`
- optional compat adapter: `.agents/skills/aigc/_shared/detail_root_adapter.py`
- optional syntax evidence: legacy `分镜帧/prompt-assembly-spec.md`

## Readiness Gate

1. canonical detail root 经适配后达到 `detail_in_progress | ready`。
2. 目标 shot 在 `groups[].detail.分镜列表` 中唯一命中，且 `分镜ID` 为四段式 canonical ID。
3. 目标 group 至少能提供：
   - `分镜组ID`
   - `global.剧本正文`
   - `global.全局风格`
   - `global.类型元素`
   - `global.导演意图`
   - `detail.分镜列表`
4. 目标 shot 至少能提供：
   - `时间`
   - `剧本正文`
   - `主体锚定`
   - `角色表现`
   - `氛围表现`
   - `分镜构图`
   - `摄影表现` 或 `摄影美学`
   - `运镜手法`
   - `转场特效` 或等价镜头衔接说明
5. 兼容过渡期可把旧字段作为补证：`角色背景面 / 角色站位走位 / 道具及状态 / 分镜表现 / 镜头类型兼容`。
6. 缺失字段只能保守留空、降级为 `partial` 或写入 exception note，不得虚构镜头事实。

## Frame Context Pack

`F2-context-pack` 必须形成可审计的 `frame_context_pack`，而不是临场读字段即写 prompt。

| pack slot | source | rule |
| --- | --- | --- |
| `project_episode` | 用户输入 + detail root | 记录项目、集号、source file |
| `shot_identity` | canonical `groups[].detail.分镜列表` | 记录 `group_id`、`shot_id`、组内序号、长度为 1 的 `source_shot_ids` |
| `group_global` | `groups[].global` | 提取 `剧本正文 / 全局风格 / 类型元素 / 导演意图` |
| `group_design_hint` | compat projection 或 design assets | 仅作上下文补证，尤其是 `出场角色及穿搭`，不得覆盖 canonical 镜头事实 |
| `shot_detail` | target shot | 提取时间、镜头、角色、动作、氛围、构图、摄影、运镜、转场等镜级事实 |
| `script_bridge` | target shot `剧本正文` first，compat `正文切分参考[] / 正文回指` fallback | canonical shot 自带 `剧本正文` 足够时不强依赖 compat bridge；若桥接失败，只允许回退整组正文作边界参考 |
| `coverage_note` | 本轮审计 | 标记 `ready / partial` 与缺口 |

### Context Priority

1. canonical target shot 字段优先。
2. canonical group `global.*` 只提供本帧必须继承的风格、类型、导演意图和剧本文本边界。
3. compat projection 只补 `正文切分参考[] / 正文回指 / 组间设计` 等旧 helper，不得重新定义第一真相。
4. `4-Design` 与 `Assets` 在蒸馏阶段只提供可见锚点提示，不得直接写入 `model.reference_images`；真实绑定留给 `F5-F6`。

## Prompt Assembly Method

### Authorship Gate

- 单帧 prompt 正文、组级设计块压缩、单镜融写行和画面取舍必须由 LLM 直接完成。
- 脚本可做读取、投影、校验、字数统计和 JSON 包装；不得生成 canonical creative truth。
- 若旧 runner 产出了 prompt，只能视为兼容样例或校验材料，不能自动成为最终 prompt。

### Composition Contract

最终 prompt 固定采用：

```text
固定英文前缀
组级设计块
单镜融写行
```

硬规则：

1. 固定英文前缀必须逐字保留。
2. 组级设计块紧跟前缀之后，不插入说明性标题。
3. 单镜融写行固定以 `xx秒-xx秒｜分镜<组内序号>：` 开头。
4. 单镜融写行只服务当前唯一 `分镜ID`，不得写成整组剧情摘要，也不得复述整段对白。
5. 完整四段式 `分镜ID` 只保留在结构化回链字段中，不暴露进 prompt 正文。
6. 除 `分镜<组内序号>` 标签外，不暴露字段标题。

### Fixed Prefix

```text
Create a single cinematic frame based on the following shot breakdown.
Render only the specified shot moment as one full-frame image (no multi-panel layout).
Do not add any text, subtitles, speech bubbles, or graphic overlays.
Preserve the shot's composition, camera angle, subject positions, and atmosphere as the primary visual focus.
```

### Group Design Block

组级设计块用 `；` 连接以下字段，字段缺失时跳过该 clause，但不得编造：

| field | clause template | transform |
| --- | --- | --- |
| `全局风格` | `全局风格统一为{value}` | 去尾标点 |
| `类型元素` | `本组类型元素为{value}` | 去尾标点 |
| `导演意图` | `本组导演意图聚焦{value}` | 去尾标点 |

组级 `剧本正文` 不再作为独立 A 段全文放入 prompt；它只用于帮助 `script_bridge` 锁定当前单镜融写行的剧情边界。

### Single Shot Line

单镜融写行采用以下顺序融写，不暴露字段标题：

1. opening: `{time_range}｜分镜{shot_index}：`
2. script bridge: 当前 shot 的 `剧本正文`，必要时由 compat `正文回指` 回链到 `正文切分参考[]`
3. camera clauses:
   - `景别`
   - `镜头视角`
   - `分镜构图`
   - `运镜手法`
   - `镜头速度`
4. detail clauses:
   - `运动表现`
   - `角色表现`
   - `氛围表现`
   - `摄影美学` 或 canonical `摄影表现`
   - `道具及状态`
   - `视觉强化`
   - fallback `镜头类型兼容`

字段归一：

| canonical or legacy field | prompt role |
| --- | --- |
| `主体锚定` | 约束主体位置、主体关系和画面焦点，可融入 script bridge 或角色表现 |
| `角色表现` | 角色神态、动作、姿态和关系 |
| `运动表现` | 当前帧可见动态趋势，不把整段运动过程写成剧情梗概 |
| `氛围表现` | 空气、情绪、光影感和环境压力 |
| `分镜构图` | 构图与主体位置 |
| `摄影表现 / 摄影美学` | 镜头质感、光学特征和影像调性 |
| `运镜手法` | 保留镜头设计，但最终仍渲染单帧瞬间 |
| `转场特效` | 只在当前画面可见时写入，否则保留在结构化备注 |

### Budgeting Levels

同一 `single_frame_shot` 可按字符压力选择压缩等级：

| level | usage | rule |
| --- | --- | --- |
| `full` | 字数充足、字段完整 | 尽量保留 script bridge、camera clauses 和 detail clauses |
| `normal` | 默认 | 保留核心剧情边界、构图、角色、氛围和摄影 |
| `tight` | 接近 char limit | 压缩修饰词，保留可见事实和镜头抓手 |
| `ultra` | 超限返工 | 只保留必要主体、构图、动作、氛围和摄影锚点 |

压缩只能删减或合并表达，不能新增事实。

## Single Frame Distillation

`F3-llm-distill` 产出的 `single_frame_shot` 必须满足：

- 只围绕当前目标 `分镜ID`。
- 保留必要组级风格、类型和导演意图。
- 显式承接目标镜头的时间、主体、角色、氛围、构图、摄影和运镜。
- 若字段不完整，标记 `partial`，保守输出已有事实。
- 不把组级剧本文本、大段对白或多镜运动链条压成一条泛化故事梗概。

## Request JSON Fields

### `meta`

- `shot_level = storyboard_frame`
- `source_tranche = 分镜帧`
- `group_id`
- `source_shot_ids` 长度为 1
- 可选但推荐保留：`episode_id / source_file / shot_index / output_mode / exception_note`

### `prompt_style`

- `type` 固定服务单帧图像。
- `language = mixed`。
- `char_limit` 优先继承共享模板；若无上游覆盖，默认按旧 spec 的 `2200` 处理。

### `model`

必须继承共享 image-generation 模板骨架，尤其保留：

- `model_version`
- `ratio`
- `image_size`
- `output_format`
- `num_images`
- `reference_images`
- `image_markers`

无参照图时也必须保留 `reference_images` 与 `image_markers` 空骨架，不得伪造绑定。

### Prompt Fields

- `prompt`
- `prompt_char_count`

`prompt_char_count` 必须与最终 prompt 实际字符数一致。任何后处理改动 prompt 后都必须重新统计。

## Output Modes

| output_mode | output | rule |
| --- | --- | --- |
| `json_only` | `第N集.json` | 默认模式，只写 canonical request JSON |
| `full_trace` | `第N集.json + _manifest.json` | 仅用户、父级或调试要求时输出 |

`_manifest.json` 最低字段：

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `shot_count`
6. `shots[].group_id`
7. `shots[].shot_id`
8. `shots[].prompt_char_count`
9. `shots[].has_reference_slots`
10. `shots[].exception_note`

## Distillation Audit

| dimension | pass standard | fail code | rework entry |
| --- | --- | --- | --- |
| `input_traceability` | `分镜ID / group_id / source_shot_ids` 同时成立且唯一 | `FAIL-FRAME-DISTILL-INPUT` | `F0-F1` |
| `context_pack` | `frame_context_pack` 能解释 prompt 来源，且 compat 只作补证 | `FAIL-FRAME-DISTILL-CONTEXT` | `F2` |
| `object_boundary` | `single_frame_shot` 只服务当前帧 | `FAIL-FRAME-DISTILL-SCOPE` | `F2-F3` |
| `prompt_integrity` | 固定前缀、组级设计块、单镜融写行顺序正确 | `FAIL-FRAME-DISTILL-PROMPT` | `F3` |
| `template_compatibility` | `meta / prompt_style / model` 骨架完整，引用槽位保留 | `FAIL-FRAME-DISTILL-TEMPLATE` | `F4` |
| `output_consumability` | `第N集.json` 可被 `F5` 或 `F7` 继续消费 | `FAIL-FRAME-DISTILL-HANDOFF` | `F4-F9` |

## Script Boundary

旧 runner `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/scripts/generate_episode_packets.py` 只允许承担兼容投影和校验辅助。

允许用途：

- 读取 canonical detail root。
- 经 adapter 投影旧 helper。
- 包装已有 LLM prompt 为 JSON。
- 校验固定前缀、字段骨架和字数统计。
- dry-run 对比旧输出。

禁止用途：

- 直接生成 canonical prompt 正文。
- 用规则拼接替代 LLM 的画面审美裁决。
- 在默认路径写入 legacy script-authored prompt。
- 让 `_manifest.json` 或 runner sidecar 成为第二业务真源。
