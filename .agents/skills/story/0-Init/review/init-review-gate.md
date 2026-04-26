# Init Review Gate

本文件拥有 `story-init` 的质量门禁、审计维度、review provider 口径与 verdict 模型。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：审查结构、运行时写回、team 真源、脚本边界、模板对齐和初始化语义漂移。
- 若更高优先级 system/developer/tool/user 策略阻断真实 reviewer 或 subagent 调度，允许本地 checklist 降级，但必须报告阻断来源、原路径、实际路径和未启动 reviewer。

## Sufficiency Checklist

| dimension | required check | fail_code |
| --- | --- | --- |
| route | story 与 aigc film 路由没有混线 | `FAIL-INIT-ROUTE` |
| mode | `init_mode` 固定为 `team代入模式`，只允许 `auto/custom` | `FAIL-INIT-MODE` |
| team | `team.yaml` 是唯一 team 真源，成员均位于 `.agents/skills/team/` | `FAIL-INIT-TEAM` |
| subagents | planning 固定题包直答有真实执行证据；若只有阻断/降级报告且没有等价 planning patch，verdict 必须为 `blocked` 或 `needs_rework` | `FAIL-INIT-SUBAGENT` |
| runtime | `STATE.json.paths` 与实际目录骨架一致 | `FAIL-INIT-RUNTIME` |
| project memory | 项目 `MEMORY.md` 与 `CONTEXT/` 已创建，职责未互相替代 | `FAIL-INIT-MEMORY` |
| handoff | `north_star`、source manifest、handoff 与 team provenance 一致 | `FAIL-INIT-HANDOFF` |
| next entry | 下一入口指向 `1-Cards` 或明确的返工/阻塞项 | `FAIL-INIT-NEXT` |
| scripts | 脚本只做机械落盘，不生成核心创作判断 | `FAIL-INIT-SCRIPT` |
| templates | `templates/output-template.md` 对齐 Output Contract 五字段 | `FAIL-INIT-TEMPLATE` |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付并进入 `1-Cards` |
| `pass_with_followups` | 可交付，但存在非阻断后续项 |
| `needs_rework` | 工件、provenance、runtime 或 team 真源有阻断问题 |
| `blocked` | 缺少关键输入、权限或真实 subagent/reviewer 被阻断且不可降级 |

## Review Flow

1. 运行 Skill 2.0 结构校验。
2. 对初始化语义执行本 checklist。
3. 若涉及脚本变更，运行 `.agents/skills/story/scripts/init_project.py` dry run 或对应 pytest。
4. 汇总为单一 verdict，不能让多个 reviewer sidecar 并列夺权。
5. findings 必须回指 `SKILL.md`、`references/`、`steps/`、`types/`、`templates/`、`scripts/` 或 `CONTEXT.md` 的 owner。

## Minimal File Checks

```bash
test -f "./projects/story/示例小说/team.yaml"
test -f "./projects/story/示例小说/MEMORY.md"
test -f "./projects/story/示例小说/STATE.json"
test -d "./projects/story/示例小说/CONTEXT"
test -f "./projects/story/示例小说/0-Init/north_star.yaml"
test -f "./projects/story/示例小说/0-Init/story-source-manifest.yaml"
test -f "./projects/story/示例小说/0-Init/init_handoff.yaml"
```

## Root-Cause Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: route | mode | team | subagents | runtime | handoff | scripts | templates
  symptom: ""
  direct_cause: ""
  section_owner: ""
  source_contract: ""
  rework_target: ""
```
