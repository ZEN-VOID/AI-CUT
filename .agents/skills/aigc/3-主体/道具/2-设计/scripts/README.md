# Scripts Boundary

`道具/2-设计/scripts/` 只承载机械辅助脚本或说明，不承载核心创作正文。

允许脚本做：

- 枚举 `projects/aigc/<项目名>/3-主体/道具/1-清单/道具清单.md` 中的表格行。
- 创建 `projects/aigc/<项目名>/3-主体/道具/2-设计/` 目录。
- 将主体 ID 与道具名称转换为 `<主体ID>-<安全文件名>.md`；主体 ID 默认来自上游清单、manifest 或按清单顺序生成的 `PROP-###`。
- 检查 Markdown 是否包含必填章节。
- 检查是否存在 `研究证据链`、`Prompt Evidence Chain`、`risk_uncertainty` 或等价字段。
- 检查是否存在 `Design Appeal Target`、`Signature Detail`、`Cultural Element Strategy`、`Craft / Ornament Detail`、`Period Context Guardrail`、`Prop Corpus Usage Trace` 或等价字段。
- 统计 English Prompt 字符数是否小于等于 1300 characters，并检查不含 Midjourney `--no` 参数。
- 解析 `references/design-slot-review-contract.md` 的 `PROP-BUNDLE-01`，输出 required slots 供 review gate 逐项验收。
- 生成缺字段报告或 dry-run manifest。

禁止脚本做：

- 自动生成研究考据、物语、Photography、Prop Design 或英文 prompt 正文。
- 自动判断来源置信度、研究不确定性、形制/材料/工艺/设计细节/文化元素/年代/使用/保存状态/功能逻辑如何转译为设计。
- 自动选择明星/器物/文物/文化元素灵感、自动生成装饰纹样、铭文、徽记、封缄、signature detail 或“好看”的道具设计正文。
- 自动把 `knowledge-base/prop-design-corpus.md` 拼接成道具描述或 prompt；语料库只能由 LLM 做原创转译，脚本最多检查是否有使用追踪字段。
- 通过模板拼接扩写道具设计。
- 自动判断初始化成员或大师风格如何影响道具设计；这类创作判断必须由 LLM 在正文阶段完成，脚本只能校验证据是否存在。
- 修改 `1-清单`、`3-生成`、父级 registry、角色设计或场景设计目录。

若未来新增脚本，必须默认支持 dry-run，并在 README 或脚本 docstring 中声明 LLM-first 边界。
