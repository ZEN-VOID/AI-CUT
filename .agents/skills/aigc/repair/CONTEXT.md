# CONTEXT.md

本文件是 `aigc-repair` 的经验层知识库，不是执行流水账。它用于沉淀 AIGC 影视阶段产物修复时的源层回看、跨阶段影响判定、豆包执行降级和中文润色边界。

## Purpose & Loading Contract

- 每次调用 `$aigc-repair` 时，必须同时加载同目录 `CONTEXT.md`。
- 本文件只保存经验性 Type Map、Repair Playbook 与 Reusable Heuristics，不改写 `SKILL.md` 的入口、模式和输出合同。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `SKILL.md` > 分区合同 > 本 `CONTEXT.md`。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 30000
hard_limit_chars: 60000
status: ok
last_checked_at: 2026-05-24
recommended_action: keep-repair-heuristics-only
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只改下游提示词，下一轮又生成旧事实 | source owner drift | 回到最早 owning stage 修源层，再同步下游 | repair 必须先做 source rule review 和 impact map | 旧口径在上游无正向残留 |
| 中文润色把镜头事实、对白或角色动作顺手改了 | polish overreach | 限定润色只处理表达、节奏和可读性 | 豆包 task packet 写明 forbidden changes | 事实、对白、顺序和镜头编号一致 |
| 审片 finding 直接改 `8-分组`，没有回看 `7-摄影` | review route shortcut | 先判断缺陷源于视频、图像、分组还是摄影 | review finding 必须映射 source owner | repair report 列出 source_rules_reviewed |
| 多个子技能包互相覆盖同一资产口径 | cross-stage consumer drift | 建 impact map，列出上游、同层、下游和 future guardrail | `3-主体`、`9-图像`、`10-画布` 修复统一走 owner route | 所有消费者引用同一新版对象 |
| 豆包调用失败但报告声称已执行 | provider evidence gap | 记录 provider-failed-local-plan，不宣称 provider 执行 | `provider_evidence` 必填文本和 report 路径或阻断原因 | evidence 路径存在或失败说明明确 |
| repair 只做结构化正确，但中文仍像翻译腔/工程腔 | local expression miss | 将中文润色和本土语境创意交给豆包执行 lane | 在 `doubao_task_packet` 写明中文气口、本土文化语境和目标受众 | review 包含 `local_chinese_fit` |
| 生成资产返工被写成“修改图片/视频文件” | asset truth confusion | repair 只失效、重建任务或路由生成 leaf | 图像/视频结果由 owning provider/leaf 生成 | asset action 是 preserve / invalidate / regenerate |
| 项目长期偏好未写 MEMORY，后续阶段又偏回旧口径 | project memory drift | 用户明确长期要求时更新项目 `MEMORY.md` | repair intake 区分一次性改动和长期偏好 | MEMORY 与 repair report 口径一致 |
| 修复正文或润色像模板替换 | scripted repair layer | 标记 `FAIL-REPAIR-SCRIPTED-REPAIR`，回到 provider/LLM 主创 lane | scripts 只做 diff、扫描、投影、校验 | repair text 有 source rule refs 和 authorship note |

## Repair Playbook

1. 先锁定 `projects/aigc/<项目名>/`、目标输出物、修复意图和写回权限。
2. 定位目标输出物所属 stage / leaf / satellite，加载其 `SKILL.md + CONTEXT.md` 和必要分区。
3. 用 `types/type-map.md` 选择 scope、operation 和 acceptance 包；多对象、多阶段修复必须多选叠加。
4. 建立 impact map：上游源层、同层相邻、当前局部、下游已产物、生成资产、future guardrail、review/state。
5. 先修最早 canonical owner，再同步投影和下游消费者；不得用下游润色掩盖上游错误。
6. 执行型文本修复默认整理上下文给豆包；若 provider 不可用，报告降级并只输出 repair plan 或当前模型可审计草案。
7. 中文润色只优化清晰度、自然度、影视执行可读性和中文气口；创意激发只能给候选增强，不自动改写源层事实。
8. 修复后必须执行 review gate，至少检查 source rule 回看、旧口径残留、stage owner、provider evidence、资产状态和 residual risks。
9. 形式化 diff、字段齐全或替换成功不能证明 repair 合格；若修复正文只是把旧模板换锚点，必须返工到 LLM/provider 主创。

## Reusable Heuristics

- AIGC repair 的核心产物不是 patch，而是 `source_rules_reviewed + impact_map + writeback_order`。
- 越靠后的产物越像症状：图像/视频失败常常源自 `3-主体` 的资产锚点、`7-摄影` 的镜头语言或 `8-分组` 的组内连续性。
- “更好看”不是合法修复目标；必须翻译成阶段合同可验收的目标，例如表演更可见、镜头更连续、场景锚点更稳定、提示词更可执行。
- 豆包适合做中文分析、表达润色、结构化 repair brief 和创意候选；最终 canonical 写回仍由 owning stage 合同裁决。
- 本技能的差异化价值在“双模型分工”：当前模型负责工程化治理，豆包负责中文语境、本土文化气息和创意表达主执行。
- 对多个子技能包输出物做整体调整时，先找共同源层，不要逐个文件局部打补丁。
- 审片 finding 是证据入口，不是自动改稿权；它要回到 `3-主体`、`7-摄影`、`8-分组`、`9-图像` 或 `10-画布` 的 owner route。
- 若用户要求“以后都按这个口味”，优先写项目 `MEMORY.md`；若只是本次返工，不要污染长期记忆。
- repair 的脚本价值在定位和校验，不在主创；任何“批量润色/批量修复正文”都要有 provider evidence 或明确降级为 repair plan。
