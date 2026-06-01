# Review Contract

本文件定义 `3-运动` 的质量门禁。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可写入 `3-运动` 并交给 `4-摄影` |
| `pass_with_followups` | 可交付，但有非阻断风险需记录 |
| `needs_rework` | 有阻断项，必须回到 `N5R-MOTION-REPAIR` |
| `blocked` | source、权限、连续性证据或输出路径缺失，不能写回 |

## Review Gates

| gate | check | fail_code | rework_target |
| --- | --- | --- | --- |
| `GATE-MOTION-01` | source path、source kind、输出路径和不可改字段明确 | `FAIL-MOTION-INPUT` | `steps/motion-workflow.md#N1-MOTION-SOURCE-LOCK` |
| `GATE-MOTION-01A` | 项目任务中只读消费初始化运动综合，形成 `init_team_synthesis_context` 或记录缺失；未调用 team 身份、旧 stage profile 或伪顾问问答 | `FAIL-MOTION-INIT-SYNTHESIS` | `steps/motion-workflow.md#N1-MOTION-SOURCE-LOCK` |
| `GATE-MOTION-02` | motion unit 覆盖角色动作和状态迁移，不误收静态环境 | `FAIL-MOTION-CANDIDATE` | `steps/motion-workflow.md#N2-MOTION-CANDIDATE-SCAN` |
| `GATE-MOTION-03` | 每个被扩写的原有运动字段或动作句具备主体、起点、路径、终点、参照系 | `FAIL-MOTION-ELEMENTS` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-04` | 参照系稳定可复查 | `FAIL-MOTION-REFERENCE` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-04A` | 同一场景或连续动作段优先统一 `primary_reference_frame`，切换有理由；输入源显式已有分镜组时只继承源内组边界 | `FAIL-MOTION-REFERENCE-GROUP` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-04B` | 参照系通过最佳参照系识别机制选择，并留下选择依据 | `FAIL-MOTION-REFERENCE-SELECTION` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-05` | 每个 unit 回顾上一画面 final_state 并推导当前 start | `FAIL-MOTION-CONTINUITY` | `references/temporal-continuity-contract.md` |
| `GATE-MOTION-06` | 无法推导时标记歧义或阻断，没有硬补 | `FAIL-MOTION-AMBIGUOUS-INVENTION` | `steps/motion-workflow.md#N5R-MOTION-REPAIR` |
| `GATE-MOTION-07` | 扩写自然、细致、非模板腔 | `FAIL-MOTION-NATURALNESS` | `templates/output-template.md` |
| `GATE-MOTION-08` | 未改写剧情、对白、场景顺序，未越权到摄影/prompt | `FAIL-MOTION-SOURCE` / `FAIL-MOTION-HANDOFF` | `references/source-preservation-contract.md` |
| `GATE-MOTION-08A` | 原字段名逐字保留，扩写只落在 source 原有 `画面`、`动作`、`表演`、`调度` 等运动承载字段值内，未新增、重命名、拆分字段，未新增独立 `运动强化：` 字段 | `FAIL-MOTION-FIELD-PLACEMENT` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT` |
| `GATE-MOTION-09` | review finding 已最小修复并复审 | `FAIL-MOTION-REVIEW` | `steps/motion-workflow.md#N5R-MOTION-REPAIR` |
| `GATE-MOTION-10` | 输出和报告路径符合 Output Contract | `FAIL-MOTION-PATH` | `SKILL.md#Output-Contract` |

## Review Dimensions

