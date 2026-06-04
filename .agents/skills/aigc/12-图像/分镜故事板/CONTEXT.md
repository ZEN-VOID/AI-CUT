# Context: aigc-image-storyboard-sheet

本文件是 `B-分镜故事板` 的经验层知识库，不是执行日志。它用于沉淀从 `10-分组` 生成组级多格 storyboard 时的类型判断、修复打法和可复用经验。

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
| `TM-SHEET-12` | panel 图片比例漂移或被固定成不适合 storyboard 的比例 | aspect ratio drift | 恢复默认 `panel_image_aspect_ratio: 16:9`；仅用户显式要求才改 9:16 或其他 | group extraction、prompt、handoff 固化默认比例 | group-index/prompt/plan 均记录 16:9 或用户指定比例 |
| `TM-SHEET-13` | 黑白线稿丢失角色、场景或道具既有形象 | subject fidelity loss | 重新绑定 YAML 主体参照并要求还原身份、轮廓、空间结构和道具外形 | reference 与 handoff gate 固化主体保真锚定 | bound references 可见且 plan 记录 subject fidelity |
| `TM-SHEET-14` | 彩色被用于角色、服装、背景或氛围渲染 | annotation color drift | 恢复黑白线稿基底，把颜色限制到标注系统 | prompt、handoff 与 review gate 固化 annotation color system | plan/report 记录 red/blue/green/orange/purple/black 语义且 color rendering forbidden |
| `TM-SHEET-15` | 标注颜色语义混乱，例如蓝色表示身体动作或红色表示摄影机 | annotation semantic drift | 按用户声明的颜色语义重建 `annotation_plan` | frame unit 与 imagegen plan 固化颜色图例 | 每个 frame unit 的 annotation plan 语义正确或写 none |
| `TM-SHEET-16` | 可见角色头顶缺少角色名，或角色名与分组稿/YAML 不一致 | character label drift | 从组底 YAML `角色` 字段重建 `character_name_labels`，放在对应角色头顶 | group extraction、prompt、handoff 与 review gate 固化角色头顶名称字段 | 每个可见角色都有黑色文本角色名，且未改名、缩写、翻译或猜名 |
| `TM-SHEET-17` | panel 下方文字过短像标签、过长不可读，或出现原文没有的新事实 | panel description density drift | 由 LLM 从 `source_span` 和分组稿分镜描述原文重建 `rich_brief panel_description` | group extraction、prompt、handoff 与 review gate 固化 rich_brief 描述密度 | 每个 panel 描述 1-2 句、来源可回指、信息足够且无新增事实 |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、主体参照、imagegen handoff、输出持久化还是报告闭环。
2. 若 `group_id` 不唯一或组正文截断，回到 `references/group-source-extraction.md` 重新建立 `group-index.json`。
3. 若任务执行前缀不是当前合同文本，回到 `references/prompt-assembly-contract.md` 重写 prompt 包。
4. 若主体来自正文而非 YAML，清空该轮绑定，重新从 fenced YAML 建立 subject list。
5. 若存在 `-多视图.png|jpg|jpeg|webp`，不得退到 `-主图`。
6. 若只有 `.json` 设计稿而无图片，主体应进入 `missing`，不要保留空字符串路径。
7. 若批量 imagegen 部分失败，保留成功结果，报告失败组与可重试命令，不回滚成功图片。
8. 若镜头数过多导致单图完整性风险，优先报告分页/分批建议；没有用户确认前不要擅自拆分 canonical 组。
9. built-in `image_gen` 使用本地参照图时，路径记录不够；必须先 `view_image` 让图片进入对话上下文。确无绑定图片时才记录 `reference_input_status: no_reference_images_bound` 并走 text-prompt-only。
10. 若 panel 数与原始 `分镜N` 标签数不一致，不是错误；只要 `storyboard_frame_units` 能回指源正文，就按 frame units 生成。
11. 分镜故事板不再援引全局风格或场景光影氛围作为风格词；统一使用标准分镜手稿风格黑白线稿。
12. 场景参照图只承担空间结构和主体身份锚定；角色参照图承担身份/轮廓锚定；道具参照图承担形状与关键细节锚定。
13. 多格 storyboard 不适合沿用 2K 默认；即便单组 frame units 不多，也按 4K 固定生成，避免后续放大审片时 panel 不清晰。
14. 每个 panel 都要有图片区和下方文字区；文字区来自 `panel_description`，不能遮挡 panel 图片。
14A. `panel_description` 不应只写短标签；默认用 `rich_brief`，由 LLM 从分组稿对应分镜描述原文保真精简为 1-2 句，优先保留主体/动作/画面状态、构图/运镜、情绪/叙事强调和关键场景/道具，删除重复修饰和过长对白。
15. panel 图片区默认 16:9；用户显式要求时才改为 9:16 或其他比例。
16. 彩色只允许作为标注叠加在黑白线稿基底上：红=身体运动、蓝=摄影机运动、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑色文本=角色头顶名称、简短镜头笔记和面板标签。
17. 若某 panel 没有对应标注信息，`annotation_plan` 中该项写 `none`；不要为了使用某个颜色而发明不存在的信息。
18. 每个可见角色头顶都要有黑色文本角色名；名称来自分组稿或组底 YAML `角色` 字段，不从参照图文件名、外观或正文泛称猜测。

## Reusable Heuristics

- `B-分镜故事板` 的核心对象是 `group_id`，不是四段式单镜 `shot_id`。
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
- 缺图不是阻塞 prompt 的理由，但必须阻塞“伪绑定”；空槽位应移除或进入 missing。
- 批量生成默认是计划层能力，不等于后台并行执行；索引、prompt 包、manifest 和报告应统一汇流写入。
- 已绑定本地参照图必须在生成前通过 `view_image` 可见化；否则只能算路径证据，不能算已传入视觉参照。
