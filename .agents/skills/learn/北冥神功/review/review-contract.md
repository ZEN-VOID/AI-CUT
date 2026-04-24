# Review Contract

本文件定义 `北冥神功` 的质量门禁、reviewer 触发器和降级口径。

## Default Provider

- 默认 reviewer 口径：`code-reviewer`。
- 真实 subagent/provider dispatch 仅在当前上层策略、工具权限与用户授权允许时启动。
- 若上层 system/developer/tool/user 策略阻断真实 reviewer 或 subagent，必须降级为 `degraded-local-review`，并报告：
  - 阻断来源层级
  - 原计划 provider 路径
  - 实际采用的本地 checklist
  - 未真实启动的 reviewer

## Trigger Matrix

| trigger | required gate |
| --- | --- |
| 修改 `scripts/`、validator、template 或 shared carrier | `standard` review |
| 修改 registry/routes | `standard` review + discovery check |
| 修改 2 个以上载体类型 | `standard` review |
| 存在 sibling parity 风险 | `deep` review |
| 用户要求“有机融合”“不要草率拼接” | `standard` review |
| 只改局部经验，不改入口、脚本、shared carrier | `light` review |

## Checklist

| dimension | checks |
| --- | --- |
| `structure` | 目标载体是否存在，新增分区是否符合 canonical owner |
| `typing` | 每个升级点是否有 `point_type` 与 landing rationale |
| `sync_scope` | 父级、siblings、shared carrier、registry/routes 是否按需检查 |
| `dynamic_reference` | 主 `SKILL.md` 是否只承载入口、路由、门禁和输出合同 |
| `scripts` | 脚本是否只承担机械辅助，未替代 LLM 主创判断 |
| `templates` | 模板是否映射 Output Contract，不另立路径或命名规范 |
| `learning` | 目标与本技能的经验沉淀是否落在正确作用域 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付 |
| `pass_with_todo` | 可交付，但存在非阻断 TODO |
| `needs_rework` | 存在阻断问题，必须返工 |
| `blocked` | 缺关键输入、权限或上层策略阻断 |

## Local Review Output

```yaml
review:
  mode: local | provider | degraded-local-review
  verdict: pass | pass_with_todo | needs_rework | blocked
  checks: []
  findings: []
  residual_risks: []
```
