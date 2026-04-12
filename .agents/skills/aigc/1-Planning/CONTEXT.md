# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 规划组 team 指向不存在的父 skill | 路由锚点层 | 补齐 `1-Planning/SKILL.md` 并同步 team 回指 | 将阶段父级锚点视为规划组可执行前置，不再只保留 agent 投影 | `team.md` 与 registry 能回到真实父 skill |
| 可直接命中的规划 skill 已有执行合同但缺少 `agents/openai.yaml` | 入口元数据层 | 补齐对应 skill 的 `agents/openai.yaml` | 把“可直接命中的规划 skill 必须同时具备 `SKILL.md + CONTEXT.md + agents/openai.yaml`”视为规划阶段入口基线 | 规划 skill 可被 Codex 正常发现并按入口摘要触发 |
| `1-分集` 与 `2-剧本` 的真源边界混写 | 输出治理层 | 收回 `1-分集` 到逐集原文真源，保留 `2-剧本` 为唯一逐集主稿 | 在 `_shared/IO_CONTRACT.md` 固化“1-分集原文真源 -> 2-剧本主稿”两层结构 | 同一集不再由上游 leaf 直接覆盖主稿 |
| `2-剧本` 被拆成两个本地子技能包 | 子技能治理层 | 收敛回单一 `2-剧本` 技能包，由 `标准剧 / 解说剧` subagents 触发 | 在 `2-剧本/SKILL.md` 固化“单包 + subagent 变体” | 本地目录下不再出现伪 sibling 技能真源 |
| `3-分组` 缺少本地真源，导致下游只能依赖 agent 投影 | leaf 合同层 | 补齐 `3-分组/SKILL.md + manifest + validator` | 在父 skill 与 shared I/O 固化 `3-分组/第N集.md + 执行报告.md` | `2-Global` 与 `节奏` 能回指真实文件 |
| `3-分组` 混用 `分镜组ID` 和 `分镜ID` | ID 语义层 | 把正文标题改回三段式 `分镜组ID` | 在 `3-分组`、父 skill 与 `2-Global` 同步固化“组三级、镜四级” | 下游不再把组标题当帧级 ID |
| `3-分组` 只靠直觉分段，量化浮动过大 | 量化合同层 | 回到场景顺序与时长策略投影重新切组 | 在 `3-分组` 的 reference、validator 与执行报告固化字窗门槛 | `effective_text_chars` 超硬上限时不会继续通过 |
| 故事正文输入根被写模糊 | 共享输入层 | 强制先锁定 `projects/<项目名>/Story/` | 在 `_shared/IO_CONTRACT.md` 固化故事目录优先、manifest 作为索引证据 | 输入范围不再漂移 |
| 单一 `1-分集` 角色仍被挂成规划组 subagent | 结构治理层 | 把 `1-分集` 收回 direct leaf skill，删除孤立 agent 文档 | 在父 skill、team、audit 与入口元数据中固化“单角色 leaf 不走 team/subagent 模式” | `1-分集` 不再依赖 `.codex/agents/aigc/规划组/分集.md` |
| 规划组角色越权写回 | 编排边界层 | 收回 `1-Planning/2-剧本/第N集.md` 写回权到父 skill | 在 team 与父 skill 固化 `agents_plan + patch / note / report` | agent 不再宣告阶段完成 |
| subagents 的思考/plan 与 skill 的执行闭环分工不清 | 执行治理层 | 收回 canonical 落盘、validator 与阶段收束到 skill | 在父 skill 与 completed leaves 固化“subagents 负责思考和 plan，skill 负责统筹和执行” | 规划组投影不再越权成并列执行面 |
| 把 planning subagent 的 thinking sidecar 当成硬门槛 | 子代理合同层 | 取消强制 thinking sidecar，改为 subagent 返回 `agents plan` | 在父 skill、leaf skills 与规划组 team 中统一“agents 思考计划，skills 执行落盘”的合同 | planning 闭环不再被可选证据文件阻塞 |
| 规划组 agent 只有“职责/输入/输出/禁令”，角色可识别但执行仍易漂移 | agent 合同层 | 给 team 与各角色补齐 `Goal / Done Criteria / Workflow / Fallback / Quality Check` | 将 planning agents 视为可执行提示合同，而不是静态岗位说明；对格式变体与节奏类角色额外固化主变体/重排护栏 | 相同输入下的角色判定、停止条件和 handoff 更稳定，父 skill 不再反复猜 agent 意图 |
| `规划组/team.md` 与某个 stage skill 同时持有同一段局部拓扑 | canonical source 治理层 | 把 stage-local topology 收回具体 stage skill，让 team 只保留 shared dispatch plane 与 handoff matrix | 在父 skill、stage skill 与 team 文档同步写明 stage-local ownership | 不再把 team 文档误读成局部第二父合同 |
| `3-分组` 的量化规则只写在 reference，计算仍停留在手填 | 计算真源层 | 为 `3-分组` 增加 quantizer，并让 validator 直接消费计算结果 | 让“方法论 digest + quantizer + validator”形成闭环，而不是“reference + 手填解释” | 分组量化字段可复算、可核对、可回归 |

