# CONTEXT.md

本文件是 `story-plan-chapter-level` 的经验层知识库，不承载核心执行合同，不记录流水日志。每次调用本技能时必须与同目录 `SKILL.md` 成对加载。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-chapter-planning-heuristics-only
last_checked_at: 2026-04-26
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 章级只有梗概，没有节奏 | chapter-level rhythm gap | 补七步结构、规划义务和 Mermaid 图 | 在模板固定节奏段落，并在 review gate 检查 handoff slots | 节奏可供 drafting 直接读取 |
| 章级写了节奏，但 drafting 还得二次猜 pack/mode | rhythm handoff under-spec | 在 `本章节奏曲线` 中补齐 `selected_pack / selected_mode / 规划义务 / 义务段位 / 建议写法` | 把共性 handoff 合同回指到 shared contract，并在模板固定槽位 | drafting 可直接读取 planning handoff |
| 线索与伏笔混写 | chapter-level information drift | 拆开 `本章线索` 和 `本章伏笔` | 在模板固定两个标题，review gate 禁止合并 | 信息推进和长期回照可区分 |
| 伏笔只写铺设，不写兑现位判断 | foreshadow incompleteness | 即使无兑现也明确标 `本章无兑现` | 在模板保留 `铺设 / 兑现` 双槽位 | 伏笔段落完整 |
| 本章支流没有汇聚动作或去向 | task convergence gap | 补 `汇聚动作 / 未汇聚任务去向` | 在模板固定任务关系槽位，review gate 检查支流闭环 | validation 能判断支流是否回到主任务 |
| 章级局部补写漂离卷级职责 | upstream reread skipped | 重新回读目标卷 `卷规划.md` 与 `整体规划.md` 后再修订 | steps 固定 `N1-UPSTREAM-REREAD`，Input Contract 禁止缺上游落盘 | 章级 `上承卷级任务` 能回指卷级任务线 |
| 建议写法变成正文句段 | planning/drafting boundary drift | 删除对白、叙述段、正文桥段，只保留结构建议 | review gate 固定非正文化检查 | 章级文件仍是 planning，不是 drafting |

## Repair Playbook

1. 先判断故障属于上游回读、节奏 handoff、任务汇聚、信息层、模板对齐、review gate 还是正文化越界。
2. 若缺上游，暂停落盘并补读 `2-卷章/整体规划.md` 与目标卷 `2-卷章/第N卷/卷规划.md`。
3. 若节奏字段不足，优先回到 `../../_shared/chapter-rhythm-handoff-contract.md` 与 `references/chapter-rhythm-rules.md`。
4. 若任务线悬空，优先补 `上承卷级任务 / 汇聚动作 / 未汇聚任务去向`，再看主线与支线。
5. 若信息推进混乱，先拆 `本章线索` 与 `本章伏笔`，再分别检查可见信息推进和长期回照。
6. 若输出模板或标题不齐，回到 `templates/chapter-planning.template.md` 与 `templates/output-template.md`。
7. 若审查意见指出正文化，删除句段级文本，只保留 planning 义务、建议写法和结构意图。
8. 修复技能包结构后运行工作车间 validator；修复业务章规划后运行父层 planning 输出校验或人工 review gate。

## Reusable Heuristics

- 章级是 planning 的最细层，但仍不是正文。
- 七步结构只要求职责完整，不要求七段等长。
- 章级最重要的节奏动作不是替 drafting 写句子，而是把 `pack / mode / obligation / suggestion` 移交清楚。
- 章级如果不说清支流当章怎么汇、没汇后去哪，下游通常会把“悬念”写成“悬空”。
- `义务段位` 只锁必须出现或必须完成的结构义务；`建议写法` 只给推荐编排，不拥有正文法律效力。
- Mermaid 图不是装饰；它至少要让读者看见起势、转折、升级、高潮和尾钩。
- 局部修订也要完整回读上游，因为章级字段之间牵连很紧，改一处任务线常常会影响节奏和章末达成。
