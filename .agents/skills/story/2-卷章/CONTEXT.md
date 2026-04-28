# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 0
current_lines: 0
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-22T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按旧 `1-7` 并列技能思考 planning | parent contract | 回到父层 `SKILL.md` 的三层结构合同 | 在根技能、workflow、bridge、脚本里统一改写为 `部级/卷级/章级` | 不再把旧六技能当成 active dispatch |
| 先做卷或章，后补整部总纲 | fractal order | 强制补 `整体规划.md` 后再继续 | 把回读顺序写死在父技能与 validator | 卷级/章级文件都能上溯到部级 |
| 卷级只是“章节清单 + 一句摘要” | volume design thinness | 按卷级节奏机制补强任务、人物、场景、道具与卷末达成 | 在卷级模板固定段落与节奏图 | `第N卷/卷规划.md` 能回答卷内推进与卷末兑现 |
| 三层规划没有时间线体系 | chronology system gap | 补部级 `故事编年史`、卷级 `本卷时间线`、章级 `本章时间推进` | 用 `_shared/timeline-design-contract.md` 固定事件顺序、因果、幕后事件和状态变化 | 低层时间线能上溯到高层，不靠节奏字段替代 |
| 章级只有情节提要，没有节奏职责 | chapter rhythm drop | 回到章级七步结构与动静结合规则 | 在章级 reference 和模板中固定 Mermaid + 七步投影 | `第N卷/第N章.md` 能回答本章如何推进、如何转调 |
| 把冲突/任务/线索/伏笔继续拆成平行 skill | decomposition drift | 归拢进卷级和章级必填段落 | 在 shared contract 明确旧六技能已内化，不再并列存在 | 输出只剩三层技能包 |
| planning 直接开始写正文 | stage boundary drift | 删掉正文段落，回到规划句法 | 在父层和 child skill 都写死“planning 不产正文” | 输出文件只包含规划性内容 |
| 角色卡/场景卡/道具卡被完整复制进规划文件 | cross-stage duplication | 回到 bridge，只保留 planning 所需最小引用与摘要 | 在 bridge 和子技能中固定最小导入边界 | planning 文件不再冒充第二套卡册 |

## Repair Playbook

1. 先判断问题属于层级顺序、输出结构、时间线体系、节奏设计还是跨阶段复制。
2. 若卷级或章级质量漂移，先检查它有没有回读上一级，而不是直接修当前文案。
3. 若发现旧六技能概念混回主链，优先修父层合同和 workflow 文案。
4. 收尾时至少同时核对：父技能、三个 child、共享合同、路径脚本。

## Reusable Heuristics

- 分形规划最容易失败的地方不是文档写少，而是层级倒置。
- `整体规划.md` 应回答“整部书为什么成立”；`第N卷/卷规划.md` 应回答“这一卷怎样交付总承诺”；`第N卷/第N章.md` 应回答“这一章怎样承担卷内职责”。
- 部级、卷级、章级三层节奏不能用同一把尺子缩放，必须各自有独立方法核。
- 时间线体系比节奏体系更底层：先锁故事世界里的事件顺序和状态变化，再决定读者体验上的节奏起伏。
- 旧的冲突/任务/线索/伏笔并不是被删除，而是从“平铺的 skill”变成“卷级/章级规划段落里的内生维度”。
