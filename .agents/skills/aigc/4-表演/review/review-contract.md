# Review Contract

## Review Purpose

`4-表演` 的 review gate 验证逐集编导稿中的表演层是否到位：心理反应可演可感知、演员演技控制精准、主角内心独白人称正确、动作字段客观可拍、表演提示和场面调度已拆入对应剧本句段而非末尾总结，并能被下游摄影和视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和表演字段门禁。
- review 必须加载 `../references/performance-and-scene-craft-contract.md`，检查场景状态差、潜台词行为、演员任务、场面调度内嵌、沉默反应和摄影越权风险。
- review 必须加载 `../references/psychological-reaction-contract.md`，检查 `心理反应` 是否有主体、有上游触发点、有可见/可听/可演通道，主角内心想法和主角视角判断是否保留为 `独白/内心独白` 或可感知反应，且没有抽象想象、内心解释、因果论文、未授权新对白、无关回忆或场景末尾总结块。
- review 必须加载 `../references/actor-performance-control-contract.md`，检查关键情绪 beat 是否避免情绪标签和模板化表情，是否具备上游触发点、情绪动机、微表情、非面部生理联动、环境声音或沉默余波、微动态限制，并已内嵌到既有字段而未新增剧情、对白或摄影方案。
- review 必须加载 `../types/type-map.md` 与 `../types/performance-evidence-type-map.md`，检查 `performance_type_profile`、证据字段 owner、required shape 和 consumed_by 是否一致。
- 若本轮启动 subagents 模式，review 还必须加载 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`，检查是否优先从 `team.yaml.roles.supervision.stage_profiles."4-表演"` 解析表演监制 roster、是否基于当前 `PASS-PERF-*` / `N*-PERF-*` 思维·执行节点派生顾问问题、是否形成 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写 `3-导演` 原文。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N8R-PERF-REPAIR`，由 `4-表演` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `4-表演/第N集.md`。
- 允许直接修复的范围：心理反应可感知化、表演提示内嵌、场面调度内嵌、沉默反应、主角内心独白回收、动作客观可拍化、直接情绪转译、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `2-编剧` 或 `3-导演` 修剧情。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何心理反应、演员控制、主角内心、动作纯度或表演集成问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-PERF-01` | 心理反应、演员控制、主角内心独白和动作纯度全部达标：`心理反应` 有主体、触发点和可见/可听/可演通道；关键情绪 beat 避免情绪标签空转，有触发点、情绪动机、微表情、非面部身体联动或环境声音承托；`内心独白（主角）` 引号内指代主角自身时使用第一人称；`角色动作` / `动作画面` 只写客观可拍动作，不含主观预判或心理意图词 | `FAIL-PERFORMANCE-TASK` |
| `GATE-PERF-02` | 表演提示和场面调度已拆入对应画面、动作、对白画面、道具、群像、声音或反应字段，没有在场景末尾或分镜组末尾总结式列出；场面调度不写机位、景别、镜头运动、分镜编号或 `分镜明细预设` | `FAIL-PERFORMANCE-INTEGRATION` |
| `GATE-PERF-03` | 启动 subagents 模式时，已完成 `team.yaml` 表演监制顾问请教；顾问问题同步于当前思维·执行节点，并沉淀为后续上下文，或记录上层阻断降级 | `FAIL-PERF-13A` |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在心理反应、演员控制、主角内心、动作纯度或表演集成阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_script_path: projects/aigc/<项目名>/2-编剧/第N集.md
  output_path: projects/aigc/<项目名>/4-表演/第N集.md
  checks:
    psychological_reaction: pass
    actor_performance_control: pass
    protagonist_inner_voice: pass
    objective_action_purity: pass
    performance_integration: pass
    advisor_consultation: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
  psychological_reaction_evidence:
    - scene_id: ""
      source_anchor: ""
      subject: ""
      reaction_function: "fear | recognition | suspicion | concealment | shame | trust_shift | power_pressure | withheld_speech | reasoning | memory"
      pov_owner: "protagonist | other_character | external"
      trigger: ""
      performance_task: ""
      getability_channels:
        visible: []
        audible: []
        performable: []
      target_fields:
        - "心理反应"
      risk_check:
        abstract_inner_life: false
        new_dialogue: false
        new_event: false
        over_explaining: false
        field_summary_block: false
        subjective_intent_in_action: false
        unrelated_backstory: false
        third_person_pov_judgment: false
  actor_performance_control_evidence:
    - scene_id: ""
      source_anchor: ""
      subject: ""
      trigger: ""
      surface_emotion: ""
      suppressed_emotion: ""
      hidden_motive: ""
      micro_expression:
        brow: ""
        eyes: ""
        mouth: ""
        facial_muscle: ""
      body_linkage:
        breath: ""
        hands: ""
        posture: ""
        object_action: ""
        voice: ""
      ambient_support:
        sound: ""
        silence_or_room_tone: ""
        environment: ""
      micro_dynamics: ""
      embedded_in_fields:
        - ""
      risk_check:
        emotion_label_only: false
        template_expression: false
        overacting: false
        new_dialogue: false
        new_event: false
        cinematography_overreach: false
  protagonist_inner_voice_evidence:
    - scene_id: ""
      source_anchor: ""
      protagonist: ""
      original_subjective_judgment: ""
      target_field: "内心独白（主角）"
      paired_visual_field: "内心独白画面"
      risk_check:
        third_person_pov_judgment: false
        new_dialogue: false
        unrelated_backstory: false
  objective_action_purity_evidence:
    - scene_id: ""
      field: "角色动作 | 动作画面"
      removed_subjective_wording: []
      objective_projection: ""
      risk_check:
        subjective_intent_in_action: false
        direct_emotion_label: false
  findings: []
  advisor_consultation_packet:
    status: "present | downgraded | not_applicable"
    roster_source_note: ""
    node_refs: []
    execution_brief: ""
    downgrade:
      blocked_by: "system | developer | tool | user | none"
      skipped_members: []
```
