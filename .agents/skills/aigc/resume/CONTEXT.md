# CONTEXT.md

本文件是 `aigc-resume` 的经验层知识库，不是执行流水账。它用于恢复范围判定、危险动作过滤、runtime 漂移识别和唯一回接 heuristics。

## Purpose & Loading Contract

- 每次调用 `$aigc-resume` 时，必须同时加载同目录 `CONTEXT.md`。
- 本文件只保存经验性 Type Map、Repair Playbook 与 Reusable Heuristics，不改写 `SKILL.md` 的入口、模式和输出合同。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `SKILL.md` > 分区合同 > 本 `CONTEXT.md`。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-04-26
recommended_action: keep-resume-heuristics-only
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把仓库根目录误判为项目根目录 | project-root guard | 先锁定 `projects/aigc/<项目名>/` | 在 `references/project-runtime-layout.md` 固定判定顺序 | 恢复建议基于真实项目目录 |
| 旧英文 runtime 名泄漏到新版项目 | runtime migration layer | 将 `0-Init / 5-Image / 6-Video` 等只作为 legacy 输入兼容 | 新版 resume 默认引用中文 runtime 落点 | 输出下一入口不再指向旧路径 |
| 设计阶段在 `4-设计` 与 `11-主体` 间漂移 | runtime transition layer | 默认恢复读取 `11-主体`，把 `4-设计` 当 transition/compat 输入 | 根技能、registry、query、review 与 resume 同步收敛设计阶段读写口径 | 恢复设计产物时不会查错目录 |
| 只凭最近修改文件猜阶段 | evidence chain | 同时读取 `STATE.json`、`MEMORY.md`、`CONTEXT/`、初始化 scaffold 和阶段真实产物 | 在 workflow reference 固定“状态 + 产物 + gate”三证据 | 恢复结论列出证据来源 |
| 缺 `preflight-verdict.yaml` 仍建议高风险续跑 | governance gate | 回根 `aigc` 补 preflight 或 route gate | 在 review gate 中标记高风险阻断 | 高风险恢复不会跳过 gate |
| 把轻量初始化态一律判成治理重建 | init layering | 先确认 current scaffold、`MEMORY.md`、`CONTEXT/` 与可选 `STATE.json` 是否足够 | 保留 `lightweight_init_continue` 模式，legacy `team.yaml` 缺失不阻塞 | 低风险下一步不会被治理补件卡死 |
| 把 review repair route 当成普通阶段续跑 | review bridge | 读取 `review_bridge` 与 `resume_contract.required_repairs` | 单列 `review_repair_reentry` 模式 | 输出入口包含 repair rationale |
| 用户明确要求重起盘却进入 resume | satellite boundary | 直接回 `0-初始化` 的 rebootstrap | 在类型矩阵中标记 `reset_intent=explicit` | 主动回炉不沿旧方向继续 |
| 输出多个下一入口 | convergence gate | 退回 blocker 或选择唯一 gate owner | 模板固定 `唯一下一入口` 字段 | 最终答复没有无序候选列表 |
| 默认给 destructive Git 建议 | safety contract | 改成只读检查、diff、status 或人工确认 | hard guards 禁止默认 destructive action | 答复不含默认 `git reset --hard` |

## Repair Playbook

1. 先定位 `PROJECT_ROOT`，无法唯一定位时停止猜测。
2. 读取 `STATE.json`，再按需读取 `governance-state.yaml`、`MEMORY.md`、`CONTEXT/`、`0-初始化/`、legacy optional `team.yaml` 与阶段产物。
3. 先判定是否是 `rebootstrap`，再判定恢复模式；不要把“重来”当“续跑”。
4. 将证据分成 `state_truth`、`artifact_truth`、`gate_truth` 三类，再汇流成唯一下一入口。
5. 若涉及高风险执行，先检查或补 `mission-brief.yaml`、`route-plan.yaml`、`preflight-verdict.yaml`。
6. 若 review 已写 repair route，优先消费该结构化入口，不重新猜阶段。
7. 输出时说明 blocker、缺口和唯一下一入口；无法唯一裁决时只要最小补充信息。

## Reusable Heuristics

- `resume/` 恢复的不是聊天记忆中的上一步，而是磁盘与治理工件能够证明的最后稳定入口。
- 对当前新版 `aigc`，中文 runtime 是默认真源：`0-初始化 / 1-分集 / 2-编剧 / 3-美学 / 4-导演 / 5-表演 / 6-氛围 / 7-分镜 / 8-摄影 / 9-光影 / 10-分组 / 11-主体 / 12-图像 / 13-画布 / 14-审片`。旧英文路径、旧 `2-编导 / 3-运动 / 4-摄影` 与 transition `4-设计` 只能作为迁移输入读取。
- `STATE.json` 是轻量起盘的 live route truth；`governance-state.yaml` 是复杂恢复、review bridge 和高风险 gate 的结构化断点真源。
- 空阶段目录只是初始化 skeleton，不是阶段完成证据。
- 恢复建议越接近实际执行，越需要 preflight 或 review gate；越接近事实查询，越应该回 `query/`。
- “继续当前方向但补断点”属于 `resume/`；“推翻当前方向重新起盘”属于 `0-初始化`。
- 最稳的 resume 输出不是长选项列表，而是一个能被根技能或目标阶段直接消费的唯一下一入口。
- 恢复时最危险的不是“缺一个文件”，而是把某个缺口误当成已经完成的事实。
- `governance-state.yaml` 缺失不必然阻断轻量继续；但进入复杂多步执行、review repair 或高风险生成前，应补成结构化断点。
- `STATE.json.recommended_entry_path` 是恢复起点，不是免检结论；必须与磁盘产物存在性核对。
- `review_bridge` 和 `resume_contract.required_repairs` 是跨技能沟通入口，不是阶段内容本身。
- 旧项目迁移时先保留旧路径证据，再由根技能决定是否迁移；resume 不边恢复边悄悄改路径真源。
- 用户说“接着上次”时先找 checkpoint；用户说“重来”时先锁 reset intent。
- 问“上次跑到哪”优先看 `governance-state.yaml.last_stable_checkpoint`，再看 `STATE.json.current_stage` 与阶段产物。
- 问“现在能不能继续”优先看 `preflight-verdict.yaml`、`route-plan.yaml` 和阶段 validation。
