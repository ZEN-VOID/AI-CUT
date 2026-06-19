# 4-编剧 Type Map

`types/` 保存 `4-编剧` 的二维类型配置。它只提供类型识别、策略偏置和组合画像，不替代 `SKILL.md` 的 `Type Routing Matrix`、思行节点、review gate、输出路径或写回权限。

## Type Axes

一次编剧任务必须先形成两个轴的选择，再把二者组合为最终编剧策略：

1. `presentation_axis`：剧本呈现方式，当前支持 `正剧`、`解说剧`。
2. `genre_axis`：题材类型，当前支持 `武侠剧`、`玄幻剧`、`科幻剧`、`魔幻剧`，无法稳定命中时回退 `default`。

最终消费口径不是单独的题材标签，而是：

```text
screenwriting_type_combination = presentation_axis x genre_axis
```

例如：`解说剧 x 武侠剧`、`正剧 x 科幻剧`、`解说剧 x 魔幻剧`。

## Package Index

| package_id | axis | path | match_signals | load_mode | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `presentation-zhengju` | `presentation_axis` | `types/presentation/正剧.md` | 无显式解说剧要求；用户要求正剧、影视化正剧、按当前方式改编 | default_selectable | `presentation-jieshuoju` | `SKILL.md` |
| `presentation-jieshuoju` | `presentation_axis` | `types/presentation/解说剧.md` | 用户或项目长期记忆显式要求解说剧、解说模式、旁白解说剧 | explicit_selectable | `presentation-zhengju` | `SKILL.md` |
| `genre-wuxia` | `genre_axis` | `types/genre/武侠剧.md` | 江湖、门派、侠义、师承、武功、兵器、恩怨、武林规矩 | selectable | none | `types/default/default.md` |
| `genre-xuanhuan` | `genre_axis` | `types/genre/玄幻剧.md` | 修炼体系、境界、灵力、宗门、秘境、法宝、血脉、天命 | selectable | none | `types/default/default.md` |
| `genre-kehuan` | `genre_axis` | `types/genre/科幻剧.md` | 科技系统、实验、AI、时间/空间异常、星际、末世科技、科学规则 | selectable | none | `types/default/default.md` |
| `genre-mohuan` | `genre_axis` | `types/genre/魔幻剧.md` | 魔法、诅咒、神谕、异族、魔物、圣物、黑暗力量、奇幻王国 | selectable | none | `types/default/default.md` |
| `genre-narrative-default` | `genre_axis` | `types/default/default.md` | 未命中稳定题材，或题材只作为弱背景 | fallback_always_available | none | `SKILL.md` |

## Default Package Rule

- `presentation_axis` 默认包是 `types/presentation/正剧.md`：仅当用户请求、项目长期记忆或最新任务指令没有显式 `解说剧` 信号时启用。
- `presentation_axis` 不允许因为 source 叙述较多、对白较少或用户要求“更好理解”而自动切换到 `types/presentation/解说剧.md`。
- `genre_axis` 默认包是 `types/default/default.md`：仅当 `2-美学/类型风格.md` 缺失稳定题材、source 信号不足，或题材只是弱背景时启用。
- 若 `2-美学/类型风格.md` 已包含 `Genre Axis Classification`，必须优先读取其中的 `primary_genre_axis`、`raw_genre_label`、`classification_basis`、`source_anchor_evidence`、`genre_confidence`、`genre_conflict_state` 和 `fallback_policy`，再决定 `genre_package`。
- 默认题材包不得覆盖已经明确的 `武侠剧`、`玄幻剧`、`科幻剧`、`魔幻剧` 主体材；若题材冲突，应写入 `type_axis_selection.conflict_state` 并回到父级 gate。
- 默认包只提供兜底叙事策略，不拥有输出路径、写回权限、review verdict 或最终 pass 权。

## Type Profile Schema

```yaml
type_axis_selection:
  presentation_mode: "zhengju | jieshuoju"
  presentation_package: "types/presentation/正剧.md | types/presentation/解说剧.md"
  primary_genre_type: "wuxia | xuanhuan | kehuan | mohuan | generic"
  genre_package: "types/genre/<题材>.md | types/default/default.md"
  secondary_genre_types: []
  source_signals: []
  upstream_genre_axis: ""
  upstream_genre_axis_evidence: ""
  upstream_type_style_basis: ""
  confidence: "high | medium | low"
  conflict_state: "none | mode_conflict | genre_conflict | insufficient_signal"
  fallback_policy: ""

presentation_type_profile:
  voice_policy: ""
  source_unit_policy: ""
  field_variety_policy: ""
  evidence_required: []
  prohibited_operations: []

genre_type_profile:
  genre_contract: ""
  dramatic_pressure_bias: ""
  rhythm_bias: ""
  controlled_supplement_bias: ""
  field_material_bias: ""
  prohibited_drift: []
  evidence_required: []

screenwriting_type_combination_profile:
  combination_id: "<presentation_mode>x<primary_genre_type>"
  selected_presentation_strategy: ""
  selected_genre_strategy: ""
  combined_voice_and_field_strategy: ""
  combined_rhythm_strategy: ""
  combined_dramatization_strategy: ""
  combined_climax_hook_strategy: ""
  boundary_checks: []
  report_landing: "Type Axis Selection Map / Screenwriting Type Combination Profile"
```

