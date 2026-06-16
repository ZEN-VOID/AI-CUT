# Review Contract

## Review Gate

| check_id | check | pass_condition | severity |
| --- | --- | --- | --- |
| `REV-PROP-01` | 来源回指 | 每项都能回指 registry `subjects.props` 条目 | blocking |
| `REV-PROP-02` | 表格字段 | 主体表格仅含 `名称`、`首次登场`、`原文描述（关键词式）` | blocking |
| `REV-PROP-03` | 首次登场 | 每项优先标注 `第N集 x-y-z` | blocking |
| `REV-PROP-04` | 归并质量 | 明显别名、代称和同一叙事道具未重复列项 | blocking |
| `REV-PROP-05` | 背景过滤 | 纯背景杂物未污染清单 | major |
| `REV-PROP-06` | LLM-first | 无脚本替代归并、过滤或命名裁决 | blocking |
| `REV-PROP-07` | 输出落点 | canonical 清单写入 `3-主体/道具/1-清单/道具清单.md`，可选报告和 manifest 不替代主体清单 | blocking |
| `REV-PROP-08` | 非创作边界 | 清单不扩写道具造型、材质设计、三视图、生成提示词或设计说明 | major |

## Fail Codes

| fail_code | meaning | route |
| --- | --- | --- |
| `FAIL-PROP-SOURCE` | 道具主体来自 registry `subjects.props` 之外，或无法回指 source anchor | `N2-REGISTRY-CANDIDATES` |
| `FAIL-PROP-EVIDENCE` | source anchor 证据缺失、越源回查，或正文/项目资料被当作新增候选来源 | `N3-EVIDENCE` |
| `FAIL-PROP-FIRST-APPEARANCE` | `首次登场` 不是归并后最早出现的分镜组 ID，或写成模糊描述 | `N4-MERGE` |
| `FAIL-PROP-MERGE` | 明显别名、代称、持有者称呼、状态称呼重复列项，或不同叙事道具被强行归并 | `N4-MERGE` |
| `FAIL-PROP-FILTER` | 纯背景杂物、普通陈设、空间构件或氛围词污染主体清单，或保留项缺少叙事/规则/视觉/生成锁定理由 | `N5-FILTER` |
| `FAIL-PROP-RENDER` | 表格字段、关键词边界、canonical 路径、可选报告或 manifest 边界不符合输出合同 | `N6-RENDER` |
| `FAIL-PROP-LLM-FIRST` | 脚本、模板或正则规则替代 LLM 完成归并、过滤、命名或重要性裁决 | `N4-MERGE` / `N5-FILTER` |
| `FAIL-PROP-DESIGN-OVERREACH` | `原文描述（关键词式）` 或清单正文扩写为道具造型、材质细节、三视图、生成提示词或设计说明 | `N6-RENDER` |

## Reviewer Output

review 结论应包含：

- verdict: `pass` / `needs_fix` / `blocked`
- findings: 按 `check_id` 列出问题
- required_fix: 最小修复动作
- source_scope: 已审查的 `subject-registry.yaml` 和 source anchor 范围

## 顾问与复核流程 Note

若上层工具环境支持外部顾问与复核 provider 调度，本 review 可由单独 reviewer provider 执行；若工具层不提供 dispatch 能力，主 agent 可使用本地 review，但必须在交付中报告阻断层级、原路径和实际路径。
