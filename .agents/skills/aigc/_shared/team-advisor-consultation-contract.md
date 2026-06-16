# AIGC Legacy Init Team Synthesis Consumption Contract

本合同是旧“创作阶段 team advisor consultation”口径的兼容替代。当前 `0-初始化` 是 scaffold-only：只创建当前 0-10 阶段目录和项目根 `MEMORY.md`，不主动生成 `team.yaml`、`north_star.yaml`、`init_handoff.yaml` 或 `story-source-manifest.yaml`。因此本合同只约束旧项目已有、用户显式提供或迁移脚本补建的 legacy/optional team synthesis carrier；它不是当前初始化必出项。

## Active Policy

- `team.yaml` 若存在，只能是初始化配队、成员问答来源、综合摘要和迁移证据，不是创作阶段运行时 roster；缺失时按 `N/A` 处理，不阻塞当前阶段。
- 创作阶段只可读取已经存在的冻结上下文：`team.yaml.init_synthesis.stage_seed_summary.<stage>`，以及显式存在的 legacy `init_handoff.stage_entry_seeds.<stage>`、legacy `north_star.yaml.创作阶段不变量.<stage>` 和必要成员问答 provenance。
- 创作阶段不得调用 team 成员身份技能，不得本地扮演初始化成员，也不得生成新的创作阶段 team advisor packet。
- 创作阶段不得解析或执行 `roles.supervision.stage_profiles`、`roles.supervision.stage_bindings`、`roles.supervising.*`、`roles.production.*`、`team_setup.shared_agents` 或 `dispatch_policy: stage-front-advisor|leaf-advisor`。
- 若旧项目已有 `advisor_consultation_packet`、stage profile 或顾问 sidecar，只能作为只读历史证据；不得据此重新调度 team 角色身份或把主 agent 的本地判断伪装成成员回答。
- 阶段本地 review、quality gate、LLM 主创、脚本校验和项目状态回写仍按各阶段 `SKILL.md + CONTEXT.md` 执行，不受本合同削弱。

## Allowed Consumption Shape

创作阶段可把初始化综合映射成一个短上下文块：

```yaml
init_team_synthesis_context:
  project_team_ref: "projects/aigc/<项目名>/team.yaml"
  stage: "2-美学 | 3-主体 | 4-编剧 | 5-导演 | 6-分镜 | 7-摄影 | 8-分组 | 9-图像 | 10-画布 | archived:5-表演|6-氛围|9-光影"
  synthesis_sources:
    - "team.yaml.init_synthesis.stage_seed_summary.<stage>"
    - "legacy init_handoff.stage_entry_seeds.<stage> if present"
    - "legacy north_star.yaml.创作阶段不变量.<stage> if present"
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
| If a legacy/explicit `team.yaml` exists, is it marked as init-only synthesis instead of creative-stage advisor runtime? | `FIELD-INIT-04` | `FAIL-INIT-04` | `_shared/council-runtime/team.template.yaml` legacy-optional projection | Report cites `runtime_policy.team_identity_usage`, `creative_stage_persona_dispatch_allowed`, and absence or legacy marking of stage-runtime fields. |
| Did the creative stage consume only frozen initialization synthesis and avoid re-dispatching team member identities? | Local stage review gate | `FAIL-TEAM-RUNTIME-LEAK` | Current stage `SKILL.md`, templates, and review contract sections that mention team context | Report cites the consumed `init_team_synthesis_context` sources and any removed or blocked persona dispatch path. |
| Were old advisor packets or stage profiles treated as read-only migration evidence rather than active instructions? | Local stage review gate | `FAIL-LEGACY-TEAM-ACTIVE` | Project `team.yaml`, legacy sidecars, and current stage handoff code/text | Report records each legacy field, whether it was ignored, migrated, or explicitly left as provenance. |
