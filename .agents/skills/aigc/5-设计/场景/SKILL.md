---
name: aigc-design-scene
description: Use when the AIGC 5-设计/场景 domain needs to route work into scene list, scene detail design, or scene image generation leaf skills under `.agents/skills/aigc/5-设计/场景/{1-清单,2-设计,3-生成}`.
governance_tier: router
metadata:
  short-description: Route the 5-设计 scene skill group
---

# aigc 5-设计/场景

`场景` 是 5-设计阶段的域级组根导引。它只负责判断当前场景任务应进入 `1-清单`、`2-设计` 还是 `3-生成`，并维护场景清单、单场景设计与场景生成资产之间的交接边界；它不直接生成场景清单正文、场景设计稿或图像提示词。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用 `$aigc-design-scene` 或直接命中 `.agents/skills/aigc/5-设计/场景/SKILL.md` 时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按需加载项目根 `CONTEXT/` 中与场景命名、世界观地点、建筑/空间规则、无人空镜禁区或长期视觉偏好相关的文件。
- 进入任一叶子技能时，必须继续加载该叶子的 `SKILL.md + CONTEXT.md`；组根上下文不得替代叶子上下文。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/5-设计/SKILL.md` > 本 `SKILL.md` > 叶子 `SKILL.md` > 叶子分区文件 > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md` > 叶子 `CONTEXT.md`。

## Group Ownership

| scope | owner |
| --- | --- |
| 场景域入口判断、叶子调度、顺序门与边界说明 | 本组根 |
| 场景清单主体、归并/拆分、首次登场和清单验收 | `1-清单` |
| 单场景细目设计、空间解构、摄影语汇和设计验收 | `2-设计` |
| 场景主图、多视图、同名 JSON prompt 和生成验收 | `3-生成` |

本组根不得补空场景、把角色或道具目录误写入场景域、生成默认场景设计稿，或替代叶子技能进行空间/美术/摄影判断。

## Input Contract

- Accepted input: 场景清单、场景设计、场景生成、场景面板、scene panel、场景九宫格、场景域修复、或泛称“处理 5-设计/场景”的任务。
- Required input: 可定位的 `projects/aigc/<项目名>/`，或足以判断目标叶子技能的文件路径、集号、场景名、清单/设计/生成缺口。
- Optional input: 指定叶子阶段、指定场景范围、已有参考图、项目 `MEMORY.md` / `CONTEXT/`、上游 `4-分组` 文件。
- Reject or clarify when: 无法定位项目且用户没有提供可核验输入；用户要求组根直接完成全部叶子正文；用户要求脚本替代 LLM 做场景归并、空间拆分、设计判断或提示词主创。

## Mode Selection

| mode | 触发信号 | route_to | primary output owner |
| --- | --- | --- | --- |
| `scene_list` | 场景清单、从 `4-分组` YAML 提取场景、修复场景清单 | `1-清单/SKILL.md` | `场景清单.md` |
| `scene_detail` | 场景设计、单场景细目、从场景清单扩展设计稿 | `2-设计/SKILL.md` | `S###-<场景名>.md` |
| `scene_generation` | 场景生成、主图、多视图、场景面板、JSON prompt | `3-生成/SKILL.md` | `<主体名称>-主图 / 多视图` 与同名 JSON |
| `domain_repair` | 路径、registry、输出目录或叶子顺序漂移 | 按症状选择对应叶子 | 修复报告或最小 patch |
| `domain_closeout` | 检查场景域是否可交给 6-图像/7-视频 | 已完成叶子输出的验收回查 | 域级状态摘要 |

未明确阶段时采用保守判定：缺清单先走 `1-清单`；有清单缺设计走 `2-设计`；有设计缺生成资产走 `3-生成`；三者都存在时进入 `domain_closeout` 或按用户点名阶段执行。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 任意场景域任务 | 本 `SKILL.md + CONTEXT.md` |
| 场景清单 | `1-清单/SKILL.md + 1-清单/CONTEXT.md` |
| 场景细目设计 | `2-设计/SKILL.md + 2-设计/CONTEXT.md` |
| 场景图像生成 | `3-生成/SKILL.md + 3-生成/CONTEXT.md` |
| 叶子输出验收 | 对应叶子的 `review/review-contract.md` |
| 叶子输出样板 | 对应叶子的 `templates/` |
| 产品入口摘要 | 对应叶子的 `agents/openai.yaml` |

