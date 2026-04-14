# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `query/` 的经验层知识库，不是过程日志。
- 每次调用 `query/` 时，应自动预加载本文件，用于 truth-role 判定、真源选路、冲突拆分与失败闭环。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 把仓库根目录或技能目录当成 `PROJECT_ROOT` | project-root guard | 先解析 `projects/aigc/<项目名>/`，再读 runtime | 在 `SKILL.md` 固定 project-root 判定顺序 | 查询输出的证据路径都落在真实项目目录 |
| 只列出文件存在，不判断是否已通过验收 | truth-role contract | 同时读取阶段或项目 `validation-report.md` | 在 truth-role 表中固定“存在不等于 PASS” | 查询回答会显式区分产物存在与验收状态 |
| 问 `第N集` 事实时只扫 sidecar，不读主 JSON | directing root contract | 优先读取 `projects/aigc/<项目名>/3-Detail/第N集.json` | 把编导根文件写成 directing query 的唯一主入口 | 回答会以主 JSON 为先 |
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
- 对 `aigc` 项目来说，`projects/aigc/<项目名>/` 是第一层真源；`.agents/skills/` 只是合同源，不是项目结果源。
- 文件存在只能证明“有产物”，不能证明“可交付”；验收结论仍要回到 `validation-report.md`。
- 若一个查询横跨多个阶段，最稳的表达是拆成“项目治理 / 阶段产物 / 验收状态”三栏，而不是混成一句。
- 当问题带有“现在停在哪、从哪继续、还缺什么治理工件”时，`governance-state.yaml` 的优先级应高于 `project_state.yaml`。
- 若 `governance-state.yaml` 缺失但 `project_state.yaml` 与 `Init/` 核心工件都在，优先判为“轻量初始化态”，不要直接说成治理失效。
