# Changelog

## 2026-06-19

- 同步 `2-美学` 题材轴交接：`types/type-map.md` 与 `SKILL.md` 优先消费 `类型风格.md` 的 `Genre Axis Classification` / `primary_genre_axis`。
- `Type Axis Selection Map` 新增 `upstream_genre_axis` 与 `upstream_genre_axis_evidence`，保留上游题材轴、source anchor 和 fallback 证据，再组合 `presentation_axis x genre_axis`。
- 同步 `CONTEXT.md`，防止后续退回只读自然语言题材标签、由编剧阶段重新猜题材的漂移。

## 2026-06-18

- 新增父级共享的 `Dramatized Adaptation Supplement Contract`：将 `4-编剧` 从单纯字段化/格式化扩展为“戏剧意图提炼 -> 影视化缺口诊断 -> 受控补写 -> 改写边界复核”的编剧主创链路。
- 新增并同步 `Dramatic Intent Map`、`Dramatization Gap Map`、`Controlled Adaptation Plan`、`Continuity Detail Map` 与 `Rewrite Scope Check` 证据要求，接入 `N2/N3/N6/N8`、`GATE-SCR-11`、`GATE-SCR-12`、`GATE-SCR-16`、输出模板、review contract、CONTEXT、README、入口元数据、test prompts 和审计脚本。
- 新增 `dramatic_adaptation_repair` 路由信号，用于修复“字段齐全但不成戏、剧情不连贯、心理未外化、过渡/动机/阻力缺失”的剧本问题；明确补写不得未经授权改变核心事实、人物关系、因果链和事件结果。
- 在 `types/` 下建立二维类型配置：`types/presentation/` 承载 `正剧`、`解说剧` 呈现方式，`types/genre/` 承载 `武侠剧`、`玄幻剧`、`科幻剧`、`魔幻剧` 题材类型；正式编剧任务必须落成 `呈现方式 x 题材类型` 的 `screenwriting_type_combination_profile`，但这些类型包仍是父级授权策略卡，不升级为子技能。
- 新增 `Type Axis Combination Contract`、`Type Axis Selection Map`、`Screenwriting Type Combination Profile`、`C2F-TYPE-AXIS-COMBINED` 和 `FAIL-SCR-TYPE-AXIS-COMBINATION`，并同步 `SKILL.md`、`review/review-contract.md`、`templates/output-template.md`、`README.md`、`test-prompts.json`、`CONTEXT.md` 与审计脚本。
- 增强 `§10.3 Long Dialogue Beat Segmentation` 为 `Long Voice Field Beat Segmentation`：适用范围从长对白扩展到所有声音字段类型（对白/旁白/独白/内心独白）；新增旁白节拍画面必须随内容变化而变化的硬规则；新增禁止"同一条泛化旁白画面承托内容完全不同的多个旁白节拍"禁止模式；证据名从 `long_dialogue_beat_map` 升级为 `long_voice_beat_map`（向后兼容）。
- 同步更新 `review/review-contract.md` `GATE-SCR-07`，增加长声音字段节拍拆分审查和 `FAIL-LONG-DIALOGUE-BEAT` 失败码；更新 `CONTEXT.md` 新增长声音字段共用泛化画面故障行；更新 `SKILL.md` Module Loading Matrix 引用。

## 2026-06-17

- 新增 `正剧` / `解说剧` 两种剧本呈现模式：未显式指定时默认 `正剧`；显式 `解说剧` 时陈述性 source 信息全部落为 `旁白（主体）` + `旁白画面`。
- 新增 `GATE-SCR-25` / `FAIL-SCR-SCREENPLAY-MODE`，并要求执行报告包含 `Screenplay Mode Decision` 和 mode-aware `Narration To Voice Adaptation Map`。
- 增强 `解说剧` 处理细则：新增 `Jieshuoju Source Unit Coverage Map`，先类型化覆盖 `source_dialogue`、`visible_action`、`environment_state`、`declarative_fact`、`background_exposition`、`time_bridge`、`relationship_state`、`result_summary`、`rule_or_system_info`、`mixed_action_declaration` 等 source 单元，再决定旁白、画面字段或双落点。
- 明确 `解说剧` 禁止 `summary`、`fact_drop`、`cause_reorder`、`new_exposition`、`tone_rewrite`，并禁止把可见动作/环境过度旁白化。
- 同步更新 `SKILL.md`、`references/`、`review/review-contract.md`、`templates/output-template.md`、`agents/openai.yaml`、`README.md`、`test-prompts.json` 与 `CONTEXT.md`。
- 增强 `解说剧` 字段节奏规则：新增 `Jieshuoju Field Variety Map`，要求叙事段落功能进入报告而不是正文方括号小标题；含 3 条及以上旁白对的场景必须有非旁白视觉字段承托；连续无承托旁白清单触发 `FAIL-SCR-JIESHUOJU-FIELD-MONOTONY`。

## 2026-06-16

- 新增 `scene_asset_context` 继承合同：当 `3-主体/场景/2-设计`、`3-主体/场景/3-生成` 或 `design-manifest.yaml` 已存在时，`4-编剧` 必须生成 `Scene Asset Integration Map` 或明确 N/A。
- 新增 `GATE-SCR-24` / `FAIL-SCR-SCENE-ASSET-CONTEXT`，限制场景设计和场景图只能只读用于场景标题、环境白描、空间连续性和 AIGC handoff，不得覆盖 `1-分集` 剧情事实、改主体注册表、复制图像 prompt 或写镜头/生成参数。
- 同步更新 `SKILL.md`、`review/review-contract.md`、`templates/output-template.md`、`test-prompts.json` 与 `CONTEXT.md`。

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求 `1-分集` 或用户指定 source 的剧本化应用写入 `Upstream Context Application Map`。
- 新增 `FAIL-SCR-UPSTREAM-CONTEXT`、`GATE-SCR-20` 和报告必填项，证明上游 source 如何投影为剧本事实、声画字段、节奏、高潮和尾钩。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-04

- 修复画面字段重复拆写风险：新增同画面连续性规则、`same_frame_continuity_map` 报告证据，并同步 `GATE-SCR-07`、field-routing reference、review contract、输出模板、README、CONTEXT 与测试 prompts。
- 将执行报告升级为正式完成门禁：新增 `Execution Decision Trace`、`Reference Execution Matrix`、`Rule Evidence Map`、`N/A Justification` 与 `Repair Log` 标准，并同步 review gate、模板、README、CONTEXT 与测试 prompts。
- 新建 Skill 2.0 runtime-spine 版 `4-编剧` 技能包。
- 将用户指定的 `2-编导/references/` 八个合同全量复制到本包 `references/`，并新增 `imported-reference-adaptation-map.md` 约束 stage 适配和越权边界。
- 新增 `screenwriting-masters-and-shortdrama-rhythm-contract.md`，吸收编剧改编方法、黑泽明式转置、短剧节奏机制、高潮和尾钩细则。
- 补齐 `review/review-contract.md`、`templates/output-template.md`、`types/type-map.md`、`knowledge-base/research-sources.md`、`test-prompts.json`、`agents/openai.yaml` 与 README。
