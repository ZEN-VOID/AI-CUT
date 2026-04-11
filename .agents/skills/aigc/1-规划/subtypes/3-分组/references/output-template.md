# 3-分组 · 输出模板细则

## 模块定位

- 本文件是 `3-分组` 的标准输出模板模块。
- 模板骨架本体仍以 `templates/` 为真源，本文件负责解释“哪个产物承担什么职责、字段应落到哪一层、validator 会检查什么”。
- 它不替代模板文件，也不改动当前产物结构。

## Artifact Roles

| artifact | canonical template | 角色 | 不应承担的职责 |
| --- | --- | --- | --- |
| `group-plan.md` | `templates/group-plan.md` | 跨集总览、主路由与集级量化摘要 | 不能变成单集分组真源 |
| `第N集.md` | `templates/grouped-episode.md` | 单集分组真源，承载组表和组级容器 | 不能改写集边界，也不能拆成 `第N组.md` |
| `执行报告.md` | `templates/validation-report.md` | 输入清单、路由决议、边界证据、依赖检查、验收结论 | 不能替代组级容器本体 |

## Field-to-Artifact Mapping

| field_id | 默认落点 | 模板来源 |
| --- | --- | --- |
| `FIELD-GRP-INPUT-01` | `执行报告.md / 输入清单` | `templates/validation-report.md` |
| `FIELD-GRP-ROUTE-02` | `执行报告.md / 路由决议` | `templates/validation-report.md` |
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
| `estimated_duration_seconds` | `第N集.md / 分组计划表` | 当前组总时长的规划层投影，必须与 frontmatter 解析结果一致 |
| `estimated_duration_seconds` | `第N集.md / 组级章节 / 量化指标` | 组章节中的量化复写口径，不能与计划表或 frontmatter 漂移 |
| `默认组时长 / 分镜组时长映射 / 分镜时间读取链` | `执行报告.md / 量化摘要` | 供下游与审阅者确认组总时长来源链，而不是凭整集时长猜测 |

## 模板使用规则

1. 新建产物时，先从模板实例化，再填内容，不得从空白文档自由发挥。
2. 若需要说明跨集情况，写在 `group-plan.md`；若需要说明单集成组与组容器，写回对应 `第N集.md`。
3. 若某条理由只用于解释“为什么这样分”，优先落在 `执行报告.md`，不要让 `第N集.md` 背负过多过程叙述。

## Validator 对齐

`scripts/validate_grouping.py` 当前重点检查：

1. `group-plan.md` 是否具备总览结构和集级总览表
2. `执行报告.md` 是否具备输入、路由、边界、依赖、验收等必需区块
3. `第N集.md` 是否具备 frontmatter、分组计划表和完整组级章节
4. `默认组时长 / 分镜组时长映射` 是否存在且与每组 `estimated_duration_seconds` 对齐
5. 是否错误生成了 `第N组.md`

补充说明：

- 帧级 `time_range` 不属于 `3-分组` 当前模板的直接输出，但本阶段若遗漏组总时长基线，下游更容易触发 `FAIL-TIME-CONTINUITY` 或 `FAIL-TIME-OVERFLOW`。

## 局部变体边界

允许：

- 在模板骨架上增加项目特定说明
- 为某一项目补充 mode-specific 字段说明

不允许：

- 删除模板要求的强制区块
- 把单集真源从 `第N集.md` 挪到其他文件
- 用自由文本替代结构表与组级固定字段
