# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/3-分组` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/3-分组/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 输入没有锁定到 `2-剧本/第N集.md` | 输入真源层 | 回到规划主稿重新锁定当前集范围 | 在 `SKILL.md + validator` 固化输入根与文件名门禁 | 输入清单与当前集一致 |
| 把 `3-分组` 写成摘要说明稿，而不是带分组切口的正文稿 | 输出治理层 | 回到 `2-剧本/第N集.md`，只在正文内部插入分组标题 | 在 `SKILL.md + template + validator` 固化“grouped script 而非摘要稿” | `第N集.md` 与 `2-剧本` 保持同形态 |
| 忽略 `preset_registry` 锁轴导致越权拆分 | 锁轴继承层 | 重新读取 manifest 并登记不可拆锚点 | 在 `SKILL.md` 固化 `P1>P2>P3>P4` 与 `V-PRESET-LOCK` | hard/soft lock 不再被跨组破坏 |
| 分组切口混用了 `分镜组ID` 与 `分镜ID`，或把第3段写成槽位号 | ID 合同层 | 把正文标题改回三段式 `分镜组ID`，并让第3段只表达“场内第N组” | 在模板、validator、父 skill 与 `2-Global` 固化“组三级、镜四级；组号按 1/2/3 递增” | 标题语义不再漂移 |
| `3-分组` 长出 `.grouping.json`、`thinking/` 等平行真源 | 真源治理层 | 删掉非 canonical 输出，只保留 `第N集.md + 执行报告.md` | 在 shared I/O、skill_manifest 与脚本中去掉 sidecar 默认生成 | 目录输出与 `1-分集/2-剧本` 一致 |
| 分组只靠叙事直觉，组粒度浮动过大 | 量化合同层 | 回到场景顺序与时长策略投影重新切组 | 在 reference、`SKILL.md`、validator 与执行报告中固化 `effective_text_chars` 门槛 | 超硬上限组不会继续通过 |
| `3-分组` 虽然挂了 subagent，但父 skill / team / specialist 边界不清 | subagent 治理层 | 把 stage-local topology、writeback、audit 收回 `3-分组/SKILL.md`，让 shared team 只保留调度入口 | 在 `3-分组/SKILL.md`、`1-Planning/SKILL.md`、`规划组/team.md` 与 `分组.md` 固化 stage-local ownership | 不再把 team/agent 文档误读成第二层阶段总线 |
| 量化规则只写在 reference，计算仍靠手填 | 计算真源层 | 增加 `scripts/grouping_quantizer.py` 统一计算时长、字窗与 `effective_text_chars` | 让 validator 直接消费 quantizer 结果，并在混合源命中镜号范围时强制回算 | `effective_text_chars` 不再只是说明性字段 |

## Repair Playbook

1. 先确认 `2-剧本/第N集.md` 是否是唯一输入主证据。
2. 再确认 `episode-split-plan.json` 与 `story-source-manifest.yaml` 是否给出了 lock/handoff 约束。
3. 再看 grouped script 是否仍保持上游正文结构，只在切口处新增三段式 `分镜组ID` 标题。
4. 再检查 `effective_text_chars / base_text_window / hard_text_window` 是否真的参与裁决。
5. 最后检查唯一 `执行报告.md` 是否已更新当前集结论。

## Reusable Heuristics

- `3-分组` 最稳的定位不是摘要板，而是“在 `2-剧本` 正文里切出组边界后的 grouped script”。
- 对这个阶段来说，用户最需要看见的是正文里的组切口，不是另一套组说明表。
- 若 `preset_registry` 已经给出 `hard_lock`，优先保骨架，不要为了组数好看去拆锁轴。
- `3-分组` 的标题最稳口径是三段式 `分镜组ID`：`集号-起始场景号-该场第N组`；四段式 `分镜ID` 要留给后续拆镜阶段。
- `3-分组` 的真正门槛不是再造 sidecar，而是保证 grouped script 对上游正文保真，同时让下游能从 `【x-x-x】` 直接回链。
- 对当前阶段最有效的抗漂移机制是：先锁场景顺序，再用 `15秒默认时长 + pace_tier + effective_text_chars` 收缩边界。
- 对 `3-分组` 来说，最稳的 subagent 形态不是再造本地 team，而是“父 skill 持有 stage-local topology，shared planning team 只提供 specialist 路由”。
- 涉及 `effective_text_chars / duration mapping / mixed-source recompute` 的规则，一旦进入 validator，就应该有独立脚本真源，不要继续靠人工抄数。

