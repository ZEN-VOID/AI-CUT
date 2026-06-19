# AIGC Project Memory Init Context Consumption Contract

本合同替代旧“创作阶段 team advisor consultation”口径。当前 `0-初始化` 是 scaffold-plus-memory：创建当前 `1-分集` 到 `10-画布` 阶段目录、项目根 `MEMORY.md` 与 `CONTEXT/README.md`，不创建项目级 `0-初始化/`，并把初始化时用户指定的团队配置、协作偏好、参考资料吸收摘要、生产限制和下游读取指南直接写入 `MEMORY.md`。

`team.yaml`、旧初始化风格载体、`init_handoff.yaml` 和 `story-source-manifest.yaml` 不是当前初始化必出项。旧项目已有的这些文件只能作为 legacy evidence；新项目和新阶段默认先消费项目 `MEMORY.md`，美学方向默认消费 `2-美学` 输出。

## Active Policy

- 创作阶段必须优先读取 `projects/aigc/<项目名>/MEMORY.md` 中的初始化要求、团队配置与协作偏好、资料吸收摘要、长期偏好、禁区、生产限制和阶段上下文读取指南。
- 项目 `CONTEXT/` 是补充资料侧车；只有当 `MEMORY.md` 指向具体 sidecar 或阶段需要查证原始资料时才继续读取。读取后应在阶段报告中说明该资料如何影响当前阶段决策。
- `MEMORY.md` 中的团队配置是项目上下文，不是创作阶段 advisor runtime；不得调用 team 成员身份技能，不得本地扮演初始化成员，不得补造顾问问答，不得生成新的创作阶段 team advisor packet。
- 若 legacy `team.yaml` 存在，只能作为只读迁移证据；可把其中仍有用的 `init_synthesis.stage_seed_summary.<stage>` 提炼进 `project_memory_init_context.provenance_notes`，但不得覆盖 `MEMORY.md` 中的用户最新要求。
- 创作阶段不得解析或执行 `roles.supervision.stage_profiles`、`roles.supervision.stage_bindings`、`roles.supervising.*`、`roles.production.*`、`team_setup.shared_agents` 或 `dispatch_policy: stage-front-advisor|leaf-advisor`。
- 阶段本地 review、quality gate、LLM 主创、脚本校验和项目状态回写仍按各阶段 `SKILL.md + CONTEXT.md` 执行，不受本合同削弱。

## Allowed Consumption Shape

创作阶段可把项目记忆映射成一个短上下文块：

```yaml
project_memory_init_context:
  project_memory_ref: "projects/aigc/<项目名>/MEMORY.md"
  project_context_refs: []
  stage: "1-分集 | 2-美学 | 3-主体 | 4-编剧 | 5-导演 | 6-分镜 | 7-摄影 | 8-分组 | 9-图像 | 10-画布"
  consumed_memory_sections:
    - "初始化时用户要求"
    - "初始化资料吸收摘要"
    - "团队配置与协作偏好"
    - "阶段上下文读取指南"
  accepted_constraints: []
  useful_inspirations: []
  production_or_model_limits: []
  risks_to_watch: []
  deferred_or_rejected_points: []
  provenance_notes: []
```

该块只帮助阶段 LLM 主创理解初始化上下文，不拥有新的裁决权；最终输出仍由当前阶段合同、上游 canonical truth 与 review gate 裁定。

## Legacy Migration

迁移旧项目或旧技能文本时：

1. 将旧 advisor packet 或旧初始化综合字段改写为 `project_memory_init_context`。
2. 将旧初始化 team/handoff/style carrier 中仍稳定、可复用且未被用户新要求覆盖的内容，压缩为 `MEMORY.md` 的初始化资料吸收摘要、团队配置与协作偏好、阶段上下文读取指南或 provenance note；美学方向不得从旧 carrier 恢复为真源，应转入或对齐 `2-美学` 输出。
3. 删除 `stage-front-advisor`、`leaf-advisor`、`review-advisor` 等调度语义，或移入 legacy 说明。
4. 保留必要 provenance，但明确它来自旧初始化证据，不代表阶段重新咨询。
5. 若阶段确需外部评审或质量复核，必须使用该阶段自己的 review/provider 合同，不得借 team 成员身份技能恢复旧顾问流。

## Review Gate Mapping

本共享合同不独立拥有交付 gate；消费者必须把下列问题映射到各自本地 review gate 或 `0-初始化` 的 `FIELD-INIT-09`。

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does initialization preserve user-specified team/context/reference information in project `MEMORY.md` instead of creating `team.yaml`? | `FIELD-INIT-09` | `FAIL-INIT-09` | `0-初始化/SKILL.md` `N3-memory`; `templates/project-memory.template.md` | Report cites captured memory sections or explicit N/A/deferred reason. |
| Did the creative stage consume project memory as read-only initialization context and avoid re-dispatching team member identities? | Local stage review gate | `FAIL-TEAM-RUNTIME-LEAK` | Current stage `SKILL.md`, templates, and review contract sections that mention project memory context | Report cites `project_memory_init_context` sources and any blocked persona dispatch path. |
| Were old advisor packets, `team.yaml`, or stage profiles treated as read-only migration evidence rather than active instructions? | Local stage review gate | `FAIL-LEGACY-TEAM-ACTIVE` | Project `MEMORY.md`, legacy sidecars, and current stage handoff code/text | Report records each legacy field, whether it was ignored, migrated, or explicitly left as provenance. |
