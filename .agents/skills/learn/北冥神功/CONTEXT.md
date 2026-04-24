# Context: 北冥神功

本文件是 `北冥神功` 的经验上下文知识库，不是执行日志。它用于沉淀 skills-update 吸收裁决、同步范围判断、review 降级和学习沉淀中的可复用经验。

## Context Health

```yaml
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-heuristic-focused
last_checked_at: 2026-04-24
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 升级点被直接塞进目标 `SKILL.md`，但其实只是经验性启发 | 吸收落点裁决层 | 改回目标 `CONTEXT.md` 或本技能 `CONTEXT.md` | 固定先做 `point_type` 判型，再决定 landing set | 经验型内容不再污染主合同 |
| 只修目标 leaf，没有检查父级、siblings 或 shared carrier | 技能组上下文层 | 回补 group scan 与 parity scope | 把 `N3-GROUP-CONTEXT-SCAN` 设为硬门槛 | 相关 sibling / shared carrier 同步到位 |
| 升级点改变触发语义，但 registry/routes 没更新 | 发现与路由层 | 同轮补 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml` | 在执行硬规则中固定 discovery sync | 新技能可被发现，旧触发不漂移 |
| 共享 schema 或 runner 改了，但只修一条链 | parity 层 | 横向补齐 sibling runner / validator / template | 把 `parity_targets[]` 变为显式字段 | 同级链路都接受新口径 |
| 写了改动，却没有学习沉淀 | learning deposition 层 | 追加目标 `CONTEXT.md`、本技能 `CONTEXT.md` 或 `CHANGELOG.md` | 固定 `double_learning` 闭环 | 本轮升级拥有可复用经验 |
| 升级点需要长细则或判型表，却硬塞在主 `SKILL.md` | 真源分层层 | 下沉到 `references/`、`steps/`、`review/` 或 `types/` 并从主合同回链 | 固定 dynamic-reference-first 原则 | 主 `SKILL.md` 仍可扫描 |
| 目标技能自身进入 Skill 2.0 升级窗口 | meta-workshop 迁移层 | 使用 `skill-工作车间` 的迁移矩阵、canonical layout 与 validator | 将迁移矩阵、输出模板、agents 元数据和 review gate 纳入升级闭环 | 目标包通过 Skill 2.0 结构校验 |

## Repair Playbook

1. 先确认本轮问题属于“落点错了”“同步范围漏了”“parity 漏了”“学习沉淀缺失”还是“结构升级不完整”。
2. 回看目标 skill 自己的 `SKILL.md + CONTEXT.md`，再回看其父级、siblings、shared carrier 与 registry/routes。
3. 重新做一次 `upgrade_point -> point_type -> landing_set -> sync_scope`。
4. 若目标进入 Skill 2.0 迁移，先建立迁移矩阵，再拆分 owner；不要直接删除旧段落。
5. 优先修源层载体，再修局部文案或单次输出。
6. 把局部经验写回目标 `CONTEXT.md`，把跨 skill 吸收模式写回本文件或 `knowledge-base/`。

## Reusable Heuristics

- `skills-update` 最容易犯的错不是不会改，而是改得太快，没先判型。
- 对 skill 升级来说，目标 skill 现状和技能组上下文缺一不可；只看前者会局部最优，只看后者会空泛。
- 若升级点改变的是“什么时候该触发这个 skill”，往往不止要改 `description`，还要顺带检查 registry/routes。
- 若升级点改变的是“这个 skill 怎么执行”，优先检查是否应落 `SKILL.md` 骨架、`references/`、`steps/` 或 `review/`，而不只是补一段经验。
- 若升级点来源于一次真实失败，最稳的落点通常是：目标 skill 收局部修复经验，本技能收跨技能吸收策略。
- 任何牵动 shared schema、runner、validator 或 template 的升级，都要怀疑存在 sibling parity 风险。
- 长期维护技能进入 Skill 2.0 升级窗口时，先用 `skill-工作车间` 拆分结构 owner，再让本技能保留“如何吸收升级点”的业务判断，不要让结构迁移吞掉业务语义。
