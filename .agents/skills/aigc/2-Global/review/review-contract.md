# 2-Global Review Contract

本文件定义 `aigc/2-Global` 的交付审计门。它只提供质量评估和 verdict，不拥有业务主真源写回权。

## Review Scope

| scope | 检查对象 | verdict |
| --- | --- | --- |
| `structure` | Skill 2.0 目录、`SKILL.md + CONTEXT.md`、动态引用、`agents/openai.yaml` | `pass / fail / warn` |
| `json_first` | `第N集.json` 是否仍为唯一 creative business truth，且同构于 `templates/episode-root.template.json` | `pass / fail` |
| `global_style` | `project_global.全局风格` 与 `groups[].global.全局风格` 是否符合真人古装写实摄影基线 | `pass / fail / needs_type_profile` |
| `group_alignment` | `groups[].global.剧本正文 / 类型元素 / 导演意图` 是否逐组对齐 | `pass / fail` |
| `handoff` | `validation-report.md` 与 `3-Detail` handoff 是否可消费 | `pass / fail / blocked` |

## Global Style Review Gate

`global_style` 必须通过以下检查：

1. 覆盖真人版古装影视、高清电影级画质与真实摄影语法。
2. 覆盖真实人物皮肤、服饰纹理、自然毛发、材质反射和空间层次。
3. 光影符合场景动机光与物理照明逻辑，保留高光不过曝与暗部可读。
4. 使用电影化纵深、权力关系调度、前中后景关系等高层构图约束，不写具体镜头参数。
5. 镜头语言克制稳定，动作反馈符合真实物理。
6. 明确排除动画描线、赛璐璐分层、夸张残影等污染方向。
7. 收束为写实、细腻、4K HDR、影院级调色与轻胶片颗粒。

## Reviewer Provider Policy

- 默认可以使用 `code-reviewer` 或等价 reviewer 做辅助审计。
- 若更高优先级策略阻断真实 reviewer / subagent 调度，则由主 agent 按本地 checklist 执行，并在最终报告中说明降级来源、原计划路径和实际路径。
- Review 只能给出 findings 与修复建议；最终 canonical 写回仍由 `2-Global` 主技能聚合裁决。

## Minimum Output

```yaml
review_result:
  structure: pass
  json_first: pass
  global_style: pass
  group_alignment: pass
  handoff: pass
  findings: []
```
