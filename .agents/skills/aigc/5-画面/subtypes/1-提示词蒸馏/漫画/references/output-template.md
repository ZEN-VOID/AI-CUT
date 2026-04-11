# 漫画输出契约细则

## 共享真源

- JSON 模板：`.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`

本子技能不再维护私有 `templates/` 下的平行模板真源，只负责按组填充共享模板并写出本子技能产物。

## 单输出落点

- `projects/<项目名>/画面/漫画/第N集/第N集.json`
- `projects/<项目名>/画面/漫画/第N集/_manifest.json`（仅当本轮要求 `full_trace` 时）

## 子技能负责填充的 JSON 字段

1. `meta`
2. `prompt_style`
3. `model`
4. `prompt`
5. `prompt_char_count`

## 硬规则

1. `第N集.json` 是 canonical completeness carrier；结构完整性、字段齐全性和下游工具消费能力一律以 JSON 为准。
2. 当前模式只输出 JSON，不输出 `.txt` 派生视图。
3. 每个分镜组在 `第N集.json` 中只生成 1 条请求对象。
4. `prompt` 必须严格由以下固定前缀开头：

   ```text
   Create a single comic page based on the following storyboard group.
   Keep exactly one panel per shot in the original sequence.
   Place dialogue, monologue, and narration only inside their corresponding panels.
   Auto-adapt the comic page layout based on the total number of shots.
   ```

5. 固定前缀之后必须直接拼接 `comic_page_group` 内容块。
6. `comic_page_group` 必须覆盖该分镜组的 `分镜组ID`、`剧本正文`、`组间设计.全局风格`、`组间设计.类型元素`、`组间设计.导演意图` 与全部按原顺序排列的 `分镜明细[]`。
7. `comic_page_group` 必须显式表达 `1 shot = 1 panel`，并要求对白、独白、旁白只能落在对应 panel 内。
8. `comic_page_group` 的内容允许直接使用上游信息，不做文字压缩，也不虚构补写上游没有的镜头事实。
9. `meta.shot_level` 固定为 `storyboard_group`；`meta.group_id` 与 `meta.source_shot_ids` 必须能完整回链该组。
10. `prompt_style.type` 固定服务漫画单页；`prompt_style.language` 默认标记为 `mixed`，以容纳固定英文前缀与上游原文内容。
11. `model` 必须保持图像侧参数骨架完整；`reference_images` 与 `image_markers` 在缺图时也必须保留空骨架，不得删除。
12. `prompt_char_count` 必须与实际 `prompt` 内容一致。
13. 只有用户或父级明确要求时，才额外输出 `_manifest.json`；否则默认 `json_only`。

## `_manifest.json` 最低要求

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `group_count`
6. `groups[].group_id`
7. `groups[].source_shot_ids`
8. `groups[].prompt_char_count`
9. `groups[].has_reference_slots`
10. `groups[].exception_note`
