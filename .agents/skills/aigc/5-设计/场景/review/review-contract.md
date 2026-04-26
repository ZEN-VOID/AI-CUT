# Scene Review Contract

## Gates

| gate_id | check |
| --- | --- |
| `SCENE-R1-PATH` | 所有最终交付物在 `projects/aigc/<项目名>/4-设计/` 根目录 |
| `SCENE-R2-LIST` | `场景清单.md` 至少包含场景名、空间类型、叙事功能、证据回链 |
| `SCENE-R3-DESIGN` | `[场景名].md` 遵循 `scene_masterprompt.structured.v2.md` |
| `SCENE-R4-PANEL` | `[场景名].json` 回链同 stem `[场景名].md`，不重写场景事实 |
| `SCENE-R5-LLM-FIRST` | 创作性研究、设计和 prompt 决策由 LLM 完成，脚本只做辅助 |

## Verdict

- `pass`: 全部门通过。
- `repair`: 给出失败 gate、owner 文件与最小修复动作。
- `blocked`: 上游输入缺失或用户要求违反 LLM-first 主创规则。
