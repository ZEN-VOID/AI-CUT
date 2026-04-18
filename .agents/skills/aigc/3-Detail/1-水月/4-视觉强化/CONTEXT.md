# CONTEXT.md

## Purpose & Loading Contract

- 本文件保存 `4-视觉强化` 的经验层。
- 命中本 skill 时必须和同目录 `SKILL.md` 一起加载。

## Context Health

- `status`: ok
- `soft_limit_chars`: 40000
- `hard_limit_chars`: 80000
- `soft_limit_cases`: 80
- `hard_limit_cases`: 140
- `maintenance_note`: 当前以知识库模式维护；优先更新 Type Map / Playbook / Heuristics，不追加流水账。

## Type Map

| failure_or_outcome_type | immediate_fix | verification_point |
| --- | --- | --- |
| 视觉强化太多导致失焦 | 只保留一个 `冲击力` | 第一眼重点唯一 |
| `品味` 变成空话 | 改写成可拍行为或构图收益 | 后续 `分镜构图` 可直接消费 |
| 叶子模块跑完但无法汇成 canonical 三槽位 | 回到 `SKILL.md` 的 `N4-FOCUS-SYNTHESIS`，按 `visual_hook/concrete_detail/viewing_flow` 显式映射到 `冲击力/观赏性/品味` | `视觉强化` 三槽位齐全且没有内部字段泄漏到最终 patch |
| 视觉强化开始越权扩写成独立美术设定 | 回退到 `N2-VISUAL-SEED-READ`，重新从当前组事实与已写回上游字段抽取视觉接口，只做增益不另起炉灶 | 输出仍只命中 `视觉强化`，且能回指当前组已有戏剧收益 |

## Repair Playbook

1. 先看 `FIELD-WV-01/02` 是否确认了当前 root 与 visual-only ownership；若没有，先修输入锁定，再修文字。
2. 再看 `FIELD-WV-03/04/05` 是否分别留下了抓手、具像细节、拖速删减证据；若缺任一项，不要直接硬写最终三槽位。
3. 最后只在 `FIELD-WV-06` 做三槽位汇流；若最终结果还是空话，优先回退到叶子节点补 evidence，而不是继续加形容词。

## Reusable Heuristics

- 视觉强化不是加形容词，是给镜头一个必须看见的东西。
- `观赏性` 要服务主冲突，不要自己抢主线。
- `冲击力` 由 `冲击力` 决定，`品味` 由 `品味` 收口，`观赏性` 由 `观赏性` 清拖速；不要让三者在最终汇流时重新打架。
- 当叶子模块已经提供足够 evidence 时，最终汇流只做映射与减法，不再重新发明新的视觉亮点。
