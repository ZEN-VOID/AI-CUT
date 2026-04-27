# Type Package: grouped-script

## Purpose

用于已存在 `1-漫画剧本改编/第N组.md` 的项目。此时 `第N组.md` 是唯一文本真源，一个 group 文件对应一份 `nine_blade_comic_prompts.v1` JSON。

## Fixed Context

- 只把 `【漫剧正文】` 视为业务正文真相权。
- `【本组跨度】`、`【边界判定】`、`【组末钩子】` 只作为切页辅证。
- frontmatter 中的 `type_stack_active_packs` 与 `type_pack_projection_nine_blade` 需要透传到 group JSON。
- 不再额外挂出 `page_group_plan.json` 竞争真源。

## Required Output Bias

- `page_group.group_id` 与文件序号一致，例如 `page-group-01`。
- `page_group.rhythm_rationale` 解释当前组为什么适合压成 9 页。
- `continuity_context` 说明该组继承的角色、风格、场景锁。

## Review Gate

- 确认每个 group 都独立具备 entry hook、中段推进/阻力、exit hook 或余波。
- 确认没有把多个 group 合并成单一 JSON。
