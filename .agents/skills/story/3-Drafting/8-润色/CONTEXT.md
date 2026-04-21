# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `8-润色` 的局部经验层，只服务 `3-Drafting` Step 8。
- 先读 `SKILL.md`，再读本文件及四个局部子模块。
- 子模块级经验先落在对应 `module-spec.md` 邻近逻辑；跨模块经验再回写本文件或根级 `3-Drafting/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 润色后像“另一位作者”重写了前文 | polish overreach | 回到终修而非重起稿件的边界 | 在子技能硬写“润色不是再起一篇” | 前 7 步成果仍保留 |
| AI 评语腔、直白代答仍明显 | anti-commentary module | 优先执行 `反评论腔` 模块再做文笔优化 | 固定终修顺序先去评语再提文笔 | 叙述减少作者评判 |
| 文本更顺了，但角色和节奏被磨平 | polish flattening | 回查前 4-7 步特征点并恢复差异 | 在终修时保留人物/节奏差异为硬门 | 润色后仍保有角色与节奏层次 |
| 章节结尾为了做钩子，留下明显的提纲式问句或“问题只剩一个”这类外部发问 | hook-as-outline question | 改成危险逼近、余波未平、脚步声/消息声/人心变化等场面化收束 | 在终修层固定“结尾先让麻烦自己走近，再决定要不要发问” | 章末有续读感，但不露提纲骨架 |
| 终修后仍残留“卷次、阶段、时间压力落锁”这类 meta 表述 | meta residue after polish | 把外部术语收回到人物预感、局势收紧或未来麻烦的临场语言 | 终修时专门扫一遍“谁都不会在戏里这么说”的句子 | 不再出现破次元的项目管理口吻 |

## Repair Playbook

1. 先清理最显眼的评论腔和机械重复，再做自然感和文笔收束。
2. 若润色后味道变淡，先恢复人物差异和节奏脉冲，再继续修句。
3. 若文笔优化想走向“像某大师”，只取判断与气质，不取桥段与标志性套路。

## Reusable Heuristics

- 最危险的 AI 味常常不是词太普通，而是叙述者突然替读者解释“这一切意味着什么”。
- 真正自然的文本允许有轻微的不规则，而不是每句都圆、都满、都像模板。
- 章末最容易暴露“提纲感”的，不是有没有钩子，而是钩子是不是由作者亲自替故事发问；如果把问句换成脚步声、余波、将至的人或信，往往更像小说。
- 一旦某句里出现“第几卷、阶段、节点、时间压力落锁”这一类读者在戏内听不见的话，终修就该立刻把它打回人物经验层。
