# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `1-分镜表现/分镜构图` 的经验层知识库，不是执行日志。
- 调用本子技能时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 有镜数但没有镜头感 | 字段合同层 | 补齐八项静态字段 | 固化固定字段集 | 每镜不再只剩编号 |
| 连续多镜构图雷同 | 质量层 | 拉开景别/视角/构图风格 | 固化组内反重复门槛 | 连续镜不再复制 |
| 全组没有视觉峰值 | 审美门槛层 | 强化至少一镜的非常规构图 | 固化“每组至少一镜峰值” | 全组不再平铺 |
| 构图层越界写运镜或色彩 | 边界层 | 清除越界字段 | 在 SKILL 固定静态字段边界 | 内联字段只保留静态镜头语义 |
| 直接把整集时长拿来切单组分镜 | 时间真源层 | 回到 `分镜组时长映射 -> 默认组时长 -> 切分时长策略` 重新解析组总时长 | 把组总时长读取链写进 execution flow 与 output template | 帧级时间范围闭合到当前组而非整集 |
| 上游 `panel_count` 合法，但实际构图过不了模板门槛 | 上下游协同层 | 先重排功能位、景别、角度与遮挡，再必要时申请 `refined_range` 内微调 | 明确“镜数真源在上游，构图层只做落地验收与回退” | 模板门槛在实际镜头字段中成立 |
| 同场景相邻组首帧与上一组尾帧断开 | 连续性层 | 把上一组尾帧的主体动作/状态压缩复述进本组首帧 `角色及站位` | 固化组间回溯合同与失败码 | 首帧能识别承接上一组尾势 |
| 侧车 canonical shot 与父级八字段投影互相漂移 | 写位投影层 | 以 canonical shot 为真源重投影父级单行 | 固化“Layer A 真源 + Layer B 投影”双层合同 | 父级单行能回放到侧车明细 |

## Repair Playbook

1. 先确认 `panel_count / template_id / group_duration` 三个上游真源已经稳定。
2. 再判 `scene_type`，并检查是否命中同场景组间回溯。
3. 再切每镜 `时间`，保证连续与闭合。
4. 再补 canonical shot 字段，并把至少一镜推到全组最大胆的构图峰值。
5. 最后才投影父级八字段单行并回写。

## Reusable Heuristics

- 对当前脚本阶段来说，最有价值的不是把导演阶段所有字段照搬过来，而是保住“最小可读镜头骨架”。
- 构图阶段先看 `panel_count / rhythm / scene_type / group_duration`，再落到逐帧字段；不要一上来就凭直觉写第一套顺手镜头。
- 更稳的裁决顺序是 `叙事 -> 合理 -> 审美`：先让镜头服务信息与关系，再排除翻轴、断裂和不可拍，最后才在合法候选里选最有电影张力的那组。
- `构图方式` 才是 canonical shot 真源，`构图风格` 只是父级单行里的用户向投影名；真源和投影不能倒挂。
- 组总时长问题不在本层拍脑袋估；先走 `分镜组时长映射 -> 默认组时长 -> 切分时长策略`，再谈帧级时长。
- 如果一组所有镜都安全常规，说明不是“稳”，而是“塌”。
- 审美峰值最好由“反常规角度 / 强前景压迫 / 纵深穿透 / 极窄焦点”中的至少一类承担，而不是只靠把景别写得更近。
- 每帧都要能回答“观众先看哪里”；焦点不明时，优先通过亮度、清晰度、面积、对比或唯一运动建立单一主焦点。
- 对话或稳定互动组，先守轴线与背景极点，再谈变化；无过桥不要为了变化私自翻转主反位。
- 同场景相邻组的首帧最好压缩带上一条上一组尾帧动作短语，比空泛写“承接上一组尾势”更稳定。
- 构图层真正的比较尺不是“字段是不是填满了”，而是“上游镜数有没有被落成可拍、可读、可回写、不过门槛塌缩的一组镜头”。

## Case Log

### Case-20260409-AIGC-SCRIPT-STORYBOARD-COMPOSITION

- milestone_type: source_contract_change
- outcome: 为 `分镜构图` 建立了适配脚本阶段的静态镜头字段合同，把 ZEN-VOID 的导演阶段经验压缩成内联脚本可消费的八项字段。
- root_cause_or_design_decision: 用户要求“除了分镜序号还要景别、景深、构图风格等内容”，并明确参照 ZEN-VOID 的 `5-分镜构图`；但当前仓的 `3-明细` 阶段并不需要继承导演阶段全部 JSON 结构，因此必须做适配层收缩。
- final_fix_or_heuristic: 保留最关键的静态镜头骨架八项字段，显式排除运镜、色彩、光影、转场，让本子技能只承担当前父级真正需要的构图裁决。
- prevention_or_replication_checklist:
  - [x] 已固定八项静态字段
  - [x] 已加入视觉峰值门槛
  - [x] 已加入组内反重复门槛
  - [x] 已把越界字段排除出责任范围
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/5-分镜构图/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/5-分镜构图/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“除了注入分镜序号还要，景别，景深，构图风格等内容，由子技能包：分镜构图决定”。

### Case-20260409-AIGC-SCRIPT-STORYBOARD-COMPOSITION-CANONICAL-SHOT

- milestone_type: source_contract_change
- outcome: 将 `分镜构图` 从“八字段轻量合同”升级为“双层写位合同”：侧车维护 canonical shot 真源，父级继续消费八字段单行投影。
- root_cause_or_design_decision: 用户要求把候选镜数、时长切分、反平庸门控、同场景组间回溯、canonical shot 字段句法等精华内容融合进 `分镜构图`，但这些内容同时跨越上游镜数裁决与本层构图落地。如果直接整段塞进本目录，会让 `分镜密度` 与 `分镜构图` 长出重复真源，因此必须先划清“镜数在上游、落地在本层、父级只吃投影”的关系，再分发到 `SKILL / references / CONTEXT`。
- final_fix_or_heuristic: 保留 `panel_count / template_id` 在 `分镜密度` 的真源地位，在本层新增 `group_duration` 读取链、`scene_type` 判定、帧级时间分配、canonical shot 字段、构图审美峰值、组间回溯与集级去塌缩门禁，并把 `构图方式 -> 构图风格` 的投影关系写死。
- prevention_or_replication_checklist:
  - [x] 已写清上游镜数真源与本层落地真源的边界
  - [x] 已补 `分镜组时长映射 -> 默认组时长 -> 切分时长策略` 读取链
  - [x] 已补 canonical shot 字段与父级八字段投影关系
  - [x] 已补同场景组间回溯与 `FAIL-INTERGROUP-ECHO-*`
  - [x] 已补构图审美峰值与 `FAIL-SEQUENCE-COLLAPSE`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/references/execution-flow.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/scene-duration-projection.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“如已有相关内容不必赘述，仅作缺失补全；不得直接大段插入，要消化吸收后融合和分配到 `分镜构图` 各子部目录”。
