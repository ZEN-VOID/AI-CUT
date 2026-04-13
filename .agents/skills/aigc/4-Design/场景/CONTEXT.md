# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/场景` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 场景类目没有先做清单就直接进入设计 | 类目路由层 | 回退到 `1-清单` 先产出场景对象池 | 固化 `清单 -> 设计 -> 面板` 的默认顺序 | 下游能复用同一份场景清单 |
| 场景设计叶子技能缺父层边界 | 类目治理层 | 先补 `1-场景` 父级合同，再让 `2-设计` 成为设计入口 | 保持类目父级作为路由真源，叶子技能只承接局部执行 | `1-场景` 不再是空目录 |
| 场景链继续依赖外挂 scene-design agent 合同 | 真源治理层 | 把有效能力面收回 `2-设计/SKILL.md` | 在父级合同中明确外挂真源已退役 | 路由与技能加载不再回指 `.codex/agents/aigc/设计组/场景设计` |
| 场景链有设计 carrier，但没有面板收口入口 | 下游承接层 | 补齐 `3-面板` 叶子技能，让 `panel_handoff` 有实际接收方 | 在父级合同中把 `3-面板` 维持为 active | `2-设计 -> 3-面板` 链路打通 |

## Repair Playbook

1. 先查输入是否已有 `1-清单` 的 scene catalog。
2. 再查当前任务是否真的需要场景设计，而不是图片生成。
3. 若进入 `2-设计`，优先检查其主合同是否已内收能力镜面，而不是继续加载外挂 agent 文档。
4. 若进入 `3-面板`，优先检查 `场景设计.json -> 场景面板.json` 的 carrier handoff 是否闭环。

## Reusable Heuristics

- 场景链的第一真源不是设计稿，而是先由 `1-清单` 锁定的 scene catalog。
- 当用户要求把外挂能力“融合回 `SKILL.md`”时，父级最重要的职责是先改路由口径，明确新真源落在叶子技能主合同，而不是只删旧目录。
- 一旦 `2-设计` 已经内收全部能力镜面，父级就不应再把场景设计描述成“外挂 agents 协作”的系统。
