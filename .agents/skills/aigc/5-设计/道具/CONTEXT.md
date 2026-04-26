# Context: aigc 5-设计/道具

## Purpose & Loading Contract

- 本文件是 `aigc-design-prop` 道具域组根的经验层，不是道具设定库，也不是执行流水日志。
- 调用 `.agents/skills/aigc/5-设计/道具/SKILL.md` 时，必须同时加载本文件。
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
| `PROP-GROUP-TM-01` | 用户只说“道具”但没有阶段 | 先查是否存在 `道具清单.md`、设计稿和生成资产，再路由到最早缺失叶子 | 不越级生成下游 |
| `PROP-GROUP-TM-02` | 用户把普通布景物都要求列道具 | 进入 `1-清单` 过滤判断，保留叙事/规则/视觉/生成锁定道具 | 背景杂物不污染主清单 |
| `PROP-GROUP-TM-03` | 下游设计发现清单漏项或误归并 | 下游只写修复建议，回到 `1-清单` 修主真源 | 清单仍为唯一上游 |
| `PROP-GROUP-TM-04` | 关键道具成为长期项目偏好 | 写项目根 `MEMORY.md`，不写入组根 CONTEXT | 项目记忆可回读 |

## Repair Playbook

1. 先判断问题是入口路由、上游缺失、叶子输出漂移、杂物过滤还是 LLM-first 越权。
2. 路由问题只修组根 `SKILL.md` 或 registry routes；叶子业务问题下钻到具体叶子。
3. 下游缺输入时，回到最早缺失叶子，不用空文件或默认模板假装完成。
4. 背景杂物过多通常不是 `2-设计` 问题，而是 `1-清单` 的主体过滤问题。
5. 若经验只影响某个叶子，沉淀到该叶子 `CONTEXT.md`，不要上收到组根。

## Reusable Heuristics

- 道具域的第一问是“这个物件是否需要被后续设计或生成锁定”，不是“文本里是否出现过一个名词”。
- 道具清单回答“哪些物件进入资产链”，道具设计回答“如何制作这个物件”，道具生成回答“如何交付可引用资产”。
- 组根越像交通标志越稳；一旦开始替道具写材质、结构或 prompt，就该下钻到叶子。
