# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global/全局风格` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/全局风格/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 全局风格只读 `0-Init` 不读 `3-分组` | 输入优先级层 | 回到 grouped script 重做全剧证据摘要 | 在 `SKILL.md` 固定 `3-分组 > 0-Init` 的主辅关系 | 输出能明确引用 grouped script 证据 |
| 输出像单集导演意图，不像全剧风格母体 | 范围收束层 | 重新提炼跨集重复视觉信号与系列命题 | 在 `Convergence Contract` 固定“必须全剧级” | 成稿中能看到跨集稳定法则 |
| 大师灵感写成直接模仿某个导演/作品 | 灵感抽象层 | 把参考从“表皮元素”改写为“机制 + 禁借项” | 在 `masterwork-inspiration.md` 固化“借机制不借表皮” | 灵感矩阵同时包含借用项与拒绝项 |
| 风格句只有形容词堆叠，无法指导下游 | 句法执行层 | 重写为“词汇组 + 风格母句 + 继承法则”三件套 | 在模板中固定 `风格词汇造句 + 稳定继承法则` | 下游可直接抽用句子与 guardrails |
| 输出路径漂移回 `projects/<项目名>/2-Global/全局风格.md` | 真源治理层 | 改回子目录 canonical 输出 | 在 `SKILL.md` 固化 child-local canonical rule | 真源只存在于 `全局风格/全局风格设计.md` |

## Repair Playbook

1. 先确认 `projects/<项目名>/1-Planning/3-分组/` 是否已有完整 grouped script。
2. 再检查 `north_star.yaml` 与 `init_handoff.yaml` 是否只是补约束，没有越权代替主输入。
3. 再做大师灵感映射，强制写出“借用机制 / 拒绝照搬”。
4. 最后用模板写回，检查章节是否完整、是否是全剧视角、是否能直接给下游继承。

## Reusable Heuristics

- 对 `全局风格` 来说，最稳的起手式不是先想“这部片像谁”，而是先看 grouped script 在跨集维度重复出现了什么空间、节奏、光影和情绪结构。
- `0-Init` 最适合回答“这部片不能偏到哪里去”，`3-分组` 最适合回答“这部片在实际叙事里已经长成什么样”；前者定边界，后者定主形。
- 大师灵感最有价值的不是名字本身，而是其可迁移的视觉机制，例如空间秩序、光影哲学、情绪速度、镜面距离、现实/风格化比例。
- 风格词汇造句若不能被 `3-Detail / 4-Design / 5-Image` 直接复用，就说明它还不是合格的系列级风格母句。
- 当全局风格与类型元素未来并存时，最稳的分工是：`全局风格` 负责连续的视觉世界和感知方式，`类型元素` 再负责类型化的规则、母题和叙事偏压。
