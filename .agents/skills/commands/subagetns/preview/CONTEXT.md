# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3365
current_lines: 56
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

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
| `task_scope / decision_focus / target_scope` 不完整，顾问团开始泛化发散 | input contract | 先让父级补齐 bounded 任务、待决问题和目标范围 | 父级 dispatch 前增加输入字段检查 | 输出中不出现整仓开放咨询，必要时 `decision_state=blocked` |
| roster 解析超过必要范围，拉起整棵 team 技能树 | roster scope | 收束到 `1-4` 个与 `target_type + focus` 匹配的顾问 | 把“安全补选只补足必要问题域”作为调度前检查 | `resolved_advisors` 数量可解释，`advisor_source_trace` 能追溯每个来源 |
| `team.yaml.enabled=false` 时完全忽略项目线索，导致显式预演无顾问 | team override | 若父级显式调用本技能，可把 `team.yaml` 作为手工 override 线索源 | 输出中区分手工 override 与常驻运行时 | `advisor_source_trace` 写明 override，不宣称 team 常驻启用 |
| 本技能直接写回父级 canonical 产物 | truth ownership | 停止写回，只返回 advisory `decision packet` | 父级 orchestrator 保持最终裁决与落盘权 | 本技能输出没有业务总稿或最终 patch，只含建议、拒绝项和执行计划 |

## Repair Playbook

1. 先确认当前任务是不是“执行前预演”，而不是“执行后审计”。
2. 锁定 `task_scope + decision_focus + target_scope`，不要扩成整仓咨询。
3. 优先检查是否已显式传入 `advisor_group`；有就不要再被 `team.yaml` 覆盖。
4. 若需要回退到 `team.yaml`，先按角色解析 `members`，再看 `shared_agents`，最后才用 `source_skill_refs` 做提示或安全补选。
5. 把候选 roster 控制在 `1-4` 个顾问；无法解释来源时阻塞，不用“完整性”补空顾问。
6. 只要 roster 已稳定且无上层阻断，就真实启动 subagents；否则显式降级。
7. 汇流结果必须压成 `decision packet`，让父级可直接消费。
8. 若没有形成稳定结论，明确写 `decision_state=blocked|needs-owner-choice`，不要把不确定包装成共识。

## Reusable Heuristics

- `preview` 的价值不在于“顾问越多越好”，而在于“在执行前把关键分叉压缩成一份可执行决议包”。
- 对预演类 council 来说，显式顾问组比项目默认 roster 更强；项目 team 只是默认线索源，不是覆盖器。
- `team.yaml` 回退最好先按角色解，再看共享池；只有前两层不足时才做安全补选。
- `source_skill_refs` 很适合表达 provenance，不适合表达 runtime 授权；一旦把它升格，顾问团就会被阶段技能污染。
- `preview` 最终应该把父级送上更稳的执行路径，而不是生成第二份平行稿。
- `used_subagent_runtime` 是硬事实字段，不是语气字段；只要没真实启动顾问 subagents，就必须写降级路径。
- `needs-owner-choice` 比强行“达成共识”更有价值；预演技能可以把分歧交给 owner，不必伪造裁决。
- 顾问来源解释要比顾问观点更先稳定；来源不清时，后续共识没有治理价值。

## Promotion Backlog

- [ ] 候选规则: 为 `decision packet` 增加轻量字段完整性校验，防止泛建议替代结构化回包。
  - 证据计数: 0
  - 目标落点: 父级 orchestrator 或本技能的 shared validator
  - 状态: pending
- [ ] 候选规则: 将 `degraded-local-council` 的 `blocking_layer / expected_path / actual_path / missing_runtime` 做成固定片段。
  - 证据计数: 0
  - 目标落点: `SKILL.md` 输出说明或共享 council runtime 规范
  - 状态: pending