## LLM-First Creative Authorship Contract

- 本组根只能做路由、边界裁决、输入缺口判断和域级验收摘要。
- 场景归并/拆分、空间设计、摄影语汇、审美判断、提示词蒸馏与生成策略必须由 LLM 在对应叶子技能内直接完成。
- 脚本只允许读取、枚举、校验、投影、格式检查和文件存在性检查；不得生成 canonical 场景清单、设计正文或图像提示词主创内容。

## Execution Contract

1. 锁定项目根 `projects/aigc/<项目名>/` 与场景域输出根 `projects/aigc/<项目名>/5-设计/场景/`。
2. 读取本 `SKILL.md + CONTEXT.md`；项目任务继续加载项目 `MEMORY.md` 与相关 `CONTEXT/`。
3. 根据用户措辞、目标路径和现有产物判定 `mode`。
4. 只加载并执行命中的叶子技能；未命中的叶子不得补占位输出。
5. 叶子技能按自身合同写入 `1-清单/`、`2-设计/` 或 `3-生成/` 子目录。
6. 若发现上游缺失，按链路返回最早缺失叶子，不越级生成下游产物。
7. 若用户要求域级验收，只汇总叶子输出状态和缺口，不改写叶子业务真源。

## Root-Cause Execution Contract (Mandatory)

遇到场景域失败时沿链路上溯：

`Symptom -> Misrouted Scene Leaf -> 场景组根 Mode Selection -> 叶子 SKILL.md -> AGENTS.md LLM-first / Skill 2.0 Rule`

优先修复顺序：

1. 入口错路由：修本组根 `Mode Selection` 或 registry route 文案。
2. 叶子顺序错乱：回到 `1-清单 -> 2-设计 -> 3-生成` 顺序门。
3. 输出目录漂移：回到对应叶子 `Output Contract`。
4. 场景归并/拆分错误：回到 `1-清单` 的场景边界裁决。
5. 脚本主创越权：回到 `LLM-First Creative Authorship Contract`。

## Field Mapping

| field_id | owner | must_contain |
| --- | --- | --- |
| `SCENE-GROUP-01` | 本组根 | 场景域 mode、叶子路由、顺序门 |
| `SCENE-GROUP-02` | `1-清单` | 场景清单、归并/拆分、首次登场 |
| `SCENE-GROUP-03` | `2-设计` | 单场景细目设计 Markdown |
| `SCENE-GROUP-04` | `3-生成` | 场景主图、多视图与 JSON prompt |
| `SCENE-GROUP-05` | 项目根 | 场景命名、空间规则、无人空镜等长期偏好 |

## Thought Pass Map

| step_id | thought pass | action pass | evidence |
| --- | --- | --- | --- |
| `SCENE-PASS-01` | 判断项目与输入根 | 锁定项目路径和场景域根 | runtime path |
| `SCENE-PASS-02` | 判断缺清单/缺设计/缺生成 | 选择一个叶子技能 | selected mode |
| `SCENE-PASS-03` | 判断是否越级 | 回退到最早缺失叶子 | upstream evidence |
| `SCENE-PASS-04` | 判断是否需要域级验收 | 汇总叶子状态 | domain summary |

## Pass Table

| pass_id | pass_condition | rework_entry |
| --- | --- | --- |
| `PASS-SCENE-GROUP` | 已命中唯一叶子，且加载叶子 `SKILL.md + CONTEXT.md` | done |
| `REWORK-SCENE-ROUTE` | 入口语义与叶子不匹配 | 本组根 `Mode Selection` |
| `REWORK-SCENE-UPSTREAM` | 下游输入缺失 | 最早缺失叶子技能 |
| `REWORK-SCENE-OUTPUT` | 输出路径或命名漂移 | 对应叶子 `Output Contract` |

## Output Contract

- Required output: 路由决定、命中的叶子技能、必要的上游缺口说明；业务文件由叶子技能写入。
- Output format: Markdown 路由说明、域级状态摘要或最小修复 patch。
- Output path: 叶子输出固定在 `projects/aigc/<项目名>/5-设计/场景/{1-清单,2-设计,3-生成}/`。
- Naming convention: 组根报告使用清晰的域名与叶子名；叶子产物按叶子 `Output Contract` 命名。
- Completion gate: 本组根已加载同目录 `CONTEXT.md`；只调度命中叶子；未越权主创；叶子输出按其自身 review gate 验收。