## Case Log

### Case-20260412-AIGC-PLANNING-GROUPING-MIGRATION

- milestone_type: source_contract_change
- outcome: 参照 `AIGC-ZEN-VOID` 的 `3-拍摄段落`，在 DREAMER runtime 下重建 `1-Planning/3-分组` 的 leaf 合同。
- root_cause_or_design_decision: 仓内 `3-分组` 目录为空，但父 skill、`2-Global` 与 `节奏` agent 已把它当成前置路径；若继续空置，规划阶段会长期依赖纯 agent 投影，没有本地真源与校验链。
- final_fix_or_heuristic: 保留 `3-拍摄段落` 的 manifest、postprocess、validator、Field Master 和 QA 闭环，但把 canonical 输出收束为 `projects/<项目名>/1-Planning/3-分组/第N集.md + 执行报告.md`。
- prevention_or_replication_checklist:
  - [x] 已固定 `2-剧本/第N集.md` 输入根
  - [x] 已固定 `3-分组/第N集.md` local canonical 输出
  - [x] 已新增 `grouping-output.template.md`
  - [x] 已新增 postprocess + validate 脚本
  - [x] 已把 `group_count + group_order + bootstrap_output` 固化进 handoff
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/3-分组/skill_manifest.json`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/postprocess_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
- user_feedback_or_constraint: 用户要求基于 `skill-subagents`，全面参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/3-拍摄段落` 完善 `1-Planning/3-分组`，但输入输出必须改为当前项目仓库路径。

### Case-20260412-AIGC-PLANNING-GROUPING-INLINE-GROUPED-SCRIPT

- milestone_type: source_contract_change
- outcome: 将 `3-分组` 从“摘要说明稿 + sidecar”改写成“在 `2-剧本` 正文内插入分组标题的 grouped script”。
- root_cause_or_design_decision: 用户明确指出现有结果“不 OK”，核心问题不是分组判断本身，而是输出形态错了：`3-分组` 应与 `1-分集`、`2-剧本` 一样产出逐集正文文件和一份总执行报告，而不是再长出摘要板和机读 sidecar。
- final_fix_or_heuristic: 在 `SKILL.md`、shared I/O、template、postprocess、validator 与项目产物中统一改写为：`3-分组/第N集.md` 直接基于 `2-剧本/第N集.md` 插入组标题，`执行报告.md` 为目录总报告，默认不再生成 `.grouping.json`、`thinking/` 等平行真源。
- prevention_or_replication_checklist:
  - [x] `3-分组` 改为 grouped script 合同
  - [x] `执行报告.md` 改为总一份
  - [x] validator 改为检查分组标题、量化字段与正文保真
  - [x] 默认 sidecar 输出已下线
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/1-Planning/3-分组/templates/grouping-output.template.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/postprocess_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
- user_feedback_or_constraint: 用户明确要求 `3-分组` 输出“同 `1-分集 / 2-剧本` 一样的 `第N集.md + 执行报告.md`”，并在正文中直接展示分组切口。

### Case-20260412-AIGC-PLANNING-GROUPING-QUANTIZED-IDS

