# Chapter Rhythm Execution Contract

## Purpose

本文件是 `3-Drafting` 父层 owning 的 `Step 2 / 2-节奏优化` 正文兑现合同。

`2-Planning/3-章级` 已经持有章级节奏规则与 handoff 真源，因此 drafting 侧不再保留独立 `2-节奏优化/` 子技能目录；Step 2 继续作为正式 runtime 工序存在，但其执行规则统一回收到本 shared contract。

## Canonical Upstream

- `../../_shared/chapter-rhythm-handoff-contract.md`
- `../../_shared/core-constraints.md`
- `../../2-Planning/3-章级/references/chapter-rhythm-rules.md`

## Parent-Owned Scope

Step 2 固定拥有：

- 消费 planning 已锁定的 `selected_pack / selected_mode / 七步职责映射 / 规划义务 / 义务段位 / 建议写法`
- 把已锁 handoff 兑现成正文里的 `pulse_ladder`
- 段落并拆、局部前后重排、`reaction bridge`、`middle build`
- 在不破坏 planning 义务与设定物理的前提下强化读感起伏
- 依据 planning 已锁 mode 写回 frontmatter `rhythm_type`
- 为 inline validation 准备 Step 2 合规证据

Step 2 不拥有：

- 重定义 `selected_pack`
- 重定义 `selected_mode`
- 重画七步职责映射
- 把 planning 的结构义务偷偷改成别的交易
- 靠新增设定、新能力、新道具制造假高潮

## Required Inputs

- 当前 `第N章.md`
- `第V卷.写作日志.yaml`
- `2-Planning/整体规划.md`
- 当前卷 `2-Planning/第V卷/卷规划.md`
- 当前章 `2-Planning/第V卷/第N章.md`
- `../../_shared/core-constraints.md`
- 当前项目 `类型卡 / genre_corridor`（若存在）

## Step-2 Owned Moves

1. 把 planning 已锁 `entry_promise / conflict_axis / micro_payoff / exit_hook` 摆进正文里能被读者感知的位置。
2. 基于既有 handoff 建立 `pulse_ladder`。
3. 并段、拆段、前移有效脉冲、后置解释。
4. 补 `reaction bridge`。
5. 补 `middle build`。
6. 调整段尾牵引与章末续推。

## Practical Moves

### Entry Hook

- 第一屏优先处理“失衡”，不是处理“设定完整度”。
- 开头最常见的有效切口：
  - 某件事出错了
  - 某个秘密要露了
  - 某个欲望马上能摸到
  - 某个关系正要变
  - 某个危险已经逼近

### Pulse Ladder

`pulse_ladder` 不是第八个槽位，而是把七步骨架编排成读感起伏的方式。

常用编排：

1. `hook`
2. `promise visible`
3. `conflict`
4. `发展`
5. `升级`
6. `高潮`
7. `尾钩`

不是每章都必须 7 步等长齐全，但至少要有“引、推、变、升、收、续”。

## Handoff Consumption Checklist

- `entry_promise` 是否在第一屏或前两段内被感知到
- `conflict_axis` 是否不再停留在 planning 摘要，而是真正被场面化
- `micro_payoff` 是否被兑现为局面变化，而不是仍停在 promise
- `exit_hook` 是否从正文自然长出，而不是生硬断章

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
- 有转向，但没有后续发展与升级，高潮像凭空出现。
- 全章只有 `入场` 和 `尾钩`，中间没有任何兑现。
- 为了快，把必要因果剪断。
- 为了更刺激，临时发明新设定。
- 尾钩只是作者不肯结尾，不是人物和局势的自然余波。
