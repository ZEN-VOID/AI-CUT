# Changelog

## 2026-06-10

- 执行 Skill 2.0 最新版 runtime-spine 升级：删除 `steps/` 第二节点真源，将 N1-N10 主流程、Mermaid 拓扑、量化口径、注意力协议、checkpoint、模块授权、触发矩阵、汇流门和 review binding 收回 `SKILL.md`。
- 新增 `test-prompts.json`，覆盖单组生成、整集批量和 repair/review 再生成三类回归场景。
- 同步 `types/type-map.md`、默认类型包与 README，不再加载 `steps/storyboard-sheet-workflow.md`。
- 将分镜平面图职责迁移到 `12-图像/分镜平面图` 独立 Skill 2.0 叶子；`分镜故事板` 不再生成、验收或维护平面图，也不再输出 floor-plan manifest / floor-plans 目录。
- 将原 `spatial_floor_plan` / `floor_plan_to_panel_mapping` 前置门禁收束为可选 `spatial_handoff` 消费接口：若 `分镜平面图` 已有 accepted 侧车，可作为站位、动线、机位和空间连续性证据；缺失不得阻断 storyboard sheet imagegen。
- 同步 `SKILL.md`、prompt assembly、imagegen handoff、review gate、workflow、type map、默认类型包、prompt/output template、README、agents metadata 与 CONTEXT，新增 `FAIL-SHEET-SPATIAL-HANDOFF` 误用防护。
- 收紧完成态：`分镜故事板` 不得停在 `imagegen-plan.json`；该文件只是调用 `.agents/skills/cli/imagegen` 的执行载体。
- 同步 `SKILL.md`、imagegen handoff、review、output template、workflow、type map 与 README，明确必须直接调用 `.agents/skills/cli/imagegen` 生成并持久化 `images/<分镜组ID>.png` 后才能 pass。

## 2026-06-07

- 针对 storyboard sheet 成图“风格漂移、平面图不一定匹配、生图提示不精准”的反馈新增三道硬门禁：`style_lock_spec`、`visual_prompt_atoms`、`floor_plan_to_panel_mapping`。
- 强化黑白线稿画风锁定：完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感和胶片颗粒等词必须隔离为 `evidence_only_not_style_directive`，不得进入最终绘制 atoms 或 imagegen 可执行指令。
- 新增逐 panel 生图原子合同：每格必须记录 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip 和 negative_prompt_atoms，避免只用长组稿或摘要让 imagegen 自行理解。
- 新增 accepted floor plan 到 storyboard panel 的映射门：每格必须回指平面图区块、角色站位/朝向、道具位置、摄影机方向、运动路径和禁止空间漂移项；只附 floor plan 路径不得通过。
- 同步 `SKILL.md`、prompt assembly、imagegen handoff、spatial floor plan contract、review gate、workflow、type map、默认类型包、prompt/output template、README 与 CONTEXT，新增 `FAIL-SHEET-STYLE-LOCK`、`FAIL-SHEET-PROMPT-ATOMS`、`FAIL-SHEET-FLOOR-PLAN-MAPPING`。
- 强化 source comprehension 前置节点：生成 frame units 前必须先记录本组叙事功能、动作链、空间/主体/道具锚点、视觉转折、必须保留源事实和禁止补写项，避免 prompt 形式完整但对现有内容理解不足。
- 新增 `layout_aspect_decision` 合同：先根据实际 `storyboard_frame_units.length` 和目标单格 panel 比例枚举行列候选，再在 `gpt-image-2` 合法尺寸范围内选择整张 sheet 的比例与 `selected_sheet_size`，不得固定整图比例后挤压 panel。
- 强化 panel 比例感门禁：`layout_aspect_decision` 必须包含 `panel_geometry_blueprint`，逐格记录 `cell_norm`、固定 `16:9 image_box`、`text_strip`、outer margin、gutter 和 `panel_image_box_ratio_error <= 0.06`；只声明 16:9 但没有几何坐标不得通过。
- 新增 `G8A-LAYOUT-ASPECT` review gate 与 `FAIL-SHEET-LAYOUT-ASPECT` 失败码，并同步 prompt template、imagegen handoff、执行报告模板、默认类型包和经验层。
- 新增 storyboard sheet 前置 `spatial_floor_plan`：每个分镜组先生成顶视图空间站位平面图，验收 `accepted` 后才能生成 storyboard sheet；相邻分镜组必须记录与上一张 accepted floor plan 的空间连续性。
- 新增 `G8B-FLOOR-PLAN`、`G8C-FLOOR-PLAN-CONTINUITY`、`G8D-FLOOR-PLAN-ACCEPTANCE` review gates 与对应失败码，并同步 workflow、prompt package、imagegen handoff、输出模板、类型包和经验层。
- 收紧完成态：`分镜故事板` 技能包不得以 prompt-only、review-only、平面图验收或等待确认作为完成态；所有内部 gate 失败均应自动返工并继续 imagegen，最终 pass 必须包含持久化 storyboard sheet 图片路径。

