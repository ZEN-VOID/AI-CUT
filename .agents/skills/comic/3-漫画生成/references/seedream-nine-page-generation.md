# Legacy: Seedream 九页漫画生成执行细则

> 当前 `comic-generation` 默认生图路径已经切换为 Codex built-in `image_gen`，默认模型口径为 `GPT-IMAGE-2-default`。本文仅保留为 legacy Seedream/API 追溯资料；除非用户显式要求切换 provider，或 built-in `image_gen` 不可用且用户确认 fallback，否则不得作为默认执行路径。

## 1. 单请求原则

legacy Seedream 路径曾默认只发起一次 Seedream 请求：

- `sequential_image_generation=auto`
- `max_images=9`
- `stream=true`
- prompt 内声明 `Generate exactly 9 separate images/pages`

该规则仅适用于 legacy Seedream provider。built-in `image_gen` 默认路径必须拆成 9 次单页调用，以避免九宫格和同图变体风险。

当上游 2 号技能已经把一个 episode 切成多个 `page-group` 时：

- 每个 `page-group` 仍然只发起一次 Seedream 请求。
- 3 号技能一次只消费一个 group JSON，不在执行层重新拼组。
- 默认应把执行产物落到 group 级目标目录或 group 级文件名前缀下，避免不同 group 的计划、报告和图片互相覆盖。

## 2. Master Prompt 结构

顺序固定：

1. `Execution Contract`
   - exactly 9 separate images
   - each image one complete vertical 9:16 comic page
   - not nine-grid collage
   - not nine variations of the same scene
2. `Global Style Bible`
3. `Character Locks`
4. `Comic Text System`
5. `Page 1` 到 `Page 9`
6. `Global Negative Prompt`

如果 JSON 中存在 `page_group / continuity_context`：

- `Page Group Meta` 应在 master prompt 顶层被显式展开。
- `Continuity Context` 应在 `Global Style Bible` 之前或之后紧邻注入，用于提醒模型“当前只是 episode 的一个 group，但要继承同一视觉 DNA”。

## 3. 验收标准

Seedream 报告必须满足：

- `ok=true`
- `result_count=9`
- `saved_files` 长度为 9
- 流式时 `stream_event_types` 至少包含 9 个 `image_generation.partial_succeeded`

若不满足，不得宣称生成完成。

## 4. 失败回退

| 失败 | 回退点 |
| --- | --- |
| JSON 不合格 | `2-九刀流漫画提示词` validator |
| prompt 缺少硬约束 | 本技能 master prompt 编译器 |
| Seedream 认证/解析失败 | `.agents/skills/api/anyfast/image/seedream` |
| 少于 9 张 | 重跑 Seedream；若复现，检查服务端限制与 prompt |
| 九宫格拼图 | 2 号 `hard_constraints` + 本技能 execution contract |
| 九个变体 | 2 号 `story_beat_map / pages[]` |
| 多个 group 执行后互相覆盖 | 本技能 `group target resolve`、默认 output_dir / filename_prefix |
