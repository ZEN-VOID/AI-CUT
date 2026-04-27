# Chapter Rhythm Handoff Contract

`2-卷章规划/3-章级` 与 `3-初稿` 的 `Step 2 / 2-节奏优化` 共享这一份章级节奏移交合同。

## Ownership Split

### Planning Owns

- `selected_pack`
- `selected_mode`
- 七步职责映射
- 本章 `entry_promise / conflict_axis / micro_payoff / exit_hook`
- 哪些段位属于必须兑现的规划义务
- 哪些段位只是建议写法、允许 drafting 在不破义务时重排

### Drafting Step 2 Owns

- 把已锁定 handoff 兑现成正文里的 `pulse_ladder`
- 段落并拆、局部前后重排、`reaction bridge`、`middle build`
- 在不破坏 planning 义务与设定物理的前提下强化读感起伏
- `rhythm_type` 写回与最终合规审计

## Shared Base Spine

章级统一七步骨架固定为：

1. `入场`
2. `推动`
3. `转折`
4. `发展`
5. `升级`
6. `高潮`
7. `尾钩`

默认节奏包固定为：

- `动静结合`
  - `势能式`
  - `动能式`

## Required Handoff Slots

`2-卷章规划/第N卷/第N章.md` 的 `本章节奏曲线` 段必须至少包含以下槽位：

- `selected_pack`
- `selected_mode`
- `七步职责映射`
- `规划义务`
  - `entry_promise`
  - `conflict_axis`
  - `micro_payoff`
  - `exit_hook`
- `义务段位`
- `建议写法`
- `Mermaid` 节奏图

## Slot Semantics

- `selected_pack`
  - 说明本章调用的节奏包；当前默认值为 `动静结合`
- `selected_mode`
  - 说明本章当前 mode；合法值固定为 `势能式` 或 `动能式`
- `七步职责映射`
  - planning 负责回答每一步在本章究竟承担什么功能，而不是只写标签
- `规划义务`
  - 是 drafting 不得静默删失的结构义务
- `义务段位`
  - 只负责锁“必须出现什么 / 至少要完成什么”，不锁死具体段落长度与文面顺序
- `建议写法`
  - 只提供推荐落法、节奏取向与编排提示；drafing 可在合法边界内重排

## Non-Drift Rules

1. planning 锁的是义务与 mode，不是 Step 1 当前写法的逐段排版。
2. drafting 不得重新发明第二套 `selected_pack / selected_mode / 七步职责映射`。
3. 若正文要偏离已锁 handoff，必须回源到 `2-卷章规划/3-章级` 修 planning，而不是在 drafting 的 Step 2 静默改法律。
4. `micro_payoff` 不等于必须大高潮；只要局面真实改变，就可视为有效兑现。
5. `exit_hook` 必须从本章现有压力自然长出，不得靠生硬断章伪造牵引。