## Repair Playbook

1. 先检查 `1-Planning/SKILL.md` 是否还能清楚解释整条链路：`Story/ -> 1-分集 -> 2-剧本 -> 3-分组`。
2. 再检查 `_shared/IO_CONTRACT.md` 是否仍把 `1-分集/第N集.md` 和 `2-剧本/第N集.md` 分成两层真源。
3. 再检查 `projects/<项目名>/Story/` 是否仍是默认输入根，以及 `2-剧本` 是否仍是单技能包。
4. 最后才看局部 leaf 输出是否需要返工。

## Reusable Heuristics

- 对规划阶段来说，最容易坏的不是 leaf 本身，而是“输入根和主稿路径没有锁死”。
- `1-分集` 的最稳职责是从 `projects/<项目名>/Story/` 收束出 `1-分集/第N集.md` 与 `source_profile` handoff，而不是直接覆盖 `2-剧本` 主稿。
- `1-分集` 的更稳职责是先收束出 `1-分集/第N集.md` 逐集原文真源，再由 `2-剧本` 继续整理成 canonical 主稿。
- `2-剧本` 的价值不是再切一次故事，而是把 `格式判模 + 标准剧/解说剧` 的变体判断收束成一份可继续分组的 canonical 主稿。
- `3-分组` 最稳的落点是“正文 grouped script + 总执行报告”，不要把导演阶段 JSON 或 `grouping.json` sidecar 再搬回规划层。
- `1-Planning` 里的 `3-分组` 只应该落三段式 `分镜组ID`；四段式 `分镜ID` 要留给后续拆镜阶段。
- 对 `3-分组` 来说，最有效的稳边界器不是描述性理由，而是 `场景顺序先锁定 + 15秒默认时长 + effective_text_chars 硬上限`。
- 只要后续 `2-Global` 和 `3-Detail` 共用同一条导演链路，规划阶段就应该把重点放在 handoff，而不是另造第三套 episode 真相。
- 对能被直接命中的规划 skill，`SKILL.md`、`CONTEXT.md` 和 `agents/openai.yaml` 应视为同一入口基线；缺少入口元数据时，执行合同虽然存在，但发现链会断。
- `2-剧本` 最稳的形态是单技能包：`格式判模` 决定变体，`标准剧 / 解说剧` 只做 patch，父技能统一写 canonical 主稿。
- 在 `1-Planning` 里，subagents 最适合负责思考和 plan；skill 自己必须保留执行统筹、validator、写回和验收，否则规划阶段会重新碎成多份局部真相。
- 如果某个 leaf 当前只有一个命中的角色、且不存在真实分叉路由价值，应直接融合回 skill 本体，不要额外维护 team/agent/audit 三层同步成本。
- 对 `1-Planning` 来说，subagents 更适合返回 `agents plan + patch / note / report`；是否把 plan 另行落成 sidecar 只应是可选证据策略，不应成为写回主稿的硬门槛。
- 对 `1-Planning` 已完成的 leaf skills，也应把这条分工同步写进 `agents/openai.yaml`；否则入口摘要仍会把 agent 说成并列执行者。
- 规划阶段即使出现 `标准剧 + 解说剧` 并行对照，也应默认按后台 subagents 处理；前台逐轮交互只应留给补事实或人工裁决节点。
- 对 `规划组` 这类高分叉 team，只有 `角色职责 + 输入输出 + 禁止越权` 还不够；至少还要补 `Done Criteria + Workflow + Fallback + Quality Check`，否则父 skill 虽然知道该调谁，却仍不知道 agent 何时该停、何时该回退、何时该阻塞。
- 对 `格式判模 / 标准剧 / 解说剧 / 节奏` 这类易漂移角色，最有效的稳定器通常不是增加语气说明，而是显式写出默认主案、触发条件、保守回退和禁止跨层扩写的规则。
- 当某个 planning stage 已经拥有自己的 stage-local parent skill 时，`规划组/team.md` 最稳的定位是 shared dispatch plane，而不是再复制一层局部阶段总线。
- 对 `3-分组` 这类量化驱动 stage，reference 只负责完整方法论；真正能防漂移的是“主合同 digest + quantizer + validator”三件套一起存在。

