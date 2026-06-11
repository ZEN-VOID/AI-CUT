# Polishing Type Map

本文件辅助 `story-polishing` 判定任务模式；主路由仍以 `SKILL.md` 的 Type Routing Matrix 为准。

| mode | trigger | required_context | gate |
| --- | --- | --- | --- |
| `chapter_polish` | 目标润色稿不存在 | 源初稿、planning、north_star、MEMORY/CONTEXT | 生成第一版最小修补稿 |
| `polish_rewrite` | 用户明确要求重润/覆盖/整章重写 | 源初稿、既有润色稿、覆盖授权 | 扩大改写范围有明确理由 |
| `local_repair` | 用户或内置验收指定局部坏点 | finding、affected span、源初稿 | 只修问题及必要上下文 |
| `acceptance_repair` | 用户显式要求多维审计后直接优化，或终稿验收 FAIL | 验收维度 findings、repair brief、源初稿 | 验收 findings 必须进入正文修补 |
| `dry_run` | 只检查或装配上下文 | 源初稿和上游校准资料 | 不写正文 |

## Execution Environment Notes

用户给出执行环境偏好时，不改变 `mode`，只追加执行备注。
