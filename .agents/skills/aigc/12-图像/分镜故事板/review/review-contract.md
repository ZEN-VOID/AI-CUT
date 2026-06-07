# Review Contract

本 review gate 只裁决 `分镜故事板` 的组级 prompt、主体参照、imagegen 计划与项目持久化，不改写 `10-分组` 主真源。

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，目标组已生成并持久化 storyboard sheet 图片 |
| `pass_with_todo` | 目标组已生成并持久化 storyboard sheet 图片，但存在明确记录的缺失参照、非阻断风险或可后续优化项 |
| `needs_rework` | 存在会污染 prompt、参照或生成结果的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `group_id` 可回指 `10-分组` 源标题、组正文和 YAML | `FAIL-SHEET-GROUP` | `references/group-source-extraction.md` |
| `G2-PREFIX` | prompt 逐字包含任务执行前缀，且前缀声明标准分镜手稿风格黑白线稿基底、受控彩色标注系统、不使用全局风格词 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `G2A-STYLE-LOCK` | prompt / plan 包含 `style_lock_spec`，完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感和胶片颗粒等词被隔离为 evidence-only，最终绘制指令和 `visual_prompt_atoms` 不含彩色电影 still、写实渲染、场景氛围或全局画风词 | `FAIL-SHEET-STYLE-LOCK` | `references/prompt-assembly-contract.md` |
| `G3-FRAME-UNITS` | prompt 包含可追溯的 storyboard frame-unit plan，panel 编号不默认等同原始 `分镜N`，每个 frame unit 可回指源正文，并包含 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 与默认 `panel_image_aspect_ratio: 16:9` | `FAIL-SHEET-GROUP` | `references/group-source-extraction.md` |
| `G3A-SOURCE-COMPREHENSION` | prompt、group-index 和报告包含具体的 source comprehension：叙事功能、动作链、空间/主体/道具锚点、视觉转折、必须保留事实和禁止补写项，且可回指当前组源内容 | `FAIL-SHEET-SCRIPTED-PROJECTION` | `references/group-source-extraction.md` |
| `G3B-PROMPT-ATOMS` | prompt / plan 逐 panel 包含 `visual_prompt_atoms`，每个 atom 至少有 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip 和 negative_prompt_atoms；不得只用摘要、完整组稿或通用模板让 imagegen 自行理解 | `FAIL-SHEET-PROMPT-ATOMS` | `references/prompt-assembly-contract.md` |
| `G4-CONTENT` | prompt 主体直接引用 `10-分组` 对应分镜组完整内容，源分镜顺序与底部 YAML 完整 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `G5-SUBJECTS` | Characters / Scene / Props 只来自组底 YAML | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G6-SLOTS` | 只绑定存在图片；同一主体有多视图时必须优先绑定多视图，只有缺多视图时才用主图；缺图不留空路径 | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G7-SUBJECT-FIDELITY` | manifest、prompt 和 imagegen plan 均声明参照图用于黑白线稿下的角色身份、场景空间结构、道具外形保真；不得把全局风格或场景光影氛围作为风格词 | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `G8-LAYOUT` | prompt、imagegen plan 和 result 均声明 `resolution_target: 4K`、默认 locked `panel_image_aspect_ratio: 16:9`、panel 图片下方 `rich_brief` 分镜描述文字、每个可见角色头顶黑色角色名、受控彩色标注系统和 layout aspect decision；不得降级为 2K | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G8A-LAYOUT-ASPECT` | `layout_aspect_decision` 先按实际 panel 数和目标单格比例反推候选行列、整图比例、`panel_geometry_blueprint` 与 `gpt-image-2` 合法尺寸；每个 image box 锁定 16:9 且 `panel_image_box_ratio_error <= 0.06`；不得固定整图比例后挤压 panel | `FAIL-SHEET-LAYOUT-ASPECT` | `references/imagegen-handoff.md` |
| `G8B-FLOOR-PLAN` | 每个分镜组在 storyboard sheet 前有顶视图 `spatial_floor_plan`，清楚展示场景边界、角色站位/朝向、道具位置、摄影机位置/方向、运动路径，并能对应 frame units | `FAIL-SHEET-FLOOR-PLAN` | `references/spatial-floor-plan-contract.md` |
| `G8C-FLOOR-PLAN-CONTINUITY` | 当前平面图与上一张已验收平面图的空间变化逻辑连续，记录 unchanged anchors、changed positions 和 movement logic | `FAIL-SHEET-FLOOR-PLAN-CONTINUITY` | `references/spatial-floor-plan-contract.md` |
| `G8D-FLOOR-PLAN-ACCEPTANCE` | `spatial_floor_plan.acceptance.verdict == accepted` 后才允许进入 storyboard sheet imagegen | `FAIL-SHEET-FLOOR-PLAN-GATE` | `references/spatial-floor-plan-contract.md` |
| `G8E-FLOOR-PLAN-MAPPING` | accepted floor plan 已逐 panel 转译为 `floor_plan_to_panel_mapping`，每格能回指平面图区域、角色站位/朝向、道具位置、摄影机方向、运动路径和禁止空间漂移项 | `FAIL-SHEET-FLOOR-PLAN-MAPPING` | `references/spatial-floor-plan-contract.md` |
| `G9-HANDOFF` | imagegen mode 合法，未经许可不切 CLI/API fallback | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G10-PERSIST` | 生成图片或计划输出位于项目目录，不只在 `$CODEX_HOME`；不得静默覆盖已有文件，除非用户明确要求 rerun / replace | `FAIL-SHEET-IMAGEGEN` | `.agents/skills/cli/imagegen/references/output-persistence.md` |
| `G11-REF-INPUT` | 若绑定本地参照图，生成前必须逐张 `view_image` 且 results/report 记录 `reference_input_status: visible_in_conversation_context`；确无绑定图片时记录 `no_reference_images_bound` | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G12-REPORT` | 执行报告列出 generated / skipped / failed 与返工入口；目标组没有生成图片路径时 verdict 不得为 pass / pass_with_todo | `FAIL-SHEET-REPORT` | `templates/output-template.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-PREFIX
    - G2A-STYLE-LOCK
    - G3-FRAME-UNITS
    - G3A-SOURCE-COMPREHENSION
    - G3B-PROMPT-ATOMS
    - G4-CONTENT
    - G5-SUBJECTS
    - G6-SLOTS
    - G7-SUBJECT-FIDELITY
    - G8-LAYOUT
    - G8A-LAYOUT-ASPECT
    - G8B-FLOOR-PLAN
    - G8C-FLOOR-PLAN-CONTINUITY
    - G8D-FLOOR-PLAN-ACCEPTANCE
    - G8E-FLOOR-PLAN-MAPPING
  todos: []
```
