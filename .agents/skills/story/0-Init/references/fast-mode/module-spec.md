# 快速模式模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `init_mode == 快速模式`
- `entrypoint`: `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Fast Mode Contract`、`Step 0.5`、`Step 0.6`
- `primary_consumers`: 初始化协调助手、结构补全线程、最终确认卡生成流程

## Scope

本模块只负责 `快速模式` 的执行细则：

- 如何从最小 brief 提取硬信号
- 如何一次性补完初始化草案
- 如何把推断项与用户确认项分层
- 如何控制阻塞卡数量

本模块不负责：

- 重新展开完整问卷链
- 用人格扮演替代结构补全
- 越权把 `1-Cards` / `2-Planning` 的 canonical 提前拍死

## Load Contract

- 加载条件：`init_mode == 快速模式`
- 互斥规则：本模块成为主执行细则后，不得再加载 `references/advisor-council-mode/module-spec.md` 或 `references/autonomous-mode/module-spec.md` 作为主路径
- 上下文规则：进入本模块后，如需局部经验与故障恢复策略，再加载同目录 `CONTEXT.md`
- 交互闸门：不得进入完整问卷链；仅允许最终确认卡，必要时加 1 张阻塞卡

## Mode Goal

让快速决策智能体基于最少输入一次性补完初始化草案，再交由用户做最终确认，而不是把“快速模式”变成换皮问卷。

## Think-Think Design Snapshot

### 三轴

| 轴角色 | 本模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | 一次性收束优先 | 当前任务是否应该直接朝“单轮补全并确认”收敛，而不是回到问卷链 | `Execution Procedure`、`mode gate` |
| `成立轴` | 保守补全成立 | 哪些字段可以保守补完、哪些必须留在 `unknowns` 或阻塞卡 | `Required Inputs`、`Output Contract`、`risk gate` |
| `优选轴` | 低幻觉高交接比 | 在可成立方案中，哪个补全粒度最利于后续 `north_star / handoff / state` 写回 | `Output Landing Contract`、`Verification Checklist` |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 当前是否命中“快速模式的一次性补全”而非问卷或顾问团 | `Load Contract`、`Mode Goal` |
| `细裁决 / Range Narrowing` | 哪些字段可推断、哪些字段必须保留不确定性 | `Execution Procedure`、`sources_breakdown`、`unknowns` |
| `离散裁决 / Final Selection` | 最终采用哪种最保守但可写回的初始化草案 | `Output Landing Contract`、`Verification Checklist` |

## Required Inputs

- 用户给出的最小 brief：一句话梗概、题材词、情绪目标、风格偏好中的任一组合
- `research_policy`
- `decision_owner`
- 当前已知字段与用户明确禁飞区
- 已触发的题材/市场/世界参考

## Shared Dependency Contract

- 必读共享入口：
  - `templates/genres/README.md`
- 按需共享依赖：
  - `templates/genres/{genre}.md`
  - `templates/genres/details/{genre_slug}/`
  - `templates/worldbuilding/*.md`
  - `references/creative-seed-routing/module-spec.md`

加载原则：

1. 本模块是唯一 `mode-playbook` 真源，但不是共享题材/世界观/创意资产的替代品。
2. 创意相关资产统一经 `creative-seed-routing` 判定后再最小化读取，不得在本模块里重新散列 leaf references。
3. 共享依赖只服务于快速补全，不得把外部材料堆成说明墙。
4. 若题材、平台或世界规则尚不稳定，优先保守补完并写入 `unknowns`，而不是继续扩读资料。

## One-Shot Internal Task Template

```text
你现在是 story2026 的“快速模式初始化决策智能体”。

任务目标：
基于用户提供的最小 brief，一次性补完可落盘的初始化草案。你要像一位保守而高命中率的策划执行者，而不是问卷主持人。

硬约束：
1. 优先保守补完，不追求炫技。
2. 不得改写用户已确认字段。
3. 不得把对象 canonical / 规划 canonical 在初始化层拍死。
4. 所有推断项必须打上 `assistant_inferred`。
5. 只有当字段分叉会直接改变题材承诺、目标平台、主角结构或核心冲突时，才允许请求 1 张阻塞卡。

输出结构：
1. `project_contract`
2. `cards_seed`
3. `planning_seed`
4. `unknowns`
5. `sources_breakdown`
6. `risk_notes`
7. `need_user_blocker_card`
```

## Execution Procedure

1. 读取用户最小 brief，先抽取不可违背的硬信号。
2. 结合题材参考、平台语义和约束模板，一次性补完 `project_contract`。
3. 用“够下游起跑即可”的原则补完 `cards_seed` 与 `planning_seed`。
4. 把仍有争议或证据不足的字段写进 `unknowns`，不要硬填满。
5. 如无高后果分歧，直接生成“快速初始化草案确认卡”；如有，仅补 1 张阻塞卡。
6. 用户确认后执行落盘。

## Output Contract

- 必须产出完整的 `project_contract + cards_seed + planning_seed + unknowns`
- 必须附带 `sources_breakdown`
- `sources_breakdown` 至少包含：
  - `user_confirmed`
  - `assistant_inferred`
- 若调用了额外校对线程，可额外标记 `assistant_reviewed`

## Output Landing Contract

快速模式的结果必须能直接回填到 `0-Init` 的正式写回链路：

- `Init/north_star_contract.json`
  - 读取 `project_contract` 中的长期创作承诺与 `cards_seed` 的长期对象约束
- `Init/初始化简报.json`
  - 必须写入 `project_contract / cards_seed / planning_seed / unknowns / sources_breakdown`
- `.webnovel/state.json`
  - 必须可追溯 `init_mode / research_policy / decision_owner / mode_source`
- `.webnovel/task_log.jsonl`
  - 必须能解释本轮哪些字段来自 `user_confirmed`、哪些来自 `assistant_inferred`

若产出不能稳定映射到上述写回位点，视为本模块输出未闭环。

## Research Policy Guardrail

- 联网只用于概念核验、职业/时代常识、平台当下风向等高时效字段。
- 联网内容只能服务字段补完，不得输出成外部资料墙。

## Fallback

- 若用户输入极少且分叉过大：发 1 张阻塞卡而不是退回长问卷。
- 若外部核验失败：回退到本地知识保守方案，并在 `risk_notes` 标注不确定性。

## Verification Checklist

1. `mode gate`
   - 快速模式执行中不得回流到 Step 1-4 问卷链。
2. `dependency gate`
   - 共享题材/世界观/创意资产只按需加载，没有被当作第二主合同。
3. `provenance gate`
   - `user_confirmed / assistant_inferred` 至少两层来源可追溯。
4. `landing gate`
   - 产出可直接映射到 `north_star_contract.json`、`初始化简报.json` 与 `.webnovel/state.json`。
5. `risk gate`
   - 高后果分歧没有被强行脑补，而是进入 `unknowns` 或 1 张阻塞卡。
