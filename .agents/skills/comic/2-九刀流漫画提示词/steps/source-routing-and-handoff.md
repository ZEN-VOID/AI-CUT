# 来源路由与交接合同

本文件承接 `comic-nine-blade-prompts` 中不属于题材类型包的来源模式、连续性模式和下游交接模式。`types/` 只保留漫画题材与子类型知识包；本文件由 `steps/nine-blade-workflow.md` 消费。

## Mode Index

| mode_id | match_signals | load_mode | owner |
| --- | --- | --- | --- |
| `grouped-script` | 已存在 `第N组.md`、上游 1 号阶段已完成分组、用户明确要求按组跑九刀 | stackable | source routing |
| `raw-source-fallback` | 只有 raw source，没有 `第N组.md` 或 stage-1 产物 | stackable | source routing |
| `multi-episode-continuity` | 用户提到第 2 集/第 3 集、目录已有其他集 JSON、需要保持前集角色和风格 | stackable | continuity routing |
| `poster-aware-handoff` | 下游 4 号剧集海报需要把 panels、角色、场景和风格锚点提炼为海报高光候选 | stackable | handoff routing |

## Default Routing Rule

1. 若 `projects/comic/[项目名]/1-漫画剧本改编/第*.组.md` 存在，默认启用 `grouped-script`。
2. 若用户只给 raw source，启用 `raw-source-fallback`；一旦临时切出 group，后续仍按 group 单位执行。
3. 若检测到多集命名、前序 `第N集-page-group-*` 或用户要求延续前集视觉 DNA，叠加 `multi-episode-continuity`。
4. 若用户提到剧集海报、海报高光、4 号阶段或海报生图，叠加 `poster-aware-handoff`。

## Mode: grouped-script

### Purpose

用于已存在 `1-漫画剧本改编/第N组.md` 的项目。此时 `第N组.md` 是唯一文本真源，一个 group 文件对应一份 `nine_blade_comic_prompts.v1` JSON。

### Fixed Context

- 只把 `【漫剧正文】` 视为业务正文真相权。
- `【本组跨度】`、`【边界判定】`、`【组末钩子】` 只作为切页辅证。
- frontmatter 中的 `type_stack_active_packs` 与 `type_pack_projection_nine_blade` 需要透传到 group JSON。
- 不再额外挂出 `page_group_plan.json` 竞争真源。

### Required Output Bias

- `page_group.group_id` 与文件序号一致，例如 `page-group-01`。
- `page_group.rhythm_rationale` 解释当前组为什么适合压成 9 页。
- `continuity_context` 说明该组继承的角色、风格、场景锁。

### Review Gate

- 确认每个 group 都独立具备 entry hook、中段推进/阻力、exit hook 或余波。
- 确认没有把多个 group 合并成单一 JSON。

## Mode: raw-source-fallback

### Purpose

用于用户只提供 raw source、没有 `第N组.md` 的兼容场景。此模式只允许本轮内部做最小整形与临时切组，不创建第二套长期 canonical 真源。

### Fixed Context

- 先判定 `scene-led / explainer-led / compare`。
- `scene-led` 保留场景动作和对白块。
- `explainer-led` 将摘要压成顺时序事件单元，补人物、场景、转场和视觉动作。
- `compare` 只在输入模糊时双路比较，最终只保留一份 canonical handoff。

### Grouping Rule

- 约 1000 字原文为一个 9 pages 组单元。
- 不满 1000 字的一组直出。
- 长文尾组 300 字以内并入上一组，700 字以上可独立成组，301-699 字默认并入上一组，除非存在明确 scene/hook 边界。
- 自然边界优先于机械字数。

### Review Gate

- 临时 group 不得丢失关键角色、场景、转场、高潮或余波。
- raw source fallback 完成后，后续执行仍按 group 单位进入九刀主流程。

## Mode: multi-episode-continuity

### Purpose

用于同一漫画项目的多集连续执行。目标是保护前集角色、场景、风格和命名真源，避免新集覆盖旧集或视觉 DNA 断层。

### Fixed Context

- 若上一集存在 `第N集-page-group-*.json` 或旧单集 `page-group-*.json`，优先读取其中的 `main_character_lock`、`style_bible`、`character_locks`、`scene_continuity_bible`。
- 新集只对新增人物和新增场景做增量扩展。
- 多集文件名必须使用 `第N集-` 前缀。

### Continuity Rules

- `style_bible.style_anchor_prompt` 必须跨集继承，除非用户明确要求重启视觉风格。
- 主角锚定句不得被拆散后弱化；新集页级 prompt 继续注入同一主角锚。
- 前集重要地点再次出现时，沿用原 `scene_id` 与场景锚；新增地点使用新的 `scene_id`。

### Review Gate

- 新集 JSON 不得覆盖旧集 JSON。
- 新集 page prompt 读起来仍像同一部漫画，而不是独立短篇重启。

## Mode: poster-aware-handoff

### Purpose

用于下游 `4-剧集海报` 需要继续消费九刀流 JSON 的场景。此模式要求每页保留可转译为海报高光候选的剧情、角色、场景、panel 粒度和风格锚点。

### Fixed Context

- `pages[].panels[]` 是剧集海报发现候选高光点的重要输入。
- 默认映射：`one page / key panel -> one highlight candidate`。
- `positive_prompt` 不得只写单幅插画描述；必须保留版式、panel 动作、角色锁、场景锁与文字系统语义。

### Handoff Rules

- 每个 panel 至少包含 `shot`、`action`、`comic_techniques` 和 `text_slots`。
- 动作应具体到海报可提炼：谁、在哪里、做什么、视觉压力点是什么。
- `page_number_overlay`、`active_character_ids`、`scene_id`、`continuity_context` 必须保留，legacy 脚本只能基于这些字段做受控投影。

### Review Gate

- 4 号阶段能从 JSON 中抽出 3-5 个剧情高光候选。
- 不允许只剩一个页级大 prompt 导致海报无法追溯具体代表性画面。

## Boundary

- 本文件不承载漫画题材知识包；恐怖、推理、喜剧、少年战斗等题材偏置仍归 `types/漫画/<题材>/`。
- 本文件不改写 JSON schema；结构字段由 `templates/` 和 `scripts/` 校验。
- 本文件不替代 `review/review-contract.md`；这里只定义模式合同，review 负责验收。
