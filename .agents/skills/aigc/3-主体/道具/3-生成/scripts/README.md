# Scripts Boundary

`道具/3-生成/scripts/` 只承载机械辅助，不拥有创作裁决权。

Allowed:

- 枚举 `projects/aigc/<项目名>/3-主体/道具/2-设计/*.md`。
- 检查输出目录、文件名后缀、JSON 字段和路径是否存在。
- 统计 JSON 与图像 stem 是否一致。
- dry-run 打印待生成主体列表。

Forbidden:

- 用脚本生成、扩写或重写道具主体设计。
- 用脚本替代 LLM 抽象审美判断或提示词主创。
- 自动修改 `2-设计`、registry、父级技能或其他 worker 文件。
- 未经用户显式选择直接切换 `$imagegen` CLI/API fallback。
