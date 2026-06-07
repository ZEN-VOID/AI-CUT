# Context: aigc-image-storyboard-sheet

本文件是 `分镜故事板` 的经验层知识库，不是执行日志。它用于沉淀从 `10-分组` 生成组级多格 storyboard 时的类型判断、修复打法和可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-group-storyboard-specific
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-SHEET-01` | prompt 像单帧画面而不是多格 storyboard | prompt object boundary | 恢复任务执行前缀，并保留完整分镜组内容 | 在 `prompt-assembly-contract.md` 固化组级边界 | prompt 第一行即声明 storyboard sheet |
| `TM-SHEET-02` | 绑定了正文泛称主体而不是 YAML 主体 | subject source drift | 只消费组底 YAML 的 `角色 / 场景 / 道具` | reference gate 检查 `source: group_yaml` | manifest 中每个主体可回指 YAML |
| `TM-SHEET-03` | 有多视图图却绑定到主图 | asset priority drift | 重新扫描同名 `-多视图` 图片 | 在绑定规则中固定多视图优先 | bound 条目记录 `selected_variant: multi_view` |
| `TM-SHEET-04` | 只有 JSON 没有 PNG/JPEG/WebP 却被视为可参照 | asset existence drift | 将该主体列入 missing 并移除参照槽位 | binding gate 要求真实图片存在 | 所有 bound path 均存在且为图片 |
| `TM-SHEET-05` | 批量执行覆盖同一输出文件 | execution boundary | 一组一文件，已有文件按 rerun 策略处理 | imagegen plan 固定 group_id 级写锁 | `images/<group_id>.png` 无多任务冲突 |
| `TM-SHEET-06` | 组正文被摘要导致镜头缺失 | source fidelity | 使用原组正文作为 prompt 主体，不做压缩 | review 检查分镜编号完整性 | 分镜1..N 均出现在 prompt 主体 |
| `TM-SHEET-07` | 本地参照图只写入路径但未进入对话上下文 | imagegen source semantics | 生成前逐张 `view_image` 已绑定本地图片并标注角色 | 在 handoff 与 review gate 固化 `view_image` 前置门禁 | results/report 记录 `reference_input_status: visible_in_conversation_context` |
| `TM-SHEET-08` | storyboard 每格被机械映射成原文 `分镜1`、`分镜2` | panel mapping drift | 重建 `storyboard_frame_units`，按当前分组正文中的视觉节拍判断 panel 落点 | group extraction 与 prompt gate 固化 frame-unit plan | 每个 panel 有 `source_span`，且允许 split/merge |
| `TM-SHEET-09` | prompt 援引全局风格或场景光影氛围作为风格词 | style source drift | 删除全局/场景风格词，恢复标准分镜手稿风格黑白线稿基底 + 受控彩色标注任务前缀 | prompt、handoff 与 review gate 固化 `standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors` | manifest/prompt/plan 均记录 global style forbidden |
| `TM-SHEET-10` | 分镜故事板 2K 出图导致单个 panel 细节不清晰 | resolution target too low | 将 prompt、plan、result 的 `resolution_target` 统一改为 `4K` | imagegen handoff 与 review gate 固化 4K 默认 | prompt / plan / report 均记录 4K |
| `TM-SHEET-11` | panel 只有画面没有分镜描述文字 | panel text missing | 从 `source_span` 补 `rich_brief panel_description`，放在对应 panel 图片下方 | prompt 与 review gate 固化 panel 下方描述文字 | 每个 frame unit 均有 `panel_description` 与 `panel_description_density` |
| `TM-SHEET-12` | panel 图片比例漂移或被固定成不适合 storyboard 的比例 | aspect ratio drift | 恢复默认 locked `panel_image_aspect_ratio: 16:9`，补 `panel_geometry_blueprint`；仅用户显式要求才改 9:16 或其他 | group extraction、prompt、handoff 固化默认比例和几何蓝图 | group-index/prompt/plan 均记录 locked 16:9、image_box 坐标和用户指定比例 |
| `TM-SHEET-13` | 黑白线稿丢失角色、场景或道具既有形象 | subject fidelity loss | 重新绑定 YAML 主体参照并要求还原身份、轮廓、空间结构和道具外形 | reference 与 handoff gate 固化主体保真锚定 | bound references 可见且 plan 记录 subject fidelity |
| `TM-SHEET-14` | 彩色被用于角色、服装、背景或氛围渲染 | annotation color drift | 恢复黑白线稿基底，把颜色限制到标注系统 | prompt、handoff 与 review gate 固化 annotation color system | plan/report 记录 red/blue/green/orange/purple/black 语义且 color rendering forbidden |
| `TM-SHEET-15` | 标注颜色语义混乱，例如蓝色表示身体动作或红色表示摄影机 | annotation semantic drift | 按用户声明的颜色语义重建 `annotation_plan` | frame unit 与 imagegen plan 固化颜色图例 | 每个 frame unit 的 annotation plan 语义正确或写 none |
| `TM-SHEET-16` | 可见角色头顶缺少角色名，或角色名与分组稿/YAML 不一致 | character label drift | 从组底 YAML `角色` 字段重建 `character_name_labels`，放在对应角色头顶 | group extraction、prompt、handoff 与 review gate 固化角色头顶名称字段 | 每个可见角色都有黑色文本角色名，且未改名、缩写、翻译或猜名 |
| `TM-SHEET-17` | panel 下方文字过短像标签、过长不可读，或出现原文没有的新事实 | panel description density drift | 由 LLM 从 `source_span` 和分组稿分镜描述原文重建 `rich_brief panel_description` | group extraction、prompt、handoff 与 review gate 固化 rich_brief 描述密度 | 每个 panel 描述 1-2 句、来源可回指、信息足够且无新增事实 |
| `TM-SHEET-18` | 多组 storyboard prompt 只替换主体名、场景名或颜色标注，句架高度重复但形式字段齐全 | scripted authorship pseudo-difference | 标记 `FAIL-SHEET-SCRIPTED-PROJECTION`，回到完整组稿由 LLM 重建 frame-unit plan、panel 描述、annotation plan 和 layout 策略 | Pass Table 固化脚本化生成、批量插入、正则套句和映射投影不得通过 | 每组输出能指出本组独有 source_span 判断，而不只是锚点替换 |
| `TM-SHEET-19` | panel 图片区被压扁，或整张 storyboard 固定 16:9 后导致单格比例不对 | sheet aspect decision missing | 根据实际 `storyboard_frame_units.length` 重算 `layout_aspect_decision`：枚举行列，建立 `panel_geometry_blueprint`，锁定每个 16:9 image_box，选择 `gpt-image-2` 合法 `selected_sheet_size`；必要时分页/多 sheet | group extraction、prompt、handoff 与 review gate 固化 `G8A-LAYOUT-ASPECT` | plan/report 记录 panel_count、candidate_grids、selected_grid、selected_sheet_size、panel_geometry_blueprint、panel_image_box_ratio_error |
| `TM-SHEET-24` | 已声明 16:9，但成图里的 panel 仍像竖条、扁条或不同格比例不一致 | image box geometry missing | 不再只写比例；在 prompt/plan 中加入每格 `cell_norm`、`image_box_norm`、`text_strip_norm`，要求先画可见 16:9 图片框再填内容 | prompt template 和 imagegen handoff 固化 `panel_geometry_blueprint` | 每个 panel 的 image_box 有可见边框，`ratio_error <= 0.06`，文字条不侵入图片区 |
| `TM-SHEET-20` | prompt 形式完整但对现有分组内容理解浅，panel 设计像通用模板 | source comprehension shallow | 回到完整组稿，补 `source_comprehension`：叙事功能、动作链、空间/主体/道具锚点、视觉转折、必须保留事实和禁止补写项 | workflow 增加 source comprehension gate，脚本不得生成理解摘要 | 每组 source comprehension 有具体 source anchor，不是“保持一致/突出情绪”等泛化句 |
| `TM-SHEET-21` | storyboard 每格角色站位漂移，前后 panel 或相邻分镜组空间关系对不上 | floor plan missing | 在 storyboard 前补 `spatial_floor_plan` 顶视图平面图，验收 accepted 后再生成 storyboard | workflow 增加 N5A-FLOOR-PLAN 与 G8B/G8C/G8D gates | floor-plan manifest 记录顶视图、站位、摄影机、连续性和 accepted verdict |
| `TM-SHEET-22` | 下一个分镜组的角色/道具/摄影机位置与上一个组无逻辑衔接 | floor plan continuity drift | 对照上一张 accepted floor plan，补 unchanged anchors、changed positions、movement logic；连续性失败则返工 | spatial-floor-plan contract 固化 continuity_from_previous | `continuity_from_previous.spatial_consistency_verdict` 为 consistent 或 initial |
| `TM-SHEET-23` | 流程停在 prompt、review、平面图验收或等待确认，没有生成 storyboard sheet 图片 | no-generation close | 回到失败 owning node 自动返工，随后继续 N7 imagegen；不可恢复时只写 failed 报告 | mode/type/review/output gate 固化“生图为结束” | 目标组有持久化图片路径，或报告为 failed 且说明不可恢复输入缺口 |
| `TM-SHEET-25` | 明明要求黑白线稿 + 彩色标注，成图仍漂移成彩色电影 still、写实光影或场景氛围图 | upstream style leakage | 建立 `style_lock_spec`，把完整组稿中的上游电影风格、光影、氛围、胶片颗粒、渲染词隔离为 evidence-only，并从 `visual_prompt_atoms` 删除 | prompt、handoff、review gate 固化 `G2A-STYLE-LOCK` | plan/report 记录 `upstream_style_quarantine`，最终绘制 atoms 只含黑白线稿和标注颜色 |
| `TM-SHEET-26` | 已有 accepted floor plan，但故事板角色站位、方向或镜头仍和它不确定匹配 | floor plan not transduced | 为每个 panel 建 `floor_plan_to_panel_mapping`，逐格绑定平面图区块、角色朝向、道具、摄影机方向和禁止漂移项 | spatial-floor-plan、prompt、handoff 固化 `G8E-FLOOR-PLAN-MAPPING` | 每个 panel 可回指 floor plan 区域和 camera cone；只写 floor plan path 不通过 |
| `TM-SHEET-27` | prompt 看起来完整，但生图对分镜组内容理解不精准，画面像通用摘要或模型自行脑补 | executable prompt atoms missing | 从 `source_span`、panel description、annotation plan 和 floor-plan mapping 逐 panel 写 `visual_prompt_atoms` | prompt、handoff、review gate 固化 `G3B-PROMPT-ATOMS` | 每个 panel 有 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip、negative_prompt_atoms |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、主体参照、imagegen handoff、输出持久化还是报告闭环。
2. 若 `group_id` 不唯一或组正文截断，回到 `references/group-source-extraction.md` 重新建立 `group-index.json`。
3. 若任务执行前缀不是当前合同文本，回到 `references/prompt-assembly-contract.md` 重写 prompt 包。
4. 若主体来自正文而非 YAML，清空该轮绑定，重新从 fenced YAML 建立 subject list。
5. 若存在 `-多视图.png|jpg|jpeg|webp`，不得退到 `-主图`。
6. 若只有 `.json` 设计稿而无图片，主体应进入 `missing`，不要保留空字符串路径。
7. 若批量 imagegen 部分失败，保留成功结果，报告失败组与可重试命令，不回滚成功图片。
8. 若镜头数过多导致单图完整性风险，自动采用分页或多 sheet，并在计划/报告中记录拆分理由、页码和覆盖的 frame units；不要等待用户确认，也不要删减视觉节拍。
9. built-in `image_gen` 使用本地参照图时，路径记录不够；必须先 `view_image` 让图片进入对话上下文。确无绑定图片时才记录 `reference_input_status: no_reference_images_bound` 并走 text-prompt-only。
10. 若 panel 数与原始 `分镜N` 标签数不一致，不是错误；只要 `storyboard_frame_units` 能回指源正文，就按 frame units 生成。
11. 分镜故事板不再援引全局风格或场景光影氛围作为风格词；统一使用标准分镜手稿风格黑白线稿。
12. 场景参照图只承担空间结构和主体身份锚定；角色参照图承担身份/轮廓锚定；道具参照图承担形状与关键细节锚定。
13. 多格 storyboard 不适合沿用 2K 默认；即便单组 frame units 不多，也按 4K 固定生成，避免后续放大审片时 panel 不清晰。
14. 每个 panel 都要有图片区和下方文字区；文字区来自 `panel_description`，不能遮挡 panel 图片。
14A. `panel_description` 不应只写短标签；默认用 `rich_brief`，由 LLM 从分组稿对应分镜描述原文保真精简为 1-2 句，优先保留主体/动作/画面状态、构图/运镜、情绪/叙事强调和关键场景/道具，删除重复修饰和过长对白。
15. panel 图片区默认 locked 16:9 image box；用户显式要求时才改为 9:16 或其他比例。不要只写“16:9”，必须给出 image box 几何坐标。
15A. 整张 sheet 画布比例必须由当前组 frame-unit 数量反推：先确定 `panel_count`，再用目标 panel 图片比例、下方文字区和标注安全边距枚举行列候选，建立 `panel_geometry_blueprint`，最后选择 `gpt-image-2` 合法尺寸。不要把整图固定为 16:9 后压缩每个 panel。
15C. `panel_geometry_blueprint` 是比例感的硬门槛：每个 panel 需要 `cell_norm`、`image_box_norm`、`text_strip_norm`、`image_box_aspect_ratio: 16:9` 和 `ratio_error <= 0.06`；cell 里可以留白，image box 不可以拉伸。
15B. `gpt-image-2` 合法尺寸检查应使用本地 imagegen 合同：最大边 `<=3840px`、宽高为 `16px` 倍数、长短边比例 `<=3:1`、总像素 `655360..8294400`。4K storyboard 优先使用接近上限像素预算的合法尺寸。
16. 彩色只允许作为标注叠加在黑白线稿基底上：红=身体运动、蓝=摄影机运动、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑色文本=角色头顶名称、简短镜头笔记和面板标签。
17. 若某 panel 没有对应标注信息，`annotation_plan` 中该项写 `none`；不要为了使用某个颜色而发明不存在的信息。
18. 每个可见角色头顶都要有黑色文本角色名；名称来自分组稿或组底 YAML `角色` 字段，不从参照图文件名、外观或正文泛称猜测。
19. 如果 storyboard prompt 的差异主要来自 `group_id`、角色名、场景名、道具名或同义词替换，而 panel 设计、镜头功能和标注计划没有本组源 span 的判断痕迹，应视为伪差异，不得用形式完整性放行。
20. 如果 source comprehension 不能说明本组动作链、空间锚点、主体/道具状态和禁止补写项，就不要进入 layout 或 imagegen；这通常意味着模型还没有真正理解现有内容。
21. storyboard sheet 前必须有顶视图 `spatial_floor_plan`；它用于锁空间站位，不是场景插画、透视图或氛围图。
22. 相邻组的 floor plan 必须连续；不要让角色从上一组位置无解释地跳到新位置，也不要让摄影机方向与 frame units 不对应。
23. 分镜故事板技能包的自然终点是已持久化的 storyboard sheet 图片；prompt 包、review note、floor plan acceptance 都只是内部工件，不能作为完成态。
24. 如果完整组稿里保留了“全局风格”“35mm 胶片”“体积光”“光影和氛围与场景参照图保持一致”等上游风格句，必须在 `style_lock_spec.upstream_style_quarantine` 中逐项隔离；不要相信一句“黑白线稿”前缀能压住后文长段电影风格。
25. accepted floor plan 不等于 storyboard 已锁空间；必须有 `floor_plan_to_panel_mapping`，否则生图模型仍可能只按构图美观重摆角色。
26. `panel_description` 是读图文字，`visual_prompt_atoms` 才是生图执行指令；缺 atoms 时，模型容易把长组稿压成泛化画面。

## Reusable Heuristics

- `分镜故事板` 的核心对象是 `group_id`，不是四段式单镜 `shot_id`。
- `source_shot_labels` 是运镜中心结果的追溯标签，`storyboard_frame_units` 才是多格 storyboard 的 panel 落点。
- `10-分组` 已经包含足够的组级风格、场景、分镜明细和入出场信息；本技能不需要重新蒸馏上游剧情。
- 组底 YAML 是主体参照绑定的唯一默认入口；正文中出现的普通名词不自动变成参照对象。
- 多格 storyboard 的任务执行前缀必须足够明确，否则生图模型容易把它当成单张电影 still 或彩色电影画面。
- 分镜故事板默认 4K 出图；2K 是单格可读性风险，不作为本技能可接受默认值。
- 标准分镜手稿风格黑白线稿是本技能唯一默认画风；全局风格文字不是本技能的风格来源。
- 彩色标注系统是信息层，不是画风层；一旦颜色进入渲染、服装、背景或氛围，就应判定为漂移。
- 黑白线稿不等于放弃主体一致性；所有已绑定主体参照都要服务角色、场景、道具的形象还原。
- 角色头顶名称是读图索引层；它必须使用分组稿/YAML 角色名原文，不能被模型改成外号、英文名、泛称或外观描述。
- panel 下方描述是读图说明层；它应该比单词标签丰富，但仍是压缩后的分镜说明，不是剧本正文复刻。
- 整张 storyboard sheet 的比例不是默认 16:9；它应由 panel 数量和 locked 16:9 image box 反推。2 panels 可能接近宽画幅，3 panels 通常需要比较 3x1 与 2x2 在 `gpt-image-2` `3:1` 上限内的取舍，更多 panel 通常需要网格或分页。
- panel 比例感不能只靠自然语言声明；必须在 prompt 和 plan 中给出 `panel_geometry_blueprint`，让模型先画固定 16:9 图片框和下方文字条。
- source comprehension 是防止浅理解的前置证据；它不暴露自由思维链，只记录可审计的源内容理解摘要和事实边界。
- style lock 是防止画风漂移的前置证据；凡完整组稿带有电影风格词，都要隔离成 evidence-only，并在最终 atoms 中只保留黑白线稿和标注系统。
- visual prompt atoms 是防止生图不精准的执行层；每格至少要写清可见主体、动作/状态、空间锚点、机位/构图、线稿要求、标注覆盖、文字条和负向原子。
- spatial floor plan 是防止角色空间站位漂移的前置证据；只有 accepted floor plan 才能进入 storyboard sheet generation。
- floor plan to panel mapping 是 accepted floor plan 到 storyboard sheet 的桥；没有这层桥，平面图只是附件，不是每格画面的站位约束。
- floor plan 连续性要按同一集内分镜组顺序审查：第一组是 initial，之后每组都要说明相对上一张 accepted floor plan 的不变锚点与变化路径。
- floor plan acceptance 是内部自动 gate；不通过就返工平面图或 source comprehension，不能变成等待用户确认的断点。
- 缺图不是阻塞 prompt 的理由，但必须阻塞“伪绑定”；空槽位应移除或进入 missing。
- 批量生成默认是计划层能力，不等于后台并行执行；索引、prompt 包、manifest 和报告应统一汇流写入。
- 已绑定本地参照图必须在生成前通过 `view_image` 可见化；否则只能算路径证据，不能算已传入视觉参照。
- 脚本可以抽取 `source_span`、计数、整理已定 JSON 字段和检查路径。
- 脚本不能生成 source comprehension、panel 描述、annotation plan、floor plan 空间裁决、layout 决策或 prompt 正文，也不能批量插入、正则套句或映射投影；这些位置需要 LLM 主创和可审计源 span 依据。
