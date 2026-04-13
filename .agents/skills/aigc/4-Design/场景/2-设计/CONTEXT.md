# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/场景/2-设计` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc -> 4-Design -> 1-场景` 根链之后加载本文件。
- 本技能当前已取消 `references/` 规范载体，也不再依赖 `.codex/agents/aigc/设计组/场景设计/`。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 6281
current_lines: 123
current_cases: 4
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-13T00:25:52-0700
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍从 `3-Detail` 直接发明场景设计 | 输入真源层 | 回退到 `scene catalog -> 2-Global -> optional detail` 的输入顺序 | 在 `SKILL.md` 的 `Total Input Contract` 与 `Field Master` 固化第一输入根 | 不再跳过 `1-清单` |
| 规范内容再次分裂到 `references/*` 或外置场景设计 agent | 真源治理层 | 把流程、节点、判型与 gate 全部收回 `SKILL.md` | 在 `Legacy Migration Mapping` 固化“旧载体已内联并删除” | 技能目录不再残留第二真源 |
| 场景设计只剩风格词，没有空间/建筑/布景实义 | 能力拆解层 | 回到 `D3-D5`，按空间、建筑、布景三条能力链重做 | 在 `Thinking-Action Node Contract` 固化每链的着手面 | 设计卡具备可拍、可搭、可消费细节 |
| review 或 audit 缺位，直接写回 | 汇流门层 | 阻止写回，补跑 `D7-D8` 并按返工入口回退 | 在 `Convergence Contract` 固化双重 gate | `场景设计.json` 总带最小 trace |
| `panel_handoff` 或 `final_scene_prompt` 仍需下游重猜 | 下游接口层 | 回到 `D6` 重新整合 candidate、prompt 与 handoff | 在 `One-Shot Output Contract` 固化下游最小接口 | `3-面板 / 5-Image / 6-Video` 可直接继续消费 |
| 逐场景 Markdown 卡仍沿用旧分块模板，无法承载物语/解构/摄影参数 | 输出合同层 | 将卡片模板改为三段式 Markdown，并在 `SKILL.md` 固化 Markdown 与 JSON 映射 | 把三段式结构与兼容字段同步写进 `One-Shot Output Contract` | `<scene_key>.md` 与 `场景设计.json` 不再脱节 |

## Repair Playbook

1. 先确认问题属于输入真源、能力拆解、聚合收束、review gate、audit gate 还是下游 handoff。
2. 若输入根错，立刻回到 `scene catalog`，停止从导演 JSON 自由发挥。
3. 若内容空泛，优先检查 `D3-D5` 是否被混写或跳步。
4. 若写回异常，优先检查 `D7-D8` 是否被跳过，以及路径是否仍在 `projects/<项目名>/4-Design/场景/2-设计/`。
5. 若发现旧 `references/*` 或 `.codex/agents/aigc/设计组/场景设计/*` 回链，视为源层回退，直接修主合同而不是补兼容文案。

## Reusable Heuristics

- 对场景设计来说，最稳的输入顺序永远是：先对象池，再导演约束，再命中镜头补证据。
- 真正高质量的场景设计不是“多写点形容词”，而是让空间、建筑、布景三条链各自负责不同层面的确定性。
- `review -> audit -> writeback` 不能压成一句“复核通过”；必须显式区分内容复核和真源审计。
- 当用户要求“每个思行节点一步一步足够细”，最有效的做法不是再长角色文档，而是把着手面直接固化进节点 playbook。
- 对“这个场景像什么”不要只给抽象风格词，先判定 `reference_anchor` 是作品场景、现实场所、历史母题，还是只能在题材边界内做 `bounded_extrapolation`。
- “大胆畅想”不能脱离约束单独存在；最稳的写法是先在 `D4` 锁住历史文化和结构边界，再在 `D5` 把想象增量落成具体可见物与标志性元素。
- `templates/scene-design-card.md` 可以保留，因为它是落盘模板；但凡字段主表、workflow、判型或 output contract 跑到别的文档里，第二真源就会重新长出来。
- 当用户要求场景卡改成三段式时，不能只改 Markdown 皮相；必须同步补进节点合同，让 `物语 / 解构 / prompt整合` 都有明确生成责任。

## Case Log

### Case-20260412-AIGC-SCENE-DESIGN-SINGLE-SOURCE-ELEVATION

- milestone_type: source_contract_change
- outcome: 将 `4-Design/场景/2-设计` 从“`SKILL.md + references/* + 外置场景设计组`”重构为“知行合一单技能真源”。
- root_cause_or_design_decision: 用户明确要求“内容和机制上全量参照现有配置，但根据知行合一的规范进行编排”，并指定 `复杂链路的骨架 / 细则分层=false`，同时废弃 `.codex/agents/aigc/设计组/场景设计`。旧结构把核心规则分散在 `SKILL.md`、四份 `references` 和六个 agent 文档中，已形成平行真源。
- final_fix_or_heuristic: 将六个角色能力面、四份 references 的规范内容、并发拓扑、变量判型、输出骨架与双重 gate 全部并入同一 `SKILL.md`，只保留 `templates/scene-design-card.md` 作为落盘模板。
- prevention_or_replication_checklist:
  - [x] `references/*` 规范内容已内联到 `SKILL.md`
  - [x] 场景设计组旧 agent 真源已删除
  - [x] `CONTEXT.md` 已改为只保留经验层
  - [x] `agents/openai.yaml` 已改为单技能口径
