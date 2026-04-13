# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/服装/1-清单` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 服装清单直接绕开 `角色清单.json` | 输入真源层 | 收回第一输入根到 `2-角色/1-清单/角色清单.json` | 在脚本和 SKILL 同时固定输入根 | 角色 identity 不再重复漂移 |
| `costume_state` 缺失导致服装条目混成一团 | 状态归一层 | 回退默认 `baseline` 并在 notes 中记录 | 在 bridge 中固定 `role_id + costume_state` 作为 costume 主键 | 同一角色多套服装能稳定分开 |
| 研究层只剩审美形容词 | 研究层 | 强制补 silhouette/material/accessory/continuity 四类字段 | 在输出模板中固定四类研究槽位 | `服装研究.json` 可直接支撑 `2-设计` |
| bridge 缺少可机读字段 | 设计桥接层 | 补 `prompt_anchor / layer_system / continuity_rules` | 把 bridge 视为设计输入而不是研究摘要 | `2-设计` 无需重做抽取 |
| 叶子合同只保留字段表，节点动作和返工路径不清 | 思行网络层 | 把输入锁定、状态归一、证据补包、研究链、bridge 链和汇流门写回同一 `SKILL.md` | 固化 `Thinking-Action Node Network + Capability Detail + Convergence Contract` | 叶子技能能独立闭环执行 |

## Repair Playbook

1. 先查 `角色清单.json.roles[]` 是否存在且包含 `costume_profile`。
2. 再查 `costume_state` 是否已稳定；缺失时保守回退为 `baseline`。
3. 只在角色证据和导演补充证据范围内抽服装，不补新角色。
4. 最后再补研究层与 bridge 的机读字段。

## Reusable Heuristics

- 服装对象池最稳的主键通常不是纯服装名，而是 `role_id + costume_state`。
- 服装链的研究层价值不在“多写审美词”，而在于把 silhouette/material/accessory/continuity 固化成后续可消费字段。
- 若角色链已经给出 `costume_profile`，服装链就不应再回头重做角色名提取。
- 对 `1-清单` 做知行合一改造时，最稳的方式是让 `catalog -> research -> bridge` 共享同一 costume 主键，而不是为每个输出各自解释一次输入。
