# CHANGELOG

## 2026-04-29

- 新增显式启用 subagents 时的项目 `team.yaml` 顾问请教合同，覆盖章级规划的本章职责、时间推进、爽点变奏、悬念开关、任务汇聚和 drafting handoff。
- 新增 `advisor_consultation_packet`、review gate、CONTEXT 经验与 LLM 主创前可执行指导汇流要求。
- 新增章级悬念开关体系，接入共享 `../_shared/suspense-design-contract.md`。
- 在 `SKILL.md`、`references/chapter-planning-contract.md`、`steps/chapter-planning-workflow.md`、`templates/chapter-planning.template.md`、`review/chapter-planning-review.md`、`types/chapter-planning-type-map.md`、README、CONTEXT 与 validator 字段中新增 `本章悬念开关`。
- 固定 `上承卷级悬念 / 本章读者可知 / 本章角色可知 / 本章悬念线程动作 / 本章需要隐藏的 / 本章误导/疑阵 / 本章揭秘的 / 本章只埋不揭的 / 章末悬念压力 / 本章悬念负载 / 正文禁止上帝视角说明`，要求章级规划约束线索、伏笔、节奏和正文禁区。
- 扩展章级多重悬念执行机制，新增 `本章悬念线程动作` 与 `本章悬念负载`，用于追踪每条悬念的本章状态变更。

## 2026-04-28

- 新增章级时间线体系，接入共享 `../_shared/timeline-design-contract.md`。
- 在 `SKILL.md`、`references/chapter-planning-contract.md`、`steps/chapter-planning-workflow.md`、`templates/chapter-planning.template.md`、`review/chapter-planning-review.md` 与 validator 字段中新增 `本章时间推进`。
- 固定 `chapter_start_state / visible_time_span / event_order / parallel_hidden_events / chapter_end_state / handoff_to_next_chapter`，要求章级继承卷级 `本卷时间线` 后再裁定冲突、爽点和节奏。
- 新增 `references/chapter-payoff-rules.md`，将章级爽点设计升级为独立但与节奏 handoff 高度关联的系统。
- 在模板、steps、types、review 与 Output Contract 中新增 `本章爽点设计`，固定 `reader_desire / promise_source / character_anchor / payoff_mode / build_up / delivery_action / satisfaction_delta / exaggeration_logic / cost_or_aftershock / aftertaste_hook`。
- 将动能式、势能式、浪能式分别映射到外部化结果、精神/认知/压力变化、体验/关系/生活质感/状态修复等爽点形态，并要求 `payoff_type / micro_payoff` 消费爽点设计。
- 补强角色一致性门禁：新增 `character_anchor` 与 `exaggeration_logic`，要求爽点与角色个性高度相关，夸张但合情理。
- 补强类型机制：新增 `types/payoff-genre-type-map.md` 与 `genre_payoff_profile`，要求爽点按小说类型/子类型校准口味、禁忌和兑现尺度，避免所有项目同质化。
- 将“高超的对决”纳入动能式爽点，覆盖武斗、法则碰撞、谈判交锋、棋局互算、推理追捕、手艺比赛和商业博弈等类型化表达。
- 新增高超对决变体机制：`duel_variation_axis` 要求多章对决至少在对手类型、对决场域、胜法、代价或情绪色彩上形成差异。
- 新增通用高潮点变体机制：`payoff_variation_axis` 要求反杀、打脸、揭秘、关系升温、牺牲、治愈、奇观等同类爽点在对象、机制、尺度、时序、参与者、情绪或后果上形成差异。

## 2026-04-26

- 升级为完整 Skill 2.0 包结构，补齐 `steps/`、`review/`、`types/`、`knowledge-base/`、`scripts/`、`agents/`、`README.md` 与 `CHANGELOG.md`。
- 将旧 `SKILL.md` 中的章级细则迁移到 `references/chapter-planning-contract.md`，将 Thinking-Action Network 迁移到 `steps/chapter-planning-workflow.md`。
- 新增 `review/chapter-planning-review.md`、`types/chapter-planning-type-map.md` 与 `templates/output-template.md`，让章级输出、类型画像和 review gate 与 Output Contract 对齐。
- 修正 `references/chapter-rhythm-rules.md` 中 shared handoff 合同的相对路径。
