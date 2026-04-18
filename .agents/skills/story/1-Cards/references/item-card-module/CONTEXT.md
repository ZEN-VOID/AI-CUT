# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `references/item-card-module/`，用于沉淀物品模块的局部故障模式、返工顺序与复用启发。
- 固定加载顺序：先读同目录 [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/module-spec.md)，再按需读取本文件；不得用经验层替代物品模块的规范合同。
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
| 重要物没有归属也没有代价 | 物品核心合同 | 回补 `ownership_links` 与 `usage_rules.costs` | 把“归属 + 功能 + 代价”设为重要物最小三元组 | 重要物能回答属于谁、做什么、要付什么 |
| 专属物过于模板化 | 角色接口消费 | 回读角色卡切片并补 `exclusive_fit / exclusive_item_hooks` | 物品模块默认把角色卡切片当硬输入，而不是可选背景 | 专属物像角色本人，不像通用装备 |
| 线索物和重要叙事物混桶 | 物品分类 contract | 按剧情作用而非价值高低重新分桶 | 固化“线索指向发现，重要叙事物改变局势”的判定语义 | 两类物品的剧情用途清晰分离 |
| 模块文档退化成物件设定摘要，执行者看不出何时进入本模块 | governed reference contract | 回读父 `SKILL.md` 路由与当前 `module-spec.md` 六块合同，先补路由与阶段，再补物品内容 | 把“剧情杠杆对齐 -> 归属与代价闭合 -> 专属信号收益比”固定写进思维链和阶段流程 | 执行者只读本模块也能判断何时进入、何时返工、何时回接 gate |

## Repair Playbook

1. 先判断问题是路由错误、归属链缺失、专属适配失真，还是分桶错误。
2. 若执行者无法回答“为什么要进物品模块而不是角色/场景模块”，先回父 `SKILL.md` 重做对象路由。
3. 若重要物空心，先补 `ownership_links + usage_rules + active_plot_load`。
4. 若专属物模板化，回读角色卡切片和 `exclusive_item_hooks`，不要只改物品表面描述。
5. 若线索物与叙事物混桶，按剧情作用重分桶，再看是否需要减量。

## Reusable Heuristics

- 物品卡最值钱的是“为什么这件东西非它不可”，不是设定名词密度。
- 专属物的风格匹配要落在欲望、行动方式和代价结构上，不只落在外观。
- 线索物负责打开认知，重要叙事物负责改变局势，两者不要混成“大事物”一桶。
- 物品模块的 `成立轴` 若不直接落到 `ownership_links + usage_rules + exclusive_fit`，执行者几乎一定会把“有名字的道具”误判成“成立的物品卡”。
- 如果物品模块读起来只有字段清单、没有 `Phase` 和验收门禁，它就已经退化回旧 reference 摘要卡了。

