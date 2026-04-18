# 自主模式模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `init_mode == 自主模式`
- `entrypoint`: `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Autonomous Mode Contract`、`Autonomous Questionnaire Contract`、`Step 0.5`
- `primary_consumers`: 初始化协调助手、问卷编排流程、最终确认卡生成流程

## Scope

本模块只负责 `自主模式` 的执行细则：

- 如何规划下一张问卷卡
- 如何把自由叙述回填成结构化字段
- 如何在回合间暴露 `已确认 / 助手推断 / 仍缺失 / 下游路由`
- 如何在必要时升级到其他模式

本模块不负责：

- 重复定义初始化元选项卡
- 替用户做未经确认的关键拍板
- 把属于 `1-Cards` / `2-Planning` 的问题强行在初始化层拍死

## Load Contract

- 加载条件：`init_mode == 自主模式`
- 互斥规则：本模块成为主执行细则后，不得再加载 `references/advisor-council-mode/module-spec.md` 或 `references/fast-mode/module-spec.md` 作为主路径
- 上下文规则：进入本模块后，如需局部经验与故障恢复策略，再加载同目录 `CONTEXT.md`
- 交互闸门：允许进入 `Autonomous Questionnaire Contract`，并按问卷卡节奏推进

## Mode Goal

通过多轮但收敛的结构化问卷，让用户自己给出初始化关键字段，助手只负责回填、裁剪与路由，不代替用户抢拍板。

## Think-Think Design Snapshot

### 三轴

| 轴角色 | 本模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | 阻塞缺口优先 | 下一轮问卷是否真的在减少当前最阻塞的未知项 | `Execution Procedure`、`questionnaire gate` |
| `成立轴` | 用户拍板成立 | 哪些字段必须以用户确认成立，哪些只能暂存为 `assistant_inferred` 或 `unknowns` | `Questionnaire Planner Template`、`Output Contract` |
| `优选轴` | 最小追问最大沉淀 | 在可行问法中，哪种问卷粒度最利于结构化回填与正式 handoff | `Output Landing Contract`、`Verification Checklist` |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 当前是否仍属于自主问卷，而不是应切换到快速/顾问团模式 | `Load Contract`、`Escalation` |
| `细裁决 / Range Narrowing` | 这一轮到底该问哪些问题、哪些问题该下放到下游 | `Execution Procedure`、`cards_seed / planning_seed / unknowns` 路由 |
| `离散裁决 / Final Selection` | 最终确认前采用哪张最小充分问卷卡与怎样的回填结构 | `Output Contract`、`Output Landing Contract` |

## Shared Dependency Contract

- 必读共享入口：
  - `templates/genres/README.md`
- 按需共享依赖：
  - `templates/genres/{genre}.md`
  - `templates/genres/details/{genre_slug}/`
  - `templates/worldbuilding/*.md`
  - `references/creative-seed-routing/module-spec.md`

加载原则：

1. 本模块负责问卷编排，不替代共享题材/世界观/创意资产本身。
2. 创意相关资料统一经 `creative-seed-routing` 做场景判定和 leaf reference 选择，不在本模块内部散点维护。
3. 共享依赖只在当前缺口真实阻塞下一步时加载，不为了“显得充分”而泛读。
4. 若某字段更适合交给 `1-Cards` / `2-Planning` 再收敛，应优先路由到 `unknowns`，而不是继续深问。

## Questionnaire Planner Template

```text
你现在是 story2026 的“自主模式问卷编排器”。

任务目标：
基于当前已知字段和缺口，产出下一张最小阻塞问卷卡，避免一次抛出全部问题。

硬约束：
1. 每轮只问当前真正阻塞下一步的字段。
2. 每张卡建议 4-8 题。
3. 用户自由叙述时，先结构化回填，再决定是否补问。
4. 不得把属于 `1-Cards` 或 `2-Planning` 的未决问题强行在初始化层拍死。

每轮必须返回：
1. `当前已确认字段`
2. `当前仍缺失字段`
3. `下一张问卷卡`
4. `本轮回填后的 project_contract/cards_seed/planning_seed/unknowns 更新`
```

## Execution Procedure

1. 先生成核心合同卡，锁定 `project_contract` 的最小立项信息。
2. 判断缺口属于 `cards_seed`、`planning_seed` 还是 `unknowns`。
3. 只对当前最阻塞的缺口继续发模块卡。
4. 每轮结束后回填结构化字段，并向用户展示“已确认 / 助手推断 / 仍缺失 / 下游路由”。
5. 达到充分性闸门后，发送最终确认卡并执行落盘。

## Output Contract

- 问卷过程中的每轮摘要都必须保留：
  - `user_confirmed`
  - `assistant_inferred`
  - `unknowns`
- 最终确认卡必须覆盖：
  - `project_contract`
  - `cards_seed`
  - `planning_seed`
  - `unknowns`
  - `sources_breakdown`

## Output Landing Contract

自主模式的每轮回填与最终确认，必须能稳定落到 `0-Init` 的正式写回链路：

- 回合中间态
  - 用于更新当前 `project_contract / cards_seed / planning_seed / unknowns`
- `Init/north_star_contract.json`
  - 只承接长期合同与对象总规范，不吞入整轮问卷叙述
- `Init/初始化简报.json`
  - 必须成为最终确认后的唯一结构化 handoff
- `.webnovel/state.json`
  - 必须记录 `init_mode / mode_source / decision_owner`
- `.webnovel/task_log.jsonl`
  - 必须保留问卷轮次中的 `user_confirmed / assistant_inferred`

若问卷过程无法稳定回填这些位点，只说明“聊过了”，却没沉淀成可恢复结构，视为本模块失效。

## Escalation

- 若用户中途说“你直接补完”，应升级到 `快速模式`，并记录 `mode_source = switched_midway`。
- 若用户指定顾问团路径，应升级到 `智能顾问团模式`，并重新加载模式细则。

## Verification Checklist

1. `mode gate`
   - 自主模式允许问卷，但不得误入一次性快速补全或顾问团执行路径。
2. `questionnaire gate`
   - 每轮仍保持 4-8 题的成组问卷卡，而不是退化成零碎追问。
3. `routing gate`
   - 每轮都能区分 `cards_seed / planning_seed / unknowns` 的路由。
4. `provenance gate`
   - `user_confirmed / assistant_inferred` 在回合摘要与最终确认卡中都可追溯。
5. `landing gate`
   - 最终确认后的结构能直接回写到 `north_star_contract.json`、`初始化简报.json` 与 `.webnovel/state.json`。