- milestone_type: source_contract_change
- outcome: 将 `3-分组` 从误用四段式标题修正为三段式 `分镜组ID`，并引入场景顺序与时长策略量化门槛。
- root_cause_or_design_decision: 根 `AGENTS.md` 只把四段式定义给 `分镜ID`，而旧 `3-分组` 误把它当成组标题；同时缺少 `effective_text_chars` 对 `hard_text_window` 的硬校验，导致组边界可解释但不稳定。
- final_fix_or_heuristic: 在 `references/scene-order-duration-strategy.md` 固化量化规则，在 `SKILL.md`、template、validator、父 skill 与 `2-Global` 中统一三段式 `分镜组ID` 口径，并要求 `执行报告.md` 为每组落 `estimated_duration_seconds / effective_text_chars / window_status`。
- prevention_or_replication_checklist:
  - [x] 正文标题已改为三段式 `分镜组ID`
  - [x] 四段式 `分镜ID` 已保留给下游
  - [x] validator 已校验量化字段
  - [x] 父 skill 与下游消费者已同步
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/references/scene-order-duration-strategy.md`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- user_feedback_or_constraint: 用户明确指出“对分镜ID/分镜组ID 的理解不对，整个分镜划分浮动太大”，要求先把组标题改回三段式，再在源层补一套量化标准。

### Case-20260412-AIGC-PLANNING-GROUPING-SUBAGENT-GOVERNANCE-RESET

- milestone_type: source_contract_change
- outcome: 将 `3-分组` 从“leaf 合同 + 一个分组 agent 附注”重构为真正的 stage-local parent skill，并明确保留 shared planning team 而不新增本地 team。
- root_cause_or_design_decision: 旧合同虽然提到 `分组` agent，但 `3-分组` 仍主要像单技能 leaf 说明书；team 又重复持有整条 `1-Planning` 链路的拓扑，导致 `3-分组` 的 stage-local ownership 与 shared team 边界发散。
- final_fix_or_heuristic: 把 `3-分组` 的 trigger/topology/context/synthesis/audit 全部收回父 skill，shared team 只保留调度入口与 handoff matrix，`分组` specialist 只保留边界建议与 `patch / note / report`；不新增本地 `team.md`、reviewer 或 auditor。
- prevention_or_replication_checklist:
  - [x] `3-分组/SKILL.md` 已显式声明 stage-local parent skill 定位
  - [x] `1-Planning/SKILL.md` 已回指 stage-local ownership
  - [x] `规划组/team.md` 已标明自己是 shared dispatch plane
  - [x] `规划组/分组.md` 已收缩为纯 specialist
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.codex/agents/aigc/规划组/team.md`
  - `.codex/agents/aigc/规划组/分组.md`
- user_feedback_or_constraint: 用户明确要求按 `skill-subagents` 重新分析当前配套 subagents 是否合适，不合适就调整。

### Case-20260412-AIGC-PLANNING-GROUPING-QUANTIZER-SOURCE-LAYER

- milestone_type: source_contract_change
- outcome: 为 `3-分组` 增加 `scripts/grouping_quantizer.py`，把时长/字窗/有效字数/混合源回算从说明性规则提升为脚本真源。
- root_cause_or_design_decision: 旧 `3-分组` 虽然已有 reference 与 validator，但 validator 只检查字段是否存在，没有统一计算真源；这会让 `effective_text_chars`、`estimated_duration_seconds` 与混合源回算继续停留在“手填可解释”层。
- final_fix_or_heuristic: 新增 quantizer 负责解析 grouped script、duration mapping、report 中 `source_span` 与 `story-source-manifest.yaml`，统一计算 window 与 `effective_text_chars`；validator 改为直接消费 quantizer 结果，并在镜号范围可机读时强制 story-source recompute。
- prevention_or_replication_checklist:
  - [x] quantizer 已成为本阶段计算真源
  - [x] validator 已校验 frontmatter window 与 report 指标一致性
  - [x] mixed-source 命中镜号范围时会触发强制回算
  - [x] postprocess 已把 quantizer/validator 视为默认退出门
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/postprocess_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
- user_feedback_or_constraint: 用户明确追问“涉及到计算的部分是否考虑配置 scripts 配套”。 
