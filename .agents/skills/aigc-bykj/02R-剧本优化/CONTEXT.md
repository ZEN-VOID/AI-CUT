# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/02R-剧本优化` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-28

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 02R 被当成重新执行 02 | 阶段边界层 | 回到 `02` 源稿锁定，只做二次优化 | `SKILL.md` 固定 `Source Continuity Contract` | 输出落在 `02R-剧本优化`，且回指 `02` 源稿 |
| 整体调优变成自由重写 | 叙事结构层 | 恢复事实、人物关系、因果链和事件顺序，只保留必要增强 | `PASS-02R-07` 阻断破坏基本叙事结构的改写 | `narrative_integrity_check` 可复查 |
| 用户概念没有落到编辑点 | 需求映射层 | 把概念转成节奏、冲突、人物、场景、对白交付等变量 | `N3O-REQUIREMENT-MAP` 固定需求映射证据 | 每条需求有采纳/转译/拒绝状态 |
| 局部调优污染未选区 | 局部范围层 | 回滚未选区，只保留选区内最小改动 | `PASS-02R-05` 阻断未授权范围扩张 | `local_diff_summary` 不包含未选区改写 |
| 局部目标与前后剧情冲突仍被硬改 | 冲突判别层 | 停止终稿，输出 `冲突判别单` 等用户裁决 | `N4C-CONFLICT` 固定硬冲突必须阻断 | manifest verdict 为 `conflict_blocked` |
| 为满足用户需求牺牲可拍可演性 | 下游可用性层 | 把抽象诉求转成可见、可听、可演、可下游消费的表达 | `PASS-02R-09` 固定可拍可导可演门 | 优化稿仍能进入 03/04/05/06 |
| 报告只有结果没有思考过程 | 输出证据层 | 补写业务分析、模式判型、冲突扫描和汇流依据 | `FAIL-02R-REPORT` 阻断证据缺失 | `优化报告.json` 包含 `思考过程` |
| 需求冲突被平均处理 | 用户裁决层 | 明确取舍，不自行折中互斥要求 | 多需求优先级固定为显式排序 > 真源约束 > 叙事结构 > 下游可用性 > 审美增强 | `request_resolution_table` 有未采纳原因 |
| 用户自然语言被直接当成改稿指令 | 意图归一层 | 先生成 `natural_language_intent_map`，把口味词转成编辑变量 | `N2A-INTENT-NORMALIZE` 固定为前置节点 | 每个口语需求都有变量、置信度和风险 |
| “优化一下/不对味”被直接大改 | 澄清门层 | 输出 2-3 个候选方向，等待用户选择 | `N2B-CLARIFY` 阻断低信息多解需求 | verdict 为 `clarification_blocked` |
| 个人偏好被误写入长期记忆 | 记忆边界层 | 回收为本轮 `user_taste_profile`，除非用户明确要求记住 | `Temporary Personal Taste Profile` 固定不自动写 MEMORY | 无授权时项目 `MEMORY.md` 不变 |
| 修改强度越权 | 授权边界层 | 降级到 `light_touch` 或请求授权 | `Edit Intensity Ladder` 固定 heavy/experimental 需要授权 | `edit_intensity` 有授权依据 |
| 多轮自然语言调优无法回退 | 版本治理层 | 补 `version_comparison` 和 `rollback_note` | `PASS-02R-13` 固定版本对照门 | 报告能说明原意、改动和撤销方式 |

## Repair Playbook

1. 先判断失败属于源稿锁定、需求映射、范围控制、冲突判别、叙事完整性、可拍可演性还是输出证据。
2. 若源稿缺失或路径漂移，先修 `N1-SOURCE-LOCK` 和输出目录，不进入正文优化。
3. 若用户需求抽象，先回 `N3O-REQUIREMENT-MAP`，把概念拆成可编辑变量。
4. 若用户只给“优化一下/不对味/更好看”，先回 `N2B-CLARIFY`，不要直接进入整体重写。
5. 若用户要求“大胆改”但未授权改事实、顺序或对白，最多进入 `medium_rework` 或 `experimental_alt`，不要覆盖 canonical。
6. 若局部优化越界，回 `N3L-SELECTION-LOCK`，先恢复未选区，再重新做选区内最小编辑。
7. 若局部目标与前后剧情冲突，不做“聪明折中”，直接输出冲突判别单。
8. 若整体优化读起来更华丽但结构松掉，先修因果、人物动机、信息释放和场景推进。
9. 若报告证据不够，补 `思考过程`、`natural_language_intent_map`、`conflict_scan_matrix`、`review_result` 和 `repair_actions`，不要只写“已优化”。

## Reusable Heuristics

- `02R` 的价值不是比 `02` 写得更多，而是把用户明确介入的需求稳定落到已有剧本处理稿里。
- 整体调优的上限由用户需求决定，下限由基本叙事结构决定；两者冲突时先保结构，再解释取舍。
- 局部调优最容易失败在“顺手修前后文”；前后文只能做校验窗口，不是编辑范围。
- 局部目标如果必须改前后剧情才能成立，就不是局部优化，而是范围升级或真源冲突。
- 多需求调优不要平均抹平冲突；每条需求都应有 `accepted / transformed / rejected / conflict_blocked` 状态。
- 对 `02R` 来说，冲突判别单是合格产物，不是失败逃避；它保护用户的最终裁决权。
- 优化稿仍要继承 `02` 的可拍、可导、可演标准，不能退化成抽象文学润色。
- 用户说“更爽/更高级/不对味”时，最稳的第一步不是改稿，而是把这些词翻译成节奏、信息释放、冲突强度、留白、对白直白度等变量。
- 个人口味画像默认只服务本轮；长期记忆必须有用户明确授权。
- 修改强度是自然语言调优的安全阀：不确定时默认 `light_touch`，探索性需求优先 `experimental_alt` 而不是覆盖原稿。
- 多轮调优要保留版本对照和可回退说明，否则用户很难继续精确表达“保留这个，但撤掉那个”。
