# Supervised Drafting Review Loop Contract

本合同是 `story2026 / 3-初稿` 三条写作 lane 的共享监制与返工闭环。它只定义调度、证据与回流规则，不替代 `A-GPT原生`、`B-Doubao流`、`C-Deepseek流` 各自的 provider 合同。

## Default Runtime

- 正式写作调用默认启用真实 subagents 监制模式；仓库层已将调用本合同视为对默认 subagent 路径的许可。
- 启动前必须加载当前项目根 `team.yaml`。若 `team.yaml.enabled == true` 且 `roles.production.enabled == true`，`roles.production.members` 是 `3-初稿` 监制组的优先真源；不得绕过项目已锁定 roster 重新从 team 根即兴选人。
- 若 `roles.production.members` 缺失、为空或未覆盖当前 `3-初稿`，才允许按 `team_setup.shared_agents`、`roles.planning.members` 或 `.agents/skills/team/SKILL.md -> Member And Scenario Index` 补位；补位原因必须写入 `supervision_packet.roster_source_note`。
- 启动前必须加载 `.agents/skills/team/SKILL.md + CONTEXT.md`，再只深读 `team.yaml` 已指定或补位选中的 team 成员技能 `SKILL.md + CONTEXT.md`。
- subagent 的具体任务模式不是普通 worker 改稿，而是把项目 `team.yaml` 中业已指定的监制组成员作为资深创作顾问逐一“请教”：主 agent 根据当前章的题材、结构、人物、风格、连续性和风险，为不同领域的大师提出具体类型问题，并要求其输出创意脑洞、个人风格判断和可执行写作指导。
- 若上层 system / developer / tool policy 阻断真实 subagents，才允许降级为本地顺序监制纪要；报告必须说明阻断层级、原计划 subagent 路径、实际降级路径、未启动角色。
- subagents 不拥有正文 canonical truth；它们输出 `supervision_packet`、`execution_notes`、`risk_flags` 或 `repair_brief`，由当前 lane 聚合后交给写作执行层。
- 对 B/C provider lane，subagents 的 `repair_brief` 不是正文修复稿；它必须进入对应 provider 的 prompt/messages，由 provider 产出实际正文修复。除非用户显式切换 lane，否则不得由 GPT/subagents 直接改写 canonical chapter 并继续标记为原 provider 输出。

## Team Supervision Roster

默认 roster 优先来自 `projects/story/<项目名>/team.yaml`：

| source | condition | action |
| --- | --- | --- |
| `roles.production.members` | 存在、启用且成员位于 `.agents/skills/team/` | 作为本章监制组完整候选池，按当前章需要向其中相关成员请教 |
| `team_setup.shared_agents` | production 角色缺失但共享阵容存在 | 作为次级候选池，并记录 production 缺口 |
| `roles.planning.members` | production 与 shared_agents 都不可用，但 planning 已锁定 | 临时复用策划组为监制顾问，并记录复用原因 |
| `team/SKILL.md -> Member And Scenario Index` | 项目 team 真源缺失或成员引用失效 | 动态补位，补位不得改写 `team.yaml` |

从候选池中进入本章请教的最小可执行 roster 为 2 个 subagents：`narrative_supervisor` + `character_or_style_supervisor`。复杂卷、重写、返工或题材跨域时扩展到 3-5 个；若项目 `roles.production.members` 已明确给出更多成员，可按章节需要选择其中最相关者，不要求每章机械全员出动。

当需要动态补位或为已有成员分配问题轴时，按 `team/SKILL.md -> Member And Scenario Index` 映射到以下 slot：

| slot | selection rule | output |
| --- | --- | --- |
| `narrative_supervisor` | 优先选 `story/` 或 `study/文学系/` 中最贴合题材与长篇推进的角色 | 章节推进、读者拉力、章末牵引、类型气口 |
| `structure_supervisor` | 优先选 `aigc/编剧组/` 或能处理结构兑现的角色 | 本章承诺、卷级推进、场景价值转变 |
| `character_supervisor` | 优先选能处理人物声口、关系压力、表演/心理的角色 | 动机、对白、情绪余波、人物弧线 |
| `style_supervisor` | 优先选与风格卡、项目 MEMORY、审美口味匹配的美学/文学/作品维度角色 | 语体、气压、段落呼吸、禁区 |
| `continuity_supervisor` | 可由主 agent 或专门 subagent 承担，重点看上一章、当前卷线索和规划锚点 | 承接、时间、支线去向、未完成动作 |

## Consultation Mode

每个被启动的监制 subagent 必须收到“请教题包”，而不是笼统的“审一下”。题包由主 agent 根据本章 context pack 生成，至少包含：

- `consultation_question`：面向该成员专长的具体问题，例如“本章章末牵引怎样更像武侠章回推进”“这场对峙的价值转变是否成立”“女主此处的自尊与亲情修复怎样不落狗血”。
- `evidence_slice`：只提供回答所需的 planning、角色声纹、上一章承接、项目 MEMORY/CONTEXT 和风险点摘录，不要求成员重读全项目。
- `creative_probe`：允许成员提出风格化脑洞、反套路处理、个人方法论中的高价值偏方。
- `execution_request`：必须把脑洞落成执行指导，包含本章应做、应避免、可转成 prompt 的具体约束。

主 agent 汇流时必须完成三步：

1. 保留各大师的个人风格锋芒，但删除身份扮演痕迹和不可执行感想。
2. 裁决冲突意见，生成单一 `supervision_packet`；不得让多个顾问意见并列夺权。
3. 把最终指导作为正式写作前的额外重要上下文加载到 A/B/C 执行层；正文不得显式提到监制组、subagents 或请教过程。

