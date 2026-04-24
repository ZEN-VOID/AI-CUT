# Prop Review Contract

## Gates

| gate_id | check |
| --- | --- |
| `PROP-R1-PATH` | 所有最终交付物在 `projects/aigc/<项目名>/4-Design/` 根目录 |
| `PROP-R2-LIST` | `道具清单.md` 至少包含道具名、道具类型、叙事功能、证据回链 |
| `PROP-R3-DESIGN` | `[道具名].md` 遵循 `prop_masterprompt.structured.v2.md` |
| `PROP-R4-PANEL` | `[道具名].json` 回链同 stem `[道具名].md`，不重写道具事实 |
| `PROP-R5-LLM-FIRST` | 创作性研究、设计和 prompt 决策由 LLM 完成，脚本只做辅助 |

## Verdict

- `pass`: 全部门通过。
- `repair`: 给出失败 gate、owner 文件与最小修复动作。
- `blocked`: 上游输入缺失或用户要求违反 LLM-first 主创规则。
