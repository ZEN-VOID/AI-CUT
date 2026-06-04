# Scripts Boundary

`2-编剧/scripts/` 只允许放机械辅助脚本，例如：

- 路径存在性检查。
- Markdown 标题、frontmatter、场景标题天气后缀检查。
- `reference_load_manifest` 覆盖统计。
- `GATE-SCR` 字段存在性检查。

禁止：

- 生成剧本正文。
- 自动写对白、独白、尾钩、高潮、节奏机制或题材判断。
- 以模板拼接替代 LLM 主创。

当前目录未提供执行脚本；正式任务可用人工 review 或后续新增机械 validator。
