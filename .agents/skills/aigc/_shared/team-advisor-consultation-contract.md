# AIGC Team Advisor Consultation Contract

本合同定义 AIGC 创作阶段在技能合同显式要求启用 subagents 时，如何调用项目 `team.yaml` 已指定的监制组成员作为资深创作顾问进行“请教”，并把所得创意脑洞、个人风格启发和风险提示汇流为创作前可执行指导。它不替代阶段主技能的 canonical truth、输出模板、review gate 或最终写回权。

## Activation

- 当阶段或叶子技能声明 `use_subagents_by_default`、默认真实 subagents、`reviewer -> subagent`、`parallel-council`、`serial-refine` 或等价语义时，必须优先按本合同执行团队顾问请教。
- 主 agent 负责路由、提问、汇流、裁决和最终 canonical 写回；team advisor subagents 只提供顾问意见、可执行指导、risk note 或局部 patch，不直接拥有最终正文。
- 若 system / developer / tool / user 任一上层策略阻断真实 dispatch，必须输出降级报告，写明阻断层级、原计划顾问路径、实际降级路径和未真实启动的成员。

## Team Roster Resolution

项目运行时必须先读取 `projects/aigc/<项目名>/team.yaml`，再按以下优先级解析顾问 roster：

1. `roles.supervision.members`
2. `roles.supervising.members`
3. `roles.supervising.members_ref` 指向的成员列表，例如 `roles.planning.members`
4. `team_setup.shared_agents`
5. `roles.planning.members`
6. 若项目 `team.yaml` 缺失、结构不合法或没有可解析成员，可按 `.agents/skills/team/SKILL.md` 动态补位，但必须报告 `roster_source_note`，不得伪装成项目已指定成员。

解析出候选成员后，必须加载 `.agents/skills/team/SKILL.md + CONTEXT.md`，再只加载被选中成员的 `SKILL.md + CONTEXT.md`。不得批量加载全部 team 子树。

## Advisor Selection

按阶段目标选择顾问，而不是机械全员询问：

| stage | preferred advisor focus | question types |
| --- | --- | --- |
| `2-编导` | 监制、导演、编剧、表演、摄影或类型顾问 | 结构投影、场景目的、表演任务、声画承托、高潮兑现、保真风险 |
| `3-摄影` | 摄影、导演、美术、剪辑、类型视觉顾问 | 镜头连续性、节拍密度、运镜、光影、色彩、峰值镜头、转场动机 |
| `5-设计/角色/2-设计` | 角色、服装、美术、摄影、导演、类型顾问 | 身份压力、身体姿态、服装材质、定妆照拍法、prompt evidence、禁区 |
| `5-设计/道具/2-设计` | 道具、美术、摄影、导演、世界观或工艺顾问 | 形制、材料、工艺、年代、磨损、功能逻辑、45 度特写、prompt token |
| `5-设计/场景/2-设计` | 场景、美术、建筑、摄影、导演、类型顾问 | 空间结构、建筑/地理依据、材质光线、空镜构图、no people、prompt evidence |

若项目 team 成员以通用大师人格或作品维度声明，主 agent 必须把问题改写成该阶段可回答的具体问题，例如“这个空间该如何把叙事压力变成可见材质和动线”，而不是让顾问泛泛评价。

## Consultation Packet

每次启用本合同时，创作前必须形成内部或 sidecar 级 `advisor_consultation_packet`，作为额外重要上下文供 LLM 主创消费：

```yaml
advisor_consultation_packet:
  project_team_ref: "projects/aigc/<项目名>/team.yaml"
  stage: "2-编导 | 3-摄影 | 5-设计/角色/2-设计 | 5-设计/道具/2-设计 | 5-设计/场景/2-设计"
  roster_source_note: ""
  consultation_mode: "ask-team-advisors-for-executable-stage-guidance"
  roster:
    - name: ""
      skill_path: ""
      source: "roles.supervision.members | roles.supervising.members | roles.supervising.members_ref | team_setup.shared_agents | roles.planning.members | dynamic_team_index"
      selected_for: ""
  consultations:
    - member: ""
      question_type: "structure | performance | cinematography | costume | prop | space | prompt | continuity | review"
      consultation_question: ""
      answer_summary: ""
      executable_guidance:
        - ""
      risk_flags:
        - ""
  must_do:
    - ""
  must_not_do:
    - ""
  inspiration_to_use:
    - ""
  execution_brief: ""
```

`execution_brief` 必须是可直接指导创作的短指令集合，不得保留冗长思维过程、人格扮演文本或不可执行的赞美词。

## Merge Rules

- 顾问意见必须先被主 agent 合成、去重、裁决，再作为主创上下文进入阶段 LLM 写作。
- 顾问灵感可以激发风格、脑洞、质感、取舍和风险意识，但不得改写上游剧情事实、清单主体、固定画面约束、提示词长度门禁或 LLM-first 主创规则。
- 当顾问意见互相冲突，优先级为：用户显式请求 > AGENTS.md / meta 规则 > 当前阶段 `SKILL.md` > 上游 canonical truth > 顾问意见。
- 最终交付正文默认不显式列出顾问名字；执行报告或降级报告可以记录 roster、问题类型和采纳摘要。
