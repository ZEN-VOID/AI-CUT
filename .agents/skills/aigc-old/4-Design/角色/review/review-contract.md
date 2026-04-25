# Role Review Contract

## Gates

| gate_id | check |
| --- | --- |
| `ROLE-R1-PATH` | 所有最终交付物在 `projects/aigc/<项目名>/4-Design/` 根目录 |
| `ROLE-R2-LIST` | `角色清单.md` 至少包含角色名、身份层级、服装状态、证据回链 |
| `ROLE-R3-DESIGN` | `[角色名].md` 遵循 `character_masterprompt.structured.v2.md` |
| `ROLE-R4-PANEL` | `[角色名].json` 回链同 stem `[角色名].md`，不重写角色事实 |
| `ROLE-R5-LLM-FIRST` | 创作性研究、设计和 prompt 决策由 LLM 完成，脚本只做辅助 |

## Verdict

- `pass`: 全部门通过。
- `repair`: 给出失败 gate、owner 文件与最小修复动作。
- `blocked`: 上游输入缺失或用户要求违反 LLM-first 主创规则。
