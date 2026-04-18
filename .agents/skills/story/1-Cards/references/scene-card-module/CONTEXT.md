# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `references/scene-card-module/`，用于沉淀场景模块的局部故障模式、返工顺序与复用启发。
- 固定加载顺序：先读同目录 [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/module-spec.md)，再按需读取本文件；不得用经验层替代场景模块的规范合同。
- 若经验同时影响角色/场景/物品多个模块，必须回写根 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)，不能把跨模块路由经验滞留在本地。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- action_policy: 优先更新 Type Map / Repair Playbook / Reusable Heuristics，仅在里程碑事件追加 Case Log。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 场景像布景板，不像可写戏空间 | 场景功能合同 | 先补 `narrative_functions` 与 `compatible_roles` | 固化“规则先于奇观”与“谁来做什么”双问法 | 场景能回答进入者、目的与代价 |
| 超现实场景失控 | 世界规则接口 | 回补 `rule_and_risk.scene_rules / hazards / costs` | 强规则项目优先读取 `world-rules.md` 再做感官展开 | 超现实场景不再只剩氛围词 |
| 场景复用策略缺失 | 重复出场 contract | 回补 `current_focus.repeat_use_strategy` 与 `scene_links` | 将常驻场景优先级写成场景模块固定启发 | 常驻场景能说明不同阶段的用法变化 |
| 模块文档退化成空间设定摘要，执行者看不出阶段和门禁 | governed reference contract | 回读父 `SKILL.md` 路由与当前 `module-spec.md` 六块合同，先补路由与 `Phase` 再补场景内容 | 把“功能对齐 -> 规则闭合 -> 复用优选”固定写进思维链和阶段流程 | 执行者只读本模块也能判断何时进入、何时返工、何时回接 gate |

## Repair Playbook

1. 先判断问题是路由错误、功能缺失、规则失真，还是复用策略空洞。
2. 若执行者无法回答“为什么要进场景模块而不是角色/物品模块”，先回父 `SKILL.md` 重做对象路由。
3. 若只有画面没有戏，先补 `narrative_functions` 和 `compatible_roles`。
4. 若超现实场景浮空，回查 `world-rules.md` 和 `rule_and_risk`。
5. 若场景难以复用，补 `scene_links` 和 `repeat_use_strategy`，不要只加新地点。

## Reusable Heuristics

- 场景卡最值钱的是“允许什么戏发生”，不是“看起来多美”。
- 超现实场景一旦没有代价和限制，就会把世界规则冲穿。
- 常驻场景往往比奇观场景更能提升连载稳定性。
- 场景模块的 `优选轴` 不该再写成“更壮观”，而应写成 `复用回报比`；否则会不断制造一次性奇观，削弱连续叙事。
- 如果场景模块读起来只有空间描述、没有 `Phase` 和验收门禁，它就已经退化回旧 reference 摘要卡了。

