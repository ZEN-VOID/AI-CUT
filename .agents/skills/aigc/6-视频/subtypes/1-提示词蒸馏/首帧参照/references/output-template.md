# 首帧参照 输出契约细则

## 共享真源

- JSON 模板：`.agents/skills/aigc/6-视频/_shared/video-generation-input.template.json`
- TXT 模板：`.agents/skills/aigc/6-视频/_shared/视频生成入参.template.txt`

本子技能不再维护私有 `templates/` 下的平行模板真源，只负责按帧填充共享模板并写出本子技能产物。

## 双输出落点

- `projects/<项目名>/视频/首帧参照/第N集/第N集.json`
- `projects/<项目名>/视频/首帧参照/第N集/第N集.txt`
- `projects/<项目名>/视频/首帧参照/第N集/_manifest.json`

## 子技能负责填充的 JSON 字段

1. `meta`
2. `prompt_style`
3. `model`
4. `prompt`
5. `prompt_char_count`

## 硬规则

1. `第N集.json` 是 canonical completeness carrier；结构完整性、字段齐全性和下游工具消费能力一律以 JSON 为准。
2. `第N集.txt` 只是 derived display view，不是 canonical completeness carrier；它只负责展示 `prompt` 与 `prompt_char_count`，不承担结构完整性。
3. `第N集.txt` 必须严格回指共享 TXT 模板，不额外展开 JSON 字段名，不追加结构化参数区块。
4. 每个目标 `分镜ID` 在 `第N集.json` 中只生成 1 条请求对象。
5. `prompt` 必须覆盖目标分镜所属组的上下文与该目标分镜的全部镜级内容。
6. `全局风格` 必须原文保留，不得改写。
7. `剧本正文` 必须转换为对应分镜帧的剧情桥段，不得默认整段照搬全组文本；仅在组内只有 1 个分镜时允许整段直贴。
8. 其余内容允许压缩为自然语句、短语或关键词串。
9. 除 `分镜组ID` 和 `分镜ID` 外，不得显式写出字段标题。
10. 默认目标字数为 `800-1200` 中文字符；若用户或父级显式给出其他范围，以显式约束覆盖。
11. `prompt_char_count` 必须与实际 `prompt` 内容一致，且 `第N集.txt` 中的字数统计必须与 JSON 同步。
12. 参照图信息当前暂不处理；`reference_images` 与 `image_markers` 仅保留共享模板骨架，不得擅自补入虚构图片信息。
13. 若字数低于下限或存在桥段判定保守例外，必须写入 `_manifest.json`。

## `_manifest.json` 最低要求

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `txt_file`
6. `shot_count`
7. `shots[].group_id`
8. `shots[].shot_id`
9. `shots[].prompt_char_count`
10. `shots[].bridge_strategy`
11. `shots[].within_target_range`
12. `shots[].exception_note`
