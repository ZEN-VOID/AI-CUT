---
name: aigc-design
description: "Use when routing AIGC design tasks for characters, props, or scenes."
governance_tier: router
metadata:
  short-description: Route fused 6-设计 domain packages
---

# aigc-design

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若当前任务绑定 `projects/aigc/<项目名>/`，还必须先加载项目根 `MEMORY.md`，再按需加载项目根 `CONTEXT/` 中与当前设计域有关的文件。
- 本父级只拥有阶段路由、域选择、输出拓扑声明和阶段级验收；业务主创与最终文件写回由 `场景`、`角色`、`道具` 三个域级子技能包承担。
- 若命中的域级或叶子设计阶段需要 team 上下文，父级只传递 `../_shared/team-advisor-consultation-contract.md` 的初始化综合消费合同，并要求其只读消费 `team.yaml.init_synthesis.stage_seed_summary."6-设计"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`；创作阶段不得调用 team 成员身份、解析旧 stage profile、生成新顾问问答或把 team 配置当作 worker/reviewer 调度预设。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 域级子技能 `SKILL.md` > `references/*` / 域级分区 > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Multi-Subskill Continuous Workflow

当本主技能包被整体调用时，视为用户已授权按本级声明的同级子技能包自动完成整个技能组任务；在满足本技能必要输入、显式选择和安全门后，不再为“是否继续下一步”额外确认。

- 无序号同级子技能包默认全选并发执行；因此整体调用 `6-设计` 且未指定域时，默认同时调度 `场景`、`角色`、`道具` 三个域级包，再由本父级汇总验收。
- 数字序号子技能包或节点（如域级包内部的 `1-清单`、`2-设计`、`3-生成`）默认按数字升序串行执行，前一节点产物自动作为后一节点输入。
- 英文序号子技能包或路线（如 `A-`、`B-`、`C-`）默认按用户意图、父级路由或输入类型单选分流；只有用户明确要求对比、并跑或批量多路线时才多选。
- 连续调度不得绕过本技能的阻断门：缺少必需输入、域无法判定且整体调用语义不足、破坏性覆盖未授权、域级包缺失或路线歧义会造成错误 canonical 写回时，必须先停下并给出最小澄清或不可用说明。
- 每个被调度的域级包仍必须加载自身 `SKILL.md + CONTEXT.md`；脚本只能承担机械辅助，不得替代 LLM 设计主创或父级最终裁决。

## Input Contract

- Accepted input: 6-设计 阶段任务、场景/角色/道具清单-设计-生成一体化任务、旧 `1-清单 / 2-设计 / 3-面板` 路径迁移后的路由修复。
- Required input: 项目名与集数，或可定位到 `projects/aigc/<项目名>/5-分组/第N集.md` / 既有 6-设计 输入。
- Optional input: 指定域、指定主体、项目 `MEMORY.md` / `CONTEXT/`、已有参考图、域级 leaf 产物。
- Reject or clarify when: 无法判断域且没有足够上下文自动判定；用户要求在父级直接主创全部场景/角色/道具正文；用户要求恢复旧 `1-清单/2-设计/3-面板` 子技能真源。

## Stage Structure

当前 `6-设计` 只保留三个域级 Skill 2.0 子技能包：

| domain | skill package | final required outputs |
| --- | --- | --- |
| `场景` | `.agents/skills/aigc/6-设计/场景` | `场景/1-清单/场景清单.md`、`场景/2-设计/S###-<场景名>.md`、`场景/3-生成/<场景名>-*.json` |
| `角色` | `.agents/skills/aigc/6-设计/角色` | `角色/1-清单/角色清单.md`、`角色/2-设计/<角色名>.md`、`角色/3-生成/<角色名>-*.json` |
| `道具` | `.agents/skills/aigc/6-设计/道具` | `道具/1-清单/道具清单.md`、`道具/2-设计/<道具名>.md`、`道具/3-生成/<道具名>-*.json` |

