# Review Contract

## Default Provider

- 默认辅助 provider：`code-reviewer` 口径。
- 用途：审查 repair 方案与结果的结构、源层优先、跨阶段一致性、豆包 evidence、资产状态和残余风险。
- 若上层策略阻断顾问与复核流程 或外部 reviewer 调度，允许使用本地 review checklist，但直接使用本地 review checklist。

## Review Dimensions

| dimension | required checks |
| --- | --- |
| source_rule_review | 是否加载目标输出物 owning skill 与相关分区，并记录 `source_rules_reviewed` |
| impact_scope | 是否覆盖 upstream、neighbors、current、downstream、generated assets、future constraints、review/state |
| type_packages | 是否按 `types/type-map.md` 加载命中 scope / operation / acceptance 包 |
| source_priority | 是否先修 canonical owner，再修投影和下游 |
| doubao_evidence | 是否真实调用豆包或明确降级；provider 输出是否被 review 而非自动写回 |
| chinese_polish | 润色是否只改善表达和可执行性，不改事实、对白、编号、字段和引用 |
| creative_inspiration | 创意候选是否绑定 stage owner、用户禁区和可验收目标 |
| local_chinese_fit | 是否真正改善中文气口、本土文化语境、短剧/影视表达和用户-facing 可读性，而不是只做同义词替换 |
| asset_state | 图像/视频等生成资产是否以 preserve / invalidate / regenerate / review_only 表达 |
| residual_risk | 是否说明未改文件、未知消费者、后续生成 guardrail 和风险 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 修复闭环可接受 |
| `pass_with_followups` | 当前修复可用，但存在非阻断后续项 |
| `needs_rework` | 影响范围、源层、provider 或验收存在阻断缺口 |
| `blocked` | 缺关键输入、写回权限、provider 或 source owner |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: source_rule_review | impact_scope | type_packages | source_priority | doubao_evidence | chinese_polish | creative_inspiration | local_chinese_fit | asset_state | residual_risk
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Gate Rule

不得宣布完成：

- 没有 `source_rules_reviewed`。
- 没有 `impact_map`。
- 命中类型矩阵但没有加载对应类型包。
- 没有 `canonical_owner` 和 `writeback_order`。
- 下游改动早于源层裁决。
- 豆包执行型任务缺 provider evidence 或本地流程。
- 中文润色改变事实、对白、编号、字段、路径或结构化引用。
- 图像/视频修复声称完成但没有 owning provider route 或 asset action。