## 2026-06-04

- 将项目输出根从旧 `12-图像/B-分镜故事板` 收敛为与叶子技能包名一致的 `12-图像/分镜故事板`，并同步 `SKILL.md`、模板、README、CONTEXT、references、types、agents metadata 与父级/registry/query 引用。
- 将分镜故事板默认画风收束为标准分镜手稿风格黑白线稿；不再援引项目全局风格、north star 全局画风或场景光影氛围作为风格词。
- 在黑白线稿基底上新增受控彩色标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签；颜色不得用于角色、背景、光影或氛围渲染。
- 新增角色头顶名称规则：每个可见角色头顶必须显示与分组稿/组底 YAML `角色` 字段一致的黑色角色名，不得简写、改名、翻译或按外观猜名。
- 调整 prompt / imagegen 逻辑：以 `10-分组` 对应分镜组完整内容为生图基础，添加本技能任务执行前缀，并按组底 YAML 绑定角色、场景、道具参照图。
- 新增 panel 结构约束：每格包含默认 16:9 图片区和位于图片下方的分镜描述文字；用户显式要求时可调整为 9:16 或其他比例。
- 新增 `rich_brief` panel 描述规则：每格文字由 LLM 从分组稿分镜描述原文保真精简为 1-2 句，信息比短标签更完整，但必须控制长度、来源和新增事实风险。
- 调整排版合同：layout 根据 `storyboard_frame_units` 数量自适应，frame units 过多时记录分页或多 sheet 策略。
- 调整主体参照职责：即便输出黑白线稿，也必须还原已有角色身份、场景空间结构和道具外形；场景图不再作为风格/光影/氛围锚点。

## 2026-05-08

- 调整 storyboard panel 落点规则：新增 `storyboard_frame_units`，要求基于 `10-分组` 当前组正文中的视觉节拍识别 panel，而不是把原始 `分镜1`、`分镜2` 机械映射为 storyboard 格子；允许 split/merge，但每个 panel 必须能回指源正文。
- 强化场景参照图职责：场景图除空间参照外，必须同步作为生成画面的风格、光影和氛围锚点；prompt、reference manifest、imagegen plan 和 review gate 均需记录该约束。
- 固化分镜故事板 4K 出图要求：因多 panel 单格面积较小，本技能不再沿用 imagegen 通用 2K 默认，prompt、imagegen plan、result 与 review gate 均需记录 `resolution_target: 4K`。

## 2026-05-01

- 收紧图片参照选择规则：同一主体如有多视图可选，prompt slot、reference manifest 与 imagegen plan 均优先使用多视图；只有缺少多视图时才退到主图。
- 强化 built-in `image_gen` 本地参照图语义：已绑定本地图片必须先 `view_image` 进入对话上下文，再执行参照图生成；结果记录 `reference_input_status: visible_in_conversation_context`，确无绑定图片时才使用 `no_reference_images_bound`。

## 2026-04-25

- 初始化 `B-分镜故事板` Skill 2.0 配置。
- 将主信息源固定为 `projects/aigc/<项目名>/10-分组`。
- 固化用户指定的 multi-panel storyboard 固定英文开头。
- 固化组底 YAML 主体参照绑定规则：角色、场景、道具，多视图优先，主图次之，缺图移除槽位。
- 接入 `.agents/skills/cli/imagegen` 作为默认生图执行技能，并声明按分镜组批量计划、顺序或受控批量生成与项目内持久化门禁。
- 明确 built-in `image_gen` 曾可按 `text_prompt_only` 生成并持久化；该口径已由 2026-05-01 的 `view_image` 前置门禁收紧。
