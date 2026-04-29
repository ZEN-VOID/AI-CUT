# Story Team Advisor Consultation Contract

本合同定义 `story2026` 的设定与规划阶段在显式要求启用 subagents 时，如何调用项目 `team.yaml` 已指定的策划/监制成员作为资深创作顾问进行“请教”，并把创意脑洞、个人风格判断和风险提示汇流为创作前可执行指导。它不替代 `1-设定` cards 真源、`2-卷章` planning 真源、父子技能输出合同或 review gate。

## Activation

- 当 `1-设定`、`2-卷章` 或其子技能声明默认真实 subagents、`requires_subagents`、`reviewer -> subagent`、`parallel-council`、`direct-answer-packet` 或等价语义时，必须优先按本合同执行团队顾问请教。
- 主 agent 负责路由、提问、汇流、裁决和最终 canonical 写回；team advisor subagents 只提供顾问意见、可执行指导、risk note 或局部 patch，不直接拥有最终 card / planning 正文。
- 若 system / developer / tool / user 任一上层策略阻断真实 dispatch，必须输出降级报告，写明阻断层级、原计划顾问路径、实际降级路径和未真实启动的成员。

## Team Roster Resolution

项目运行时必须先读取 `projects/story/<项目名>/team.yaml`，再按以下优先级解析顾问 roster：

1. `roles.planning.members`：`1-设定` 与 `2-卷章` 的优先真源。
2. `team_setup.shared_agents`：planning 角色缺失或不可用时的共享阵容。
3. `roles.production.members`：planning 与 shared_agents 不可用时的临时复用；必须记录复用原因。
4. `roles.review.members`：仅在 review / repair 任务需要审查视角且前三者不可用时使用。
5. `.agents/skills/team/SKILL.md -> Member And Scenario Index`：项目 team 真源缺失或成员引用失效时动态补位；补位不得改写 `team.yaml`。

启动前必须加载 `.agents/skills/team/SKILL.md + CONTEXT.md`，再只加载被选中成员的 `SKILL.md + CONTEXT.md`。不得批量加载全部 team 子树。

## Stage Question Profiles

| stage | advisor focus | question types |
| --- | --- | --- |
| `1-设定/角色卡` | 人物、关系、成长、类型、风格顾问 | 角色职责、伤口/欲望/成长、关系载体、记忆点、专属物接口、反派镜像 |
| `1-设定/场景卡` | 世界规则、空间、美学、类型、导演顾问 | 场景功能、规则代价、危险机制、可返场价值、适配角色、复用策略 |
| `1-设定/物品卡` | 道具、线索、叙事杠杆、类型、角色顾问 | 归属链、启用规则、代价、专属适配、线索功能、不可替代性 |
| `1-设定/技能卡` | 能力系统、世界规则、动作/战术、成长顾问 | 启用条件、限制代价、成长路径、克制关系、失败方式、题材语义 |
| `2-卷章/1-部级` | 长篇结构、类型承诺、主题、悬念、节奏顾问 | 整书承诺、卷划分、主任务树、悬念池、时间线、长波节奏、禁飞区 |
| `2-卷章/2-卷级` | 中观结构、章功能、任务线、悬念、资源顾问 | 卷职责、章划分、六拍配器、悬念负载、资源投影、卷末兑现 |
| `2-卷章/3-章级` | 章级结构、爽点、悬念、角色逻辑、连续性顾问 | 本章职责、时间推进、爽点变奏、悬念开关、任务汇聚、drafting handoff |

每个被启动的顾问 subagent 必须收到面向其专长的“请教题包”，而不是笼统的“审一下”。问题应当要求顾问把个人风格启发落成可执行指导，例如“这个角色关系如何变成可写戏的载体”“本卷悬念负载怎样避免提前泄底”“本章爽点怎样像该类型而不串味”。

## Advisor Packet

每次启用本合同时，创作前必须形成内部或 sidecar 级 `advisor_consultation_packet`，作为额外重要上下文供 LLM 主创消费：

```yaml
advisor_consultation_packet:
  project_team_ref: "projects/story/<项目名>/team.yaml"
  stage: "1-设定/角色卡 | 1-设定/场景卡 | 1-设定/物品卡 | 1-设定/技能卡 | 2-卷章/1-部级 | 2-卷章/2-卷级 | 2-卷章/3-章级"
  roster_source_note: ""
  consultation_mode: "ask-team-advisors-for-executable-story-guidance"
  roster:
    - name: ""
      skill_path: ".agents/skills/team/..."
      source: "roles.planning.members | team_setup.shared_agents | roles.production.members | roles.review.members | dynamic_team_index"
      selected_for: ""
  consultations:
    - member: ""
      skill_path: ".agents/skills/team/..."
      question_type: "character | scene | item | skill | book_structure | volume_structure | chapter_structure | rhythm | suspense | continuity | style | review"
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

`execution_brief` 必须是可直接指导 cards 或 planning 创作的短指令集合，不得保留冗长思维过程、人格扮演文本或不可执行的赞美词。

## Merge Rules

- 顾问意见必须先由主 agent 合成、去重、裁决，再作为创作前上下文进入对应子技能 LLM 主创。
- 顾问灵感可以激发风格、脑洞、结构取舍和风险意识，但不得改写 `north_star.yaml`、项目 `MEMORY.md`、既有 cards、上层 planning、固定输出路径或 LLM-first 主创规则。
- 当顾问意见互相冲突，优先级为：用户显式请求 > AGENTS.md / meta 规则 > 当前阶段 `SKILL.md` > 上游 canonical truth > 顾问意见。
- 最终 card / planning 正文默认不显式列出顾问名字；执行报告或降级报告可以记录 roster、问题类型和采纳摘要。
