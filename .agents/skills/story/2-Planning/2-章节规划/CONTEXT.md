# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `2-章节规划` 子技能包的局部经验层，只服务 `2-Planning` Step 2。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨 child 的挂章与 holomap 收束经验仍回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 章节规划只有数量没有功能槽 | child contract | 补齐 chapter / volume blocks 与 function slots | 在子技能合同固化章节容器优先级 | Step 3-8 能稳定挂入章节容器 |
| 体量与对象密度失衡 | density contract | 回修 density contract 的区间带 | 在 Step 2 统一裁决密度，不让后序重发明 | holomap 能回指各类对象负荷 |
| drafting 无法挂章 | handoff contract | 回到本 child 修章节容器，而非直接补 holomap | 固化“挂章失败先回 Step 2” | 下游不再出现临时拼章板 |

## Repair Playbook

1. 先估算整书体量与卷数，再定章节容器。
2. 再把角色、线索、伏笔等负荷翻译成 density contract。
3. 检查关键节奏窗口是否显式存在。
4. 收尾用 Step 3 和 Step 8 反查容器是否可消费。

## Reusable Heuristics

- 章节规划最怕“平均主义”，真正稳定的是功能槽而不是均分章数。
- 当长线负荷上升时，应优先增加稳定挂点，而不是只增加章节总量。
- Step 2 如果没站稳，后面的故事大纲和 holomap 通常都会看起来“像对的”，但用起来发虚。
