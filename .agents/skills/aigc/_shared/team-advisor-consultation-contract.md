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

| stage | preferred advisor focus | question source |
| --- | --- | --- |
| `2-编导` | 监制、导演、编剧、表演、摄影或类型顾问 | 从当前 `2-编导` 的 `Thought Pass Map`、`steps/directing-workflow.md` 节点、`director_substance_plan`、review gate、目标集上下文和当前 `type_profile` 派生；顾问需代入角色意识、创作风格和专业水准参与节点判断、执行取舍、证据补强、回修建议与风险提示 |
| `3-摄影` | 摄影、导演、美术、剪辑、类型视觉顾问 | 从当前 `3-摄影` 的 `Thought Pass Map`、`steps/cinematography-workflow.md` 节点、review gate、目标集上下文和当前 `visual_unit` 派生；顾问需代入角色意识、创作风格和专业水准参与节点判断、执行取舍与风险提示 |
| `5-设计/角色/2-设计` | 角色、服装、美术、摄影、导演、类型顾问 | 从当前 `steps/character-design-workflow.md` 的 `node_id`、`N5-RESEARCH-PROFILE`、`N6-SUBAGENT-DISPATCH`、`N7-MERGE-DRAFT`、`N8-REVIEW-GATE`、目标角色上下文和 review gate 派生；顾问需代入其角色意识、创作风格和专业水准参与节点判断、执行取舍、局部 patch 与风险提示 |
| `5-设计/道具/2-设计` | 道具、美术、摄影、导演、世界观或工艺顾问 | 从当前 `steps/prop-design-workflow.md` 的 `node_id`、`N5-RESEARCH-CHAIN`、`N6-DESIGN`、`N7-REVIEW`、目标道具上下文和 review gate 派生；顾问需代入其角色意识、创作风格和专业水准参与节点判断、执行取舍、局部 patch 与风险提示 |
| `5-设计/场景/2-设计` | 场景、美术、建筑、摄影、导演、类型顾问 | 从当前 `steps/scene-design-workflow.md` 的 `node_id`、`N5-RESEARCH`、`N6-DESIGN`、`N7-REVIEW`、目标场景上下文和 review gate 派生；顾问需代入其角色意识、创作风格和专业水准参与节点判断、执行取舍、局部 patch 与风险提示 |
| `8-审片` | 监制、导演、摄影、美术、剪辑、类型视觉或质量顾问 | 从当前 `8-审片` 的 `Thought Pass Map`、`steps/video-review-workflow.md` 节点、真实视频证据包、`observed_content_summary`、prompt 匹配、创作质量、好/坏示例校准和 review gate 派生；顾问需代入角色意识、创作风格和专业水准参与证据补强、错配归因、审美质量门、rerun / repair / source escalation 落点风险判断 |

若项目 team 成员以通用大师人格或作品维度声明，主 agent 必须把问题改写成该阶段当前思维·执行节点可回答的具体问题，例如“在 `N6-DESIGN` 中，这个空间的叙事压力应怎样转成可见材质、动线和镜头边界”，而不是让顾问泛泛评价。对于声明了节点网络的技能，顾问问题必须绑定当前 `node_id / pass_id / gate_id` 或等价执行位置，不得退化为固定字段清单。

参谋不是字段填充器。参谋执行时必须先锁定当前技能包自己的思维·执行节点，再代入 `team.yaml` 所声明成员的角色意识、创作风格、审美判断和专业水准，对该节点应如何判断、如何执行、如何取舍、哪些风险会破坏交付提出意见。输出仍必须被主 agent 收束为可执行指导、局部 patch、risk note 或 reviewer finding，不保留冗长人格扮演文本，也不得越过当前 `SKILL.md` 的 canonical truth 和输出门禁。

## Consultation Packet

每次启用本合同时，创作前必须形成内部或 sidecar 级 `advisor_consultation_packet`，作为额外重要上下文供 LLM 主创消费：

```yaml
advisor_consultation_packet:
  project_team_ref: "projects/aigc/<项目名>/team.yaml"
  stage: "2-编导 | 3-摄影 | 5-设计/角色/2-设计 | 5-设计/道具/2-设计 | 5-设计/场景/2-设计 | 8-审片"
  roster_source_note: ""
  consultation_mode: "ask-team-advisors-for-executable-stage-guidance"
  roster:
    - name: ""
      skill_path: ""
      source: "roles.supervision.members | roles.supervising.members | roles.supervising.members_ref | team_setup.shared_agents | roles.planning.members | dynamic_team_index"
      selected_for: ""
  consultations:
    - member: ""
      node_ref: ""
      pass_ref: ""
      gate_ref: ""
      role_lens: ""
      question_type: "<stage-node-or-review-gate-derived>"
      consultation_question: ""
      answer_summary: ""
      executable_guidance:
        - ""
      risk_flags:
        - ""
      routeback_targets:
        - node_ref: ""
          reason: ""
  must_do:
    - ""
  must_not_do:
    - ""
  inspiration_to_use:
    - ""
  execution_brief: ""
  downgrade:
    blocked_by: "system | developer | tool | user | none"
    planned_path: ""
    actual_path: ""
    skipped_members: []
```

`execution_brief` 必须是可直接指导创作的短指令集合，不得保留冗长思维过程、人格扮演文本或不可执行的赞美词。

`routeback_targets` 只记录需要回到当前阶段已声明节点网络重做判断或证据的目标；主 agent 必须按当前阶段 `steps/` 的失败回路执行回修，不得把前置节点错误仅作为灵感继续下游。若真实 subagent dispatch 被阻断，`downgrade` 必须记录阻断层级、原计划路径、实际路径和未启动成员。

## Merge Rules

- 顾问意见必须先被主 agent 合成、去重、裁决，再作为主创上下文进入阶段 LLM 写作。
- 顾问灵感可以激发风格、脑洞、质感、取舍和风险意识，但不得改写上游剧情事实、清单主体、固定画面约束、提示词长度门禁或 LLM-first 主创规则。
- 当顾问意见互相冲突，优先级为：用户显式请求 > AGENTS.md / meta 规则 > 当前阶段 `SKILL.md` > 上游 canonical truth > 顾问意见。
- 最终交付正文默认不显式列出顾问名字；执行报告或降级报告可以记录 roster、节点锚点、角色视角和采纳摘要。
