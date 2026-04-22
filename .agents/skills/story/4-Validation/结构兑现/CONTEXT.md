# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `结构兑现` 子技能包的局部经验层，只服务结构验收维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨维度聚合经验优先回写到 `4-Validation/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 正文提到关键事件，但只是一句摘要，没形成戏剧兑现 | dramatization gate | 标成“弱兑现”，打回起盘或追读力强化 | 在本维度把“演出来”与“提到过”拆开记分 | 结构报告不再把摘要式交代误算为完成 |
| 章节功能写偏了，但 issue 只写成抽象低分 | obligation mapping | 直接回指 chapter_planning_packet 义务项 | 维度报告固定保留 `missed_obligations` 列表 | drafting 能知道到底缺哪一笔 |
| 结构问题被误判成人物或逻辑问题 | boundary split | 先回到“这集该不该发生这件事”再判其他维度 | 父层固定先聚合 structure，再看其他维度解释性 issue | issue 分类不再漂移 |

## Repair Playbook

1. 先读 `chapter_planning_packet`，列出本集必须兑现的义务。
2. 再用正文逐项对照，不要先凭阅读感受打总分。
3. 若正文只在总结段中交代关键信息，视为结构弱兑现而非完全通过。

## Reusable Heuristics

- 结构兑现最常见的假阳性，是“信息被提到过”但“故事没有真的发生过”。
- 如果读完一章后仍说不清这集完成了哪一笔规划债，结构维度通常就不该给高分。
