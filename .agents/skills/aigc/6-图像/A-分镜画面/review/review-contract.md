# Review Contract

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 imagegen |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、跳过或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照或生成结果的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `shot_id` 可回指 `4-分组` 源组与 `分镜N` | `FAIL-FRAME-ID` | `references/group-source-extraction.md` |
| `G2-NORTHSTAR` | 三项 north_star 字段为直引，未摘要、未翻译、未改写 | `FAIL-FRAME-PROMPT` | `references/prompt-assembly-contract.md` |
| `G3-PROMPT` | 英文 prompt 为单镜、核心内容未改写、<= 2000 字符 | `FAIL-FRAME-PROMPT` | `references/prompt-assembly-contract.md` |
| `G4-SLOTS` | Characters / Scene / Props 只绑定存在图片，多视图优先 | `FAIL-FRAME-REF` | `references/reference-slot-binding.md` |
| `G5-HANDOFF` | imagegen mode 合法，未未经许可切 CLI/API fallback | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G6-PERSIST` | 生成图片或计划输出位于项目目录，不只在 `$CODEX_HOME` | `FAIL-FRAME-IMAGEGEN` | `.agents/skills/cli/imagegen/references/output-persistence.md` |
| `G7-REF-INPUT` | 若使用 built-in text prompt only，results/report 明确记录 reference paths 未作为视觉输入 | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G8-REPORT` | 执行报告列出 generated / skipped / failed 与返工入口 | `FAIL-FRAME-REPORT` | `templates/output-template.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-NORTHSTAR
    - G3-PROMPT
    - G4-SLOTS
  todos: []
```
