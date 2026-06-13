# CHANGELOG

## 2026-06-11

- 同步 `3-美学` 输出 scope：氛围阶段读取 `画面基调` 全局 singleton；角色风格和场景风格按当前 `第N集` 优先读取 `3-美学/第N集/<风格>/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`README.md` 与 agent prompt，执行报告需记录风格来源与 fallback。

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求每条选择性 `氛围画面` 证明来自 `5-表演` 触发点、表演焦点和 `3-美学` 三类协议。
- 新增 `FAIL-ATM-UPSTREAM-CONTEXT`、`GATE-ATM-20-UPSTREAM-CONTEXT` 和报告 `Upstream Context Application Map`，并将完成门扩展到 `GATE-ATM-01..20`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-07

- 曾新增动作破坏点 legacy reference 细则，将动作破坏点效果强化标准化为 `6-氛围` 的授权能力。
- 在 `SKILL.md` 接入 `destruction_fx` 触发类型、`FAIL-ATM-DESTRUCTION-FX`、`GATE-ATM-19-ACTION-DESTRUCTION-FX`、`Action Destruction FX Map` 和 module trigger 路由。
- 将白刃剑风、枪风、链镰、飞剑、断链余劲等冷兵器破坏，以及战争/废墟、惊悚追逐、海战水域、室内动作、奇幻仪式、现实街巷、科幻赛博等多类型破坏边界收束到同一细则。
- 同步 `CONTEXT.md`、`README.md` 和 `test-prompts.json`，补齐动作破坏点生硬、轻飘、法术化或现代 CG 化的修复经验与回归样例。
- 修正 legacy 动作破坏细则的触发表述：总入口改为“任何改变现场材质状态的力量、行动或余波”，港风武侠仅作为类型分支之一，并新增多类型分流回归样例。
- 为动作破坏点新增显式 `destruction_type_route` 证据链，挂钩用户信号、`3-美学`、`5-表演` 场景/动作/材质和项目 `MEMORY.md`；新增 `FAIL-ATM-DESTRUCTION-TYPE-ROUTE`，防止只靠关键词误判类型。
- 将动作破坏点能力从 legacy reference 全量迁移到 `types/action-destruction-fx/` 类型模块，由 `SKILL.md` 直接路由 `index.md` 和对应类型文件。
- 新增 `wuxia-hk-cold-weapons`、`fantasy-xuanhuan`、`war-ruins`、`thriller-chase`、`naval-water`、`interior-court`、`realism-street`、`sci-fi-cyber`、`generic-material-response` 九个动作破坏类型模块。
- 明确灵光、法阵、能量、护盾、粒子或科技光效不是统一禁词；只有在当前类型、上游 source、`3-美学` 或项目 `MEMORY.md` 未授权时才构成越界。

## 2026-06-04

- 初始化 `aigc/6-氛围` Skill 2.0 runtime-spine 包。
- 建立 `SKILL.md + CONTEXT.md`、`README.md`、`agents/openai.yaml`、`test-prompts.json` 和 `knowledge-base/physical-atmosphere-index.md`。
- 从 `2-编导/references/` 接入 `atmosphere-and-mood-contract.md` 与 `scene-rhythm-contract.md`，其中 `scene-rhythm-contract.md` 在本技能中作为视觉特效节奏细则使用。
- 固化核心输出口径：默认消费 `5-表演` 表演稿和 `3-美学` 的画面基调、角色风格、场景风格；只在渲染、烘托、增强触发点新增 `氛围画面：XXX`，不得每点硬加。
- 将烟雾/雾化、打灯与光束、风效、雨效、雪效、火与热感、水汽湿度、尘土灰烬、落叶花瓣纸片、天气模拟、投影影像环境、气味触感 12 类整理为 `physical-atmosphere-index.md` 的默认选择库。
