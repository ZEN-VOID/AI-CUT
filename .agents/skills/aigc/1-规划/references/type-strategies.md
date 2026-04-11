# aigc 1-规划 / Type Strategies

本文件承载 `aigc 1-规划` 根技能的双来源类型化处理真源。

## 模块定位

- 上游真源：`projects/<项目名>/Init/story-source-manifest.yaml`
- 当前模块负责把故事源类型收束成可执行的规划策略与下游交接合同。
- 本模块不替代各子技能的局部类型策略；它只处理根技能级的“故事主源是什么，以及它如何改变后续规划与 `3-明细`”。

## 模式判定

- 当前模式：`类型策略优化设计 + 多模式路由治理`
- 症状：
  - `1-规划` 过去默认把上游理解成小说/剧本原文。
  - `storyboard_script` 会改变预设点保留规则、组级切分策略和 `3-明细` 的扩写边界。
  - 若没有根级类型矩阵，下游只能靠经验猜“哪些镜头预设能动、哪些不能动”。

## Shared Core

无论故事主源是什么，`1-规划` 的共享核心都不变：

1. 先读取 `story-source-manifest.yaml` 再进入规划。
2. 先判唯一子路径，再进入对应子技能。
3. 规划阶段只收束结构、格式、分组与节奏，不越权代替 `2-组间` 或 `3-明细`。
4. 若来源类型会影响下游写法，必须显式回写到 shared handoff，而不是留在脑内。

## Type Register

| source_mode | source_type 命中 | 说明 | 共享终局 |
| --- | --- | --- | --- |
| `SRC-NARRATIVE` | `novel_original`、`script_original`、`oral_story_transcript` | 上游以叙事原文为主，镜头层通常尚未被锁定 | 允许后续 `3-明细` 从组级文本继续生长分镜骨架 |
| `SRC-STORYBOARD` | `storyboard_script` | 上游已自带分镜/镜头/转场/运镜类预设点 | 必须保护预设点，并让后续沿预设扩写 |
| `SRC-HYBRID` | `hybrid_story_text` | 叙事原文与局部镜头预设并存 | 保护明确锁定的预设轴，其余部分按叙事原文型处理 |
| `SRC-UNKNOWN` | 其他或信号冲突 | 还不足以稳定判型 | 暂停并返回澄清/补源 |

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| VAR-PLAN-SRC-01 | 输入 | `primary_story_source.source_type` 是什么 | `narrative/storyboard/hybrid/unknown` | 读取 manifest | P0 |
| VAR-PLAN-SRC-02 | 结构 | 是否已有可直接消费的镜头/场次/转场预设 | `dense/partial/none` | 扫描主故事源正文与 notes | P0 |
| VAR-PLAN-SRC-03 | 约束 | 这些预设是否被声明为必须保留 | `preserve_and_extend/preserve_only/standard` | 读取 manifest 扩展字段 | P0 |
| VAR-PLAN-SRC-04 | 下游 | `3-明细` 是否允许自由生成分镜骨架 | `free/guided/restricted` | 由 `detail_expansion_mode` 判定 | P1 |
| VAR-PLAN-SRC-05 | 风险 | 当前集/组切分是否可能打断上游预设链 | `low/medium/high` | 对照预设轴与边界建议 | P0 |

## Strategy Matrix

| case_id | source_mode | 主策略 | 必须保留 | 允许扩写 | 失败回退 |
| --- | --- | --- | --- | --- | --- |
| C-PLAN-SRC-01 | `SRC-NARRATIVE` | 正常进入 `1-分集/3-分组/4-节奏`，由下游生成分镜组织 | 叙事事实、角色关系、关键事件顺序 | `3-明细` 可从组级正文生成新的 `分镜明细[]` 骨架 | 若结构不足，回到增量规划或补源 |
| C-PLAN-SRC-02 | `SRC-STORYBOARD` | 规划阶段按“保真切分 + 锁定预设轴”处理 | 场次边界、镜头顺序、关键运镜/转场钩子、视点顺序 | `3-明细` 只可在预设点周围补质感、角色、氛围、摄影与必要细化 | 若预设互相冲突，先暂停并返回人工裁决 |
| C-PLAN-SRC-03 | `SRC-HYBRID` | 先区分“已锁镜头预设段”与“纯叙事段”，再混合规划 | 明确锁定的镜头/运镜/转场段 | 未锁段可按叙事原文型扩写 | 信号不足时退回 `SRC-STORYBOARD` 的保守规则 |
| C-PLAN-SRC-04 | `SRC-UNKNOWN` | 暂停规划，输出补充卡或澄清卡 | 不伪造来源类型 | 不允许进入下游扩写 | 等待 manifest 补充 |

## Storyboard Preset Protection Contract

当命中 `SRC-STORYBOARD` 或 `SRC-HYBRID` 且 `preset_retention_mode != standard` 时，默认保护以下轴：

- `scene_boundary`
- `shot_order`
- `camera_motif`
- `transition_hook`
- `viewpoint_order`

规则：

1. `1-规划` 可以为集级与组级收束边界，但不得越权洗掉上述预设轴。
2. `3-分组` 若发现某条边界会打断已锁定预设轴，默认优先保预设链，再解释量化偏差。
3. `3-明细` 只能顺着预设扩写，不得把已锁定轴改造成第二套主镜头逻辑。
4. 若用户授权重写，必须先在 manifest 或阶段验收报告中显式降级保护模式。

## Routing Card

- 判定顺序：`source_type -> preset_retention_mode -> detail_expansion_mode -> planning subroute`
- 冲突解消：用户显式要求 > manifest 中显式保护模式 > 子技能默认策略 > 量化优化建议
- unknown 默认路由：`暂停澄清`
- 失败重试上限：2 次
- 停止条件：无法稳定判断 `source_type`，或 storyboard 预设轴互相冲突到无法形成单一路由

## Required Writeback

根技能完成本轮规划后，至少要把以下结论落到可消费载体：

1. `projects/<项目名>/Init/story-source-manifest.yaml`
   - `source_type`
   - `preset_retention_mode`
   - `detail_expansion_mode`
   - `locked_preset_axes`
   - `preset_registry`
2. `projects/<项目名>/规划/validation-report.md`
   - `source_mode verdict`
   - `为什么这样保留/不保留预设`
3. `projects/<项目名>/编导/第N集.json` 的 `metadata.source_profile`
   - 供 `2-组间` / `3-明细` 读取
