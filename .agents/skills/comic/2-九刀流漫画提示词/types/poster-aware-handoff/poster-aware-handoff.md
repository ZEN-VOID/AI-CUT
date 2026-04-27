# Type Package: poster-aware-handoff

## Purpose

用于下游 `4-剧集海报` 需要继续消费九刀流 JSON 的场景。此包要求每页保留可转译为海报高光候选的剧情、角色、场景、panel 粒度和风格锚点。

## Fixed Context

- `pages[].panels[]` 是剧集海报发现候选高光点的重要输入。
- 默认映射：`one page / key panel -> one highlight candidate`。
- `positive_prompt` 不得只写单幅插画描述；必须保留版式、panel 动作、角色锁、场景锁与文字系统语义。

## Handoff Rules

- 每个 panel 至少包含 `shot`、`action`、`comic_techniques` 和 `text_slots`。
- 动作应具体到海报可提炼：谁、在哪里、做什么、视觉压力点是什么。
- `page_number_overlay`、`active_character_ids`、`scene_id`、`continuity_context` 必须保留，legacy 脚本只能基于这些字段做受控投影。

## Review Gate

- 4 号阶段能从 JSON 中抽出 3-5 个剧情高光候选。
- 不允许只剩一个页级大 prompt 导致海报无法追溯具体代表性画面。
