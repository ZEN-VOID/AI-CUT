# CONTEXT.md

本文件是 `aigc-review` 的经验层知识库，不是第二份父合同。它用于帮助执行者识别 fact pack 缺口、维度聚合错误、route 误判和旧链路兼容风险。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 24000
hard_limit_chars: 48000
status: ok
recommended_action: keep-review-specific-heuristics
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-REVIEW-01` | 阶段内 validator 已通过，但跨阶段 handoff 仍不可信 | package governance layer | 运行 `aigc-review` 写 aggregate packet | checkpoint/stage/release 三层都走同一 review bus | `projects/aigc/<项目名>/review/**/*.review.json` 存在 |
| `TM-REVIEW-02` | dimensions 对同一 scope 给出互相冲突结论 | fact pack covenant layer | 重建同一份 `review_fact_pack` 后重跑 | 所有维度只消费同一 pack | sidecar 中 `scope_ref` 与 `checkpoint_id` 一致 |
| `TM-REVIEW-03` | review 只有 prose，没有返工入口 | aggregate gate layer | 补 `routing_decision / handoff_targets / rework_targets` | aggregate template 固定 route 字段 | `*.review.repair.json` 可执行 |
| `TM-REVIEW-04` | review 试图直接改写阶段主稿 | ownership boundary layer | 停止写业务 truth，改写 repair route | `SKILL.md` 固定“卫星不改阶段 canonical”边界 | 阶段文件未被 review 父层直接覆盖 |
| `TM-REVIEW-05` | 新 `aigc` 阶段名与旧 runner 兼容名混用 | compatibility layer | 在 registry 和报告中标明当前 stage 与 legacy alias | `_shared/` 仅作 runner 兼容，规范分区用当前 stage 语言 | `scripts/aigc_review_runner.py --help` 可用，文档落点不漂移 |
| `TM-REVIEW-06` | 六个维度目录被当作可直达 skill 调度 | source-layer topology drift | 删除维度目录入口，改读 `references/dimensions/*.md` | registry 只保存 `dimension_spec_ref`，runner 记录 spec runtime | `rg` 不再出现旧维度 `SKILL.md` 路径 |

## Repair Playbook

1. 先判断本轮是 `checkpoint_inline`、`stage_acceptance` 还是 `package_release`。
2. 若缺项目根，先回到 `projects/aigc/<项目名>/STATE.json` 或用户上下文定位项目。
3. 若维度输出不一致，优先检查 `review_fact_pack` 是否同一份，而不是先裁掉某个 reviewer。
4. 若 aggregate packet 与 dimension sidecar 冲突，以 aggregate packet 为 gate 真源，再修 dimension output contract。
5. 若 issue 指向上游 source truth，route 应回到 source owner，不应全塞给当前阶段返工。
6. 若 provider/顾问与复核流程 被上层策略阻断，保留本地 checklist 证据：不可用来源、原 provider、实际 checklist、本地 reviewer checklist。
7. 若 runner 兼容文件 `_shared/` 与 Skill 2.0 分区冲突，优先修 `references/` 的规范表达，再同步 `_shared/`。
8. 若发现 `review/<中文维度名>/SKILL.md` 式旧路径，按“维度细则 -> `references/dimensions/`，经验 -> 父 `CONTEXT.md`”迁移，不恢复局部 skill 包。

## Reusable Heuristics

- `aigc-review` 的关键不是多一个评分表，而是把“能不能继续交付”变成唯一 gate。
- checkpoint 审计比最终总评更容易抓住问题，因为错误通常发生在阶段 handoff 处。
- fact pack 是证据包，不是第二业务真源；它只负责把本轮审计看到的事实锁到同一快照。
- dimension reviewers 应报告维度问题和默认返工建议，但不能写最终 `routing_decision`。
- “自动修复”在 review 父层默认指生成 repair route 与治理桥接，不是替创作阶段改稿。
- 新 `aigc` 阶段名以 `0-初始化 / 1-分集 / 2-编导 / 3-运动 / 4-摄影 / 5-分组 / 6-设计 / 7-图像 / 8-视频 / 9-审片` 为主；旧英文 stage 只作为兼容线索。
- 六维审计的局部判断应保持为 dimension spec，而不是重新拆成六个独立 `SKILL.md + CONTEXT.md`。
