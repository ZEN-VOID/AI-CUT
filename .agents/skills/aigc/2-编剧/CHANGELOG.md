# Changelog

## 2026-06-04

- 修复画面字段重复拆写风险：新增同画面连续性规则、`same_frame_continuity_map` 报告证据，并同步 `GATE-SCR-07`、field-routing reference、review contract、输出模板、README、CONTEXT 与测试 prompts。
- 将执行报告升级为正式完成门禁：新增 `Execution Decision Trace`、`Reference Execution Matrix`、`Rule Evidence Map`、`N/A Justification` 与 `Repair Log` 标准，并同步 review gate、模板、README、CONTEXT 与测试 prompts。
- 新建 Skill 2.0 runtime-spine 版 `2-编剧` 技能包。
- 将用户指定的 `2-编导/references/` 八个合同全量复制到本包 `references/`，并新增 `imported-reference-adaptation-map.md` 约束 stage 适配和越权边界。
- 新增 `screenwriting-masters-and-shortdrama-rhythm-contract.md`，吸收编剧改编方法、黑泽明式转置、短剧节奏机制、高潮和尾钩细则。
- 补齐 `review/review-contract.md`、`templates/output-template.md`、`types/type-map.md`、`knowledge-base/research-sources.md`、`test-prompts.json`、`agents/openai.yaml` 与 README。
