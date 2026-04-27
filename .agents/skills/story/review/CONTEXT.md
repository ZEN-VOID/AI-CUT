# CONTEXT.md

本文件是 `story/review` 父技能组的经验层。它只沉淀跨维度调度、聚合、路由、gate ownership 与失败修复经验；单一维度的判据、案例和局部失败模式应写入对应子技能自己的 `CONTEXT.md`。

## Purpose & Loading Contract

- 先读取同目录 `SKILL.md`，再读取本文件。
- 本文件不得改写父 `SKILL.md` 中的最终 gate ownership、输出路径和 registry 单一真源规则。
- 若进入某个维度子技能，继续加载该子技能同目录 `CONTEXT.md`。
- 若经验只影响一个维度，写入该维度 `CONTEXT.md`；只有影响父层聚合、跨维度路由或技能组治理时，才写入本文件。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
status: ok
recommended_action: keep-parent-routing-only
last_checked_at: 2026-04-27
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 父 `review/SKILL.md` 为空或只像普通维度技能，导致执行者不知道谁写最终 PASS/FAIL | parent guide contract | 把父技能改成技能组导引入口，明确 root gate ownership | 父层只保留路由、调度、聚合、输出合同；维度细则留在 child skill | 任一 review 请求都能先命中父层，再进入 registry 维度 |
| child sidecar 被误当最终 gate，`context-return` 直接消费某个维度报告 | gate ownership drift | 回到 `_shared/validation-root-contract.md`，确认 aggregate JSON 才是唯一 gate truth | 在父 `SKILL.md` 和 root contract 固定 child evidence / parent gate 分工 | PASS/FAIL 只从 `第V卷.validation.json` 读取 |
| 维度名单在父技能、team contract、runner 和 child 目录中各写一份，互相漂移 | roster duplication | 以 `_shared/validation-dimension-registry.yaml` 为单一真源，其他文件只做导览或引用 | roster 调整必须同步 registry、child `SKILL.md + CONTEXT.md`、runner handler 与 shared schema | 维度数量、role_id、report_filename 与 registry 一致 |
| 父层为了“结构完整”补空维度，导致 aggregate 看似完整但没有真实审查证据 | phantom dimension | 聚合时只消费本轮真实调度且通过 schema 校验的 packets | `drafting_inline` 与 `final_acceptance` 都按 selected_agents 记录真实 dispatch | aggregate 中不存在未执行维度的假 packet |
| 子技能给出问题但没有 `source_layer_owner`，返工被错误打回 drafting | source trace missing | 父层聚合时补查 issue 是否需要上溯 `0-初始化 / 1-设定 / 2-卷章` | child output contract 固定 source owner 槽位，父层 schema gate 检查 | 失败 issue 能说明是上游 source 修复还是正文返工 |
| `drafting_inline` 与 `final_acceptance` 混用，单章即时 hook 误写卷级最终 gate | invocation mode confusion | 先判 mode；inline 只返回阻断/回退信号，终验才写 aggregate JSON | 在父 `SKILL.md` 固定 mode selection 与输出路径差异 | inline 运行不会生成或覆盖 `第V卷.validation.json` |
| 六维审查权重或 mandatory 规则修改后，父导览表和 registry 不一致 | guide drift | 以 registry 为准修正父导览表 | 父导览表明确声明只作入口导览，冲突时回修导览 | `rg role_id` 与 registry 对齐 |
| review 失败后只给总分，不给可执行返工入口 | route insufficiency | 聚合时保留 `routing_decision / rework_targets / handoff_targets` | 父层 Completion Gate 要求 PASS/FAIL 同时解释下一步 | 失败结果能直接路由到 source contract 或具体 drafting step |
| 上层策略阻断真实 reviewer dispatch，但报告写成“已并发审查” | dispatch transparency | 明确记录降级来源、未真实启动的维度和实际采用路径 | 父层 dispatch contract 固定真实 dispatch 与降级报告口径 | 最终报告能区分真实 child result 与本地降级纪要 |
| 维度 issue 分类漂移，结构、连续性、逻辑、人物、时间线互相抢问题 | boundary blur | 回到 child `Parent Positioning` 与父层 registry scope 拆分 issue | 父层只做聚合，不在父层重写维度判据 | 每条 issue 有唯一主维度，必要时用 related_dimensions 辅助说明 |

## Repair Playbook

1. 先判当前问题属于父层导引、registry、shared contract、child 输出、runner 实现还是项目运行态数据。
2. 若问题涉及最终 PASS/FAIL，优先读取 `_shared/validation-root-contract.md` 与现有 `第V卷.validation.json`，不要先看 child sidecar。
3. 若问题涉及维度名单、权重、sidecar 文件名或 hook，优先读取 `_shared/validation-dimension-registry.yaml`。
4. 若问题涉及输入包缺字段，先检查 `_shared/validation-fact-pack-spec.md`，再上溯到 `0-初始化 / 1-设定 / 2-卷章 / 3-初稿` 的 source owner。
5. 若 child 输出无法聚合，先对照 `_shared/validation-child-output-contract.md` 与 `_shared/checker-output-schema.md`，再修对应 child skill。
6. 若 review 结果不能指导下一步，补齐 `routing_decision / source_layer_owner / rework_targets / handoff_targets`。
7. 若要新增、删除、重命名或调整维度，先改 registry，再同步 child 包、runner handler、shared schema、父 `SKILL.md` 导览表和必要的项目文档。
8. 若上层策略阻断真实 subagent / reviewer 调度，最终输出必须说明阻断层级、原本的 reviewer 路径、实际降级路径与未真实启动的维度。

## Reusable Heuristics

- 父 `review` 的价值不在于多说一遍六个维度，而在于让所有维度有同一个入口、同一个输入包、同一个聚合 gate。
- `第V卷.validation.json` 是验收判定，`第V卷/<维度>.md` 是证据；证据可以很多份，gate 只能有一份。
- review 失败最重要的问题通常不是“分数低”，而是“该回哪一层修”。没有返工归属的 review 只能制造噪音。
- 维度边界要保持窄：结构看义务兑现，连续性看承接不断带，逻辑看能否成立，人物看是否仍像自己，时间线看锚点和窗口，任务汇聚看支流是否服务主线。
- 聚合层不要替 child 做审美细判；聚合层只负责把 child 的证据变成可执行 gate 和路由。
- registry 是技能组的心脏。只要 roster 在两个地方都像真源，后面一定会漂移。
- `drafting_inline` 是过程刹车，`final_acceptance` 是终验门；两者共用维度定义，但不能共用输出落点。
- 最稳的 PASS 不是“没有问题”，而是“mandatory 维度都真实执行、关键问题可解释、handoff 明确授权下一阶段”。
