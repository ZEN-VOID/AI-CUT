# 2-格式 / Output Template

本文件是 `2-格式` 父技能的输出模板真源。

## `validation-report.md` Template

```markdown
# 2-格式 验证报告

## 输入清单
- north_star:
- init_handoff:
- 分集来源:
- 用户显式偏好:

## 变体裁决
- 推荐主变体：
- 判定理由：
- 关键证据：

## 采用格式合同摘要
- 子技能：
- 合同入口：
- 样例入口：
- 局部验证入口：

## 放弃另一变体的原因
- 未采用变体：
- 放弃原因：
- 若未来切换，需要补什么：

## 下游交接说明
- 推荐下一入口：
- 下游必须遵守的格式边界：
- 本阶段不解决的问题：

## 验收结论
- PASS / REWORK：
- fail_code：
- rework_entry：
```

## Dual-Track Addendum

若用户要求双案对照，在 `validation-report.md` 中新增：

```markdown
## 双案对照
- 标准剧入口：
- 解说剧入口：
- 推荐主案：
- 备选案：
- 推荐理由：
```

## Minimum Acceptance

- 至少存在一个推荐主变体
- 至少回链一个可用子技能合同
- 至少给出一个失败码或 PASS 结论
