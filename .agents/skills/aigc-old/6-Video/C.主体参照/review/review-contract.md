# Review Contract

本 review gate 只裁决 `C.主体参照` 的结构、三段 handoff、主体识别、输出路径和可复核性，不改写业务主真源。

## Review Inputs

- `SKILL.md`
- `CONTEXT.md`
- `references/source-fusion-map.md`
- `references/prompt-distillation-contract.md`
- `references/subject-reference-binding-contract.md`
- `references/provider-handoff-contract.md`
- `steps/subject-reference-workflow.md`
- `types/type-map.md`
- 当前运行时 artifacts

## Review Checklist

| gate_id | check | pass condition | fail route |
| --- | --- | --- | --- |
| `R-SUBJREF-01` | Skill 2.0 结构 | canonical 目录与必需文件齐全 | 回工作车间 validator |
| `R-SUBJREF-02` | LLM-first | prompt/TXT 和主体语义裁决没有被脚本主创替代 | 回 `references/prompt-distillation-contract.md` |
| `R-SUBJREF-03` | 源映射 | 旧三段核心语义都有新 owner | 回 `references/source-fusion-map.md` |
| `R-SUBJREF-04` | 主体识别 | `subject-index.json` 能回链来源镜头和主体字段 | 回 `references/subject-reference-binding-contract.md` |
| `R-SUBJREF-05` | 引用绑定 | 所有绑定路径真实位于 `Assets/`，歧义不默选 | 回 `reference-binding/` |
| `R-SUBJREF-06` | Handoff | `submit-plan.json` 与 `submit-brief.md` 有唯一下一入口 | 回 `provider-handoff` |
| `R-SUBJREF-07` | 局部模式 | 未执行段没有补占位或伪造产物 | 回 `types/type-map.md` |

## Verdict Shape

```yaml
verdict: pass | pass_with_todo | fail
blocking_findings:
  - gate_id:
    finding:
    rework_entry:
non_blocking_todos:
  - item:
evidence:
  source_root:
  output_root:
  artifacts:
```

## Local Review Fallback

若上层策略阻断真实 reviewer/subagent，主 agent 应降级为本地 review checklist，并在最终说明中报告：

- 阻断来源属于 `system / developer / tool / user` 的哪一层
- 原本应执行的 reviewer 或 subagent 路径
- 实际采用的本地 checklist 路径
- 哪些 reviewer / 角色 / 子任务没有真实启动
