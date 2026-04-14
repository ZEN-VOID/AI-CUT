# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/1-主体清单/服装` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 服装清单直接绕开 `角色清单.json` | 输入真源层 | 收回第一输入根到 `4-Design/角色/1-清单/角色清单.json` | 在脚本和 SKILL 同时固定输入根 | 角色 identity 不再重复漂移 |
| `3-Detail` canonical 与 legacy `编导` 路径同时被当第一输入 | 真源治理层 | 固定 `3-Detail/第N集.json` 为 direct detail 补证主路径，`编导/第N集.json` 仅作 fallback | 在 sibling leaf 共享消费合同中统一 canonical / fallback 口径 | 服装链与角色/道具/场景的 detail 输入规则一致 |
| `costume_state` 缺失导致服装条目混成一团 | 状态归一层 | 回退默认 `baseline` 并在 notes 中记录 | 在 bridge 中固定 `role_id + costume_state` 作为 costume 主键 | 同一角色多套服装能稳定分开 |
| 导演句子残片被误升格成新 `role_id` 或新 costume identity | identity 归一层 | 先回链 `角色清单.json` 的 `role_id + canonical_name`，无法命中时忽略残片或回角色链修 canonical | 在 `references/type-strategies.md` 与主 `SKILL.md` 固定“identity 回角色链，不在服装链现场发明主键” | `服装清单.json` 不再出现无来源新角色 |
| 研究层只剩审美形容词 | 研究层 | 强制补 silhouette/material/accessory/continuity 四类字段 | 在输出模板中固定四类研究槽位 | `服装研究.json` 可直接支撑 `2-设计` |
| bridge 缺少可机读字段 | 设计桥接层 | 补 `prompt_anchor / layer_system / continuity_rules` | 把 bridge 视为设计输入而不是研究摘要 | `2-设计` 无需重做抽取 |
| 叶子合同只保留字段表，节点动作和返工路径不清 | 思行网络层 | 把输入锁定、状态归一、证据补包、研究链、bridge 链和汇流门写回同一 `SKILL.md` | 固化 `Thinking-Action Node Network + Capability Detail + Convergence Contract` | 叶子技能能独立闭环执行 |

## Repair Playbook

1. 先查 `角色清单.json.roles[]` 是否存在且包含 `costume_profile`。
2. 再查 `costume_state` 是否已稳定；缺失时保守回退为 `baseline`。
3. direct detail 证据默认先查 `3-Detail/第N集.json`，只有主路径缺失时才回退到 legacy `编导/第N集.json`。
4. 只在角色证据和导演补充证据范围内抽服装，不补新角色。
5. 最后再补研究层与 bridge 的机读字段。

## Reusable Heuristics

- 服装对象池最稳的主键通常不是纯服装名，而是 `role_id + costume_state`。
- 服装链的研究层价值不在“多写审美词”，而在于把 silhouette/material/accessory/continuity 固化成后续可消费字段。
- 若角色链已经给出 `costume_profile`，服装链就不应再回头重做角色名提取。
- 如果导演句子里冒出未 canonicalize 的人名残片，优先把它当作角色链待修缺口，而不是在服装链里临时发明新 `role_id`。
- 对 `1-清单` 做知行合一改造时，最稳的方式是让 `catalog -> research -> bridge` 共享同一 costume 主键，而不是为每个输出各自解释一次输入。
- 当多个 sibling leaf 共用 `3-Detail` 作为上游时，应先在共享合同里统一 canonical 路径和字段映射，再分别细化各自的抽取节点；否则最容易出现一个 leaf 修好了、另一个 leaf 继续沿旧 alias 漂移。
- 服装链的四文件输出之所以成立，不是因为“文件越多越好”，而是因为 `2-设计` 的第一输入根确实是 `costume_design_bridge.json`；这类扩展文件应被明确定义为派生 sidecar，而不是平行真源。
