# Story Source Contract

本文件是 `aigc` 技能树中“故事/小说原文/剧本原文/分镜脚本”落盘与缺失提示的单一真源。

## Canonical Landing

- 项目级故事目录：`projects/<项目名>/故事/`
- 故事源登记真源：`projects/<项目名>/Init/story-source-manifest.yaml`

## Ownership

- `0-Init` 负责首次生成 `story-source-manifest.yaml`。
- 主故事源与辅助源文件本体统一落在 `projects/<项目名>/故事/`。
- `1-规划/1-分集` 只消费 `story-source-manifest.yaml` 与其登记路径，不自行发明第二套源文件清单。

## Minimum Readiness Gate

故事源 readiness 必须分层，而不是把“能否开始规划”和“能否完成整季正式分集”压成同一个门：

1. `projects/<项目名>/Init/story-source-manifest.yaml` 存在。
2. `primary_story_source.status == ready` 且已登记实际正文路径时，允许把该正文覆盖范围作为规划真源。
3. `readiness.can_enter_episode_split == true` 时，允许进入 `1-规划/1-分集`，但默认只对 `coverage_scope` 已覆盖范围执行。
4. `readiness.can_finalize_full_season_episode_split == true` 时，才允许宣称“整季正式分集完成”。

若仅满足第 1-3 条而不满足第 4 条，则：

- 允许进入 `1-规划/1-分集` 做增量分集或覆盖范围内规划。
- 必须显式标记为“增量/局部分集”，不得伪装成整季正式切分。
- 必须保留覆盖缺口与后续补源要求。

若连第 3 条都不满足，则：

- 不得宣布可以正式分集。
- 不得假设执行案、大纲、角色设定文档天然等价于“小说原文/剧本原文”。
- 必须返回标准补充提示，而不是让用户猜该补什么。

## Source Roles

- `primary_story_source`
  - 唯一主故事源。
  - 合法类型：`novel_original`、`script_original`、`storyboard_script`、`oral_story_transcript`、`hybrid_story_text`
- `auxiliary_sources`
  - 章节补遗、人物小传、设定补丁、参考梗概等辅助材料。
- `development_briefs`
  - 执行案、方法论文档、项目提案、角色总结、结构蓝图。
  - 可服务 `0-Init` 和部分 `1-规划` 子路径，但默认不等价于 `primary_story_source`。

## Source-Type Extension Fields

当主故事源已经带有镜头/分镜/转场预设时，manifest 还必须声明：

- `preset_retention_mode`
  - `standard`
  - `preserve_and_extend`
  - `preserve_only`
- `detail_expansion_mode`
  - `free_expansion`
  - `guided_expansion`
  - `respect_storyboard_presets`
- `locked_preset_axes`
  - 推荐枚举：`scene_boundary`、`shot_order`、`camera_motif`、`transition_hook`、`viewpoint_order`
- `preset_registry`
  - 对外部分镜脚本中的预设点做结构化登记，供 `3-分组` 与 `3-明细` 继续消费
  - 每条至少说明：`anchor_id`、`source_span`、`lock_level`、`owned_axes`、`expandable_axes`、`forbidden_changes`

规则：

1. 当 `source_type == storyboard_script` 时，默认推荐 `preset_retention_mode = preserve_and_extend`。
2. 当 `preset_retention_mode != standard` 时，`1-规划` 必须把同样的结论继续写入 bootstrap `第N集.json` 的 `metadata.source_profile`。
3. `preset_registry` 中的 `lock_level` 默认分三档：
   - `hard_lock`: 只能补厚，不能改骨架
   - `soft_lock`: 核心意图不变，但允许一锚多镜式细分
   - `reference_only`: 仅保留叙事功能，可在 `3-明细` 中重构
4. `3-分组` 必须根据 `preset_registry` 判断哪些锚点不可拆、哪些可拆成连续子组。
5. `3-明细` 读取到 `respect_storyboard_presets` 或 `preserve_only` 时，只能顺着预设补强，不得把已锁定预设轴改造成第二套主镜头逻辑。

## Standard Missing Prompt

```markdown
故事源补充卡

当前还不能正式进入 `1-规划/1-分集`，因为缺少可覆盖分集边界的主故事源。

请补充以下信息：

1. 主故事源类型
- 小说原文
- 剧本原文
- 分镜脚本
- 口述故事整理稿
- 其他（请说明）

2. 文件路径
- 请优先放到：`projects/<项目名>/故事/`

3. 覆盖范围
- 全文
- 前 N 章 / N 幕
- 指定段落

4. 使用授权
- 是否允许仅凭现有执行案/大纲做“开发式分集”：是 / 否
```

## Verification

- `story-source-manifest.yaml` 能明确区分“主故事源”和“执行案/提案”。
- 若主故事源是分镜脚本，manifest 必须继续声明 `preset_retention_mode`、`detail_expansion_mode` 与 `preset_registry`。
- 当主故事源缺失时，`readiness.can_enter_episode_split` 必须为 `false`。
- 当只导入部分正文时，`readiness.can_enter_episode_split` 可以为 `true`，但 `readiness.can_finalize_full_season_episode_split` 必须为 `false`。
- `coverage_scope`、`split_scope` 与 `partial_limitations` 必须能解释当前是“增量规划”还是“整季正式分集”。
- `1-规划/1-分集` 的输入清单应来自 manifest，而不是临时口头约定。
