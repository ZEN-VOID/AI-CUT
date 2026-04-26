# Scripts Boundary

`道具/2-设计/scripts/` 只承载机械辅助脚本或说明，不承载核心创作正文。

允许脚本做：

- 枚举 `projects/aigc/<项目名>/4-设计/道具/1-清单/道具清单.md` 中的表格行。
- 创建 `projects/aigc/<项目名>/4-设计/道具/2-设计/` 目录。
- 将道具名称转换为安全文件名。
- 检查 Markdown 是否包含必填章节。
- 统计 English Prompt 字符数是否小于等于 2000。
- 生成缺字段报告或 dry-run manifest。

禁止脚本做：

- 自动生成研究考据、物语、Photography、Prop Design 或英文 prompt 正文。
- 通过模板拼接扩写道具设计。
- 自动判断大师监制风格如何影响道具设计。
- 修改 `1-清单`、`3-生成`、父级 registry、角色设计或场景设计目录。

若未来新增脚本，必须默认支持 dry-run，并在 README 或脚本 docstring 中声明 LLM-first 边界。
