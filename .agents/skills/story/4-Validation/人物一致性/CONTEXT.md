# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `人物一致性` 子技能包的局部经验层，只服务人物一致性维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 父层聚合、route 与 source trace 经验不在本地重复维护。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 角色行为怪，但报告说不出为什么怪 | character state read | 回到当前态、关系压力与近期 history | issue 必须指向“违背了哪一条当前态/关系态” | OOC 结论不再只靠主观感觉 |
| 角色没有明显 OOC，但整场戏只剩功能推进、看不见个性和偏移 | arc visibility check | 回到本集压力点，补“他想要什么、怕什么、因此怎么偏移” | 人物一致性维度把“功能性空转”单列为 Step 4 返工信号 | validation 不再只拦错，不拦空 |
| 多视角/证词场里人人都像作者代言人 | self-justification differentiation | 回到每个角色最想保住的体面与省略事实重写 | 在人物一致性维度固定检查“不同角色是否保护不同版本的自己” | 罗生门式结构不再写成统一口径分段复述 |
| 宏观设定很强，但人物只负责解释系统，不负责承担系统 | system-pressure embodiment | 回到角色在命令链、装置、倒计时和集体代价中的位置重写 | 在人物一致性维度固定检查“系统压力是否压到人” | 人物不再只是灾难/科幻设定的讲解器 |
| 对白不对劲，却被笼统写成“人物扁平” | dialogue check | 拆成 `speech_violations` 与 `manual_exposition` | 在人物维度输出中固定保留声口问题槽位 | drafting 能精确回到对白优化 |
| 关系突然升降温，但没有被抓到 | relationship pressure | 把关系压力变化视为硬证据而非软感受 | 维度报告保留 `relationship_pressure_drops` | 关系线跳变不再漏检 |
| 主角明明启用了成长系统，但新一集完全看不见技能/心路/情感承接 | growth continuity | 先读 `current_state.growth_state`，再找正文中的延续信号 | 人物一致性维度固定保留 `growth_continuity_checked` 与增长轴快照 | 主角成长不会只停在 cards 里，正文里也能继续被看见 |
| Step 4 inline 被对白问题误判阻塞，导致下一步还没开始就先被卡住 | step ownership boundary | Step 4 只拦行为/关系失真，把纯 `speech_violations` 延后到 Step 5 | runner 按 `current_step_id` 区分 Step 4 与 Step 5 的声口 gate | Step 4 可通过，Step 5 仍会真实拦截对白问题 |

## Repair Playbook

1. 先锁人物当前态、最近 history 与关系压力。
2. 若主角启用了成长系统，再锁 `growth_state.skill / heart / emotion` 当前段位与 tension。
3. 再看行为、个性化偏移、自我辩护差异、系统压力承担与对白是否顺着这些状态长出来。
4. 若问题主要出在说话方式，优先回 `5-对白优化`；若是内心活动像作者评论或 POV 漂移，优先回 `6-心理活动描写`；若是行为/动机失真，再回 `4-角色形象刻画`。
5. `drafting_inline` 下若当前是 `Step 4`，对白问题默认记为 Step 5 待处理项，不得把 Step 5 的工序债务提前当成 Step 4 的阻塞失败。

## Reusable Heuristics

- 人物一致性不是“人设标签还在不在”，而是“这个人在当前压力下会不会这么做、这么说”。
- 人物一致性不只检查“错没错”，还要检查“是不是只剩功能”；没写崩不等于写活了。
- 当证词彼此冲突时，一致性不是让他们说出同一真相，而是让他们各自保护不同的自己。
- 当世界规则被改写时，人物一致性还包括“这个人会怎样理解和承担新的规则代价”，否则人物很容易退化成设定讲解员。
- 角色问题最怕只给形容词，不给违反了哪条当前态证据。
