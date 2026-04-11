# 全能参照 输出契约细则

## 共享真源

- JSON 模板：`.agents/skills/aigc/6-视频/_shared/video-generation-input.template.json`
- TXT 模板：`.agents/skills/aigc/6-视频/_shared/视频生成入参.template.txt`

本子技能不再维护私有 `templates/` 下的平行模板真源，只负责按组填充共享模板并写出本子技能产物。

## 双输出落点

- `projects/<项目名>/视频/全能参照/第N集/第N集.json`
- `projects/<项目名>/视频/全能参照/第N集/第N集.txt`
- `projects/<项目名>/视频/全能参照/第N集/_manifest.json`

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
4. 每个分镜组在 `第N集.json` 中只生成 1 条请求对象。
5. `prompt` 必须覆盖该组全部组级与镜级内容。
6. `剧本正文` 与 `全局风格` 必须原文保留，不得改写。
7. 其余内容允许压缩为自然语句、短语或关键词串。
8. 除 `分镜组ID` 和 `分镜ID` 外，不得显式写出字段标题。
9. 目标字数为 `1800-2000` 中文字符；若源信息客观不足，不得为凑字数虚构新事实。
10. `prompt_char_count` 必须与实际 `prompt` 内容一致，且 `第N集.txt` 中的字数统计必须与 JSON 同步。
11. `reference_images` 必须保留；`image_markers` 的顺序必须与实际上传顺序一致。
12. 若字数低于下限或存在其他保守例外，必须写入 `_manifest.json`。

## `_manifest.json` 最低要求

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `txt_file`
6. `group_count`
7. `groups[].group_id`
8. `groups[].prompt_char_count`
9. `groups[].within_target_range`
10. `groups[].exception_note`
