# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `references/character-card-module/`，用于沉淀角色模块的局部故障模式、返工顺序与复用启发。
- 固定加载顺序：先读同目录 [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/module-spec.md)，再按需读取本文件；不得反过来用经验层替代规范合同。
- 若经验跨越角色/场景/物品多个模块，必须回写根 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)，不能滞留在本地经验层。

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
| 角色很多但互相撞位 | 角色桶设计 | 先回查 `narrative_function` 与关系边，再删并或重分桶 | 把“功能桶先于设定细节”写成角色模块硬启发 | 每张主角色都能回答自己推进哪类戏 |
| 时间线写成事件流水账 | Character Time Contract | 把事件改写为成长阶段与认知转折 | 强制保留 `experience_timeline + timeline_anchor` 双锚点 | 时间线能说明“角色因此变成什么” |
| 专属物像通用道具 | 跨模块接口 | 回补 `exclusive_item_hooks` 与角色欲望/行动方式 | 角色模块先留专属物接口，物品模块再做适配收束 | 专属物能一眼看出角色归属 |
| 模块文档退化成字段摘要卡，执行者看不出何时进入本模块 | governed reference contract | 回读父 `SKILL.md` 路由与当前 `module-spec.md` 六块合同，先补路由与阶段，再补单卡内容 | 把“适用场景 -> 预加载上下文 -> 思维链 -> Phase -> 交付 -> 验收”固定为角色模块最小合同 | 执行者仅读本模块也能判断触发条件、返工入口与交付落点 |

## Repair Playbook

1. 先判断问题是路由错误、角色桶失衡、关系链断裂，还是时间线/专属物接口失真。
2. 若执行者无法一句话说明“为什么现在进入角色模块”，先回父 `SKILL.md` 做对象路由，不直接改角色内容。
3. 若角色撞位，先修 `narrative_function` 和 `relationship_edges`，不先叠设定。
4. 若成长弧失真，回到 `experience_timeline`，不要把 MAP 事件流水直接抄进卡。
5. 若专属物失真，先补 `exclusive_item_hooks`，再把约束交给物品模块。

## Reusable Heuristics

- 角色模块的第一问不是“酷不酷”，而是“这张卡负责哪类戏”。
- `experience_timeline` 的价值在于沉淀成长含义，不在于罗列发生过什么。
- 专属物接口越早留出，后面的物品模块越不容易模板化。
- 角色模块的 `方向轴` 不该落在“设定浓度”，而应落在 `角色戏份职责对齐`；否则角色会越写越满，戏份却越来越虚。
- 如果角色模块看起来只有字段表、没有 `Phase` 和验收门禁，它就已经退化回旧 reference 摘要卡了。

