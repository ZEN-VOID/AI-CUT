# Storyboard Sheet Heuristics

## Stable Heuristics

- 组级 storyboard 的 prompt 越贴近 `10-分组` 原文，越容易保留镜头完整性；额外摘要反而容易丢镜头。
- storyboard panel 落点应按当前分组正文中的视觉节拍判断；原始 `分镜N` 是追溯标签，不是 panel 编号真源。
- 任务执行前缀应保持单段原文，避免模型误把三条要求当作画面文本或回到彩色电影画风。
- `角色 / 场景 / 道具` 的 YAML 列表已经是上游聚合后的主体清单，默认比正文扫描更可靠。
- 多视图图片适合 storyboard 连续性；主图更适合单个主体的造型锚定。二者同时存在时，多视图优先。
- 标准分镜手稿风格黑白线稿是默认画面基底；不要援引项目全局风格或场景光影氛围作为风格词。
- 彩色只属于标注系统，不属于画面渲染：红=身体运动，蓝=摄影机运动，绿=取景/构图，橙=灯光方向，紫=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。
- 黑白线稿仍要还原已有主体形象；角色看身份与轮廓，场景看空间结构，道具看形状和关键细节。
- 每个可见角色头顶的角色名是强制读图标注，必须与分组稿/YAML 角色名一致，不得按外观改名或翻译。
- panel 图片区默认 16:9，panel 下方必须有来自源正文的 `rich_brief` 分镜描述文字；LLM 做语义压缩，规则控制来源、长度和信息优先级。
- 只有 JSON 设计稿时，应把主体列为 missing，而不是把 JSON 交给 imagegen 当图片参照。

## Risk Patterns

| pattern | risk | mitigation |
| --- | --- | --- |
| 分镜数过多 | 单图网格过密，细节不可读 | 记录 `layout_risk`，必要时建议分页 |
| 缺少场景图 | 空间一致性下降 | 保留 prompt 主体，报告缺图 |
| prompt 使用全局风格或场景光影词 | 漂移成电影 still 或彩色概念图 | 恢复黑白线稿分镜手稿任务前缀 |
| 彩色进入角色/背景/氛围渲染 | 破坏分镜手稿基底 | 恢复黑白线稿基底，只保留标注色 |
| 标注颜色语义错配 | 下游读图误判运动、机位或强调 | 重建 `annotation_plan` 并校对颜色图例 |
| 角色头顶名称缺失或不一致 | 下游无法稳定对应角色与动作 | 从组底 YAML `角色` 字段重建 `character_name_labels`，并放在对应角色头顶 |
| 有场景图但未声明主体保真锚定 | 空间结构和场景身份漂移 | 在 manifest、prompt、plan 中记录 `spatial_structure_and_subject_identity` |
| panel 缺少下方描述文字 | storyboard 不能作为可读分镜稿 | 从 `source_span` 补 `panel_description` |
| panel 描述像标签或过长段落 | 读图信息不足或排版不可读 | 按 `rich_brief` 重写为 1-2 句，保留主体动作、构图/运镜、情绪/叙事重点和关键场景/道具 |
| panel 比例未声明 | layout 在批量生成时不稳定 | 默认写入 `panel_image_aspect_ratio: 16:9` |
| panel 数机械等同 `分镜N` 标签数 | storyboard 可能漏掉关键视觉状态或过度切碎运镜结果 | 建立 `storyboard_frame_units`，按视觉节拍 split/merge |
| 同名主体多候选 | 参照错绑 | 进入 ambiguous，不自动选择 |
| 批量 rerun 未锁覆盖策略 | 覆盖已有成图 | 默认跳过已有文件，除非用户要求 replace |
