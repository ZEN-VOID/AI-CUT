# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design/1-主体清单` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/1-主体清单/SKILL.md` 时，应在 `aigc -> 3-Detail -> 1-主体清单/_shared` 之后加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `场景 / 角色 / 道具` 各自解释不同的 detail 输入口径 | 共享输入合同层 | 回到 `_shared/detail-output-consumption-contract.md` 统一第一输入根 | 父层 `SKILL.md` 固定 shared input order 与 fallback 规则 | 三域都先读同一份 `3-Detail/第N集.json` |
| `服装` 跳过 `角色清单.json` 直接从导演 JSON 发明对象池 | 依赖门层 | 回退到 `角色 -> 服装` 顺序 | 在父层固定 `服装` 的前置条件与 full-build 顺序 | `服装` 只有在角色清单稳定后才执行 |
| 某个 leaf 试图生成并列总稿或把 manifest 当主稿 | 输出治理层 | 恢复 domain-local catalog 为唯一对象池真源 | 在 `_shared/list-output-contract.md` 与父层同步锁定 catalog / sidecar 分层 | 没有 `1-主体清单.json` 或 manifest 承载业务事实 |
| full-build 时四域全串行导致成本过高 | 调度拓扑层 | 回到 `场景 + 角色 + 道具` 先行、`服装` 后置 | 在父层明确“并行可候选 + 依赖门”的调度规则 | 全量构建既满足依赖，又不过度串行 |
| leaf 输出存在，但 `2-主体设计` 仍需重猜主键 | canonical source 层 | 回查对象池主键与 shot/group 回链 | 在父层验收中强制检查 catalog 与 bridge 的 traceability | 下游直接消费，不再补猜 identity |

## Repair Playbook

1. 先确认本轮命中的是哪一个 domain，避免把父层问题误修到某个 leaf。
2. 再检查 `3-Detail` 输入口径是否统一，尤其是 canonical 与 legacy fallback 是否混写。
3. 若命中 `服装`，先检查 `角色清单.json` 是否存在并属于当前 episode。
4. 再核对各域输出是否仍遵守 `catalog + manifest + optional sidecars` 的分层。
5. 最后才汇总到 `projects/aigc/<项目名>/4-Design/validation-report.md`，记录当前轮 dispatch、缺口与下一入口。

## Reusable Heuristics

- `1-主体清单` 最容易漂移的不是 leaf 内部抽取，而是四域对共享输入口径的不同解释。
- `服装` 属于跨域消费链，因此父层必须显式守住 `角色 -> 服装` 的依赖门。
- 对父层来说，最稳的交付不是“再汇总一份总稿”，而是保证四个 domain catalog 都能被 `2-主体设计` 直接读取。
- `全量构建` 不等于“所有 leaf 都串行”; 真正的顺序约束只有依赖门，剩余应以 selective dispatch 降低成本。
- stage-level `validation-report.md` 只应记录 coverage、缺口和 handoff，不应回写 domain 事实。