## Lane-Specific Layering

| lane | supervisor layer | execution layer | hard rule |
| --- | --- | --- | --- |
| `A-GPT原生` | GPT subagents 在隔离上下文中担任监制、审计与修复顾问 | 当前 GPT/LLM 会话生成 canonical draft | 即使同为 GPT，也必须用后台隔离 subagents 保持评估客观性；不得把主写作者自评伪装成独立监制。 |
| `B-Doubao流` | GPT subagents 产出监制包、prompt 约束与返工 brief | Doubao provider 生成或重写正文 | GPT 是监制层，Doubao 是执行层；不得把 GPT 改写正文冒充 Doubao lane。 |
| `C-Deepseek流` | GPT subagents 产出监制包、prompt 约束与返工 brief | DeepSeek provider 生成或重写正文 | GPT 是监制层，DeepSeek 是执行层；不得把 GPT 改写正文冒充 DeepSeek lane。 |

## Supervision Packet

subagents 汇流后必须形成一个面向执行层的 `supervision_packet`。它可以作为脚本参数 `--supervision-packet <path>` 进入 A/B/C 的 messages pack。

```yaml
supervision_packet:
  project_team_ref: "projects/story/<项目名>/team.yaml"
  roster_source_note: ""
  consultation_mode: "ask-senior-creative-advisors"
  roster:
    - slot: narrative_supervisor
      skill_path: ".agents/skills/team/..."
      focus: ""
      source: roles.production.members | team_setup.shared_agents | roles.planning.members | dynamic_team_index
  consultations:
    - member: ""
      skill_path: ".agents/skills/team/..."
      slot: ""
      question_type: narrative | structure | character | style | continuity | genre | repair
      consultation_question: ""
      answer_summary: ""
      executable_guidance:
        - ""
  must_do:
    - ""
  must_not_do:
    - ""
  opening_bridge:
    facts_to_carry: []
    emotional_residue: []
  chapter_obligations:
    structural: []
    character: []
    style: []
    continuity: []
  risk_flags:
    - severity: high | medium | low
      issue: ""
      prevention: ""
  inspiration_to_use:
    - ""
  execution_brief: ""
```

约束：

- `supervision_packet` 只能承载可执行要求，不写 subagent 思维过程。
- 包内意见若与 planning、cards、north_star、项目 MEMORY 冲突，必须回到主 agent 裁决；不得让监制包改写上游 truth。
- `consultations` 必须体现“向谁请教了什么问题、获得什么创意启发、最终落实成什么写作指导”；没有可执行指导的顾问回答不得直接进入 `execution_brief`。
- 执行层必须吸收监制包，但正文 frontmatter 不记录监制角色或路径。

## Writing And Review Loop

1. `N1-N3` 串行锁源、判型、装配上下文。
2. 启动 team supervision subagents，产出 `supervision_packet`。
3. A/B/C 各自执行正文主创或 provider 调用，并把 `supervision_packet` 纳入 prompt / messages。
4. 单章完成只表示 candidate draft 完成；默认不宣称 validated final draft。
5. 当前卷完成后进入 `.agents/skills/story/review` 的 `final_acceptance`，默认卷单位为 10 章，除非项目规划或用户另行指定。
6. `review` 必须启用 `code-reviewer` 作为独立审计 provider，并并发执行 registry 中 `final_acceptance.mandatory = true` 的维度。
7. `PASS` 才可进入 review / 上下文回流；`FAIL-QUALITY` 必须回到原 lane 的 `chapter_rewrite`、`local_repair` 或更大范围重写；`FAIL-COVENANT` 或 source conflict 回到上游 source contract。
8. 返工时必须保留 `original_drafting_lane`。A lane 的正文修复可由 GPT 原生执行；B/C lane 的正文修复必须由 Doubao/DeepSeek provider 执行，GPT/subagents 只负责 issue 分解、repair brief、prompt 约束、复核与父层聚合。

## Rework Routing

| review result | route |
| --- | --- |
| 单章局部失真、声口漂移、承接轻微断带 | 原 lane `local_repair`，携带 review finding 与 `repair_brief` |
| 多处章节共享同一结构/节奏问题 | 原 lane `chapter_rewrite`，按 affected chapters 分批重写 |
| 整卷目标未兑现、主线支线关系错误、卷级结构失败 | 原 lane volume-level rewrite plan，然后逐章执行 `chapter_rewrite` |
| provider evidence 缺失、模型/参数漂移 | 修 provider / script 后同 lane 重跑 |
| cards / planning / north_star 自身冲突 | `back_to_source_contract`，不得让 drafting 背锅 |

BC 返工时 GPT/subagents 只生成 `repair_brief` 与 provider prompt 约束，正文仍由对应外部 LLM 执行。A 返工时仍应把监制 subagents 放在隔离后台上下文中运行，再由主 GPT 写回。

若用户明确要求“启用 subagents 多路修复”，默认解释为多路诊断、拆单、brief 生成、provider 调用协调与复核，而不是授权改变 B/C lane 的正文主创模型。若确需切换为 GPT 直接修复，必须获得用户显式改口，并同步更改 `写作模型` 与 evidence 报告。

## Evidence Requirements

- `supervision_packet` 路径或降级报告。
- 被选 team skill 列表与每个角色的 focus。
- A/B/C messages pack 中包含 `supervision_packet` 摘要或全文。
- provider / GPT-authored draft sidecar。
- 卷级 `review/第V卷.validation.json`，含 `code-reviewer` findings 映射结果。
- 若返工，必须记录原 lane、rework mode、affected chapters 与 source owner。
- B/C 返工必须记录 provider sidecar 或 messages/report；若缺失，不得宣称返工按原 provider lane 完成。
