# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `command-subagent-preview` 的经验层知识库，不是过程日志。
- 每次调用本技能时，应自动预加载同目录 `CONTEXT.md`，用于顾问解析、边界控制与降级报告。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 明明显式给了顾问组，却仍被 `team.yaml` 自动覆盖 | advisor precedence | 把解析顺序改回“显式顾问组 > `team.yaml`” | 在 `SKILL.md` 固化顾问来源优先级 | 输出里 `advisor_source=explicit-advisor-group`，且 roster 与输入一致 |
| 把 `roles.*.source_skill_refs` 直接当成顾问授权 | roster resolution | 仅把 `source_skill_refs` 降为领域提示 | 在 `SKILL.md` 与 shared runtime 口径中写死“hint-only” | 非 `.agents/skills/team/**/SKILL.md` 条目不会直接进入 roster |
| 实际是本地顺序模拟，却写成正常顾问团路径 | runtime contract | 在结果中写明 `degraded-local-council` 与阻断来源 | 在父/子合同都固定 runtime 字段集 | 结果里出现 `runtime_mode + used_subagent_runtime + blocking_layer` |
| 输出只有泛建议，没有 `decision packet` | output discipline | 强制改回 `consensus / divergences / recommended_action / execution_plan` 结构 | 在 `SKILL.md` 固化 decision packet 字段 | 输出可直接被父级拿来执行或继续 ask-owner |
| 预演与事后 `review` 混层，既像审计又像执行 | boundary contract | 收回到“执行前 council preview”边界 | 在 sibling skills 中固定 preview/review 分工 | `preview` 不输出 findings-first 审计稿，`review` 不承担执行前决策 |
| 企图把 `subagetns/` 路径自动更正成 `subagents/` | path governance | 保留当前拼写，先报告兼容风险 | 真正重命名必须走全仓 rename+引用同步 | 本轮无悬空路径引用，且未擅自改名 |

## Repair Playbook

1. 先确认当前任务是不是“执行前预演”，而不是“执行后审计”。
2. 锁定 `task_scope + decision_focus + target_scope`，不要扩成整仓咨询。
3. 优先检查是否已显式传入 `advisor_group`；有就不要再被 `team.yaml` 覆盖。
4. 若需要回退到 `team.yaml`，先按角色解析 `members`，再看 `shared_agents`，最后才用 `source_skill_refs` 做提示或安全补选。
5. 只要 roster 已稳定且无上层阻断，就真实启动 subagents；否则显式降级。
6. 汇流结果必须压成 `decision packet`，让父级可直接消费。

## Reusable Heuristics

- `preview` 的价值不在于“顾问越多越好”，而在于“在执行前把关键分叉压缩成一份可执行决议包”。
- 对预演类 council 来说，显式顾问组比项目默认 roster 更强；项目 team 只是默认线索源，不是覆盖器。
- `team.yaml` 回退最好先按角色解，再看共享池；只有前两层不足时才做安全补选。
- `source_skill_refs` 很适合表达 provenance，不适合表达 runtime 授权；一旦把它升格，顾问团就会被阶段技能污染。
- `preview` 最终应该把父级送上更稳的执行路径，而不是生成第二份平行稿。
