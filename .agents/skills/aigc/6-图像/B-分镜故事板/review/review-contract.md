# Review Contract

本 review gate 只裁决 `B-分镜故事板` 的组级 prompt、主体参照、imagegen 计划与项目持久化，不改写 `4-分组` 主真源。

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 imagegen |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、跳过或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照或生成结果的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `group_id` 可回指 `4-分组` 源标题、组正文和 YAML | `FAIL-SHEET-GROUP` | `references/group-source-extraction.md` |
| `G2-PREFIX` | prompt 逐字包含固定英文开头 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `G3-CONTENT` | prompt 主体直接使用现有组正文，分镜顺序完整 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `G4-SUBJECTS` | Characters / Scene / Props 只来自组底 YAML | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G5-SLOTS` | 只绑定存在图片；同一主体有多视图时必须优先绑定多视图，只有缺多视图时才用主图；缺图不留空路径 | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G6-HANDOFF` | imagegen mode 合法，未未经许可切 CLI/API fallback | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G7-PERSIST` | 生成图片或计划输出位于项目目录，不只在 `$CODEX_HOME` | `FAIL-SHEET-IMAGEGEN` | `.agents/skills/cli/imagegen/references/output-persistence.md` |
| `G8-REF-INPUT` | 若绑定本地参照图，生成前必须逐张 `view_image` 且 results/report 记录 `reference_input_status: visible_in_conversation_context`；确无绑定图片时记录 `no_reference_images_bound` | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G9-REPORT` | 执行报告列出 generated / skipped / failed 与返工入口 | `FAIL-SHEET-REPORT` | `templates/output-template.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-PREFIX
    - G3-CONTENT
    - G4-SUBJECTS
    - G5-SLOTS
  todos: []
```