旧 `1-清单`、`2-设计`、`3-面板` 合同已作为迁移资料归档到 `references/legacy/` 或各域级 `references/legacy/`；它们不再是 active skill 入口。

## Mode Selection

| mode | 触发信号 | 主要动作 |
| --- | --- | --- |
| `single_domain` | 用户明确命中场景、角色或道具 | 加载对应域级 `SKILL.md + CONTEXT.md` 并执行 |
| `multi_domain` | 用户要求一次处理多个域，或整体调用 `6-设计` 且未指定单一域 | 无序号域级包默认全选并发调度；若用户显式给出域集合但未给顺序，也按并发汇总处理 |
| `incremental_reconcile` | `5-分组` 只完成部分集数后曾执行过 6-设计，随后又新增或更新 `第N集.md` | 先按域执行增量对账，再进入缺口对应的 `1-清单 -> 2-设计 -> 3-生成` |
| `domain_repair` | 旧路径、registry、脚本或输出合同漂移 | 进入 `references/阶段路由矩阵.md` 与对应域级 review gate |
| `stage_closeout` | 域级输出已完成，需要阶段验收 | 汇总域级 review verdict；失败域必须回到对应叶子直接修复并复审，通过后写 `validation-report.md` |
| `stage_closeout_review_repair` | closeout 发现域级清单/设计/生成存在阻断项 | 路由到对应域级 leaf `review -> direct repair -> re-review`，父级只聚合结果 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 父级路由与域选择 | `references/阶段路由矩阵.md` |
| 父级思行节点 | `references/思行网络.md` |
| 上游分批完成、后续追加集数、既有设计需要补缺 | `references/incremental-reconciliation-contract.md` |
| 父级增量对账、legacy archive 边界与阶段 closeout 验收 | `review/review-contract.md` |
| 阶段末域级验收后直接修复闭环 | 本 `Stage-Closeout Review-Repair Contract`、`references/思行网络.md`、对应域级 leaf `review/review-contract.md` |
| 设计创作阶段消费初始化团队综合 | `../_shared/team-advisor-consultation-contract.md`；只读消费 `team.yaml.init_synthesis.stage_seed_summary."6-设计"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`，由命中域级/叶子技能压缩为 `init_team_synthesis_context` |
| 场景域执行 | `场景/SKILL.md + 场景/CONTEXT.md` |
| 角色域执行 | `角色/SKILL.md + 角色/CONTEXT.md` |
| 道具域执行 | `道具/SKILL.md + 道具/CONTEXT.md` |
| 旧 tranche 父合同追溯 | `references/legacy/` |

## Execution Contract

1. 锁定项目根：`projects/aigc/<项目名>/`。
2. 锁定 6-设计 输出根：`projects/aigc/<项目名>/6-设计/`。
3. 根据用户请求、输入文件或现有产物判定命中域。
4. 若检测到 `5-分组` 新增、更新、只覆盖部分集数，或既有 `6-设计` 产物已存在，必须进入 `incremental_reconcile`：读取 `references/incremental-reconciliation-contract.md`，并要求每个命中域先产出本轮 `reconcile_delta`。
5. 只调度命中的域级子技能包；未命中的域不得补空清单、补占位主体或伪造面板 JSON。
6. 域级子技能内部固定处理顺序为 `清单 -> 设计 -> 生成`，但每步只处理增量对账后的缺口；不得静默覆盖既有清单、设计稿或生成资产。
7. 当命中 `角色/2-设计`、`道具/2-设计`、`场景/2-设计` 且项目存在初始化综合时，父级验收必须检查域级是否只读消费 `team.yaml.init_synthesis.stage_seed_summary."6-设计"`、`init_handoff.design_seed` 或 `north_star.yaml.创作阶段不变量.设计` 并形成 `init_team_synthesis_context`；不得检查或要求创作阶段顾问请教、team 身份调用、旧 stage profile 或 leaf 专属 persona profile。
8. 父级只验证域级最终文件是否按 leaf 合同落到对应域内子目录；不直接改写域级业务主稿。
9. 若需要阶段级 closeout，先汇总每个命中域的 leaf review verdict；存在 `needs_rework` 时，父级必须把问题路由回对应域级 leaf，要求该 leaf 直接修复并复审，不得由父级补写业务正文或伪造通过。
10. 所有命中域通过复审后，写入 `projects/aigc/<项目名>/6-设计/validation-report.md`，并记录本轮上游范围、新增主体、跳过既有产物、初始化综合消费/本地复核、repair actions、复审结果和遗留风险。

