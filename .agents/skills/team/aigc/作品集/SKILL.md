---
name: team-work-dimension-root
governance_tier: lite
description: "Use when a named film, series, or work perspective is needed for creative analysis."
---

# Team · 作品维度

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若继续命中某个具体作品条目，必须再加载该作品目录下的 `SKILL.md` 与同目录 `CONTEXT.md`。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > `team/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md` > 具体作品条目 `SKILL.md` > 具体作品条目 `CONTEXT.md`。

> 作品维度不扮演作者本人，它提炼的是一部作品已经成形的世界语法、主题张力和场景运行规则。

## Scope And Truth Ownership

| 层级 | 真源职责 | 不拥有的内容 |
| --- | --- | --- |
| `作品维度/SKILL.md` | 作品型 skill 的路由规则、边界、加载顺序与 side-input 原则 | 单部作品的具体模型、研究事实、局部语气 |
| `作品维度/CONTEXT.md` | 跨作品的复用 heuristics、常见误路由与治理经验 | 单作品细节、具体场景分析底稿 |
| `作品维度/<作品>/SKILL.md` | 单部作品的主题、形式、世界规则、回答流程与事实边界 | 作者全生涯方法论、其他作品共用规则 |
| `作品维度/<作品>/CONTEXT.md` | 单部作品的局部 heuristic、陷阱与修复策略 | 跨作品规则、team 根级路由经验 |

## Trigger And Non-Goals

使用本技能的场景：

- 用户明确点名某一部作品，如“像《银翼杀手2049》那样处理”“用《花样年华》的方式看这场戏”。
- 用户要借某部作品的单一语法，而不是调用该作品导演/编剧/演员的整个方法论。
- 用户要求维护 `.agents/skills/team/作品维度/` 下的技能结构、路由或真源边界。

不使用本技能直接替代的场景：

- 用户明确要“某导演/某编剧/某摄影”的思维方式，此时优先进入人物 skill。
- 用户只是要百科式剧情简介、奖项列表或粉丝向 trivia，不需要作品语法提炼。
- 用户的问题显然属于跨作品史论或作者论；此时作品维度只能做 side input。

## Route Decision

1. 先锁定用户要借的是“作品整体语法”还是“创作者本人方法”。
2. 若用户点名单部作品，优先进入对应条目。
3. 若用户同时点名作品和创作者，默认以作品为主、创作者为 side input；除非用户明确要求反过来。
4. 若用户只描述“像某部作品那样的气质”，但作品条目不存在，可先创建作品条目，或临时说明最接近的现有条目与缺口。
5. 作品型问题涉及真实上映、奖项、票房、版本、删减、续作状态等事实时，必须先核验来源，再进入作品语法判断。

## Output Contract

默认输出收束为一个结果，而不是散乱的影评摘抄：

1. `核心判断`：这部作品真正可复用的东西是什么。
2. `作品语法`：主题、结构、空间、声音、角色、场景运行规则。
3. `可迁移用法`：如何借到新的剧本、分镜、设计或制作问题里。
4. `风险/误用`：最容易把这部作品借坏的方式。

## 字段中心映射（Tier-Lite）

| field_id | 触发问题 | 处理动作 | 质量维度 | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `work_lock` | 用户点名具体作品 | 锁定唯一作品条目与版本语境 | 对象唯一 | `work_ambiguous` | 先澄清作品对象 |
| `grammar_scope` | 想借作品风格 | 区分主题/形式/世界规则/场景机制 | 借力准确 | `work_generic_style` | 重写为具体作品语法 |
| `creator_side_input` | 同时提到导演/编剧 | 只在必要时把人物 skill 作为 side input | 真源边界 | `work_creator_blur` | 重新分配主从关系 |
| `fact_gate` | 奖项/上映/版本/续作 | 先核验来源，再给作品判断 | 事实安全 | `work_fact_unverified` | 补核验或降级为推断 |
| `transfer_rule` | 想把作品方法迁移到新任务 | 生成“可借/不可借/怎么借” | 可执行性 | `work_nonportable` | 补迁移规则和误用提醒 |

## 根因执行合同

当作品型 skill 出现“被误路由成人物 skill”“只剩剧情简介”“只会复刻表面美术”“事实越界”时，必须按以下链路修复：

`Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

- Direct Technical Cause：定位是对象未锁定、作品/作者边界混淆、事实核验缺口，还是迁移规则写得过泛。
- Rule Source：优先检查本 `SKILL.md` 的路由规则，以及命中作品条目的 `SKILL.md` / `CONTEXT.md`。
- Meta Rule Source：上溯到 `team/SKILL.md` 与仓库根 `AGENTS.md` 的路由、根因优先和 canonical source 规则。
- Fix Landing Points：共享规则写回本根 `SKILL.md` / `CONTEXT.md`；单作品问题写回对应作品目录。

## 诚实边界

- 作品维度 skill 提炼的是“已完成作品的运行逻辑”，不是作者私人动机真相。
- 对争议、隐喻和政治含义，只能基于公开材料做高置信提炼，不替创作者宣布唯一正确解读。
- 若用户需要的是作者全生涯方法、产业履历或人格判断，应切换到人物 skill。

