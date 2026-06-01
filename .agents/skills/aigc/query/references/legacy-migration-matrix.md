# Legacy Query Migration Matrix

本文件记录 `.agents/skills/aigc-old/query` 语义迁入 `.agents/skills/aigc/query` 的 owner 去向，避免旧配置意图在 Skill 2.0 化时丢失。

| source | legacy intent | target owner | operation | semantic risk | validation gate |
| --- | --- | --- | --- | --- | --- |
| old `SKILL.md` frontmatter | `$aigc-query` 入口元数据 | `SKILL.md`、`agents/openai.yaml` | rewrite | low | validator checks frontmatter and metadata |
| Purpose / Stage Position | 卫星技能，不是主阶段 | `SKILL.md` | keep and adapt | low | `SKILL.md` states satellite boundary |
| Project Root Guard | 先解析 `PROJECT_ROOT` | `SKILL.md`、`steps/query-workflow.md` | split | low | field `FIELD-QUERY-01` |
| Truth Role Decision | 先判 truth role 再读文件 | `types/query-type-map.md`、`references/system-data-flow.md` | split | medium | mode table and carrier table align |
| old `1-Planning` mixed planning/grouping/report facts | 旧规划目录同时承载规划、格式、分组、节奏和报告线索 | `references/project-runtime-layout.md`、`types/query-type-map.md`、对应阶段执行报告 | split and annotate | medium | query maps episode split to `1-分集`、grouping to `5-分组`、validation/report facts to `执行报告.md` 或 legacy fallback |
| old `3-Detail` 主文件查询 | 旧编导/detail root | `references/project-runtime-layout.md` | adapt to `2-编导` with legacy fallback | medium | output marks legacy fallback |
| old `4-Design/5-Image/6-Video/7-Cut` | 旧资产阶段 | `references/project-runtime-layout.md` | adapt to `6-设计/7-图像/8-视频` | medium | no default answer points to legacy |
| Workflow Checklist | 查询执行顺序 | `steps/query-workflow.md` | rewrite as nodes | low | steps has route, evidence, gate |
| Conflict Rules | 存在不等于验收 | `review/review-contract.md`、`templates/output-template.md` | keep | low | output includes validation distinction |
| old `CONTEXT.md` | 经验层 Type Map/Heuristics | `CONTEXT.md`、`knowledge-base/query-heuristics.md` | split | low | context has Type Map/Repair/Heuristics |
| old `references/system-data-flow.md` | carrier 表 | `references/system-data-flow.md` | rewrite | medium | current Chinese stages are canonical |

## Non-Loss Notes

- 未把旧 `aigc-old/query` 的 `project-runtime-layout.md` 引用照搬过来，因为新 `aigc` 树当前不存在根 `_shared/`；本包用 `references/project-runtime-layout.md` 暂作局部共享布局。
- 旧英文阶段名不删除语义，只降级为 legacy compatibility。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 旧 `$aigc-query` 入口元数据是否已迁入当前 `SKILL.md` 与 `agents/openai.yaml`，且没有形成比 `SKILL.md` 更强的隐藏规则？ | `GATE-QUERY-01` | `FAIL-QUERY-CONTEXT` | `N0-load-contract` | 报告已加载的 `SKILL.md + CONTEXT.md`，并列出入口元数据只作为发现层证据。 |
| 旧 Purpose / Stage Position 是否被保留为“查询卫星技能”边界，而不是被误作 AIGC 主阶段或验收执行器？ | `GATE-QUERY-03` | `FAIL-QUERY-TRUTH-ROLE` | `N2-truth-role` | 输出 truth role 判定，并说明本技能只查询、不生成、不验收、不改写项目真源。 |
| 旧 Project Root Guard 是否仍先锁定真实 `projects/aigc/<项目名>/`，而不是把仓库根、技能目录或 registry 当项目根？ | `GATE-QUERY-02` | `FAIL-QUERY-PROJECT-ROOT` | `N1-project-root` | 报告 `project_root_lock` 的证据路径；无法唯一定位时报告 `needs_clarification`。 |
| 旧 Truth Role Decision 是否被拆入 `types/query-type-map.md` 与 carrier 表，并在读取文件前完成主次 query role 判定？ | `GATE-QUERY-03` | `FAIL-QUERY-TRUTH-ROLE` | `N2-truth-role` | 报告选中的 truth role、次要 role 以及消费的类型包。 |
| 旧 `1-Planning` 的规划、分组、报告混合语义是否被拆回当前中文阶段与执行报告，而不是继续用旧目录默认回答？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告 current carrier 与 legacy fallback 的对应关系，并标明旧 `1-Planning` 只作兼容回读。 |
| 旧 `3-Detail` 主文件查询是否默认改查 `2-编导/第N集.md`，只有证据需要时才标注 legacy JSON fallback？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 输出当前 `2-编导` 路径、旧 `3-Detail` 路径及 fallback 原因。 |
| 旧 `4-Design/5-Image/6-Video/7-Cut` 是否只作为 legacy compatibility，而不冒充当前 `6-设计/7-图像/8-视频` 的默认产物根？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前资产 carrier 优先级，并列出被降级的旧英文阶段名。 |
| 旧 Workflow Checklist 是否已被 `steps/query-workflow.md` 的节点网络承接，查询回答能回溯到具体读取、验收或治理节点？ | `GATE-QUERY-04` | `FAIL-QUERY-EVIDENCE` | `N6-answer` | 报告每条结论对应的节点、读取路径和缺口来源。 |
| 旧 Conflict Rules 中“存在不等于验收”的规则是否在完成/通过类回答中强制补读执行报告或验收载体？ | `GATE-QUERY-05` | `FAIL-QUERY-VALIDATION` | `N4-validation-crosscheck` | 报告产物存在、执行报告存在、验收通过三者的区分证据；缺失时写明未见验收证据。 |
| 旧 `CONTEXT.md` 经验是否只进入当前 `CONTEXT.md` / `knowledge-base`，没有反向覆盖 `SKILL.md`、references 或运行时 carrier 真源？ | `GATE-QUERY-01` | `FAIL-QUERY-CONTEXT` | `N0-load-contract` | 报告经验层只作为查询策略参考，并列出规范真源仍来自 `SKILL.md`、`references/`、`steps/`、`review/`。 |
| 旧 `system-data-flow.md` carrier 表迁移后，是否以当前中文阶段为 canonical，并把英文旧阶段明确标为 legacy only？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告 canonical carrier 表读取结果、legacy 标注和回答中使用的真实路径。 |
