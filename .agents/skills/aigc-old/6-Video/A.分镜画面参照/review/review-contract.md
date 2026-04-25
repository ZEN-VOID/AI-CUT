# Review Contract

## Scope

本 review gate 只裁决 `A.分镜画面参照` 的结构、三段 handoff、输出路径和可复核性，不改写业务主真源。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 若上层策略阻断真实 reviewer/subagent 调度，降级为本地 checklist，并在最终交付说明中报告。

## Checklist

| dimension | checks |
| --- | --- |
| structure | Skill 2.0 目录和根文件齐备 |
| source_fusion | 旧三段来源在 `references/source-fusion-map.md` 中有 owner |
| distill | prompt/TXT 仍遵守 LLM-first，JSON/TXT/manifest 齐备 |
| reference_binding | 引用只指向真实 `Assets/`，歧义不默选 |
| provider_handoff | `submit-plan.json` 和 `submit-brief.md` 明确唯一下一入口 |
| templates | `templates/output-template.md` 映射 Output Contract 五字段 |
| context | `CONTEXT.md` 是知识库，不是流水日志 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付 |
| `pass_with_todo` | 有非阻断 TODO，可交付 |
| `needs_rework` | 有阻断问题，必须返工 |
| `blocked` | 缺关键输入、权限或上层策略阻断 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: structure | source_fusion | distill | reference_binding | handoff | templates | context
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Gate Rule

不得宣布完成：

- 缺少任一 Skill 2.0 canonical 目录或根文件。
- `SKILL.md` 没有 `Input Contract`、`Reference Loading Guide`、`Field Mapping` 或 `Output Contract`。
- `CONTEXT.md` 缺少 `Type Map / Repair Playbook / Reusable Heuristics`。
- 三段旧链路来源没有明确融合 owner。
- `full_chain` 输出没有唯一下一入口。
