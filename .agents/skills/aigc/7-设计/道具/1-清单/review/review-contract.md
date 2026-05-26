# Review Contract

## Review Gate

| check_id | check | pass_condition | severity |
| --- | --- | --- | --- |
| `REV-PROP-01` | 来源回指 | 每项都能回指组底 YAML `道具` 字段 | blocking |
| `REV-PROP-02` | 表格字段 | 主体表格仅含 `名称`、`首次登场`、`原文描述（关键词式）` | blocking |
| `REV-PROP-03` | 首次登场 | 每项优先标注 `第N集 x-y-z` | blocking |
| `REV-PROP-04` | 归并质量 | 明显别名、代称和同一叙事道具未重复列项 | blocking |
| `REV-PROP-05` | 背景过滤 | 纯背景杂物未污染清单 | major |
| `REV-PROP-06` | LLM-first | 无脚本替代归并、过滤或命名裁决 | blocking |

## Reviewer Output

review 结论应包含：

- verdict: `pass` / `needs_fix` / `blocked`
- findings: 按 `check_id` 列出问题
- required_fix: 最小修复动作
- source_scope: 已审查的 `6-分组` 文件范围

## 顾问与复核流程 Note

若上层工具环境支持外部顾问与复核 provider 调度，本 review 可由单独 reviewer provider 执行；若工具层不提供 dispatch 能力，主 agent 可使用本地 review，但必须在交付中报告阻断层级、原路径和实际路径。
