# 分镜帧输出契约细则

## 共享真源

- JSON 模板：`.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`

本子技能不再维护私有 `templates/` 下的平行模板真源，只负责按帧填充共享模板并写出本子技能产物。

## 单输出落点

- `projects/<项目名>/画面/分镜帧/第N集/第N集.json`
- `projects/<项目名>/画面/分镜帧/第N集/_manifest.json`（仅当本轮要求 `full_trace` 时）

## 子技能负责填充的 JSON 字段

1. `meta`
2. `prompt_style`
3. `model`
4. `prompt`
5. `prompt_char_count`

## 硬规则

1. `第N集.json` 是 canonical completeness carrier；结构完整性、字段齐全性和下游工具消费能力一律以 JSON 为准。
2. 当前模式只输出 JSON，不输出 `.txt` 派生视图。
3. 每个目标 `分镜ID` 在 `第N集.json` 中只生成 1 条请求对象。
4. `prompt` 必须严格由以下固定前缀开头：

   ```text
   Create a single cinematic frame based on the following shot breakdown.
   Render only the specified shot moment as one full-frame image (no multi-panel layout).
   Do not add any text, subtitles, speech bubbles, or graphic overlays.
   Preserve the shot's composition, camera angle, subject positions, and atmosphere as the primary visual focus.
   ```

5. 固定前缀之后必须直接拼接 `single_frame_shot` 内容块。
6. `single_frame_shot` 必须覆盖目标分镜所属组的 `分镜组ID`、`剧本正文`、`组间设计.全局风格`、`组间设计.类型元素`、`组间设计.导演意图` 与目标 `分镜明细`。
7. `single_frame_shot` 必须收束到当前单一 `分镜ID` 的可见画面，不得扩写为整组多镜头摘要。
8. `single_frame_shot` 的内容允许直接使用上游信息，不做文字压缩，也不虚构补写上游没有的镜头事实。
9. `meta.shot_level` 固定为 `storyboard_frame`；`meta.group_id` 与长度为 1 的 `meta.source_shot_ids` 必须能完整回链该帧。
10. `prompt_style.type` 固定服务单帧图像；`prompt_style.language` 默认标记为 `mixed`，以容纳固定英文前缀与上游原文内容。
11. `model` 必须保持图像侧参数骨架完整；`reference_images` 与 `image_markers` 在缺图时也必须保留空骨架，不得删除。
12. `prompt_char_count` 必须与实际 `prompt` 内容一致。
13. 只有用户或父级明确要求时，才额外输出 `_manifest.json`；否则默认 `json_only`。

## `_manifest.json` 最低要求

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `shot_count`
6. `shots[].group_id`
7. `shots[].shot_id`
8. `shots[].prompt_char_count`
9. `shots[].has_reference_slots`
10. `shots[].exception_note`
