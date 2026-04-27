# Output Template

## Output Contract Alignment

- Required output: `projects/story/<项目名>/2-卷章/第N卷/第N章.md`，或对该文件的局部 section patch / review verdict。
- Output format: Markdown 章级规划；完整正文结构由 `templates/chapter-planning.template.md` 承载。
- Output path: canonical 业务真源固定为 `projects/story/<项目名>/2-卷章/第N卷/第N章.md`。
- Naming convention: 卷目录使用 `第N卷`，章文件使用 `第N章.md`；任务 ID 和引用 ID 保持 ASCII 安全字符。
- Completion gate: 上游已回读，必填标题齐全，节奏 handoff 齐全且含 Mermaid，任务线可汇聚，线索/伏笔分离，无正文越界，review verdict 至少为 `pass_with_followups`。

## Final Output

完整章级规划请使用：

- `templates/chapter-planning.template.md`

局部修订输出应包含：

| section | patch_summary | replacement_or_delta | validation_note |
| --- | --- | --- | --- |
| `[目标标题]` | `[本次改动摘要]` | `[可直接写回的局部内容]` | `[对应 review gate]` |

## Evidence

- 上游 `整体规划.md` 已读取：
- 目标卷 `卷规划.md` 已读取：
- 命中的 Cards 真源：
- review verdict：
