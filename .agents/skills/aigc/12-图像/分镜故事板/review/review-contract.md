# Review Contract

本 review gate 只裁决 `B-分镜故事板` 的组级 prompt、主体参照、imagegen 计划与项目持久化，不改写 `10-分组` 主真源。

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 imagegen |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、跳过或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照或生成结果的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `group_id` 可回指 `10-分组` 源标题、组正文和 YAML | `FAIL-SHEET-GROUP` | `references/group-source-extraction.md` |
| `G2-PREFIX` | prompt 逐字包含任务执行前缀，且前缀声明标准分镜手稿风格黑白线稿基底、受控彩色标注系统、不使用全局风格词 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `G3-FRAME-UNITS` | prompt 包含可追溯的 storyboard frame-unit plan，panel 编号不默认等同原始 `分镜N`，每个 frame unit 可回指源正文，并包含 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 与默认 `panel_image_aspect_ratio: 16:9` | `FAIL-SHEET-GROUP` | `references/group-source-extraction.md` |
| `G4-CONTENT` | prompt 主体直接引用 `10-分组` 对应分镜组完整内容，源分镜顺序与底部 YAML 完整 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `G5-SUBJECTS` | Characters / Scene / Props 只来自组底 YAML | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G6-SLOTS` | 只绑定存在图片；同一主体有多视图时必须优先绑定多视图，只有缺多视图时才用主图；缺图不留空路径 | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G7-SUBJECT-FIDELITY` | manifest、prompt 和 imagegen plan 均声明参照图用于黑白线稿下的角色身份、场景空间结构、道具外形保真；不得把全局风格或场景光影氛围作为风格词 | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G8-LAYOUT` | prompt、imagegen plan 和 result 均声明 `resolution_target: 4K`、默认 `panel_image_aspect_ratio: 16:9`、panel 图片下方 `rich_brief` 分镜描述文字、每个可见角色头顶黑色角色名、受控彩色标注系统和自适应排版；不得降级为 2K | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G9-HANDOFF` | imagegen mode 合法，未经许可不切 CLI/API fallback | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G10-PERSIST` | 生成图片或计划输出位于项目目录，不只在 `$CODEX_HOME`；不得静默覆盖已有文件，除非用户明确要求 rerun / replace | `FAIL-SHEET-IMAGEGEN` | `.agents/skills/cli/imagegen/references/output-persistence.md` |
| `G11-REF-INPUT` | 若绑定本地参照图，生成前必须逐张 `view_image` 且 results/report 记录 `reference_input_status: visible_in_conversation_context`；确无绑定图片时记录 `no_reference_images_bound` | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G12-REPORT` | 执行报告列出 generated / skipped / failed 与返工入口 | `FAIL-SHEET-REPORT` | `templates/output-template.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-PREFIX
    - G3-FRAME-UNITS
    - G4-CONTENT
    - G5-SUBJECTS
    - G6-SLOTS
    - G7-SUBJECT-FIDELITY
    - G8-LAYOUT
  todos: []
```
