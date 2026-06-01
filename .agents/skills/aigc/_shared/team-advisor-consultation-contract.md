# AIGC Init Team Synthesis Consumption Contract

本合同是旧“创作阶段 team advisor consultation”口径的兼容替代。当前有效规则是：`.agents/skills/team/` 成员身份技能只允许在 `0-初始化` 阶段被调用，用于固定题包问答、初始化复核与综合；`2-编导 / 3-运动 / 4-摄影 / 5-分组 / 6-设计` 等创作阶段不得再调用 team 成员技能、不得代入成员人格、不得生成新的 team 顾问包。

## Active Policy

- `team.yaml` 是初始化配队、成员问答来源、综合摘要和迁移证据，不是创作阶段运行时 roster。
- 创作阶段只可读取冻结上下文：`team.yaml.init_synthesis.stage_seed_summary.<stage>`、`init_handoff.stage_entry_seeds.<stage>`、`north_star.yaml.创作阶段不变量.<stage>`，以及必要的成员问答 provenance。
- 创作阶段不得解析或执行 `roles.supervision.stage_profiles`、`roles.supervision.stage_bindings`、`roles.supervising.*`、`roles.production.*`、`team_setup.shared_agents` 或 `dispatch_policy: stage-front-advisor|leaf-advisor`。
- 若旧项目已有 `advisor_consultation_packet`、stage profile 或顾问 sidecar，只能作为只读历史证据；不得据此重新调度 team 角色身份或把主 agent 的本地判断伪装成成员回答。
- 阶段本地 review、quality gate、LLM 主创、脚本校验和项目状态回写仍按各阶段 `SKILL.md + CONTEXT.md` 执行，不受本合同削弱。

## Allowed Consumption Shape

创作阶段可把初始化综合映射成一个短上下文块：

```yaml
init_team_synthesis_context:
  project_team_ref: "projects/aigc/<项目名>/team.yaml"
  stage: "2-编导 | 3-运动 | 4-摄影 | 5-分组 | 6-设计"
  synthesis_sources:
    - "team.yaml.init_synthesis.stage_seed_summary.<stage>"
    - "init_handoff.stage_entry_seeds.<stage>"
    - "north_star.yaml.创作阶段不变量.<stage>"
  accepted_constraints: []
  useful_inspirations: []
  risks_to_watch: []
  deferred_or_rejected_points: []
  provenance_notes: []
```

该块只帮助阶段 LLM 主创理解初始化综合，不拥有新的裁决权；最终输出仍由当前阶段合同、上游 canonical truth 与 review gate 裁定。

## Legacy Migration

迁移旧项目或旧技能文本时：

1. 将 `advisor_consultation_packet` 改写为 `init_team_synthesis_context`。
2. 将 `roles.supervision.stage_profiles.<stage>` 改写为 `init_synthesis.stage_seed_summary.<stage>` 或 `init_handoff.stage_entry_seeds.<stage>`。
3. 删除 `stage-front-advisor`、`leaf-advisor`、`review-advisor` 等调度语义，或移入 `legacy_compat.deprecated_fields`。
4. 保留必要的 provenance，但明确它来自初始化问答，不代表阶段重新咨询。
5. 若阶段确需外部评审或质量复核，必须使用该阶段自己的 review/provider 合同，不得借 team 成员身份技能恢复旧顾问流。

## Review Gate Mapping

本共享合同不独立拥有交付 gate；消费者必须把下列问题映射到各自本地 review gate 或 `0-初始化` 的 `FIELD-INIT-04 / FIELD-INIT-07`。

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Did initialization write `team.yaml` as init-only synthesis instead of creative-stage advisor runtime? | `FIELD-INIT-04` | `FAIL-INIT-04` | `0-初始化/references/mode-and-team-contract.md`; `0-初始化/templates/team.yaml` projection via `_shared/council-runtime/team.template.yaml` | Report cites `runtime_policy.team_identity_usage`, `creative_stage_persona_dispatch_allowed`, and absence or legacy marking of stage-runtime fields. |
| Did the creative stage consume only frozen initialization synthesis and avoid re-dispatching team member identities? | Local stage review gate | `FAIL-TEAM-RUNTIME-LEAK` | Current stage `SKILL.md`, templates, and review contract sections that mention team context | Report cites the consumed `init_team_synthesis_context` sources and any removed or blocked persona dispatch path. |
| Were old advisor packets or stage profiles treated as read-only migration evidence rather than active instructions? | Local stage review gate | `FAIL-LEGACY-TEAM-ACTIVE` | Project `team.yaml`, legacy sidecars, and current stage handoff code/text | Report records each legacy field, whether it was ignored, migrated, or explicitly left as provenance. |
