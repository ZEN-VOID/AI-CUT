# 3-分组 · 输出模板细则

## 模块定位

- 本文件负责说明 `3-分组` 当前有哪些产物、字段落点在哪里、validator 检查什么。
- 模板骨架仍以 `templates/` 为真源。

## Artifact Roles

| artifact | canonical template | 角色 | 不应承担的职责 |
| --- | --- | --- | --- |
| `group-plan.md` | `templates/group-plan.md` | 跨集总览、边界裁决摘要与集级量化摘要 | 不能变成规划阶段最终集级主稿 |
| `第N集.md` | `templates/grouped-episode.md` | 单集分组真源，承载组表和组级容器 | 不能改写集边界，也不能冒充父级 `规划/第N集.md` |
| `执行报告.md` | `templates/validation-report.md` | 输入清单、边界裁决摘要、候选边界、依赖检查、验收结论 | 不能替代组级容器本体 |

## Field-to-Artifact Mapping

| field_id | 默认落点 | 模板来源 |
| --- | --- | --- |
| `FIELD-GRP-INPUT-01` | `执行报告.md / 输入清单` | `templates/validation-report.md` |
| `FIELD-GRP-DECISION-02` | `执行报告.md / 边界裁决摘要` | `templates/validation-report.md` |
| `FIELD-GRP-BOUNDARY-03` | `执行报告.md / 候选边界` | `templates/validation-report.md` |
| `FIELD-GRP-PLAN-04` | `第N集.md / 分组计划表` | `templates/grouped-episode.md` |
| `FIELD-GRP-FILES-05` | `第N集.md / 组级容器` | `templates/grouped-episode.md` |
| `FIELD-GRP-DEP-06` | `执行报告.md / 依赖与并行性检查` | `templates/validation-report.md` |
| `FIELD-GRP-QA-07` | `执行报告.md / 验收结论与返工项` | `templates/validation-report.md` |

## Timing Handoff Mapping

| timing artifact | 默认落点 | 说明 |
| --- | --- | --- |
| `默认组时长` | `第N集.md / frontmatter` | 当前集的默认组总时长；无上游覆盖时写 `15秒` |
| `分镜组时长映射` | `第N集.md / frontmatter` | 只登记偏离默认值的组；无偏离时写 `{}` |
| `时长偏离证据` | `第N集.md / frontmatter` | 若 `分镜组时长映射` 非空，则必须登记非空上游证据；无偏离时写 `[]` |
| `estimated_duration_seconds` | `第N集.md / 分组计划表` | 当前组总时长的规划层投影，必须与 frontmatter 解析结果一致 |
| `estimated_duration_seconds` | `第N集.md / 组级章节 / 量化指标` | 组章节中的量化复写口径，不能与计划表或 frontmatter 漂移 |
| `source_span` | `第N集.md / 分组计划表` | 主故事源为 `storyboard_script / hybrid_story_text` 时，优先写成可机读镜号范围，供 validator 回算 `effective_text_chars` |
| `默认组时长 / 分镜组时长映射 / 分镜时间读取链` | `执行报告.md / 量化摘要` | 供下游与审阅者确认组总时长来源链 |
| `外部分镜预设模式` | `第N集.md / frontmatter` | 当前集是否继承 storyboard 预设保护模式 |
| `外部分镜锚点登记` | `第N集.md / frontmatter` | 当前集命中的 `preset_registry` 投影 |
| `preset_anchor_policy / preset_anchor_ids` | `第N集.md / 分组计划表` | 声明当前组对外部分镜锚点采取什么策略，并登记命中锚点 ID |

## 模板使用规则

1. 新建产物时，先从模板实例化，再填内容。
2. `group-plan.md` 和 `执行报告.md` 负责解释“为什么这样分”，`第N集.md` 负责承载正式组容器。
3. 当父级 `1-规划` 走全链时，本子路径 `第N集.md` 是聚合输入，而不是第二份父级主稿。

## Validator 对齐

`scripts/validate_grouping.py` 当前重点检查：

1. `group-plan.md` 是否具备边界裁决摘要和集级总览表
2. `执行报告.md` 是否具备输入、裁决、边界、依赖、验收等必需区块
3. `第N集.md` 是否具备 frontmatter、分组计划表和完整组级章节
4. `grouping_method` 是否显式写为 `multidimensional_quantized`
5. `默认组时长 / 分镜组时长映射` 是否存在且与每组 `estimated_duration_seconds` 对齐
6. `window_status` 是否全部为 `ok`
7. `外部分镜预设模式 / 外部分镜锚点登记 / preset_anchor_policy / preset_anchor_ids` 是否存在且可回查
8. 是否错误生成 `第N组.md`
9. 当主故事源是 `storyboard_script / hybrid_story_text` 且 `source_span` 可解析时，是否已从主源自动回算 `effective_text_chars`
