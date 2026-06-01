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
| `GATE-MOTION-02` | motion unit 覆盖角色动作和状态迁移，不误收静态环境 | `FAIL-MOTION-CANDIDATE` | `steps/motion-workflow.md#N2-MOTION-CANDIDATE-SCAN` |
| `GATE-MOTION-03` | 每条运动强化具备主体、起点、路径、终点、参照系 | `FAIL-MOTION-ELEMENTS` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-04` | 参照系稳定可复查 | `FAIL-MOTION-REFERENCE` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-04A` | 同一分镜组或连续动作段优先统一 `primary_reference_frame`，切换有理由 | `FAIL-MOTION-REFERENCE-GROUP` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-04B` | 参照系通过最佳参照系识别机制选择，并留下选择依据 | `FAIL-MOTION-REFERENCE-SELECTION` | `references/motion-five-elements-contract.md` |
| `GATE-MOTION-05` | 每个 unit 回顾上一画面 final_state 并推导当前 start | `FAIL-MOTION-CONTINUITY` | `references/temporal-continuity-contract.md` |
| `GATE-MOTION-06` | 无法推导时标记歧义或阻断，没有硬补 | `FAIL-MOTION-AMBIGUOUS-INVENTION` | `steps/motion-workflow.md#N5R-MOTION-REPAIR` |
| `GATE-MOTION-07` | 扩写自然、细致、非模板腔 | `FAIL-MOTION-NATURALNESS` | `templates/output-template.md` |
| `GATE-MOTION-08` | 未改写剧情、对白、场景顺序，未越权到摄影/prompt | `FAIL-MOTION-SOURCE` / `FAIL-MOTION-HANDOFF` | `references/source-preservation-contract.md` |
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
- 同一分镜组或连续动作段内参照系无理由漂移，且没有 `reference_switch_reason`。
- 参照系没有选择依据，或明显不是稳定、可见、可承接的最佳参照。
- 任一新画面没有上一 final_state 回顾或 current start 推导。
- 运动强化改写了剧情、对白、场景顺序或角色关系。
- 输出含机位、景别、运镜、分镜编号、图像 prompt 或视频请求。
- review verdict 为 `needs_rework` 或 `blocked`。
