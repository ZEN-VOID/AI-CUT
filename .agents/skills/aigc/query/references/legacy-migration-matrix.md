# Legacy Query Migration Matrix

本文件记录 `.agents/skills/aigc-old/query` 语义迁入 `.agents/skills/aigc/query` 的 owner 去向，避免旧配置意图在 Skill 2.0 化时丢失。

| source | legacy intent | target owner | operation | semantic risk | validation gate |
| --- | --- | --- | --- | --- | --- |
| old `SKILL.md` frontmatter | `$aigc-query` 入口元数据 | `SKILL.md`、`agents/openai.yaml` | rewrite | low | validator checks frontmatter and metadata |
| Purpose / Stage Position | 卫星技能，不是主阶段 | `SKILL.md` | keep and adapt | low | `SKILL.md` states satellite boundary |
| Project Root Guard | 先解析 `PROJECT_ROOT` | `SKILL.md`、`steps/query-workflow.md` | split | low | field `FIELD-QUERY-01` |
| Truth Role Decision | 先判 truth role 再读文件 | `types/query-type-map.md`、`references/system-data-flow.md` | split | medium | mode table and carrier table align |
| old `1-Planning` mixed planning/grouping/report facts | 旧规划目录同时承载规划、格式、分组、节奏和报告线索 | `references/project-runtime-layout.md`、`types/query-type-map.md`、对应阶段执行报告 | split and annotate | medium | query maps episode split to `1-分集`、grouping to `4-分组`、validation/report facts to `执行报告.md` 或 legacy fallback |
| old `3-Detail` 主文件查询 | 旧编导/detail root | `references/project-runtime-layout.md` | adapt to `2-编导` with legacy fallback | medium | output marks legacy fallback |
| old `4-Design/5-Image/6-Video/7-Cut` | 旧资产阶段 | `references/project-runtime-layout.md` | adapt to `5-设计/6-图像/7-视频` | medium | no default answer points to legacy |
| Workflow Checklist | 查询执行顺序 | `steps/query-workflow.md` | rewrite as nodes | low | steps has route, evidence, gate |
| Conflict Rules | 存在不等于验收 | `review/review-contract.md`、`templates/output-template.md` | keep | low | output includes validation distinction |
| old `CONTEXT.md` | 经验层 Type Map/Heuristics | `CONTEXT.md`、`knowledge-base/query-heuristics.md` | split | low | context has Type Map/Repair/Heuristics |
| old `references/system-data-flow.md` | carrier 表 | `references/system-data-flow.md` | rewrite | medium | current Chinese stages are canonical |

## Non-Loss Notes

- 未把旧 `aigc-old/query` 的 `project-runtime-layout.md` 引用照搬过来，因为新 `aigc` 树当前不存在根 `_shared/`；本包用 `references/project-runtime-layout.md` 暂作局部共享布局。
- 旧英文阶段名不删除语义，只降级为 legacy compatibility。
