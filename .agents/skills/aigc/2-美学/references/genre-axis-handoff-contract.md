# Genre Axis Handoff Contract

本合同是 `2-美学` 父级 `类型风格.md` 的题材归属交接细则。它不是子技能，不参与 6 路美学 subagents 并发，不拥有独立输出路径、写回权限或 review verdict。

## Purpose

`2-美学` 负责在编剧前完成项目级题材归属判定，并把判定结果写入 `类型风格.md`。`4-编剧` 后续只消费该归属结果，再结合自身 `presentation_axis` 形成 `呈现方式 x 题材类型` 的剧本策略。

本合同只回答三件事：

1. 这个项目的主题材归属是什么。
2. 该归属由哪些可复核 source anchor 和题材维度支撑。
3. 下游 `4-编剧` 应如何继承、降级或处理冲突。

## Canonical Genre Axis

| axis_id | label | primary_signals | downstream_package_hint |
| --- | --- | --- | --- |
| `wuxia` | `武侠剧` | 江湖规矩、门派身份、师承关系、武功招式、兵器、侠义选择、武林名声、镖局/擂台/客栈/山门等空间 | `4-编剧/types/genre/武侠剧.md` |
| `xuanhuan` | `玄幻剧` | 修炼体系、境界、灵力/灵气、宗门等级、秘境、法宝、血脉、天命、阵法、丹药、妖兽等规则材料 | `4-编剧/types/genre/玄幻剧.md` |
| `kehuan` | `科幻剧` | 科技系统、实验装置、AI/算法、太空/星际、时间循环、空间异常、末世科技、数据证据、科研伦理 | `4-编剧/types/genre/科幻剧.md` |
| `mohuan` | `魔幻剧` | 魔法规则、诅咒、神谕、王国/部族、异族、魔物、圣物、黑暗力量、契约、祭坛等奇幻材料 | `4-编剧/types/genre/魔幻剧.md` |
| `generic` | `通用叙事/其他题材` | 不稳定命中上述四类，或题材只作为弱背景；原始题材名仍可保存在 `raw_genre_label` | `4-编剧/types/default/default.md` |

## Genre Axis Classification Fields

`类型风格.md` 必须包含 `Genre Axis Classification`，字段至少覆盖：

| field | requirement |
| --- | --- |
| `raw_genre_label` | LLM 对项目题材的自然语言判断，例如 `武侠复仇短剧`、`末世科幻悬疑`、`历史正剧`。 |
| `primary_genre_axis` | 规范化主轴：`wuxia` / `xuanhuan` / `kehuan` / `mohuan` / `generic`。 |
| `primary_genre_name` | 与主轴对应的中文题材名；`generic` 时写原始题材名或 `通用叙事`。 |
| `secondary_genre_axes` | 0-3 个副题材轴；只能写有 source evidence 的题材，不能为了丰富而硬补。 |
| `classification_basis` | 题材判定依据，至少覆盖世界规则、冲突载体、能力/科技/魔法机制、核心空间材料、观众类型承诺中的 3 类。 |
| `source_anchor_evidence` | 关键 source anchor 列表，必须能回指 `1-分集` 或用户指定 source。 |
| `genre_confidence` | `high` / `medium` / `low`。`low` 时不得强行命中四类题材包，应降级或标记冲突。 |
| `genre_conflict_state` | `none` / `multi_axis` / `insufficient_signal` / `source_conflict` / `unsupported_by_source`。 |
| `fallback_policy` | 信号不足、冲突命中或不属于四类题材时，下游应如何使用 `generic` 或请求补证。 |
| `screenwriting_handoff` | 给 `4-编剧` 的继承口径：可继承题材轴、标志性元素、表现技巧、禁区和冲突处理，不包含剧本创作细节。 |

## Classification Rules

1. 先判 `raw_genre_label`，再映射 `primary_genre_axis`，不得直接用关键词命中题材轴。
2. 主题材必须由 source 的世界规则、冲突载体、能力/科技/魔法机制、空间材料和观众承诺共同支撑。
3. 多题材并存时，只选择 1 个 `primary_genre_axis`；副题材最多 3 个，并写明其不改变主题材归属的理由。
4. 不属于四类题材但有明确项目题材时，`primary_genre_axis=generic`，`raw_genre_label` 保留原始题材名。
5. 题材归属只给下游提供识别与表现边界，不替 `4-编剧` 写剧情、节奏、对白或高潮尾钩。

## Handoff To Screenwriting

`4-编剧` 消费本合同输出时：

- 优先读取 `primary_genre_axis`，匹配自身 `types/genre/*.md` 或 `types/default/default.md`。
- 读取 `source_anchor_evidence` 与 `classification_basis` 作为 `type_axis_selection.upstream_type_style_basis`。
- 若 `genre_conflict_state != none` 或 `genre_confidence=low`，必须在 `Type Axis Selection Map` 中记录冲突或 fallback。
- 不得用单集 source 信号无证据推翻 `2-美学` 的项目级主题材；只能做副题材校准。

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `类型风格.md` 是否写出规范化题材轴，而不只写自然语言题材标签？ | `GATE-AES-11-TYPE-STYLE` | `FAIL-AES-GENRE-AXIS-HANDOFF` | `N2-PACKET` / `Type Style Profile Contract` | `genre_axis_handoff_profile`、`Genre Axis Classification` |
| 题材轴是否有可复核 source anchor 和分类依据？ | `GATE-AES-11-TYPE-STYLE` | `FAIL-AES-GENRE-AXIS-EVIDENCE` | `N2-PACKET` | `source_anchor_evidence`、`classification_basis` |
| 题材冲突、低置信度或非四类题材是否有 fallback？ | `GATE-AES-11-TYPE-STYLE` | `FAIL-AES-GENRE-AXIS-FALLBACK` | `N2-PACKET` / `N7-HANDOFF` | `genre_conflict_state`、`fallback_policy`、`screenwriting_handoff` |