- evidence_paths:
  - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/CHANGELOG.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/agents/openai.yaml`
- user_feedback_or_constraint: 用户要求“每一个思维·执行节点从哪些方面着手，一步一步要足够细致，确保高品质”。

### Case-20260412-AIGC-SCENE-DESIGN-NODE-DETAIL-HARDENING

- milestone_type: source_contract_change
- outcome: 为场景设计的每个关键思行节点补齐了细化着手面、返工条件与最小证据位。
- root_cause_or_design_decision: 仅有“设计统筹 -> 三 specialist -> review/audit”的粗拓扑还不足以保证高质量；如果不把每个节点从哪些方面着手写细，执行者很容易回到抽象文案或经验性跳步。
- final_fix_or_heuristic: 在 `Thinking-Action Node Contract` 中把 `D0-D8` 分别拆为清晰的观察面、决策面、动作面与 gate。
- prevention_or_replication_checklist:
  - [x] 每个节点都具备 `objective / actions / evidence / route_out / gate`
  - [x] `D3-D5` 已写明具体着手维度
  - [x] `D7-D8` 已区分内容复核与真源审计
- evidence_paths:
  - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“每一个思维·执行节点从哪些方面着手，一步一步要足够细致”。

### Case-20260412-AIGC-SCENE-DESIGN-REFERENCE-ICONIC-HARDENING

- milestone_type: source_contract_change
- outcome: 将“作品参照、想象外扩、历史文化框架、标志性元素”固化进场景设计思行节点，而不是留给执行者临场发挥。
- root_cause_or_design_decision: 用户要求补入“这个场景参照哪部作品的哪个场景、或大胆畅想时应该是什么样子、是否需要服从既定历史文化框架、标志性元素是什么”等判断维度；若这些问题只写成补充提示，执行时会再次漂移成抽象灵感，而不能稳定落到结构和布景字段。
- final_fix_or_heuristic: 将四类判断拆解并嵌入 `D2 -> D4 -> D5 -> D6`：`D2` 建立参照锚点和想象模式判型，`D4` 落历史文化与结构边界，`D5` 落标志性元素和可见想象增量，`D6` 检查 candidate 是否形成完整闭环。
- prevention_or_replication_checklist:
  - [x] `D2` 已显式识别 `reference_anchor / reference_mode / iconic_elements_seed`
  - [x] `D4` 已要求写清参照对象、可借鉴点、不应照搬点与文化边界
  - [x] `D5` 已要求把标志性元素落成可见陈设而不是抽象形容词
  - [x] `D6` 已要求检查 `reference_anchor -> boundary -> iconic cluster -> prompt` 闭环
- evidence_paths:
  - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求把“参照作品/场景、大胆畅想、历史文化框架、标志性元素”作为思维·执行节点的内生判断维度，而不是附加提示。

### Case-20260413-AIGC-SCENE-DESIGN-THREE-PART-MARKDOWN-PROMOTION

- milestone_type: source_contract_change
- outcome: 将逐场景设计卡升级为 `物语 -> 解构 -> prompt整合` 三段式 Markdown，并把空间原型、参照转写、人文痕迹、摄影设计回写进节点合同。
- root_cause_or_design_decision: 用户要求直接重定义输出模板，同时补充一组更严格的思维·执行节点判题信号；如果只改模板，不同步更新 `D1-D6` 的责任字段和 JSON 兼容映射，执行链会继续按旧字段工作，导致 Markdown 新壳与 JSON 旧真源脱节。
- final_fix_or_heuristic: 在 `templates/scene-design-card.md` 切换到三段式模板；在 `SKILL.md` 中同步补齐三段式输出合同、Markdown/JSON 兼容映射、以及“本轮覆盖、原型去泛化、参照转写、空间可画可拍可生成”的节点门槛。
- prevention_or_replication_checklist:
  - [x] 模板已切换为三段式 Markdown
  - [x] `SKILL.md` 已固化 `prompt_integration -> final_scene_prompt` 兼容映射
  - [x] `D1-D6` 已补入逐场覆盖、原型去泛化、参照转写与空间可生成判题
  - [x] `CONTEXT.md` 已记录本次输出合同升级
- evidence_paths:
  - `.agents/skills/aigc/4-Design/场景/2-设计/templates/scene-design-card.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“按照三段式 Markdown 重新定义输出内容模板”，并追加“本轮有哪些场景、原型是否泛化、参照如何转写、空间是否可画可拍可生成”等节点判题信号。