## Case Log

### Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-DIRECT-LEAF

- milestone_type: source_contract_change
- outcome: 将 `1-分集` 从规划组中的单角色 subagent 收敛回 direct leaf skill。
- root_cause_or_design_decision: 当前 `1-分集` 唯一命中的执行投影只有 `.codex/agents/aigc/规划组/分集.md`，没有形成真正的多角色编排收益，反而让父 skill、team、audit 和入口元数据多维护一层无效真源。
- final_fix_or_heuristic: 在父 skill 中改写为“`1-分集` 直达执行、规划组只承接格式/剧本/分组/节奏判断”，删除 `规划组/分集.md`，同步更新 `team.md`、`agents/openai.yaml`、`1-分集/CONTEXT.md` 与 `scripts/aigc_skill_audit.py`。
- prevention_or_replication_checklist:
  - [x] 父 skill 已改成 direct leaf + team routing
  - [x] 规划组 `team.md` 已移除 `分集` 角色
  - [x] `1-分集` 入口元数据已改成 direct execution
  - [x] audit 已不再把 `规划组/分集.md` 视为必需
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`
  - `.codex/agents/aigc/规划组/team.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求“当前匹配的 subagents 就孤零零的一个，这就没有必要走 subagents 模式了，直接完整融合在现有 SKILL 中”。

### Case-20260412-AIGC-PLANNING-ANCHOR-RESTORE

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-Planning` 补齐父级锚点，并把 `1-分集` 纳入真实规划阶段合同。
- root_cause_or_design_decision: 仓内已有 `.codex/agents/aigc/规划组/` 执行投影，但父级 `1-Planning` 真源缺失，导致 registry、team 与 audit 形成断链。
- final_fix_or_heuristic: 建立 `1-Planning/SKILL.md + CONTEXT.md + _shared/IO_CONTRACT.md`，并把输入/output 收敛为 `projects/<项目名>/Story/ -> projects/<项目名>/1-Planning/1-分集/第N集.md -> projects/<项目名>/1-Planning/2-剧本/第N集.md`。
- prevention_or_replication_checklist:
  - [x] 父 skill 锚点已建立
  - [x] team 回指已修正
  - [x] shared I/O 已落盘
  - [x] `1-分集` leaf 合同已补齐
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `.codex/agents/aigc/规划组/team.md`
- user_feedback_or_constraint: 用户要求全面参照 `AIGC-ZEN-VOID` 的 `1-故事分集` 配置完善 `1-Planning/1-分集`。

### Case-20260412-AIGC-PLANNING-GROUPING-LEAF

- milestone_type: source_contract_change
- outcome: 参照 `AIGC-ZEN-VOID` 的 `3-拍摄段落`，补齐 `1-Planning/3-分组` 的 leaf 合同、模板、manifest 与校验链。
- root_cause_or_design_decision: 当前仓内 `3-分组` 目录为空，但父 skill、`2-Global` 与 `节奏` agent 已把它视为有效前置；若不补齐本地真源，规划阶段只能依赖抽象 agent 输出，无法做稳定 handoff 和回归校验。
- final_fix_or_heuristic: 建立 `3-分组/SKILL.md + CONTEXT.md + CHANGELOG.md + templates + postprocess + validate + skill_manifest.json`，同时在 shared I/O 与父 skill 中把 `3-分组/第N集.md + 执行报告.md` 固定为 leaf local truth。
- prevention_or_replication_checklist:
  - [x] `3-分组` 已建立本地真源
  - [x] shared I/O 已登记分组输出与 handoff
  - [x] 父 skill 已更新覆盖状态与聚合规则
  - [x] 下游显式引用路径已同步到 `projects/<项目名>/1-Planning/3-分组/第N集.md`
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/skill_manifest.json`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/2-Global/SKILL.md`
- user_feedback_or_constraint: 用户要求基于 `skill-subagents`，把 `1-Planning/3-分组` 完整对齐到参考技能的治理结构，但输入输出要改成当前仓库路径。

### Case-20260412-AIGC-PLANNING-GROUPING-QUANTIZED-GROUP-ID

- milestone_type: source_contract_change
- outcome: 把 `3-分组` 的标题从四段式误用改回三段式 `分镜组ID`，并把量化字窗门槛正式前移到规划阶段。
- root_cause_or_design_decision: 旧合同把 `episode-scene-group-frame` 误当成了组标题，同时缺少对 `effective_text_chars / warn_window / hard_text_window` 的硬门槛，导致组语义和组粒度同时漂移。
- final_fix_or_heuristic: 在 `3-分组` reference、`SKILL.md`、validator、shared I/O、父 skill 与 `2-Global` 输入合同中统一改写为“三段式组 ID + 量化裁决”；四段式只保留给下游 `分镜ID`。
- prevention_or_replication_checklist:
  - [x] `3-分组` 标题已改为三段式 `分镜组ID`
  - [x] 量化规则已进入 source-layer reference
  - [x] validator 已校验组级量化字段
  - [x] 父 skill 与 `2-Global` 已同步新口径
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/references/scene-order-duration-strategy.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- user_feedback_or_constraint: 用户明确指出“集-场-组-(镜) 的理解不对，且分组浮动太大”，要求直接把三段式组 ID 和量化标准收回源层。

### Case-20260412-AIGC-PLANNING-ENTRY-METADATA

- milestone_type: source_contract_change
- outcome: 为 `1-Planning`、`1-分集` 与 `3-分组` 补齐缺失的 `agents/openai.yaml`，恢复规划阶段入口元数据层。
- root_cause_or_design_decision: 父级与两个 leaf skill 的 `SKILL.md + CONTEXT.md` 已存在，但入口元数据层未同时补齐，导致执行合同与 Codex 发现入口脱节。
- final_fix_or_heuristic: 以仓内已存在的 `aigc` 子技能 `agents/openai.yaml` 为统一样式，为规划父级与两个 leaf skill 增加 `display_name + short_description + default_prompt`，并把“规划 skill 入口三件套”沉淀到父级经验层。
- prevention_or_replication_checklist:
  - [x] `1-Planning/agents/openai.yaml` 已补齐
  - [x] `1-分集/agents/openai.yaml` 已补齐
  - [x] `3-分组/agents/openai.yaml` 已补齐
  - [x] 父级 `1-Planning/CONTEXT.md` 已登记入口元数据缺失模式
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/agents/openai.yaml`
  - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`
  - `.agents/skills/aigc/1-Planning/3-分组/agents/openai.yaml`
  - `.agents/skills/aigc/1-Planning/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求为缺少入口元数据的规划子技能补全 `/agents/openai.yaml`。

