---
name: aigc-design-prop
description: "Use when routing AIGC prop list, design, or generation tasks."
governance_tier: router
metadata:
  short-description: Route the 11-主体 prop skill group
---

# aigc 11-主体/道具

`道具` 是 11-主体阶段的域级组根导引。它只负责判断当前道具任务应进入 `1-清单`、`2-设计` 还是 `3-生成`，并维护道具清单、道具细目设计与道具生成资产之间的交接边界；它不直接生成道具清单正文、道具设计稿或图像提示词。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用 `$aigc-design-prop` 或直接命中 `.agents/skills/aigc/11-主体/道具/SKILL.md` 时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按需加载项目根 `CONTEXT/` 中与规则物、关键物件、视觉钩子、禁用物件或生成锁定有关的文件。
- 进入任一叶子技能时，必须继续加载该叶子的 `SKILL.md + CONTEXT.md`；组根上下文不得替代叶子上下文。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/11-主体/SKILL.md` > 本 `SKILL.md` > 叶子 `SKILL.md` > 叶子分区文件 > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md` > 叶子 `CONTEXT.md`。

## Group Ownership

| scope | owner |
| --- | --- |
| 道具域入口判断、叶子调度、顺序门与边界说明 | 本组根 |
| 道具清单主体、归并、过滤和首次登场 | `1-清单` |
| 单道具细目设计、材质/结构/功能与设计验收 | `2-设计` |
| 道具主图、多视图、同名 JSON prompt 和生成验收 | `3-生成` |

本组根不得补空道具、把背景杂物批量升格为 canonical 道具、生成默认道具设计稿，或替代叶子技能进行审美与叙事判断。

## Input Contract

- Accepted input: 道具清单、道具设计、道具生成、道具面板、prop panel、道具域修复、或泛称“处理 11-主体/道具”的任务。
- Required input: 可定位的 `projects/aigc/<项目名>/`，或足以判断目标叶子技能的文件路径、集号、道具名、清单/设计/生成缺口。
- Optional input: 指定叶子阶段、指定道具范围、已有参考图、项目 `MEMORY.md` / `CONTEXT/`、上游 `10-分组` 文件。
- Reject or clarify when: 无法定位项目且用户没有提供可核验输入；用户要求组根直接完成全部叶子正文；用户要求脚本替代 LLM 做道具归并、重要性过滤、设计判断或提示词主创。

## Mode Selection

| mode | 触发信号 | route_to | primary output owner |
| --- | --- | --- | --- |
| `prop_list` | 道具清单、从 `10-分组` YAML 提取道具、修复道具清单 | `1-清单/SKILL.md` | `道具清单.md` |
| `prop_detail` | 道具设计、单道具细目、从道具清单扩展设计稿、强化道具好看程度/设计细节/文化元素/工艺装饰 | `2-设计/SKILL.md` | `<道具名>.md` |
| `prop_generation` | 道具生成、主图、多视图、道具面板、JSON prompt | `3-生成/SKILL.md` | `<主体名称>-主图 / 多视图` 与同名 JSON |
| `domain_reconcile` | 上游 `10-分组` 后续新增/更新集数，或既有道具清单、设计稿、生成资产已存在 | 先执行增量对账，再按最早缺口路由 | `reconcile_delta` / `design-manifest.yaml` |
| `domain_repair` | 路径、registry、输出目录或叶子顺序漂移 | 按症状选择对应叶子 | 修复报告或最小 patch |
| `domain_closeout` | 检查道具域是否可交给 12-图像/13-画布 | 已完成叶子输出的验收回查 | 域级状态摘要 |

未明确阶段时采用保守判定：缺清单先走 `1-清单`；有清单缺设计走 `2-设计`；有设计缺生成资产走 `3-生成`；三者都存在时进入 `domain_closeout` 或按用户点名阶段执行。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 任意道具域任务 | 本 `SKILL.md + CONTEXT.md` |
| 道具清单 | `1-清单/SKILL.md + 1-清单/CONTEXT.md` |
| 道具细目设计 | `2-设计/SKILL.md + 2-设计/CONTEXT.md` |
| 道具审美强化、设计细节、文化元素、工艺装饰、避免简单平凡 | `2-设计/SKILL.md + 2-设计/CONTEXT.md`，并由叶子按触发条件加载 `2-设计/knowledge-base/prop-design-corpus.md` |
| 道具图像生成 | `3-生成/SKILL.md + 3-生成/CONTEXT.md` |
| 上游分批完成或既有产物补缺 | `../references/incremental-reconciliation-contract.md` |
| 叶子输出验收 | 对应叶子的 `review/review-contract.md` |
| 叶子输出样板 | 对应叶子的 `templates/` |
| 产品入口摘要 | 对应叶子的 `agents/openai.yaml` |

## LLM-First Creative Authorship Contract

- 本组根只能做路由、边界裁决、输入缺口判断和域级验收摘要。
- 道具归并、背景杂物过滤、道具设计、审美判断、提示词蒸馏与生成策略必须由 LLM 在对应叶子技能内直接完成。
- 脚本只允许读取、枚举、校验、格式检查、文件存在性检查和 manifest 辅助；不得生成 canonical 道具清单、设计正文或图像提示词主创内容，不得批量生成、批量插入、正则套句或映射投影。
- 若道具清单判断、道具设计、prompt 或生成决策来自脚本、映射表、规则模板、关键词锚点替换、句式轮换、同义改写、批量插入、正则套句或映射投影产物，即使叶子字段完整也必须触发 `REWORK-PROP-PSEUDO-DIFF`，回到对应叶子 LLM-first 节点。

## Execution Contract

