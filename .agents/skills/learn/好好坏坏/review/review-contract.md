# Review Contract

本文件定义 `好好坏坏` 的质量门禁、过拟合检查和 reviewer 降级口径。

## Review Scope

| dimension | checks |
| --- | --- |
| evidence | 是否读取目标 `SKILL.md + CONTEXT.md`、任务要求、资料来源和好/坏示例 |
| contrast | 是否明确回答好在哪里、坏在哪里，并形成可复核信号 |
| source_trace | 每个坏信号是否上溯到最窄有效源层 owner |
| patch_quality | 改动是否落到正确分区，是否避免把所有规则堆入 `SKILL.md` |
| sync_scope | 是否检查父级、sibling、shared carrier、templates、scripts、registry/routes |
| anti_overfit | 是否避免把单次示例表面措辞写成硬规则 |
| validation | 是否用好/坏示例回放新规则，并保留残余风险 |
| learning | 是否把局部经验写目标 `CONTEXT.md`，跨 skill 经验写本技能经验层 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 源层调优可交付 |
| `pass_with_followups` | 可交付，但存在非阻断后续项 |
| `needs_rework` | 源层落点、同步范围或验证存在阻断问题 |
| `blocked` | 缺失关键输入、资料来源、权限或上层策略 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: evidence | contrast | source_trace | patch_quality | sync_scope | anti_overfit | validation | learning
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Gate Rule

不得宣布完成：

- 只描述好坏差异，没有源层 owner。
- 修改了输出结果，却没有修改目标 skill 源层规则或明确说明 diagnose-only。
- 把临时偏好写进硬规则。
- 涉及资料事实但无资料来源，也未写 `residual_risks[]`。
- 修改触发、路由、模板、shared carrier 或脚本后未检查同步范围。
- 目标 skill 是 Skill 2.0 包但结构/引用检查未执行。

## Reviewer Dispatch Policy

- 默认执行本地 review checklist。
- 只有用户显式要求真实 subagent、外部 reviewer 或上层 skill 合同明确且当前工具策略允许时，才启动对应 reviewer。
- 若仓库或技能合同偏好真实 reviewer，但当前 system/developer/tool policy 阻断，必须报告：阻断来源层级、原计划 reviewer 路径、实际本地降级路径、未真实启动的 reviewer。