### Case-20260412-AIGC-PLANNING-SCRIPT-SINGLE-PACKAGE

- milestone_type: source_contract_change
- outcome: 为 `2-剧本` 建立单一技能包合同，并把 `1-分集 -> 2-剧本` 的上下游真源边界重新锁定。
- root_cause_or_design_decision: 用户明确要求“标准剧/解说剧 不要分成两个子技能包，一个技能包内完成，不同的 subagents 触发”；同时当前仓内 `1-分集` 误把自己的输出直接写成了 `2-剧本` 主稿，导致源层边界混写。
- final_fix_or_heuristic: 新建 `2-剧本/SKILL.md + CONTEXT.md + CHANGELOG.md + validator + agents/openai.yaml`，并把 shared I/O 收敛为 `1-分集/第N集.md -> 2-剧本/第N集.md` 的两层结构。
- prevention_or_replication_checklist:
  - [x] `2-剧本` 已收敛为单技能包
  - [x] 变体通过 subagents 触发
  - [x] `1-分集` 与 `2-剧本` 真源边界已分离
  - [x] 统一 validator 已落盘
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
- user_feedback_or_constraint: 用户明确要求单包路由，不再拆本地变体子技能包。

### Case-20260412-AIGC-PLANNING-AGENT-CONTRACT-ENRICHMENT

