# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/04R-全局优化` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 04R 被当成重新生成 04 | 阶段边界层 | 回到 `04` 源稿锁定，只做二次优化 | `Source Continuity Contract` 固定 04R 只承接 04 输出 | 输出落在 `04R-全局优化`，且回指 04 源稿 |
| 用户自然语言被直接写成风格词 | 意图解析层 | 先生成 `high_energy_intent_map`，把口味词拆成风格轴和目标字段 | `N2A-INTENT-PARSE` 固定为前置节点 | 每个口语需求都有字段、置信度和风险 |
| “高级/不对味/更好看”被直接重塑全局 | 澄清门层 | 输出 2-3 个风格路线，等待用户选择 | `N2B-CLARIFY` 阻断低信息多解需求 | verdict 为 `clarification_blocked` |
| 风格匹配只凭主观感觉 | 风格匹配层 | 建立 `style_matching_matrix`，逐轴对比用户意图、04 字段、02 故事、参考事实和下游消费 | `PASS-04R-05` 固定匹配矩阵门 | 每条关键意图有 match/mismatch/conflict |
| 自然语言调优破坏 04 schema | Schema 连续性层 | 恢复 04 核心字段，只在允许位置增加 `optimization_meta` | `PASS-04R-09` 阻断 schema 破坏 | JSON 仍能被 05/06 消费 |
| 关键词越调越多越空 | 关键词稳定性层 | 删除重复和质量词，按媒介、色彩、光影、材质、构图、特效排序 | `N4K-KEYWORDS` 固定权重和去重证据 | keywords 短、具体、模型可理解 |
| 用户偏好被误写入长期记忆 | 记忆边界层 | 回收为本轮 `style_taste_profile`，除非用户明确要求记住 | `Temporary Style Taste Profile` 固定不自动写 MEMORY | 无授权时项目 `MEMORY.md` 不变 |
| 修改强度越权 | 授权边界层 | 降级到 `light_touch` 或请求 `heavy_reframe` 授权 | `Edit Intensity Ladder` 固定重塑和备选需要授权 | `edit_intensity` 有授权依据 |
| 局部字段调优污染其他字段 | 局部范围层 | 回滚未选字段，只保留必要同步，并说明同步理由 | `PASS-04R-08` 阻断未授权范围扩张 | `field_diff_summary` 可复查 |
| 多轮自然语言调优无法回退 | 版本治理层 | 补 `version_comparison` 和 `rollback_note` | `PASS-04R-14` 固定版本对照门 | 报告能说明原意、改动和撤销方式 |

## Repair Playbook

1. 先判断失败属于源稿锁定、自然语言意图解析、风格匹配、范围控制、schema 连续性、关键词稳定、版权边界、下游可用性还是输出证据。
2. 若源稿缺失或路径漂移，先修 `N1-SOURCE-LOCK` 和输出目录，不进入风格优化。
3. 若用户只给“更高级/不对味/更好看”，先回 `N2B-CLARIFY`，不要直接重塑全局风格。
4. 若用户自然语言抽象，先回 `N2A-INTENT-PARSE`，把词拆成媒介、色彩、光影、材质、构图、情绪、禁区等风格轴。
5. 若风格优化看似漂亮但不贴项目，回 `N2C-STYLE-MATCH`，补与 `04` 源稿、`02` 故事源和下游消费的匹配矩阵。
6. 若关键词不稳，先删重复和空泛质量词，再按权重排序，不要继续堆新词。
7. 若用户要求“大胆改”但未授权重塑全局风格，最多进入 `medium_rework` 或 `experimental_alt`，不要覆盖 canonical。
8. 若局部字段优化越界，回 `N4L-LOCAL-FIELD`，恢复未选字段或补同步理由。
9. 若版权/IP 风险出现，优先安全转译为视觉特征；无法转译时进入冲突判别。
10. 若报告证据不够，补 `思考过程`、`high_energy_intent_map`、`style_matching_matrix`、`review_result` 和 `repair_actions`。

## Reusable Heuristics

- `04R` 的价值不是另写一个更漂亮的风格词，而是把用户个人审美意图精确投影到 04 的全局风格 schema。
- “高能意图解析”的关键是把口味词拆成风格轴和目标字段；没有字段落点的审美判断不可复核。
- 风格匹配必须同时看用户意图、04 源稿、02 故事证据、参考图事实和下游 05/06 消费，少一个维度都容易跑偏。
- 用户说“高级”通常不是要更多词，而是要减少噪声、提升材质和光影秩序；先降噪再增强。
- 用户说“不对味”时，优先定位偏差轴：媒介、色彩、光影、材质、情绪、时代、关键词或版权锚点，而不是整体重写。
- 临时风格偏好默认只服务本轮；长期记忆必须有用户明确授权。
- 修改强度是自然语言风格调优的安全阀：不确定时默认 `light_touch`，探索性需求优先 `experimental_alt`。
- 多轮调优要保留版本对照和回退说明，否则用户无法继续表达“保留这部分，撤掉那部分”。
