# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-服装/1-清单` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 服装清单直接绕开 `角色清单.json` | 输入真源层 | 收回第一输入根到 `2-角色/1-清单/角色清单.json` | 在脚本和 SKILL 同时固定输入根 | 角色 identity 不再重复漂移 |
| `costume_state` 缺失导致服装条目混成一团 | 状态归一层 | 回退默认 `baseline` 并在 notes 中记录 | 在 bridge 中固定 `role_id + costume_state` 作为 costume 主键 | 同一角色多套服装能稳定分开 |
| 研究层只剩审美形容词 | 研究层 | 强制补 silhouette/material/accessory/continuity 四类字段 | 在输出模板中固定四类研究槽位 | `服装研究.json` 可直接支撑 `2-设计` |
| bridge 缺少可机读字段 | 设计桥接层 | 补 `prompt_anchor / layer_system / continuity_rules` | 把 bridge 视为设计输入而不是研究摘要 | `2-设计` 无需重做抽取 |

## Repair Playbook

1. 先查 `角色清单.json.roles[]` 是否存在且包含 `costume_profile`。
2. 再查 `costume_state` 是否已稳定；缺失时保守回退为 `baseline`。
3. 只在角色证据和导演补充证据范围内抽服装，不补新角色。
4. 最后再补研究层与 bridge 的机读字段。

## Reusable Heuristics

- 服装对象池最稳的主键通常不是纯服装名，而是 `role_id + costume_state`。
- 服装链的研究层价值不在“多写审美词”，而在于把 silhouette/material/accessory/continuity 固化成后续可消费字段。
- 若角色链已经给出 `costume_profile`，服装链就不应再回头重做角色名提取。

## Case Log

### Case-20260412-AIGC-COSTUME-LIST-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/3-服装/1-清单` 建立了 extract 层合同、经验层、openai 入口和最小 runner。
- root_cause_or_design_decision: `3-服装` 需要独立 design-source，但若直接重扫导演 JSON，会与 `2-角色/1-清单` 抢 canonical identity 真源。
- final_fix_or_heuristic: 将 `角色清单.json` 固定为第一输入根，只把导演 episode JSON 作为证据补包，从而把服装链定义为“角色清单下游的对象池收束”。
- prevention_or_replication_checklist:
  - [x] 第一输入根已固定为 `角色清单.json`
  - [x] 三份 JSON 输出已建立
  - [x] runner 已提供最小可执行入口
- evidence_paths:
  - `.agents/skills/aigc/4-Design/3-服装/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/1-清单/scripts/extract_costume_catalog.py`
  - `.agents/skills/aigc/4-Design/2-角色/1-清单/SKILL.md`
- user_feedback_or_constraint: 用户要求参照角色/场景/道具家族，把服装链补齐到同等治理层级。
