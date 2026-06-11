# Supervised Drafting Acceptance Loop Contract

本合同是 `story2026 / 3-初稿` 根技能的共享监制与返工闭环。它只定义监制调度、证据与回流规则，不替代 `3-初稿/SKILL.md` 的章节主创合同。

## Default Runtime

- 正式写作调用默认启用真实 subagents 监制模式；仓库层已将调用本合同视为对默认 subagent 路径的许可。
- 启动前必须加载当前项目根 `team.yaml`。若 `team.yaml.enabled == true` 且 `roles.production.enabled == true`，`roles.production.members` 是 `3-初稿` 监制组的优先真源；不得绕过项目已锁定 roster 重新从 team 根即兴选人。
- 若 `roles.production.members` 缺失、为空或未覆盖当前 `3-初稿`，才允许按 `team_setup.shared_agents`、`roles.planning.members` 或 `.agents/skills/team/SKILL.md -> Member And Scenario Index` 补位；补位原因必须写入 `supervision_packet.roster_source_note`。
- 启动前必须加载 `.agents/skills/team/SKILL.md + CONTEXT.md`，再只深读 `team.yaml` 已指定或补位选中的 team 成员技能 `SKILL.md + CONTEXT.md`。
- subagent 的任务模式是把项目 `team.yaml` 中指定的监制组成员作为资深创作顾问逐一“请教”；主 agent 根据当前章题材、结构、人物、风格、连续性和风险，为不同领域成员提出具体问题，并要求输出创意脑洞、个人风格判断和可执行写作指导。
- 若上层 system / developer / tool policy 阻断真实 subagents，才允许降级为本地顺序监制纪要；报告必须说明阻断层级、原计划 subagent 路径、实际降级路径和未启动角色。
- subagents 不拥有正文 canonical truth；它们输出 `supervision_packet`、`execution_notes`、`risk_flags` 或 `repair_brief`，由 `3-初稿` 根技能吸收后进入 LLM-first 主创或返工节点。
- `repair_brief` 不是正文修复稿；正文创作性改写必须回到 `3-初稿` 根技能，不得由 subagents 直接改写 canonical chapter 并宣称完成。

## Team Supervision Roster

默认 roster 优先来自 `projects/story/<项目名>/team.yaml`：

| source | condition | action |
| --- | --- | --- |
| `roles.production.members` | 存在、启用且成员位于 `.agents/skills/team/` | 作为本章监制组完整候选池，按当前章需要向其中相关成员请教 |
| `team_setup.shared_agents` | production 角色缺失但共享阵容存在 | 作为次级候选池，并记录 production 缺口 |
| `roles.planning.members` | production 与 shared_agents 都不可用，但 planning 已锁定 | 临时复用策划组为监制顾问，并记录复用原因 |
| `team/SKILL.md -> Member And Scenario Index` | 项目 team 真源缺失或成员引用失效 | 动态补位，补位不得改写 `team.yaml` |

从候选池中进入本章请教的最小可执行 roster 为 2 个 subagents：`narrative_supervisor` + `character_or_style_supervisor`。复杂卷、重写、返工或题材跨域时扩展到 3-5 个；若项目 `roles.production.members` 已明确给出更多成员，可按章节需要选择其中最相关者，不要求每章机械全员出动。

## Consultation Mode

每个被启动的监制 subagent 必须收到“请教题包”，而不是笼统的“审一下”。题包至少包含：

- `consultation_question`：面向该成员专长的具体问题。
- `evidence_slice`：只提供回答所需的 planning、角色声纹、同卷前文承接、项目 MEMORY/CONTEXT 和风险点摘录。
- `creative_probe`：允许成员提出风格化脑洞、反套路处理和高价值偏方。
- `execution_request`：必须把脑洞落成执行指导，包含本章应做、应避免和可转成 prompt 的具体约束。

主 agent 汇流时必须完成三步：

1. 保留各顾问的高价值判断，但删除身份扮演痕迹和不可执行感想。
2. 裁决冲突意见，生成单一 `supervision_packet`。
3. 把最终指导作为正式写作前的额外重要上下文交给 `3-初稿` 根技能；正文不得显式提到监制组、subagents 或请教过程。

## Supervision Packet

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
- `consultations` 必须体现“向谁请教了什么问题、获得什么创意启发、最终落实成什么写作指导”。
- 执行层必须吸收监制包，但正文 frontmatter 不记录监制角色或路径。

## Writing And Acceptance Loop

1. `3-初稿` 根技能串行锁源、判型、装配上下文。
2. 启动 team supervision subagents，产出 `supervision_packet`。
3. `3-初稿` 根技能吸收 `supervision_packet` 并执行 LLM-first 正文主创。
4. 单章完成只表示 candidate draft 完成；默认不宣称 validated final draft。
5. 当前章或当前卷完成后，由 `3-初稿` 根技能自动执行 `N6-AUTO-ACCEPTANCE`，并写出 `3-初稿/第N卷/第N章.acceptance.json` 或卷级汇总中的 `stage_acceptance_packet`。
6. `3-初稿` 内置验收覆盖 source context、结构兑现、连续性、逻辑自洽、人物一致性、时间线、任务汇聚、初稿读感和输出状态；如启用 `code-reviewer`，其 findings 只能作为辅助证据回流到本阶段验收包。
7. 初稿 `PASS` 只允许交给 `4-润色`，不得直接交 `return`；`FAIL-QUALITY` 必须回到 `3-初稿` 根技能的 `local_repair`、`chapter_rewrite` 或更大范围重写；`FAIL-COVENANT` 或 source conflict 回到上游 source contract。

## Rework Routing

| acceptance result | route |
| --- | --- |
| 单章局部失真、声口漂移、承接轻微断带 | `3-初稿` 根技能 `local_repair`，携带 acceptance finding 与 `repair_brief` |
| 多处章节共享同一结构/节奏问题 | `3-初稿` 根技能 `chapter_rewrite`，按 affected chapters 分批重写 |
| 整卷目标未兑现、主线支线关系错误、卷级结构失败 | volume-level rewrite plan，然后逐章执行 `chapter_rewrite` |
| 脚本/模板试图主创正文 | 回到 LLM-first authorship gate，废弃机械正文 |
| cards / planning / north_star 自身冲突 | `back_to_source_contract`，不得让 drafting 背锅 |

若用户明确要求“启用 subagents 多路修复”，默认解释为多路诊断、拆单、brief 生成与复核，而不是授权改变正文主创边界。正文最终仍必须由 `3-初稿` 根技能执行。

## Evidence Requirements

- `supervision_packet` 路径或降级报告。
- 被选 team skill 列表与每个角色的 focus。
- 监制包摘要进入 `3-初稿` 的创作上下文。
- candidate draft path。
- `3-初稿/第N卷/第N章.acceptance.json` 或卷级汇总 `stage_acceptance_packet`，含内置验收维度结论与辅助 findings 映射结果。
- 若返工，必须记录 owning stage、rework mode、affected chapters 与 source owner。