## Stage-Closeout Review-Repair Contract

`6-设计` 父级不拥有场景、角色、道具业务主稿写权，因此阶段末闭环采用“父级聚合，域级修复”的模式。

固定执行语义：

1. `D-N5-DOMAIN-GATE` 只汇总命中域内 `1-清单 / 2-设计 / 3-生成` 的 review verdict、输出路径、manifest 和阻断项。
2. 若任一域或叶子 verdict 为 `needs_rework`，进入 `D-N5R-DOMAIN-REPAIR`：把 findings 路由回对应域级 leaf，由该 leaf 按自身 `review/review-contract.md` 直接修复并复审。
3. 父级不得直接补清单主体、设计正文、生成 JSON 或图片资产；父级只能记录 route、owner、repair action 摘要和复审 verdict。
4. 若失败源于上游 `5-分组`、旧路径迁移或增量对账，父级可以修路由/对账合同，但业务主体仍回对应域级 leaf。
5. `validation-report.md` 只有在所有命中域通过复审或明确使用本地流程时才能写为阶段 closeout；失败域不得被写成通过。

## Root-Cause Execution Contract (Mandatory)

遇到失败时沿链路上溯：

`Symptom -> Direct Cause -> Domain Package Owner -> Source Contract -> AGENTS.md / skill-工作车间`

优先修复顺序：

1. 路由仍指向旧 `1-清单/2-设计/3-面板`：修 `references/阶段路由矩阵.md`、registry、routes 和相关脚本。
2. 域级执行叶子缺 Skill 2.0 分区：回到对应叶子技能的 canonical layout；域级组根本身按 `governance_tier: router` 验收。
3. 父级、registry 或 closeout 仍要求根目录平铺业务真源：回到域级 `SKILL.md` Output Contract。
4. 新增上游集数后覆盖旧清单、重复生成已有主体或重排场景编号：回到 `references/incremental-reconciliation-contract.md` 与对应域 `1-清单` merge 合同。
5. 设计模板或面板模板漂移：回到对应域级 `templates/` 与 `review/`。
6. 设计阶段仍调用 team 身份、解析旧 stage profile、补造顾问问答，或没有优先消费 `init_synthesis.stage_seed_summary."6-设计"`：回到 `../_shared/team-advisor-consultation-contract.md` 和对应叶子 `SKILL.md`。
7. 引用无法自动更新：记录到最终报告；若形成可复用经验，再沉淀到对应域级 `CONTEXT.md`。

## Field Mapping

| field_id | owner | must_contain |
| --- | --- | --- |
| `DESIGN-FIELD-01` | `SKILL.md` | 父级输入、路由、输出和 root-cause 合同 |
| `DESIGN-FIELD-02` | `references/阶段路由矩阵.md` | 域级包路径、触发词、输出文件 |
| `DESIGN-FIELD-03` | `references/思行网络.md` | 父级 route/dispatch/closeout 节点 |
| `DESIGN-FIELD-04` | `references/incremental-reconciliation-contract.md` | 上游分批完成时的增量对账、manifest 和补缺规则 |
| `DESIGN-FIELD-05` | `场景/角色/道具/SKILL.md` | 域级清单 -> 设计 -> 生成顺序 |
| `DESIGN-FIELD-06` | `projects/aigc/<项目名>/6-设计/validation-report.md` | 阶段级验收摘要 |
| `DESIGN-FIELD-07` | `../_shared/team-advisor-consultation-contract.md` | 设计叶子只读消费初始化团队综合，并禁止创作阶段 team 身份调用、旧 stage profile 和伪顾问问答 |
| `DESIGN-FIELD-08` | `Stage-Closeout Review-Repair Contract` | 失败域回 leaf 直接修复并复审，父级只聚合 verdict |

