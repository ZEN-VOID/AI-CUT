# Scripts Boundary

`道具/2-设计/scripts/` 只承载机械辅助脚本或说明，不承载核心创作正文。

允许脚本做：

- 枚举 `projects/aigc/<项目名>/5-设计/道具/1-清单/道具清单.md` 中的表格行。
- 创建 `projects/aigc/<项目名>/5-设计/道具/2-设计/` 目录。
- 将主体 ID 与道具名称转换为 `<主体ID>-<安全文件名>.md`；主体 ID 默认来自上游清单、manifest 或按清单顺序生成的 `PROP-###`。
- 检查 Markdown 是否包含必填章节。
- 检查是否存在 `研究证据链`、`Prompt Evidence Chain`、`risk_uncertainty` 或等价字段。
- 统计 English Prompt 字符数是否小于等于 1300 characters，并检查不含 Midjourney `--no` 参数。
- 解析 `references/design-slot-review-contract.md` 的 `PROP-BUNDLE-01`，输出 required slots 供 review gate 逐项验收。
- 生成缺字段报告或 dry-run manifest。

禁止脚本做：

- 自动生成研究考据、物语、Photography、Prop Design 或英文 prompt 正文。
- 自动判断来源置信度、研究不确定性、形制/材料/工艺/年代/使用痕迹/功能逻辑如何转译为设计。
- 通过模板拼接扩写道具设计。
- 自动判断大师监制风格如何影响道具设计。
- 修改 `1-清单`、`3-生成`、父级 registry、角色设计或场景设计目录。

若未来新增脚本，必须默认支持 dry-run，并在 README 或脚本 docstring 中声明 LLM-first 边界。
