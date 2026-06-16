# Context: aigc 3-主体/角色

## Purpose & Loading Contract

- 本文件是 `aigc-design-character` 角色域组根的经验层，不是角色设定库，也不是执行流水日志。
- 调用 `.agents/skills/aigc/3-主体/角色/SKILL.md` 时，必须同时加载本文件。
- 叶子技能经验分别沉淀在 `1-清单/CONTEXT.md`、`2-设计/CONTEXT.md`、`3-生成/CONTEXT.md`；本文件只保存跨叶子的路由和交接经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
recommended_action: keep-domain-router-scoped
last_checked_at: 2026-04-26
```

## Type Map

| type_id | 触发症状 | 立即修复 | 验证点 |
| --- | --- | --- | --- |
| `CHAR-GROUP-TM-01` | 用户只说“角色”但没有阶段 | 先查是否存在 `角色清单.md`、设计稿和生成资产，再路由到最早缺失叶子 | 不越级生成下游 |
| `CHAR-GROUP-TM-02` | 清单、设计、生成任务混在一句里 | 按 `1-清单 -> 2-设计 -> 3-生成` 串行拆解；本轮只执行用户授权范围 | 未命中叶子无占位输出 |
| `CHAR-GROUP-TM-03` | 叶子试图改写上游真源 | 回到叶子 ownership，以下游报告形式提出上游修复建议 | 上游文件未被越权改写 |
| `CHAR-GROUP-TM-04` | 角色长期偏好在多轮持续生效 | 写项目根 `MEMORY.md`，不写入组根 CONTEXT | 项目记忆可回读 |
| `CHAR-GROUP-TM-05` | 新增集数后角色别名重复、旧设计稿被覆盖或生成资产重跑 | 先执行增量对账，清单身份 merge 后只补缺设计/生成 | 旧角色设计与生成资产稳定，新角色追加 |
| `CHAR-GROUP-TM-06` | 角色叶子输出看似完整但像批量模板换名、锚点替换或句式轮换 | 标记 `REWORK-CHAR-PSEUDO-DIFF`，返工到命中叶子创作/裁决节点 | 叶子 review 记录反脚本化伪差异已通过 |
| `CHAR-GROUP-TM-07` | 父包只做目录导航，叶子路由靠经验猜测 | 补 Type Routing Matrix、Thinking-Action Node Map、Module Trigger Matrix 和 Convergence Contract，把路由、证据和返工点收回 `SKILL.md` | 任意角色域任务都能留下 selected_mode、loaded_leaf_manifest 和未命中叶子无输出证据 |

## Repair Playbook

1. 先判断问题是入口路由、上游缺失、叶子输出漂移还是 LLM-first 越权。
2. 路由问题只修组根 `SKILL.md` 或 registry routes；叶子业务问题下钻到具体叶子。
3. 下游缺输入时，回到最早缺失叶子，不用空文件或默认模板假装完成。
4. 发现项目级角色偏好、禁区或命名稳定要求时，优先写项目根 `MEMORY.md`。
5. 若经验只影响某个叶子，沉淀到该叶子 `CONTEXT.md`，不要上收到组根。
6. 分批追加上游时，角色域先保护既有角色文件与别名映射，再处理新角色；不要把新称呼直接生成成重复角色。
7. 发现脚本化、偷懒、未思考或未差异化的角色产物时，废弃候选稿并回到叶子 LLM-first 节点，不通过换脸谱词、换服装形容词或调 prompt 前后缀表层修复。

## Reusable Heuristics

- 角色域最稳的判断不是“用户提到角色就全跑”，而是“缺哪段 truth 就进哪段叶子”。
- 角色清单回答“有哪些主体”，角色设计回答“主体如何被制作”，角色生成回答“资产如何交付”，三者不要混写。
- 组根的价值是少做事但把路指准；一旦开始写角色正文，通常已经越过边界。
- 角色增量执行的首要风险是身份重复；新增称呼必须先与既有清单和设计稿对账。
- runtime-spine 升级时，组根优先补“路由真源”和“叶子加载证据”，不要把叶子创作细则上收到父包。
