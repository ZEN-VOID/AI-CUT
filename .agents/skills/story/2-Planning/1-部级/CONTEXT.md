# CONTEXT.md

本文件是 `story-plan-book-level` 的经验层知识库，不承载核心执行合同，不记录流水日志。执行时必须先读取同目录 `SKILL.md`，再加载本文件用于避坑和策略选择。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-book-level-heuristics-only
last_checked_at: 2026-04-26
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 整体规划只有概念，没有卷划分职责 | book-level completeness | 先补卷划分，再谈下层 | 在模板固定“卷划分必须写功能” | 卷级能直接接手 |
| 整体规划有卷划分，但主任务树没锁 | task topology gap | 补 `整部任务关系` | 在模板固定 `主任务树 / 卷级支流簇 / 关键汇聚里程碑` | 卷级不再凭空猜主从关系 |
| Save the Cat 被写成死百分比公式 | rhythm misuse | 改写成拍点走廊 | 在 reference 固定“长篇走廊化” | 节奏曲线可被长篇使用 |
| 规避写成空话 | avoidance drift | 改成可执行禁飞区 | 在模板中要求“不要写成什么” | 规避可直接约束卷/章 |
| 局部修订偷偷改写整部总纲 | revision blast radius | 只 patch 本轮命中的字段 | 在 steps 固定旧稿回读和 patch 范围声明 | diff 中无无关字段重写 |
| 部级规划复制角色卡/场景卡/物品卡 | cross-stage duplication | 改成 planning 所需摘要和引用 | 回到父层 bridge，禁止复制完整卡册 | planning 文件不冒充第二套卡册 |

## Repair Playbook

1. 先判断问题属于输入真源、卷划分、任务关系、冲突轴、节奏曲线、规避项还是修订范围。
2. 若卷级无法接手，优先检查 `卷划分` 与 `整部任务关系`，不要先补局部情节。
3. 若节奏曲线失真，回到 `references/book-rhythm-save-the-cat.md`，把 15 步改成跨卷拍点走廊。
4. 若用户要求局部补写，先读取旧 `整体规划.md`，再声明本轮只改哪些字段。
5. 若规划内容开始写正文语气、对白或场面段落，立即回到 planning-only 边界。
6. 若出现可复用故障模式，优先沉淀到本文件；稳定成硬规则后再晋升到 `SKILL.md` 或对应分区。

## Reusable Heuristics

- 部级最重要的不是写得宏大，而是给卷级一个不会跑偏的总方向。
- `卷划分` 质量不好，后面所有卷级和章级都会反复返工。
- 任务树如果只存在脑内、不落成字段，卷级就会把“支流扩张”和“主任务推进”混成一团。
- 部级节奏应回答整书长波，而不是把每卷都塞进同一强度的升级循环。
- 规避项要能被下游执行；“避免节奏拖沓”这类句子需要改写成具体禁飞区。
