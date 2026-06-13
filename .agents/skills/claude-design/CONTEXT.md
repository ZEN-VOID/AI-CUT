# Claude Design Codex Adapter Context

## Purpose & Loading Contract

- 本文件是 `.agents/skills/claude-design` 的经验层知识库，不是第二份设计执行合同。
- 调用 `.agents/skills/claude-design/SKILL.md` 时，必须同时加载本文件。
- 上游 `references/upstream/` 只提供设计参考；运行时 gate 以本地 `SKILL.md` 为准。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-design-heuristics-focused

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| Functional HTML but generic visual result | visual system missing | 回到 `N3-VISUAL-SYSTEM`，补 typography、color logic、layout rhythm、component hierarchy 和 media treatment | `quality_verdict` 必须拒绝 generic card layout | visual_system and quality_verdict visible |
| Context is loaded but not applied | context processing gap | 回到 `Context Processing Contract` 和 `N1-INTAKE`，生成 `loaded_context_manifest`、missing policy 和 conflict map | Final handoff must show loaded context and selected_modules separately | loaded_context_manifest and context_application visible |
| Lesson courseware artifact changes course truth | source boundary drift | 回到 `N4-SOURCE-BOUNDARY`，恢复 lesson page/slide plan 和 forbidden_content_changes | Lesson handoff must name source boundary before build | source_boundary cites leaf packet |
| Upstream modules loaded loosely or not named | module selection gap | 回到 `N2-REFERENCE-SELECTION`，按 artifact type 选择 required references | Final handoff always returns selected_modules | selected_modules match route |
| Script or template authors creative decisions | LLM-first authorship breach | 废弃机械生成的 visual_system、layout/copy decision 或 image prompt wording，回到 `N3/N4/N5` 逐条理解目标对象后落盘 | Scripts and templates may verify or scaffold mechanics only | authorship_note and script_boundary_status |
| Browser-ready artifact not verified | verification gap | 回到 `N7-VERIFY`，执行 browser/viewport/console/export 检查或写 blocker | Verification is zero-tolerance for runnable final artifacts | verification evidence or blocker |
| Final artifact is described but not written | writeback gap | 回到 `N5-BUILD`，把 artifact 写到 approved target path，或返回 blocked reason | Artifact tasks require `artifact_paths` plus `writeback_status`, not only a design description | artifact_paths and writeback_status |
| Brand/product surface invents assets or facts | brand fact drift | Load brand-context and fact-verification modules, then replace invented assets with sourced, generated, or labeled placeholders | Brand-aware route requires fact/asset boundary | brand_context and asset_manifest |
| PPT/HTML/courseware needs image elements but ships placeholders | asset bridge missing | 回到 `N5A-ASSET-BRIDGE`，加载 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`，生成或阻断并记录 fallback | Generated bitmap assets for artifacts must go through imagegen and persist in workspace | asset_generation_status and generated_asset_paths |
| Generated asset remains outside artifact workspace | asset persistence gap | 把最终图像复制/移动到 artifact assets 目录并更新引用 | Project-bound generated assets cannot remain only under `$CODEX_HOME` | artifact references workspace asset paths |
| Generated asset clashes with deck/HTML/courseware style | style adaptation gap | 回到 `N5A-ASSET-BRIDGE`，从 `visual_system` 提炼 `style_adaptation_profile` 后重建 imagegen prompt | Generated assets must inherit palette, shape language, texture, lighting, density, and composition rules from the artifact | style_adaptation_profile and style-fit verdict |
| Variants only change palette | variation weakness | 回到 `N6-VARIANTS`，让 alternatives differ by layout logic, density, navigation, or interaction model | Variants must affect experience, not only color | variant_summary |

## Repair Playbook

1. 先判断 artifact medium：HTML page、courseware、deck surface、prototype、poster、canvas 或 React/Babel prototype。
2. 再锁定 source boundary：哪些内容可改、哪些事实或 lesson plan 不可改。
3. 把本地上下文、触发的 upstream 模块和缺失上下文处理成 `loaded_context_manifest`；不要只读不消费。
4. 按 route 选择 upstream modules；courseware/deck 默认至少使用 design-principles、output-formats 和 verification。
5. 在实现前声明 visual system；不允许只用“高级、现代、简洁”这类形容词，也不允许脚本或模板生成最终设计决策。
6. 如果 PPT、HTML、deck 或课件 artifact 缺少必要图片元素，先判断是真实品牌/事实素材、可生成装饰/概念图、还是应保守占位；可生成时从 `visual_system` 提炼 `style_adaptation_profile`，再调用 `.agents/skills/cli/imagegen`，并把最终图像落到 artifact 目录或 approved assets 目录。
7. 实现或修改 artifact 时必须真实写入 approved target path；如果工具或路径阻断，返回 `writeback_status=blocked` 和原因，不得只给设计说明。
8. 实现或修改 artifact 后，必须做浏览器、viewport、console、interaction、export、asset rendering 或 blocker 验证。
9. 若结果普通、模板化、层级弱、文本拥挤、图片缺失、图片风格割裂或响应式不稳，回到 `N3/N5A/N5/N7` 修，而不是在最终报告里粉饰。
10. Lesson handoff 只消费 page/slide plan 和 manifest 边界，不改课程正文、评测、speaker notes 或父包真源。

## Reusable Heuristics

- For a messy HTML/PPT/courseware artifact, first separate content completeness from layout craft. Stabilize source text or document order, then redesign the surface.
- If content is already title-like and thin, expand it using local project resources before visual polish. Do not pad with generic filler.
- For courseware HTML, favor professional learning-product interfaces: dense but breathable sections, clear progression, examples, checklists, and practical artifacts. Avoid landing-page theatrics unless the user asks for a marketing page.
- Browser verification is part of the design pass whenever HTML is produced or substantially changed.
- Final artifact generation is not complete until `artifact_paths` exist and `writeback_status` is explicit; target descriptions alone are planning artifacts, not delivered artifacts.
- For lesson courseware/deck handoffs, always consume the lesson page/slide plan as source truth, then maximize design craft through `design-principles.md`, `output-formats.md`, and `verification.md`; do not stop at a plain conversion.
- For PPT/HTML/courseware artifacts, missing image needs should become an asset_generation_plan, not silent placeholders. Use imagegen for generated bitmap elements when the asset is illustrative/conceptual and safe to create.
- Style adaptation should be concrete, not a loose phrase. Convert `visual_system` into prompt constraints for palette, contrast, shape language, texture/material, lighting, composition, detail density, and explicit style mismatches to avoid.
- Generated images used by an artifact should live beside the artifact, such as `assets/generated/`, and the final HTML/deck must reference that workspace path.
- A design is not acceptable merely because it is clean. It needs a visible system, strong information hierarchy, purposeful spacing, responsive behavior, and a quality verdict tied to the brief.
- `loaded_context_manifest` is useful because it prevents "I read it" from masquerading as "I applied it." Keep it concise: local context, route modules, missing inputs, conflicts, and writeback decision.
- For this design skill, LLM-first does not mean avoiding code; it means scripts never choose the creative content, hierarchy, image prompt constraints, or quality verdict.

## Known Failure Modes

- Loading every upstream reference creates noise. Load only the references triggered by the matrix.
- "Beautiful" often hides a format problem. Decide whether the artifact is a report, deck, prototype, class handout, landing page, or visual canvas before styling.
- Missing media should remain a labeled placeholder or be sourced/generated under explicit constraints; for PPT/HTML/courseware generation, safe generated bitmap assets should route through `.agents/skills/cli/imagegen` instead of ad hoc prompt fragments inside the design artifact.
- Do not use generated images as fake evidence, fake product screenshots, or real brand assets. Brand/fact surfaces require sourced assets or clearly labeled illustrative substitutes.
- "Same style as the page" is too weak for imagegen handoff. If the prompt does not expose reusable style constraints, generated assets tend to drift toward generic illustration or stock-photo language.
- Returning a generic card layout without module selection, visual-system evidence, or browser verification is a design failure; reroute to the Design Excellence Contract.
- A validation pass can still miss semantic incompleteness. When upgrading this package, separately check Core Task, Context Processing, LLM-first authorship, Visual Maps, and test prompt coverage.
