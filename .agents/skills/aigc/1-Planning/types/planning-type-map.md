# Planning Type Map

`types/` 是 `aigc/1-Planning` 单包融合后的模式判型真源。先判型，再按 `steps/planning-workflow.md` 进入对应分支。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `planning_mode` | `episode_split`、`script_format`、`grouping`、`full_chain`、`stage_validation`、`repair` | 本轮命中的规划模式 |
| `input_artifact` | `story_source`、`split_episode`、`formatted_script`、`grouped_script`、`skill_package` | 主要输入对象 |
| `output_artifact` | `split_bundle`、`script_bundle`、`grouping_bundle`、`validation_report`、`structural_patch` | 主要输出对象 |
| `execution_type` | `llm-first`、`script-assisted`、`validator-only`、`hybrid` | 执行方式 |
| `risk_focus` | `readiness`、`dialogue_fidelity`、`variant_arbitration`、`quantization`、`reference_sync` | 主要风险 |
| `review_gate` | `local_checklist`、`script_validator`、`quantizer_validator`、`structural_audit` | 交付门禁 |

## Mapping Matrix

| signal | planning_mode | references | scripts/templates | review gate |
| --- | --- | --- | --- | --- |
| 用户要求“分集/拆集/逐集原文/episode split” | `episode_split` | `references/episode-splitter-contract.md` | `templates/episode-split-plan.template.json` | 本地 checklist + 索引一致性 |
| 用户要求“剧本格式/标准剧/解说剧/对白旁白整理” | `script_format` | `references/script-format-contract.md` | `scripts/validate_script_output.py` | script validator |
| 用户要求“分组/组边界/量化/尾钩借焰/grouped script” | `grouping` | `references/grouping-contract.md`、`references/scene-order-duration-strategy.md` | grouping scripts + grouping templates | quantizer + grouping validator |
| 用户要求“完整规划阶段/全链规划” | `full_chain` | 三个 mode reference + `planning-io-contract.md` | 所有命中脚本模板 | 串行 mode gate + stage validation |
| 用户要求“验收/检查/handoff/validation-report” | `stage_validation` | `references/planning-io-contract.md` | 无必需脚本 | `review/planning-review-contract.md` |
| 用户要求“升级/修复/融合/断链”或审计失败 | `repair` | `references/legacy-migration-matrix.md` | 按失败 owner 选择 | structural audit |

## Ambiguity Rules

1. 若用户只说“规划阶段继续”，优先读取已有产物：缺 `episode-split-plan.json` 则 `episode_split`，缺 `2-格式/第N集.md` 则 `script_format`，缺 `3-分组/第N集.md` 则 `grouping`。
2. 若用户指定具体文件，文件层级优先于笼统阶段名。
3. 若既有产物与用户模式冲突，以用户显式请求为准，但必须报告会覆盖或绕过哪些上游假设。
4. `repair` 只修结构、引用或合同漂移，不代替内容创作 mode。

## Anti-Patterns

- 不得因为 `1-分集 / 2-格式 / 3-分组` 名称仍是项目 runtime 子目录，就把它们重新判为三个 skill 包。
- 不得把 `full_chain` 当作默认；只有用户要求完整规划或后续 gate 明确需要时才串行执行全部模式。
- 不得用脚本生成分集正文、剧本文本、组界判断或创作型总结。
