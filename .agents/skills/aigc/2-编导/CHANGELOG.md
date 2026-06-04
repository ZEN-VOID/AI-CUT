# CHANGELOG

## 2026-06-04 (Screenwriting Upstream Restored)

- 同步 `2-编剧` 恢复为 active 剧本阶段后的上游合同：`2-编导` 优先读取 `projects/aigc/<项目名>/2-编剧/第N集.md`，仅在缺失且用户明确直接编导时回退 `1-分集/第N集.md`。
- 将 `2-编剧` 从 legacy 触发词中移除；旧 `3-导演` / `4-表演` 仍只作为兼容触发词。

## 2026-06-01 (Narration To Voice Adaptation)

- 新增 `references/narration-to-voice-adaptation-contract.md`，定义非引号客观叙事改编为对白、独白或内心独白的触发、说话者资格、语音预算、禁区和证据结构。
- 标准化 `continuity_bridge` 触发：对跨度性剧情衔接叙事先拆 `bridge_payload_units`，只把当前行动必需的 1-2 个信息簇转成派生语音，其余用画面、音效、动作或留白显像。
- 同步 script layer、类型画像、review gate、模板和经验层：上游已有对白仍逐字冻结，只有 source-grounded 派生语音可进入 canonical，并必须保留 `narration_to_voice_adaptation_map`。
- 新增 `GATE-BD-19 / FAIL-BD-NARRATION-VOICE`，阻断无锚点新增台词、作者口吻泄露、信息差提前泄露和没有画面承托的派生语音。

## 2026-06-01 (Init-Only Team Synthesis)

- 将 `2-编导` 的 team 入口收束为只读 `team.yaml.init_synthesis.stage_seed_summary."2-编导"`、`init_handoff.writing_directing_seed` 与 `north_star.yaml.创作阶段不变量.编导`。
- `init_team_synthesis_context` 仅作为编导、导演、表演内部节点的冻结上下文，不再触发 team 成员身份、旧 stage profile 或新顾问问答。
- 同步 steps、review、模板和入口合同，使创作阶段不再创建 advisor consultation packet。

## 2026-05-31 (Motion Handoff Insertion)

- 将 `2-编导` 的直接下游从 `4-摄影` 调整为 `3-运动`，新链路为 `1-分集 -> 2-编导 -> 3-运动 -> 4-摄影`。
- 新增 `motion_enrichment_handoff` 交接语义，要求编导报告列出可被运动强化消费的角色动作或画面句。
- 保留后续摄影适配边界：`2-编导` 仍不得写机位、景别、运镜、分镜编号或 prompt，`4-摄影` 默认消费 `3-运动` 输出。

## 2026-05-31 (Reference Redundancy Optimization)

- 收束 `field-routing-and-audio-visual-contract.md` 与 `aigc-visual-signal-matrix.md` 的 AIGC 视觉映射职责：前者只保留字段 owner / 字段纯度 / 许可边界，完整矩阵统一由后者维护。
- 去除 `visual-aesthetic-contract.md` 与 `atmosphere-and-mood-contract.md` 中重复的“心理反应字段约束”正文，统一回指 `psychological-reaction-contract.md`。
- 将小型 performance appendix 内容并回 `actor-performance-control-contract.md`，删除 appendix 层引用，避免强度梯度和声音查表成为第二维护点。

## 2026-05-31 (Reference Integrity Repair)

- 修复 `references/` 内合并迁移后遗留的错位相对路径，统一回指 `2-编导/references/` 内当前真源。
- 补齐演员五层控制中的强度梯度与场景声音矩阵承接；同日后续优化已并回 `actor-performance-control-contract.md`，不再保留 appendix 层真源。
- 将 `aigc-visual-signal-matrix.md` 与 `hollywood-quality-spec.md` 接入 `SKILL.md` Reference Loading Guide，并补强字段合同对视觉信号矩阵的消费关系。

## 2026-05-31 (Workflow Design Hardening)

- 补强 `2-编导` 流程不变量：单一 `candidate_writing_directing`、跨层连续画面化语言、场景字段证据索引和结构化 `4-摄影` handoff。
- 新增 `scene_field_evidence_index` 与 `cinematography_handoff.visual_unit_candidate_map` 为执行报告必备证据，避免三层证据只停留在摘要。
- 收紧 `GATE-BD-16` / `GATE-BD-18`：关键判断必须能回到来源、目标字段和正文嵌入句；摄影交接不得提前写机位、景别、运镜、分镜编号或 prompt。

## 2026-05-31 (Writing Directing Merge)

- 将旧 `2-编剧`、`3-导演`、`4-表演` 合并为 `2-编导` active stage；新 canonical 输出固定为 `projects/aigc/<项目名>/2-编导/第N集.md`。
- 主流程改为 `1-分集 -> 2-编导 -> 4-摄影`，`3-导演` 与 `4-表演` 不再保留独立技能目录，仅作为 legacy 兼容触发词和历史项目产物回读线索。
- 新 `2-编导` 逐集正文必须一次性完成保真剧本化、导演判断、表演工艺和具像画面化语言，不再拆成三份 canonical 主稿。

## 2026-05-27 (Long Dialogue Beat Segmentation)

- 新增长对白节拍拆分源层规则：`2-编剧` 负责在对白逐字冻结前提下建立 `long_dialogue_beat_map`，按语义动作、压力转折、气口和对手反应拆成连续原文片段。
- 新增 `GATE-SCRIPT-23` / `FAIL-LONG-DIALOGUE-BEAT`，要求所有节拍按顺序拼回必须逐字等于上游对白，每个节拍有就近可见承托，避免整段长对白共用一个采访式画面。
- 同步更新 workflow、review、字段路由、对白潜台词、剧本模板和经验层，使下游 `4-表演` / `4-摄影` 可直接消费长对白节拍证据。

## 2026-05-22

- 新增 `表情特写` 作为 `2-编剧` 正式可选字段，用于关键面部表演 beat 的源层落点，避免面部变化长期散落在 `心理反应`、`对白画面` 或泛化“微表情”描述中。
- 明确 `表情特写` 只写眉、眼、嘴、鼻翼、咬肌、下颌、喉头、眨眼频率或皮肤状态等具体面部变化；不得写情绪标签、心理解释、摄影机位、景别或镜头运动。
- 同步字段路由、模板、review gate、workflow、经验层和机械校验；`4-表演` 保留并精修上游 `表情特写`，不再吞回泛化心理反应。

## 2026-05-13

- 从旧合并阶段拆分初始化 `2-编剧` 技能包。
- 承接保真规则、字段格式化、对白冻结、声画配对、slugline 稳定、小说表述二次画面化和好莱坞质量规范。
- 搬入 references：script-adaptation-contract、field-routing-and-audio-visual-contract、novel-to-screen-language-contract、hollywood-quality-spec。
- 搬入 types：source-to-script-type-map、type-map。
- 搬入 scripts：validate_script_projection.py。