## Thought Pass Map

| step_id | thought pass | action pass | evidence |
| --- | --- | --- | --- |
| `DESIGN-PASS-01` | 判断项目根与输出根 | 锁定 `projects/aigc/<项目名>/6-设计/` | runtime path |
| `DESIGN-PASS-02` | 判断命中域 | 路由到 `场景 / 角色 / 道具` 包 | `domain_routes` |
| `DESIGN-PASS-03` | 判断是否存在分批上游或既有产物 | 执行增量对账门 | `reconcile_delta` |
| `DESIGN-PASS-04` | 判断域级输出是否完成 | 执行域级 review gate | `domain_verdicts` |
| `DESIGN-PASS-05` | 判断命中设计叶子是否完成初始化综合消费或缺失记录 | 汇总 `init_team_synthesis_context` 状态 | `init_team_synthesis_status` |
| `DESIGN-PASS-06` | 判断是否需要域级修复 | 将失败 finding 路由回对应域级 leaf 并要求复审 | `domain_repair_results` |
| `DESIGN-PASS-07` | 判断是否需要阶段 closure | 写或更新 `validation-report.md` | stage verdict |

## Pass Table

| pass_id | pass_condition | rework_entry |
| --- | --- | --- |
| `DESIGN-PASS` | 命中域明确，输出根正确，旧 tranche 不再作为 active 入口 | done |
| `DESIGN-REWORK-ROUTE` | 仍引用旧 `1-清单/2-设计/3-面板` | `references/阶段路由矩阵.md` |
| `DESIGN-REWORK-INCREMENTAL` | 新增 `5-分组` 后清单/设计/生成未对账或覆盖既有产物 | `references/incremental-reconciliation-contract.md` |
| `DESIGN-REWORK-DOMAIN` | 域级输出失败 | 对应域级 leaf `review/review-contract.md` -> direct repair -> re-review |
| `DESIGN-REWORK-INIT-SYNTHESIS` | 设计叶子缺少初始化综合消费，或误触发 team 身份调用 / 旧 stage profile / 伪顾问问答 | `../_shared/team-advisor-consultation-contract.md` |

## Output Contract

- Required output: 父级路由结果与可选阶段验收报告；域级任务的实际输出由对应子技能写出。
- Output format: `validation-report.md` 使用 Markdown；域级业务输出为对应 leaf 的清单、设计稿和生成请求/结果 JSON。
- Output path: 父级阶段报告写到 `projects/aigc/<项目名>/6-设计/validation-report.md`；域级业务真源写到 `projects/aigc/<项目名>/6-设计/{场景,角色,道具}/{1-清单,2-设计,3-生成}/`；域级状态 sidecar 可写到 `projects/aigc/<项目名>/6-设计/{场景,角色,道具}/design-manifest.yaml`。
- Naming convention: 父级报告固定名 `validation-report.md`；域级命名由各域 `SKILL.md` 的 Output Contract 裁决。
- Completion gate: 路由只命中 active 域级包；旧 tranche 路径不再作为 active skill 入口；命中域的 Skill 2.0 结构和输出合同验证通过；若存在分批上游或既有产物，已完成增量对账且未静默覆盖；设计叶子在初始化综合存在时已形成 `init_team_synthesis_context`，并确认未调用 team 身份、旧 stage profile 或伪顾问问答；阶段 closeout 中发现的域级阻断项已回到对应 leaf 直接修复并复审，或在 `validation-report.md` 中明确使用本地流程和未通过域。
