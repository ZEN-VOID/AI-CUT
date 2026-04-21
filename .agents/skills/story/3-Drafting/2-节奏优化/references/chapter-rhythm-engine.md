# Chapter Rhythm Engine

## Purpose

给 `3-Drafting/2-节奏优化` 用的单章节奏发动机。

本文件把“爆款网文单章节/单集节奏”收束为七个必检槽位：

1. `entry_hook`
2. `chapter_promise`
3. `conflict_axis`
4. `turn_or_reversal`
5. `reaction_decision`
6. `micro_payoff`
7. `exit_hook`

它不是题材模板，而是 chapter-level 的共性引擎。

## Research Basis

- WebNovel 平台作者教程对手机阅读、短段落、开篇 hook 与章末 `Next` 驱动的强调：
  - [How to write a WebNovel](https://www.webnovel.com/book/how-to-write-a-webnovel_32940691608320805/how-to-write-a-webnovel._94004531980976485)
- Reedsy 对节奏控制、句长/段长与 cliffhanger 的总结：
  - [Pacing in Writing: 10 Powerful Ways to Keep Readers Hooked](https://reedsy.com/blog/pacing-in-writing/)
- 中文网文实践里对爽点密度、阶段匹配和断层预警的归纳：
  - [AI一键织文十步创作法第五步：分卷节奏把控实操指南](https://www.niaogebiji.com/article-706188-1.html)

## Seven-Slot Engine

| slot | question | write move | anti-pattern |
| --- | --- | --- | --- |
| `entry_hook` | 为什么第一屏就要继续读？ | 尽快给变化、风险、异常、强情绪或局势失衡 | 先讲背景和设定，真正的事很晚才开始 |
| `chapter_promise` | 这章到底在解决什么？ | 让读者在前段知道“本章要交付的那一笔” | 全章有动作没交易，读者说不出这章要干嘛 |
| `conflict_axis` | 真正拦住人物的是什么？ | 写清目标、阻碍、代价，让章节不是自动前进 | 只有流程，没有碰撞 |
| `turn_or_reversal` | 这一章在哪一刻改向？ | 至少一次价值变化、局势翻面、误判暴露或压力升级 | 从头到尾一个方向推到底 |
| `reaction_decision` | 人物如何消化这一击，并决定下一步？ | 给出反应、两难、决定，形成下一步因果 | 只见动作，不见人物吸收 |
| `micro_payoff` | 本章至少收哪一笔？ | 至少兑现一次信息、关系、能力、资源、情绪或局面变化 | 全章只吊胃口不结账 |
| `exit_hook` | 读者为什么点下一章？ | 用 reveal / decision / threat / pressure transfer / quiet unease 留下余压 | 平收，或故意硬断在最热闹处但没有自然因果 |

## Practical Moves

### Entry Hook

- 第一屏优先处理“失衡”，不是处理“设定完整度”。
- 开头最常见的有效切口：
  - 某件事出错了
  - 某个秘密要露了
  - 某个欲望马上能摸到
  - 某个关系正要变
  - 某个危险已经逼近

### Chapter Promise

- Promise 不等于写作提纲，而是读者能感知到的“这章要给我什么”。
- 常见 promise：
  - 这次冲突谁赢
  - 这个误会会不会说破
  - 这条线索能不能拿到
  - 这个机会抓不抓得住
  - 这次压力会不会真正落下

### Conflict Axis

- 冲突不是“发生了事”，而是“人物的主动意图被某个力量阻住”。
- 最低配也要写清：
  - 角色这章想做什么
  - 谁/什么阻止他
  - 失败会损失什么

### Turn or Reversal

- 不是每章都要大翻盘，但每章最好至少有一次价值变化。
- 常见形式：
  - 原以为能赢，结果是假胜
  - 原以为完了，结果是假败后转机
  - 误会加深或被戳破
  - 时间压力突然落下
  - 外部压力转成内部压力

### Reaction Decision

- 冲突之后必须有人物吸收，不然章节只会越来越吵。
- 最常见的结构是：
  - 先反应
  - 再意识到新的两难
  - 最后作出下一步决定

### Pulse Ladder

`pulse_ladder` 不是第八个槽位，而是把七段发动机编排成读感起伏的方式。

常用编排：

1. `hook`
2. `promise visible`
3. `conflict`
4. `turn / reversal`
5. `reaction / decision`
6. `micro payoff`
7. `exit hook`

不是每章都必须 6 段齐全，但至少要有“引、推、变、收、续”。

### Micro Payoff

局部兑现不要求大高潮，但要求局面真的改变：

- 线索多知道了一格
- 关系更近或更坏了一格
- 主角得到了一个资源/位置/认可
- 某种情绪终于被戳破或释放

### Exit Hook

尾钩优先从本章现成压力里长出来。

优先级通常是：

1. `pressure transfer`
2. `reveal`
3. `decision`
4. `threat`
5. `quiet unease`

## Mobile-Read Notes

- 手机阅读优先短段、清句、快切换。
- “快”不等于全用短句，而是关键信息不要埋在厚重说明里。
- 当需要减速时，用在：
  - 关键情绪落点
  - 真正重要的感官/动作
  - 反转前的半拍停顿

## Anti-Patterns

- 第一屏还没有事件，只剩世界观说明。
- 角色想做什么不清楚，所以整章没有真正冲突。
- 有冲突，但没有转向，整章只是在加长同一件事。
- 有转向，但没有反应和决定，下一章目标像凭空出现。
- 全章只有 `entry_hook` 和 `exit_hook`，中间没有任何兑现。
- 为了快，把必要因果剪断。
- 为了更刺激，临时发明新设定。
- 尾钩只是作者不肯结尾，不是人物和局势的自然余波。