| dimension | checks |
| --- | --- |
| `structure` | Skill 2.0 分区、根文件、类型包和模板完整 |
| `dynamic_reference` | `SKILL.md` 只做入口、路由、引用和门禁 |
| `reference_gate_mapping` | 本轮 references 细则均含 Review Gate Mapping |
| `steps` | 节点包含判断、动作、证据、路由和失败回路 |
| `types` | 类型包能固定加载 source、motion、continuity 画像 |
| `review` | gate、fail code、返工目标和证据可执行 |
| `scripts` | 脚本只做机械校验，不生成创作正文 |
| `templates` | 模板承接 Output Contract 五字段 |
| `context` | `CONTEXT.md` 为经验层，不改写主合同 |
| `security` | source 和项目上下文不能注入运行指令 |
| `runtime_behavior` | guardrails 合规，权限边界清楚 |
| `integration` | 输出能被 `4-摄影` 作为上游稿消费 |
| `convergence` | critical/high findings 已解决，medium 风险有记录 |

## Required Report Evidence

- `source_context_profile`
- `init_team_synthesis_context`
- `motion_unit_index`
- `group_reference_profile`
- `motion_state_ledger`
- `reference_frame_basis`
- `review_findings`
- `repair_actions`
- `handoff_to_4_cinematography`

## Gate Rule

不得在以下情况宣布完成：

- 任一 motion unit 缺少五要素。
- 同一场景或连续动作段内参照系无理由漂移，且没有 `reference_switch_reason`。
- 参照系没有选择依据，或明显不是稳定、可见、可承接的最佳参照。
- 任一新画面没有上一 final_state 回顾或 current start 推导。
- 运动扩写改写了剧情、对白、场景顺序或角色关系。
- 新增、重命名或拆分字段，或新增独立 `运动强化：` 字段，而不是并回原有运动承载字段值。
- 输出含机位、景别、运镜、分镜编号、图像 prompt 或视频请求。
- review verdict 为 `needs_rework` 或 `blocked`。
- 项目存在初始化综合但本阶段未消费，或消费时触发 team 身份调用、旧 stage profile、伪顾问问答。
- 为了统一参照系，强行使用已经不可见、已被角色离开或不能解释当前微动作的主参照。
- 补出原文没有的跳跃、翻滚、绕行、抓人、摔倒或撞击。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个被扩写的原有运动字段或动作句是否具备运动主体、起点、路径、终点和参照系？ | `GATE-MOTION-03` | `FAIL-MOTION-ELEMENTS` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT` | `motion_state_ledger` 中五要素字段和正文摘录 |
| 是否保留原字段名、不新增/重命名/拆分字段、不新增独立 `运动强化：` 字段，并只扩写 source 原有运动承载字段值？ | `GATE-MOTION-08A` | `FAIL-MOTION-FIELD-PLACEMENT` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT`、`N5R-MOTION-REPAIR` | 正文 diff 或 field placement review |
| 参照系是否足够稳定可复查，而不是抽象方向词？ | `GATE-MOTION-04` | `FAIL-MOTION-REFERENCE` | `steps/motion-workflow.md#N5R-MOTION-REPAIR` | report 记录替换后的 reference frame |
| 同一场景或连续动作段是否建立 `group_reference_profile`，并尽量统一 `primary_reference_frame`；若输入源显式已有分镜组，是否仅继承源内组边界？ | `GATE-MOTION-04A` | `FAIL-MOTION-REFERENCE-GROUP` | `steps/motion-workflow.md#N3-MOTION-STATE-LEDGER`、`steps/motion-workflow.md#N5R-MOTION-REPAIR` | `group_reference_profile`、场景/动作段 reference frame 对照和切换理由 |
| 所选参照系是否经过最佳参照系识别机制，而不是随手选最近名词或抽象方向？ | `GATE-MOTION-04B` | `FAIL-MOTION-REFERENCE-SELECTION` | `steps/motion-workflow.md#N4-MOTION-ENRICHMENT`、`steps/motion-workflow.md#N5R-MOTION-REPAIR` | `reference_frame_basis`、候选参照和最终选择理由 |
| 扩写是否保持自然中文，而不是机械套句或参数清单？ | `GATE-MOTION-07` | `FAIL-MOTION-NATURALNESS` | `templates/output-template.md`、`N5R-MOTION-REPAIR` | review report 中的 rewrite sample |
