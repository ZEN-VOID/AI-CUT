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
| 对白不对劲，却被笼统写成“人物扁平” | dialogue check | 拆成 `speech_violations` 与 `manual_exposition` | 在人物维度输出中固定保留声口问题槽位 | drafting 能精确回到对白优化 |
| 关系突然升降温，但没有被抓到 | relationship pressure | 把关系压力变化视为硬证据而非软感受 | 维度报告保留 `relationship_pressure_drops` | 关系线跳变不再漏检 |

## Repair Playbook

1. 先锁人物当前态、最近 history 与关系压力。
2. 再看行为与对白是否顺着这些状态长出来。
3. 若问题主要出在说话方式，优先回 `5-对白个性化和声口优化`；若是行为/动机失真，优先回 `4-角色形象刻画`。

## Reusable Heuristics

- 人物一致性不是“人设标签还在不在”，而是“这个人在当前压力下会不会这么做、这么说”。
- 角色问题最怕只给形容词，不给违反了哪条当前态证据。
