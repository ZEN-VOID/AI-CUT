# CONTEXT.md

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

## Repair Playbook

1. 先确认本轮是 `single-reviewer` 还是 `degraded-local-review`。
2. 锁定 `target_scope`，不要扩成整仓 review。
3. 先查技能真源，再查 registry / routes / HARNESS 同步。
4. 只要发现源层问题，就给出 layered trace 和 landing points。
5. 若无问题，也要交代 residual risks 与 verification gaps。

## Reusable Heuristics

- 对 reviewer subagent 来说，最重要的不是“观点多”，而是“边界清、证据硬、落点准”。
- 审计 skill 合同时，`SKILL.md + CONTEXT.md + registry + routes + HARNESS` 往往是最小完整检查面。
- `used_subagent_runtime: true` 只能证明 runtime 路径成立，不等于 findings 质量自然成立；仍要检查 evidence 和 landing points 是否足够具体。
- `subagetns/` 是当前仓库兼容路径，不应在单次完善任务中偷改为 `subagents/`。
