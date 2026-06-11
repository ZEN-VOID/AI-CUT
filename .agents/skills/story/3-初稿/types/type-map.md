# Drafting Type Map

本文件辅助 `story-drafting` 判定任务模式；主路由仍以 `SKILL.md` 的 Type Routing Matrix 为准。

| mode | trigger | required_context | gate |
| --- | --- | --- | --- |
| `chapter_draft` | 目标章不存在，用户要求起草 | planning、north_star、对象卡、同卷前文、MEMORY/CONTEXT | 写出完整初稿 |
| `chapter_continue` | 目标章已存在，用户要求续写/补完 | 既有正文、续写边界、上游真源 | 保留已成立内容，补足缺口 |
| `chapter_rewrite` | 用户明确要求重写/覆盖 | 既有正文、重写授权、上游真源 | 不静默覆盖，保留必要事实 |
| `local_repair` | review 或用户指出局部问题 | finding、受影响段落、上游真源 | 只修问题及必要上下文 |
| `dry_run` | 只检查或装配上下文 | 目标章路径和上游真源 | 不写正文 |

## Genre Context Packages

- `types/网文/` 保留一份通用网文题材上下文包，供 `north_star.yaml.genre_contract`、章级 planning 或用户请求命中时按题材选择性加载。
- 题材包只提供固定上下文、风格风险和常见结构提醒，不得替代 `SKILL.md` 的主创节点、Output Contract 或 review gate。
- 命中多个题材信号时可多选加载，但最终正文仍由 `N5-CREATIVE-DRAFT` 统一汇流，不为题材包生成平行草稿。

## Execution Environment Notes

用户给出执行环境偏好时，不改变 `mode`，只追加执行备注。
