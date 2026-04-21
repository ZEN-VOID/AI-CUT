# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-线索设计` 子技能包的局部经验层，只服务 `2-Planning` Step 6。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 线索只有答案，没有发现路径 | child contract | 回到证据源 / 承载物 / 发现者 | 在子技能中固定 evidence gate | board 能回答信息如何被获得 |
| 误导只是遮蔽，不服从证据 | fairness contract | 重写 false lead 与 correction point | 把公平误导写成硬门 | 读者可回查证据链 |
| 线索没有挂回 chapter board | patch writeback | 补 `board.clues` refs | 固化本 child 对 clue refs 的 ownership | 后续 query 不再失去信息节点 |

## Repair Playbook

1. 先确认 Step 5 的任务链稳定。
2. 再锁证据源、承载物与发现者。
3. 再判断误导是否服从证据。
4. 收尾把线索 refs 挂回 board。

## Reusable Heuristics

- 线索 child 的关键不是“信息量多”，而是“信息怎么被公平获得”。
- 如果误导不服从证据，后续揭晓很容易像作者强行解释。
- board 没有 clue refs 时，query 很难回答“这章多知道了什么”。
- 卷分片模式下，线索 master 留在 global，章节 clue refs 与发现窗口写入 slice；不要把整套 clue detail 再复制回 root。
