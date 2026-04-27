# Type Package: multi-episode-continuity

## Purpose

用于同一漫画项目的多集连续执行。目标是保护前集角色、场景、风格和命名真源，避免新集覆盖旧集或视觉 DNA 断层。

## Fixed Context

- 若上一集存在 `第N集-page-group-*.json` 或旧单集 `page-group-*.json`，优先读取其中的 `main_character_lock`、`style_bible`、`character_locks`、`scene_continuity_bible`。
- 新集只对新增人物和新增场景做增量扩展。
- 多集文件名必须使用 `第N集-` 前缀。

## Continuity Rules

- `style_bible.style_anchor_prompt` 必须跨集继承，除非用户明确要求重启视觉风格。
- 主角锚定句不得被拆散后弱化；新集页级 prompt 继续注入同一主角锚。
- 前集重要地点再次出现时，沿用原 `scene_id` 与场景锚；新增地点使用新的 `scene_id`。

## Review Gate

- 新集 JSON 不得覆盖旧集 JSON。
- 新集 page prompt 读起来仍像同一部漫画，而不是独立短篇重启。
