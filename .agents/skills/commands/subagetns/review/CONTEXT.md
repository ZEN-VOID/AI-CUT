# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3252
current_lines: 47
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

## Purpose & Loading Contract

- 本文件是 `command-subagent-review` 的经验层知识库，不是过程日志。
- 每次调用本技能时，应自动预加载同目录 `CONTEXT.md`，用于 findings 组织、边界控制与降级报告。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| reviewer 输出只有泛建议，没有 evidence path / impact / landing point | findings discipline | 强制改成 findings-first 模板 | 在 `SKILL.md` 固定 findings 字段集 | 输出包含 severity、dimension、evidence path、impact、recommended action、confidence |
| 实际是本地顺序模拟，却写成正常 subagent review | runtime contract | 在结果中写明 `degraded-local-review` 与阻断来源 | 在父/子合同都固定降级报告字段 | 结果里出现 `runtime_mode + used_subagent_runtime + blocking_layer` |
| review scope 漫游到整仓，导致结果失焦 | scope contract | 重新锁定 `target_scope` 与最少必要真源 | 在技能合同中强调 bounded review | 输出只覆盖显式目标与必要上游文件 |
| 改了 skill 合同却没同步 registry / routes / HARNESS | carrier sync | 补 registry / routes / HARNESS | 把“合同变更即 carrier sync”沉到 review heuristics | 变更后 `rg` 可命中 skill、registry、routes、HARNESS 的一致回链 |
| 企图把 `subagetns/` 路径自动更正成 `subagents/` | path governance | 保留当前拼写，先报告兼容风险 | 真正重命名必须走全仓 rename+引用同步 | 本轮无悬空路径引用，且未擅自改名 |
| 父级没有给 `target_scope` 或 `review_goal`，reviewer 仍自行发现目标 | input contract | 停止审计，要求父级补齐 bounded packet | 父级 orchestrator 必须在 dispatch 前完成 scope/goal 裁决 | 输出包含 blocked 原因，而不是扩成自由巡检 |
| 需要多个 reviewer 会诊，却把本技能当 council orchestrator | mode arbitration | 回退到父级 orchestrator 或先走 `subagetns/preview` | 把多 reviewer 编排留给父级，reviewer 只消费单 reviewer packet | 本技能输出不含 parallel council / synthesis 结果 |
| 把 changelog、聊天记录或历史叙述当作业务真源 | truth-source discipline | 改读目标文件与最少必要上游真源 | 将历史材料仅作为线索，不作为最终 evidence_path | finding 的 evidence_path 可定位到当前 repo 文件或明确 runtime 证据 |
| finding 发现源层漂移，却只建议“注意同步” | landing-point precision | 拆成立即修复落点与系统预防落点 | 每条源层 finding 都要求 recommended_action 可执行 | finding 能指向具体文件、字段、检查命令或父级回收动作 |

## Repair Playbook

1. 先确认调用 packet 是否含 `target_scope`、`review_goal`、`output_mode` 与 `runtime_context`；缺任一关键项时阻塞回父级。
2. 确认本轮是 `single-reviewer` 还是 `degraded-local-review`，并写清 `blocking_layer`、`expected_path`、`actual_path`。
3. 锁定目标边界，只读取目标文件、同目录合同和与结论直接相关的 registry / routes / HARNESS / 父级真源。
4. 对每条问题走 `Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`。
5. 输出 findings-first；每条 finding 必须有 severity、dimension、evidence_path、impact、recommended_action、confidence。
6. 若无问题，输出 `findings: []`，同时说明 residual risks 与 verification gaps，避免把“没扫到”写成“绝对没风险”。

## Reusable Heuristics

- 对 reviewer subagent 来说，最重要的不是“观点多”，而是“边界清、证据硬、落点准”。
- 审计 skill 合同时，`SKILL.md + CONTEXT.md + registry + routes + HARNESS` 往往是最小完整检查面。
- `used_subagent_runtime: true` 只能证明 runtime 路径成立，不等于 findings 质量自然成立；仍要检查 evidence 和 landing points 是否足够具体。
- `subagetns/` 是当前仓库兼容路径，不应在单次完善任务中偷改为 `subagents/`。
- 本技能的“verdict”只服务 reviewer 结果，不等于父级最终裁决；最终 patch、汇流和落盘仍归父级。
- 如果用户目标是“修复问题”而不是“审计问题”，本技能最多给 patch_plan 和 landing points，不直接变成执行器。
- 对 route / registry 漂移，优先报告哪一层是 canonical owner，再列同步面；不要把所有修复都堆回本技能。

## Promotion Backlog

- 增加轻量 schema 校验器，检查 `command_subagent_review_result` 是否含 runtime、finding、risk、verification 字段。
- 为父级 orchestrator 增加 dispatch preflight，缺 `target_scope` 或 `review_goal` 时不启动 reviewer。
- 若未来正式重命名 `subagetns/`，需要单独 PRP 覆盖全仓路径扫描、引用同步和兼容迁移。
