# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global/设计元素` 的经验层知识库，不是过程日志。
- 调用本技能时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~2600
current_lines: ~55
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-13T23:30:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只看 `0-Init` 不看 `3-分组`，导致设计元素漂浮 | 主输入优先级层 | 回到 grouped script，重做阶段与世界证据摘要 | 在 `SKILL.md` 固化 `3-分组 > 0-Init` 的主辅关系 | 输出能明确引用 grouped script 证据 |
| 古代题材出现跨朝代、跨地域错植 | 时代路由层 | 重新锁定朝代 / 地域 / 阶层 / 工艺约束，并写清禁区 | 在 `era-routing.md` 固化古代路由与禁借检查 | 文稿能解释“不该出现什么” |
| 现代题材只写“像某大师”，没有机制和词汇母句 | 灵感抽象层 | 把参考改写为轮廓、材料、比例、空间秩序和词汇句法 | 在模板固定“借机制不借表皮”与“词汇造句”章节 | 下游能直接复用设计句 |
| 未来题材只剩炫技，没有社会/技术/资源逻辑 | 世界观约束层 | 回写技术水平、资源结构、社会秩序或宗教审美依据 | 在 `Convergence Contract` 固定“未来题材必须可回指世界逻辑” | 超现实元素能说清为什么成立 |
| 只写服装，不写建筑场景，或反之 | 双线收束层 | 回到双设计线节点补齐缺失一侧 | 在 `N4/N5/N8` 固化双线缺一不可 | 成稿同时具备两条设计线 |
| 文稿只有静态总则，没有阶段成长与变化 | 阶段演化层 | 补写开端 / 发展 / 转折 / 后段的设计变化矩阵 | 在 `N6-EVOLUTION-ARC` 固化阶段矩阵必填 | 输出能看到成长、异化或衰败规律 |
| 输出只有形容词堆叠，下游无法继承 | handoff 层 | 重写为“设计主陈述 + 词汇母句 + 禁区”三件套 | 在模板中固定下游 handoff 章节 | `4-Design` 可直接抽取设计指令 |

## Repair Playbook

1. 先查是否真正读取了 `1-Planning/3-分组/第N集.md` 作为第一主输入。
2. 再查时代判型是否已经落到 `古代 / 现代 / 未来 / 混合` 中的一条稳定路由。
3. 再分别检查服装线和建筑场景线是否都写出了主陈述、词汇母句和禁借项。
4. 再查阶段成长矩阵是否能覆盖全剧或至少覆盖明确的阶段变化。
5. 最后检查输出是否能被下游 `4-Design` 直接继承，而不是重新猜测。

## Reusable Heuristics

- `设计元素` 最稳的起手式不是先找参考图，而是先看 grouped script 中人物阶层、空间秩序、文明压力和叙事阶段如何反复出现。
- 古代题材里，最重要的不是“更华丽”，而是“更像这个地域、这个阶层、这个工艺条件真正能长出来的东西”。
- 现代题材最值钱的借法，不是抄某个秀场或某栋建筑，而是抽取设计师如何处理轮廓、比例、材料碰撞、秩序感和人格化空间。
- 未来题材的超现实只有在同一世界规则里同时支撑服装和建筑时才成立；否则只是两套孤立 moodboard。
- 对下游最有用的设计定调，通常不是长段抒情，而是“主陈述 + 设计词汇母句 + 明确禁区 + 阶段变化”。
