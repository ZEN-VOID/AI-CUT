# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `query/` 的经验层知识库，不是过程日志。
- 每次调用 `query/` 时，应自动预加载本文件，用于 truth-role 判定、真源选路、冲突拆分与失败闭环。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 把仓库根目录或技能目录当成 `PROJECT_ROOT` | project-root guard | 先解析 `projects/<项目名>/`，再读 runtime | 在 `SKILL.md` 固定 project-root 判定顺序 | 查询输出的证据路径都落在真实项目目录 |
| 只列出文件存在，不判断是否已通过验收 | truth-role contract | 同时读取阶段或项目 `validation-report.md` | 在 truth-role 表中固定“存在不等于 PASS” | 查询回答会显式区分产物存在与验收状态 |
| 问 `第N集` 事实时只扫 sidecar，不读主 JSON | directing root contract | 优先读取 `projects/<项目名>/3-Detail/第N集.json` | 把编导根文件写成 directing query 的唯一主入口 | 回答会以主 JSON 为先 |
| 问治理状态时只看目录结构，不看 governance artifacts | harness carrier contract | 读取 `project_state / mandate / brief / route / verdict / validation / learning` | 在 reference 固定 governance carriers 清单 | 查询项目状态时会带治理工件证据 |
| 问断点或下一入口时只读 `project_state.yaml`，忽略结构化断点 | governance snapshot contract | 优先读取 `governance-state.yaml`，再补读 `project_state.yaml` | 在 query 合同中固定“断点治理优先读 governance-state” | 查询会给出结构化 checkpoint 证据 |
| 把轻量初始化态误判为治理故障 | init layering contract | 先确认 `project_state.yaml` 与核心初始化工件是否齐全，再决定是否建议补治理快照 | 在 query 合同中固定“core first, governance lazy” | 查询会明确回答“轻量初始化态”而不是泛化成异常 |
| 把 stage 局部规则说成仓库级制度 | meta-rule boundary | 回到 registry / routes / root skill 校验 | 在 query 中固定“制度问题先查 registry/routes/root skill” | 回答不会再把局部 stage 规则冒充全局 |

## Repair Playbook

1. 先确认 `PROJECT_ROOT`，再做任何查询。
2. 先判定用户在问哪一种 truth role，不要先 `rg` 全仓。
3. 若结果涉及“是否完成 / 是否通过”，必须同时核对 `validation-report.md`。
4. 若结果涉及“为什么这么路由”，必须补读 registry / routes / root `aigc/SKILL.md`。
5. 只有在真源路径和 truth role 都锁定后，才输出结果。

## Reusable Heuristics

- `query/` 的核心不是“搜文件”，而是“先选真源，再搜文件”。
- 对 `aigc` 项目来说，`projects/<项目名>/` 是第一层真源；`.agents/skills/` 只是合同源，不是项目结果源。
- 文件存在只能证明“有产物”，不能证明“可交付”；验收结论仍要回到 `validation-report.md`。
- 若一个查询横跨多个阶段，最稳的表达是拆成“项目治理 / 阶段产物 / 验收状态”三栏，而不是混成一句。
- 当问题带有“现在停在哪、从哪继续、还缺什么治理工件”时，`governance-state.yaml` 的优先级应高于 `project_state.yaml`。
- 若 `governance-state.yaml` 缺失但 `project_state.yaml` 与 `Init/` 核心工件都在，优先判为“轻量初始化态”，不要直接说成治理失效。

## Case Log

### Case-20260411-AIGC-QUERY-BOOTSTRAP

- milestone_type: source_contract_change
- symptom_or_outcome: `aigc` 根技能此前缺少独立事实查询卫星技能，项目状态、产物定位与治理工件查证只能混在根路由说明里。
- root_cause_or_design_decision: 根技能承担总入口与路由职责，但 query 类能力横跨所有阶段、又不拥有阶段内容真源，更适合做根级卫星技能。
- final_fix_or_heuristic: 新建 `query/`，并把它固定为尚书省/户部侧的事实查询入口；查询总是先解析 `PROJECT_ROOT`，再判定 truth role。
- prevention_or_replication_checklist:
  - [x] 已建立 `query/SKILL.md`
  - [x] 已建立 `query/references/system-data-flow.md`
  - [x] 已建立 `query/CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/query/SKILL.md`
  - `.agents/skills/aigc/query/CONTEXT.md`
  - `.agents/skills/aigc/query/references/system-data-flow.md`
- user_feedback_or_constraint: 用户要求参照 `story2026/query` 的卫星技能形态，在 `aigc` 根目录补同名卫星技能。

### Case-20260412-AIGC-QUERY-4-DESIGN-RUNTIME-SYNC

- milestone_type: source_contract_change
- symptom_or_outcome: `query/` 的 truth-role 表和 system-data-flow 仍把 design 阶段资产指向旧的 `projects/<项目名>/主体/`，与当前 `4-Design` 父级和叶子技能的 runtime 已分裂。
- root_cause_or_design_decision: `4-Design` 阶段后来独立收口到了 `projects/<项目名>/4-Design/`，但 `query/` 仍沿用早期 runtime 口径，导致查询返回的 design 资产路径可能失真。
- final_fix_or_heuristic: 以 `.agents/skills/aigc/_shared/project-runtime-layout.md` 为 canonical runtime，同步更新 `query/SKILL.md` 与 `references/system-data-flow.md` 中的 design truth-role carrier。
- prevention_or_replication_checklist:
  - [x] `query/SKILL.md` 已将 design 资产查询改到 `projects/<项目名>/4-Design/`
  - [x] `system-data-flow.md` 已将 `subject` carrier 改到 `4-Design/`
  - [x] 本地 `CONTEXT.md` 已记录本轮 runtime 收口
- evidence_paths:
  - `.agents/skills/aigc/query/SKILL.md`
  - `.agents/skills/aigc/query/references/system-data-flow.md`
  - `.agents/skills/aigc/query/CONTEXT.md`
- user_feedback_or_constraint: 用户要求继续把 `4-Design` 父级与 shared runtime 一并收口，避免查询层继续读旧目录。