1. 锁定项目根 `projects/aigc/<项目名>/` 与道具域输出根 `projects/aigc/<项目名>/11-主体/道具/`。
2. 读取本 `SKILL.md + CONTEXT.md`；项目任务继续加载项目 `MEMORY.md` 与相关 `CONTEXT/`。
3. 若 `10-分组` 存在新增/更新集数或道具域已有产物，先按 `../references/incremental-reconciliation-contract.md` 建立 `reconcile_delta`，必要时更新 `projects/aigc/<项目名>/11-主体/道具/design-manifest.yaml`。
4. 根据用户措辞、目标路径、现有产物和 `reconcile_delta` 判定 `mode`。
   - 用户要求道具好看、有设计感、充满细节、文化元素、工艺装饰或避免简单平凡时，必须路由到 `prop_detail -> 2-设计/SKILL.md`；组根只传递该要求，不直接创作道具设计正文。
5. 只加载并执行命中的叶子技能；未命中的叶子不得补占位输出。
6. 叶子技能按自身合同写入 `1-清单/`、`2-设计/` 或 `3-生成/` 子目录；默认只处理新增主体、缺设计稿或缺生成资产。
7. 若发现上游缺失，按链路返回最早缺失叶子，不越级生成下游产物。
8. 若用户要求域级验收，只汇总叶子输出状态和缺口，不改写叶子业务真源。

## Root-Cause Execution Contract (Mandatory)

遇到道具域失败时沿链路上溯：

`Symptom -> Misrouted Prop Leaf -> 道具组根 Mode Selection -> 叶子 SKILL.md -> AGENTS.md LLM-first / Skill 2.0 Rule`

优先修复顺序：

1. 入口错路由：修本组根 `Mode Selection` 或 registry route 文案。
2. 叶子顺序错乱：回到 `1-清单 -> 2-设计 -> 3-生成` 顺序门。
3. 输出目录漂移：回到对应叶子 `Output Contract`。
4. 新增集数后重复道具、漏设计或覆盖既有资产：回到 `../references/incremental-reconciliation-contract.md` 与 `1-清单` 归并/过滤裁决。
5. 背景杂物误入主清单：回到 `1-清单` 的过滤与归并合同。
6. 脚本主创越权：回到 `LLM-First Creative Authorship Contract`。

## Field Mapping

| field_id | owner | must_contain |
| --- | --- | --- |
| `PROP-GROUP-01` | 本组根 | 道具域 mode、叶子路由、顺序门 |
| `PROP-GROUP-02` | `1-清单` | 道具清单、归并、过滤、首次登场 |
| `PROP-GROUP-03` | `2-设计` | 单道具细目设计 Markdown |
| `PROP-GROUP-04` | `3-生成` | 道具主图、多视图与 JSON prompt |
| `PROP-GROUP-05` | 项目根 | 关键道具偏好、禁区和长期生成锁定 |
| `PROP-GROUP-06` | `design-manifest.yaml` | 已消费上游、道具主体映射、设计/生成缺口 sidecar |

## Thought Pass Map

| step_id | thought pass | action pass | evidence |
| --- | --- | --- | --- |
| `PROP-PASS-01` | 判断项目与输入根 | 锁定项目路径和道具域根 | runtime path |
| `PROP-PASS-02` | 判断上游是否分批追加 | 执行增量对账 | `reconcile_delta` |
| `PROP-PASS-03` | 判断缺清单/缺设计/缺生成 | 选择一个叶子技能 | selected mode |
| `PROP-PASS-04` | 判断是否越级 | 回退到最早缺失叶子 | upstream evidence |
| `PROP-PASS-05` | 判断是否需要域级验收 | 汇总叶子状态 | domain summary |

## Pass Table

| pass_id | pass_condition | rework_entry |
| --- | --- | --- |
| `PASS-PROP-GROUP` | 已命中唯一叶子，且加载叶子 `SKILL.md + CONTEXT.md` | done |
| `REWORK-PROP-ROUTE` | 入口语义与叶子不匹配 | 本组根 `Mode Selection` |
| `REWORK-PROP-RECONCILE` | 上游新增后未合并清单、重复道具或覆盖既有资产 | `../references/incremental-reconciliation-contract.md` |
| `REWORK-PROP-UPSTREAM` | 下游输入缺失 | 最早缺失叶子技能 |
| `REWORK-PROP-OUTPUT` | 输出路径或命名漂移 | 对应叶子 `Output Contract` |
| `REWORK-PROP-PSEUDO-DIFF` | 命中叶子输出存在脚本化生成、批量插入、正则套句、映射投影、句式复用、锚点替换或伪差异 | 对应叶子 `LLM-first` / anti-pseudo-diff gate |

## Output Contract

- Required output: 路由决定、命中的叶子技能、必要的上游缺口说明；业务文件由叶子技能写入。
- Output format: Markdown 路由说明、域级状态摘要或最小修复 patch。
- Output path: 叶子输出固定在 `projects/aigc/<项目名>/11-主体/道具/{1-清单,2-设计,3-生成}/`；增量状态 sidecar 可写入 `projects/aigc/<项目名>/11-主体/道具/design-manifest.yaml`。
- Naming convention: 组根报告使用清晰的域名与叶子名；叶子产物按叶子 `Output Contract` 命名。
- Completion gate: 本组根已加载同目录 `CONTEXT.md`；已在分批上游或既有产物场景中执行增量对账；只调度命中叶子；未越权主创；叶子输出按其自身 review gate 验收，且未以脚本化生成、批量插入、正则套句、映射投影、句式复用、锚点替换或同义改写伪差异绕过 LLM-first。
