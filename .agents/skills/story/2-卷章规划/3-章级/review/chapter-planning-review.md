# Chapter Planning Review

本文件定义 `story-plan-chapter-level` 的质量门禁。review 只给 verdict 和修复路由，不改写业务主真源；修复由主技能按 Output Contract 聚合落盘。

## Default Provider

- 默认辅助 provider：`code-reviewer` 或同等 reviewer subagent。
- 若上层策略阻断真实 reviewer/subagent，允许降级为本地 checklist，但必须报告阻断来源、原计划 provider、实际降级路径和未启动角色。

## Review Checklist

| dimension | pass condition | fail route |
| --- | --- | --- |
| upstream | 已回读 `整体规划.md` 与目标卷 `卷规划.md` | `SKILL.md` Input Contract / `steps/N1-UPSTREAM-REREAD` |
| headings | 12 个 required headings 齐全 | `templates/chapter-planning.template.md` |
| conflict | 表层冲突、深层冲突、冲突状态变化齐全 | `references/chapter-planning-contract.md` |
| rhythm | `selected_pack / selected_mode / 七步职责映射 / 规划义务 / 义务段位 / 建议写法 / Mermaid` 齐全 | `references/chapter-rhythm-rules.md` |
| obligations | `entry_promise / conflict_axis / micro_payoff / exit_hook` 齐全 | `../../../_shared/chapter-rhythm-handoff-contract.md` |
| task_line | `上承卷级任务 / 主线 / 支线 / 支流角色 / 汇聚动作 / 未汇聚任务去向` 齐全 | `references/chapter-planning-contract.md` |
| information | `本章线索` 与 `本章伏笔` 分离，伏笔含 `铺设 / 兑现` | `templates/chapter-planning.template.md` |
| planning_only | 无对白、正文叙述段、句段级桥接或 drafting pulse ladder | `references/chapter-planning-contract.md` |
| mermaid | 图能看出起势、转折、升级、高潮、尾钩 | `steps/chapter-planning-workflow.md` |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: upstream | headings | conflict | rhythm | task_line | information | planning_only | mermaid
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可直接供 drafting 消费 |
| `pass_with_followups` | 可交付，但有非阻断优化项 |
| `needs_rework` | 有阻断问题，必须返工 |
| `blocked` | 缺上游文档、缺目标项目或权限阻断 |

## Gate Rule

不得在以下情况宣布完成：

- 缺 `整体规划.md` 或目标卷 `卷规划.md`。
- 章级节奏 handoff 任一必填槽位缺失。
- 任务线没有汇聚动作或未汇聚去向。
- 线索与伏笔合并成一个段落。
- 章级规划出现正文、对白或可直接投放到 drafting 的叙述段。
