# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `1-单集叙事起盘` 的局部经验层，只服务 `3-Drafting` Step 1。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨工序连续性经验优先回写到 `3-Drafting/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 起盘只剩提纲，没有完整正文 | child contract | 回到 scene chain，直接写完整初稿 | 在子技能合同固定“首轮必须完整可读” | `第N集.md` 已可通读 |
| 本集像凭空开始，没接上一集 | continuity bridge | 先抽上一集终稿的停点，再重写开篇 | 把上一集终稿设成 `N>1` 必需输入 | 开篇能回答“从哪接上” |
| 读到了 `story_map`，但仍不知道哪块 board 属于本集 | board locating contract | 先按 `episode_num / episode_id -> chapter_boards[].episode_ref` 定位唯一 board，再解码债务 | 在 shared contract 固定“直连 episode_ref，必要时 axis 回指，禁止数组顺序猜测” | `process_log_entry` 能说明本集 board 如何命中 |
| 只写事件，不写角色目标和阻力 | board decode | 重读 chapter board 的功能债与 threads 债务 | 先锁目标/阻力/代价，再写场景 | 初稿能回答“为什么现在要做这件事” |
| 为了兑现 planning，把“卷次/阶段/时间压力”等外部规划语言直接写进正文 | planning language leak | 改写成人物当下能感到的风险、代价、局势收紧或退路消失 | 起盘时先问“这句是谁能感觉到”，不是先问“planning 想表达什么” | 正文读起来仍在戏里，不会突然跳到提纲口吻 |
| 同一画面连续两句重复交代同一批人/同一组物件 | scene naming repetition | 第一处交代身份，第二处只推进姿态、构图或动作 | 起盘阶段把“身份信息”和“空间落位”分成两拍写 | 不再出现“平民/鱼篓/药包”在相邻句里重复点名 |
| 想桥接前作时，直接写成作者提示或外部说明 | legacy callback hard landing | 把互文改写成角色记忆、自嘲或旧伤被触发的瞬间 | 固定“旧作回响只能通过人物内部路径进场” | 前作桥接不会破坏当前章节沉浸感 |

## Repair Playbook

1. 先看本集 board 功能、上一集停点、当前压力位是否都已锁定。
2. 再检查 scene chain 是否形成了“起手 -> 推进 -> 变化 -> 钩子/兑现”的最小骨架。
3. 如果正文只是说明稿，优先补“人物要做什么、被什么拦住、付出了什么”。

## Reusable Heuristics

- 起盘最忌讳的是把 planning 翻译成“说明文”；它应该先长成故事，再留给后续工序精修。
- 跨集连续性的关键不在总结，而在抓住上一集最后一个真正改变了局面的点。
- board 未唯一命中前，不要急着写“本集要发生什么”；先解决“这到底是不是本集那块 board”。
- 起盘阶段最危险的破次元，不是词不漂亮，而是把规划层总结直接塞进角色视角里；只要一句话不像谁会在现场这么想，它就该回炉。
- 如果第二句的功能只是把第一句再说一遍，宁可删掉；起盘最需要的是“继续往前走”的句子，不是“确认刚才说过什么”的句子。
- 旧作互文真正有劲时，往往不是因为引用本身，而是因为当下场面逼得角色不得不想起那句话。