## Selection Rules

1. 先判定 `presentation_axis`：
   - 有显式 `解说剧` 信号时选择 `presentation-jieshuoju`。
   - 无显式模式时选择 `presentation-zhengju`，不得因 source 叙述多而自动切到解说剧。
   - 同轮同时要求 `正剧` 与 `解说剧` 且无法按最新指令裁决时，暂停澄清。
2. 再判定 `genre_axis`：
   - 优先读取 `2-美学/类型风格.md` 的 `Genre Axis Classification` 与 `primary_genre_axis`；若该结构存在，`genre_axis` 以它为项目级题材真源。
   - 同步读取主题材、原始题材标签、标志性元素、题材专属表现技巧、`classification_basis` 和 `source_anchor_evidence`，写入 `upstream_type_style_basis` 与 `upstream_genre_axis_evidence`。
   - 其次从 source 的人物目标、世界规则、冲突载体、场景材料和核心风险识别题材。
   - 题材信号不足时使用 `types/default/default.md`，不得硬套武侠/玄幻/科幻/魔幻。
3. 最后组合：
   - 呈现方式决定声音策略、source 单元覆盖、字段节奏和模式证据。
   - 题材类型决定戏剧压力、节奏偏置、可用场面材料、补写边界和高潮/尾钩材料。
   - 组合结果写入 `screenwriting_type_combination_profile`，由 `N2/N4/N6/N8` 消费。

## Combination Landing Matrix

| combination_layer | decided_by | affects | must_not_do |
| --- | --- | --- | --- |
| `voice_and_field_strategy` | `presentation_axis` first, `genre_axis` second | 陈述性信息转语音、旁白/对白/内心独白使用、字段节奏 | 用题材口吻覆盖 source 事实；让题材包新增模式字段 |
| `dramatic_pressure_strategy` | `genre_axis` | 角色压力、冲突承托、场面阻力、心理外化材料 | 新增 source 不支持的能力、规则、道具功能或关系 |
| `rhythm_strategy` | `presentation_axis x genre_axis` | 节奏密度、信息释放顺序、尾钩形式 | 把题材标签直接套成“燃/爽/高级” |
| `controlled_supplement_strategy` | `Dramatized Adaptation Supplement Contract` plus selected type packages | 外化心理、补过渡、补阻力、补动机触发、状态承托 | 未经授权改变因果、结局、人物选择、世界规则 |
| `report_evidence_strategy` | parent `SKILL.md` | `Type Axis Selection Map`、`Screenwriting Type Combination Profile`、既有必填证据 | 让 `types/` 自己决定 pass/fail 或输出路径 |

## Loading Flow

1. 收集用户输入、source、项目记忆、`2-美学/类型风格.md`、平台/时长/制作限制。
2. 加载本文件和 `types/default/default.md`。
3. 按 `Selection Rules` 选择一个 `presentation_axis` 包和一个主 `genre_axis` 包。
4. 形成 `type_axis_selection`、`presentation_type_profile`、`genre_type_profile`。
5. 回到 `N2-SCR-GENRE-NARRATIVE`，生成 `screenwriting_type_combination_profile`、`genre_narrative_profile` 和 `beat_inventory`。
6. `N4-SCR-RHYTHM-ENGINE`、`N5-SCR-CLIMAX-HOOK`、`N6-SCR-CANDIDATE-DRAFT` 只能消费组合画像，不得让类型包改写父级节点或输出合同。

## Conflict And Unknown Policy

| condition | policy | report_landing |
| --- | --- | --- |
| 无显式呈现方式 | 默认 `正剧` | `type_axis_selection.default_applied=true` |
| 同时命中正剧与解说剧且无法裁决 | 暂停澄清 | `conflict_state=mode_conflict` |
| 多个题材同时命中 | 选 1 个主题材、最多 2 个副题材；节奏机制最多 2 主 1 辅 | `secondary_genre_types` |
| 题材证据不足 | 回退 `genre-narrative-default` | `conflict_state=insufficient_signal` |
| 组合策略与 source 保真冲突 | source 保真优先，题材策略降级或 N/A | `boundary_checks` |

## Anti-Patterns

- 不要把 `正剧/解说剧` 和 `武侠/玄幻/科幻/魔幻` 混在同一层；前者是呈现方式轴，后者是题材轴。
- 不要把题材包升格成子技能；现阶段它们只是 `types/` 策略卡。
- 不要让 `types/` 自己决定输出路径、改写权限、review verdict 或最终 pass。
- 不要在类型包里保存执行经验；经验写 `CONTEXT.md`。
