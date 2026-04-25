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
| 用户要求“执行/继续/完成 1-Planning”且未显式指定停在某个 mode，或要求“完整规划阶段/全链规划” | `full_chain` | 三个 mode reference + `planning-io-contract.md` | 所有命中脚本模板 | 串行 mode gate + stage validation |
| 用户要求“验收/检查/handoff/validation-report” | `stage_validation` | `references/planning-io-contract.md` | 无必需脚本 | `review/planning-review-contract.md` |
| 用户要求“升级/修复/融合/断链”或审计失败 | `repair` | `references/legacy-migration-matrix.md` | 按失败 owner 选择 | structural audit |

## Ambiguity Rules

1. 若用户只说“执行/继续/完成规划阶段”或直接点名 `.agents/skills/aigc/1-Planning`，且没有显式要求在分集、格式或分组处停住，则判为 `full_chain`：从最早缺口开始，连续跑到 `grouping + stage_validation`。
2. 若用户只说“规划阶段继续”但上下文明确是在调试某个单一 mode，才按已有产物缺口选择 `episode_split`、`script_format` 或 `grouping`。
3. 若用户指定具体文件，文件层级优先于笼统阶段名。
4. 若既有产物与用户模式冲突，以用户显式请求为准，但必须报告会覆盖或绕过哪些上游假设。
5. `repair` 只修结构、引用或合同漂移，不代替内容创作 mode。

## Anti-Patterns

- 不得因为 `1-分集 / 2-格式 / 3-分组` 名称仍是项目 runtime 子目录，就把它们重新判为三个 skill 包。
- 不得把宽泛“执行 1-Planning”误判为只跑最早缺口后停住；除非用户显式要求断点，否则三步子路径应作为内部流水线连续执行。
- 不得用脚本生成分集正文、剧本文本、组界判断或创作型总结。
