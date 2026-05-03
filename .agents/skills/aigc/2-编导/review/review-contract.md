# Review Contract

## Review Purpose

`2-编导` 的 review gate 验证逐集编导稿是否忠实承接 `1-分集`，并能被下游分组、摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和剧本字段门禁。
- 若本轮启动 subagents 模式，review 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`：是否从项目 `team.yaml` 解析监制组相关智能顾问团、是否把顾问任务同步到当前 `steps/directing-workflow.md` 节点、`Thought Pass Map` 与相关 review gate、是否要求顾问代入角色意识/创作风格/专业水准参与节点判断和执行取舍、是否形成带 `node_ref/pass_ref/gate_ref/role_lens` 的 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写上游真源。
- review 必须加载 `../references/performance-and-scene-craft-contract.md`，检查场景状态差、潜台词行为、演员任务、场面调度内嵌、沉默反应和摄影越权风险。
- review 必须加载 `../references/directorial-authorship-contract.md`，检查关键场景是否有真正编导创作干货：戏剧问题、人物压力、观众位置、信息释放、表演/空间/道具/声音发动机和可拍执行策略，而不是只做结构规整或漂亮改写。
- 若本轮启用 `controlled_enrichment`，review 必须加载 `../references/controlled-enrichment-contract.md`，检查新增承托细节是否有上游锚点、是否只属于表现层、是否记录 `controlled_enrichment_ledger`。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N6R-DIRECT-REPAIR`，由 `2-编导` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `2-编导/第N集.md`。
- 允许直接修复的范围：字段投影、声画配对、slugline 去重、画面具像化、声音本体、高潮承托、表演提示内嵌、场面调度内嵌、沉默反应、controlled enrichment 留证、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `1-分集` 修剧情、把 B 路线扩展为新增对白/桥段/因果。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何保真、对白、声画、slugline、字段纯度、高潮承托、表演任务、场面调度、controlled enrichment 或 LLM-first 问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-DIRECT-01` | 输出路径为 `projects/aigc/<项目名>/2-编导/第N集.md` | `FAIL-PATH` |
| `GATE-DIRECT-02` | frontmatter 含 `source_episode_path` 且可回指上游 | `FAIL-SOURCE` |
| `GATE-DIRECT-03` | 上游事实信息量与顺序完整承接 | `FAIL-FAITHFULNESS` |
| `GATE-DIRECT-04` | 对白逐字保真，中文双引号，引号内无动作 | `FAIL-DIALOGUE` |
| `GATE-DIRECT-05` | 声音字段就近配对对应 `*画面` 字段 | `FAIL-PAIRING` |
| `GATE-DIRECT-06` | 每个场景至少一条正式画面字段 | `FAIL-SCENE-VISUAL` |
| `GATE-DIRECT-07` | 场景标题是阿拉伯编号 + slugline，同 slugline 不重复开场 | `FAIL-SLUGLINE` |
| `GATE-DIRECT-08` | `动作画面` 不含心理解释、抽象判断或小说章节名 | `FAIL-ACTION-PURITY` |
| `GATE-DIRECT-09` | 脚本没有替代 LLM 生成核心创作正文 | `FAIL-LLM-FIRST` |
| `GATE-DIRECT-10` | 所有 `*画面`、`环境描写`、`道具特写`、`表演提示` 均具像化、画面化、反抽象、反概念、反比喻 | `FAIL-CONCRETE-VISUAL` |
| `GATE-DIRECT-11` | `音效` 字段只写声音本体，不写时间说明、事件概括或描述性句子 | `FAIL-SOUND-LITERAL` |
| `GATE-DIRECT-12` | 上游存在高潮/爽点/高光成分时，输出完成 `peak_visual_pass`，高点有可回指证据、可拍承托、状态差或余波，且没有新增事实、对白或因果 | `FAIL-PEAK-VISUAL` |
| `GATE-DIRECT-13` | 启动 subagents 模式时，已完成同步于当前思维·执行节点的 `team.yaml` 监制顾问请教，并沉淀为带节点锚点的后续上下文，或记录上层阻断降级 | `FAIL-ADVISOR-CONSULT` |
| `GATE-DIRECT-14` | 关键场景完成 `director_substance_pass`：有上游锚点、戏剧问题、人物选择压力、观众位置、信息释放和可拍执行策略，并已内嵌进剧本句段 | `FAIL-DIRECTOR-SUBSTANCE` |
| `GATE-DIRECT-15` | 关键场景有可回指上游的进入状态、压力源、转折点和退出状态，或报告说明其过渡功能 | `FAIL-SCENE-TURN` |
| `GATE-DIRECT-16` | 心理、潜台词、信任变化、权力关系和沉默反应被转成可执行行为、表演任务、场面调度或反应余波，并内嵌到对应剧本句段 | `FAIL-PERFORMANCE-TASK` |
| `GATE-DIRECT-17` | `场面调度` 不写机位、景别、镜头运动、分镜编号或 `分镜明细预设` | `FAIL-CINEMATOGRAPHY-OVERREACH` |
| `GATE-DIRECT-18` | 启用 `controlled_enrichment` 时，每个新增承托细节都有上游锚点、目标字段、用途和风险检查，且没有新增对白/事件/因果/规则 | `FAIL-CONTROLLED-ENRICHMENT` |
| `GATE-DIRECT-19` | 终稿没有在场景末尾或分镜组末尾总结式列出 `表演提示` / `场面调度`；规划结果已拆入对应画面、动作、对白画面、道具、群像、声音或反应字段 | `FAIL-PERFORMANCE-SUMMARY-BLOCK` |

## Recommended Mechanical Check

```bash
python3 .agents/skills/aigc/2-编导/scripts/validate_script_projection.py projects/aigc/<项目名>/2-编导/第N集.md
```

该脚本只检查结构、字段和基础配对，不能证明剧情事实完整承接；事实完整性和对白逐字保真仍需 LLM/人工对读上游。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在保真、对白、声画或场景标题阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
  output_path: projects/aigc/<项目名>/2-编导/第N集.md
  checks:
    faithfulness: pass
    dialogue_lock: pass
    audio_visual_pairing: pass
    slugline_stability: pass
    field_purity: pass
    concrete_visuals: pass
    sound_literal: pass
    peak_visual_treatment: pass
    advisor_consultation: pass
    director_substance: pass
    scene_turn: pass
    performance_task: pass
    blocking_power: pass
    performance_integration: pass
    controlled_enrichment: pass
    hollywood_quality: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
  controlled_enrichment_ledger:
    mode: none | controlled_supportive
    items: []
  director_substance_evidence:
    - scene_id: ""
      source_anchor: ""
      dramatic_question: ""
      audience_position: ""
      character_pressure: ""
      scene_turn: ""
      directorial_strategy: ""
      embedded_in_fields:
        - ""
      risk_check:
        fact_drift: false
        new_dialogue: false
        over_explaining: false
        cinematography_overreach: false
  advisor_consultation_packet:
    status: not_applicable | completed | blocked
    roster_source_note: ""
    roster:
      - name: ""
        skill_path: ""
        selected_for: ""
    node_anchors:
      - node_ref: ""
        pass_ref: ""
        gate_ref: ""
        role_lens: ""
        accepted_guidance_summary: ""
        risk_flags: []
    routeback_targets:
      - node_ref: "N3-SCENE | N4-FIELD | N4.4-DIRECTORIAL | N4.5-PEAK"
        reason: ""
        resolution: "reworked | blocked"
    execution_brief: ""
    downgrade:
      blocked_by: "system | developer | tool | user | none"
      planned_path: ""
      actual_path: ""
      skipped_members: []
  findings: []
```

当 `advisor_consultation_packet.status == completed` 时，`node_anchors` 至少包含一个带 `node_ref/pass_ref/gate_ref/role_lens` 的采纳摘要；若顾问指出前置节点问题，`routeback_targets` 必须记录回修节点、原因和处理结果。若真实 subagent dispatch 被阻断，`downgrade` 必须完整记录阻断层级、原计划路径、实际路径和未启动成员。

`director_substance_evidence` 必须证明关键场景的编导判断来自上游原文，并已经进入正文具体字段；只写“戏剧张力更强”“电影感更好”“节奏更紧”但缺少动作、声音、空间、道具、表演或观众位置证据时，verdict 必须为 `needs_rework`。