- milestone_type: source_contract_change
- outcome: 将 `.codex/agents/aigc/规划组` 的 team 与 5 个角色文档从薄合同升级为包含 `Goal / Done Criteria / Workflow / Fallback / Quality Check` 的厚合同，并为格式变体与节奏角色补齐抗漂移护栏。
- root_cause_or_design_decision: 现有 `规划组` 文档能说明“谁负责什么”，但不能稳定说明“在什么输入下怎么推进、何时停下、何时回退、何时阻塞”；这对 `格式判模 / 标准剧 / 解说剧 / 节奏` 这类高分叉角色尤其危险，容易让父 skill 面对一批能识别岗位但不够可预测的执行器。
- final_fix_or_heuristic: 以 `team.md` 收口共享工作流、决策原则、回退升级与质量门，再为 `格式判模`、`标准剧`、`解说剧`、`分组`、`节奏` 分别补齐身份使命、完成标准、工作流、决策规则、回退条件和质量检查，使其从“角色描述”升级为“可执行提示合同”；`1-分集` 则回收到 direct leaf skill。
- prevention_or_replication_checklist:
  - [x] `team.md` 已补齐组级目标、共享工作流、共享回退与质量门
  - [x] `分组` 已补齐 coverage/边界导向的完成标准与阻塞条件
  - [x] `格式判模 / 标准剧 / 解说剧` 已补齐主变体、字段骨架与抗漂移护栏
  - [x] `节奏` 已补齐进入条件、重排权限与保序阻塞条件
- evidence_paths:
  - `.codex/agents/aigc/规划组/team.md`
  - `.codex/agents/aigc/规划组/格式判模.md`
  - `.codex/agents/aigc/规划组/标准剧.md`
  - `.codex/agents/aigc/规划组/解说剧.md`
  - `.codex/agents/aigc/规划组/分组.md`
  - `.codex/agents/aigc/规划组/节奏.md`
  - `.agents/skills/aigc/1-Planning/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求对 `.codex/agents/aigc/规划组` 同时使用 `agent-meta-prompt-engineer` 与 `senior-prompt-engineer` 强化。

### Case-20260412-AIGC-PLANNING-AGENTS-PLAN-SHIFT

- milestone_type: source_contract_change
- outcome: 将 `1-Planning` 系列 skills 的 subagent 合同从“硬性 thinking sidecar”收敛为“返回 `agents plan`，由 skill 自行执行与按需留痕”。
- root_cause_or_design_decision: 旧合同把 `thinking sidecar` 混成了执行前置，导致 subagent 的思考产物与 skill 的 canonical 执行闭环耦合过紧，不符合“agents 思考计划，skills 执行落盘”的定位。
- final_fix_or_heuristic: 在父 skill、leaf skills、shared I/O、入口元数据与规划组 team 中统一改写为 `agents plan + patch / note / report`；只保留可选 `agents-plan/` 证据路径，不再把 corresponding thinking sidecar 作为硬门槛。
- prevention_or_replication_checklist:
  - [x] 父 skill 已改写 subagent 分工
  - [x] `1-分集 / 2-剧本 / 3-分组` 已同步 agents plan 合同
  - [x] `3-分组` 校验链已移除 thinking hard gate
  - [x] 规划组 agent/team 合同已同步新返回类型
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.codex/agents/aigc/规划组/team.md`
- user_feedback_or_constraint: 用户明确要求 `1-Planning` 系列 skills 不再硬性要求对应 thinking sidecar，并将 subagent 产物改成更符合定位的 `agents plan`。

### Case-20260412-AIGC-PLANNING-GROUPING-STAGE-LOCAL-OWNERSHIP

- milestone_type: source_contract_change
- outcome: 将 `3-分组` 升格为真正的 stage-local parent skill，并把 `规划组/team.md` 收回 shared dispatch plane 定位。
- root_cause_or_design_decision: 旧 `3-分组` 虽已存在 leaf 合同和 shared `分组` specialist，但 stage-local topology 仍主要写在 leaf 说明与 team 总线之间，导致谁拥有量化规则、谁拥有 writeback、谁只负责 patch 的边界不够稳定。
- final_fix_or_heuristic: 在 `1-Planning/SKILL.md` 明确 stage-local ownership：`team.md` 只保留 shared roster / handoff matrix；`3-分组/SKILL.md` 持有本阶段 topology、方法论 digest、quantizer、validator 与 grouped-script writeback；`分组.md` 收缩为纯 specialist。
- prevention_or_replication_checklist:
  - [x] 父 skill 已声明 stage-local ownership rule
  - [x] `3-分组` 已声明自己是 stage-local parent skill
  - [x] `规划组/team.md` 已声明自己只是 shared dispatch plane
  - [x] `规划组/分组.md` 已禁止填写 authoritative 数值
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.codex/agents/aigc/规划组/team.md`
  - `.codex/agents/aigc/规划组/分组.md`
- user_feedback_or_constraint: 用户明确要求按 `skill-subagents` 重新评估当前 `3-分组` 的 subagents 配置是否合理，不合适则调整。
