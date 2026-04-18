# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/1-清单/角色` 的经验层知识库，不是执行日志。
- 调用本技能时，应在 `SKILL.md` 之后预加载本文件。
- 优先级固定为：用户显式请求 > `AGENTS.md` / meta 规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按旧链路对 markdown 第二行做角色扫描 | 输入契约层 | 回到 `3-Detail/第N集.json`，只消费 `分镜组列表[]` | 在 `SKILL.md` 与共享消费合同固化 JSON-only 主链 | 不再依赖旧式 markdown 锚点 |
| `出场角色及穿搭` 被忽略，导致服装主锚缺失 | 字段消费层 | 先以组级穿搭摘要建立 canonical 角色与服装主锚 | 在 `_shared/detail-output-consumption-contract.md` 固化优先级 | `角色清单.json` 存在主服装锚 |
| 镜级出场已存在，但 `group_role_map[]` 不能回链到 `shot_id` | 可追溯层 | 回到 `角色站位走位` 重新补 shot evidence | 在 `Pass Table` 固化 `group_id / shot_id` 追溯门 | `group_role_map[].shot_id` 可用 |
| 同一角色多套服装被压成单一描述 | 变体治理层 | 拆出 `costume_variants[]` 并保留触发镜头 | 在 references 中固化“canonical 名称可合并，服装状态不得压扁” | `role_design_bridge.json` 含变体 |
| 群像主体被误拆成多个单人角色 | 角色层级层 | 回退为 `群像角色`，保留集合语义 | 在归一化细则中固定群像判定 | `role_level` 不再漂移 |
| `display_profile` 只是字段拼接，前端不可读 | 展示层 | 重写 `tagline / short_bio / visual_bible / costume_story / performance_hook` | 在 `FIELD-ROLE-04` 固化人读门槛 | 研究 JSON 可直接渲染角色卡 |
| 研究结论只有词项，没有句子级判断 | 输出表达层 | 回到研究步骤，把字段收束成句子级结论 | 在 `FIELD-ROLE-03` 固化句子门禁 | 最终输出不再是词表 |
| 共享合同曾把角色降为单清单，但角色 leaf 保留三文件 | 输出治理层 | 将共享合同改为 `角色清单 / 角色研究 / role_design_bridge` 三业务真源 | 明确三文件职责：清单管 identity，研究管 evidence/display，bridge 管 design handoff | 角色三文件与场景/道具同构 |
| leaf 已标记 active，但没有实际脚本入口 | 执行入口层 | 补齐 `run_role_list_pipeline.py + extract_episode_roles.py + build_role_research.py` | 在 `SKILL.md` 固化 `Execution Entrypoints`，并以 dry-run 作为最小验收 | active leaf 可直接执行，不再只剩合同 |
| shared schema 已切到 `人物表演锚点 / 动作路径 / 视觉抓手`，但角色链仍把 legacy 镜级句字段当主证据 | schema handoff 层 | 优先读取 `人物表演锚点 / 动作路径 / 视觉抓手 / 空间氛围`，再把 `角色站位走位 / 分镜表现 / 角色背景面` 降为 fallback | 在 `SKILL.md + detail-role-normalization.md + extract_episode_roles.py` 同时固定 `branch-owned first, legacy fallback` | 角色清单主路径不再锚在 compatibility projection |

## Repair Playbook

1. 先检查 `3-Detail/第N集.json` 是否具备 `组间设计.出场角色及穿搭 + 分镜明细[]`。
2. 再按“组级穿搭 -> 镜级走位 -> 动作/道具/背景 -> 剧本正文回退”的顺序补角色证据。
3. 归一角色前，先判断是否为群像主体、关系称谓或 unknown，而不是急着合并。
4. 若同一角色出现多套造型，先保留 `costume_variants[]`，再决定主锚。
5. 研究稿完成后，必须再检查 `display_profile` 与 `design_bridge_profile` 是否真能被下游消费。

## Reusable Heuristics

- `出场角色及穿搭` 最适合作为 canonical 角色名与主服装锚，不适合作为唯一证据。
- 角色清单最容易丢失的信息不是“有没有这个角色”，而是“这个角色在第几镜以哪套造型出现过”。
- `角色站位走位` 通常比 `角色背景面` 更适合判断出场和走位；背景字段更适合补空间与氛围。
- 在 branch-owned 重构后，`动作路径` 应接替 `角色站位走位` 成为镜级 presence/motion 第一证据；`人物表演锚点` 和 `视觉抓手` 分别负责表演成立度与视觉识别强化。
- 同一角色 canonical 名称可以统一，但服装状态、身份态与群像语义不应被统一掉。
- 若桥接字段需要人工补全，应把缺口留在 `quality_flags`，不要伪装成稳定结论。
- 角色链的三真源边界要稳定：`角色清单.json` 不承载长研究，`角色研究.json` 不重建对象池，`role_design_bridge.json` 不反向发明角色。
- 对 active leaf 来说，“有字段合同但没有 pipeline” 本身就是源层故障；应先补入口，再谈单次 episode 执行。
