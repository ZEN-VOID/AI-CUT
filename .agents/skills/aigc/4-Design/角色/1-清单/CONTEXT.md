# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/角色/1-清单` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按旧版分镜组角色锚点取数，漏掉镜级差异 | 输入契约层 | 改从 `分镜组列表[].分镜明细[].角色及站位和穿搭` 提取 | 在脚本和合同中固定镜级字段为主路径 | `group_role_map[].shot_id` 非空 |
| 角色清单只有名字，没有证据回链 | 输出契约层 | 补齐 `group_id / shot_id / source_file / role_text` | 在字段主表中把证据链列为硬门槛 | 每个角色至少有一条 evidence |
| 群像或占位词被误当成单个普通角色 | 角色判定层 | 对 `众人/路人/群像/无角色` 走折叠或群像判定 | 固化占位黑名单与群像判定逻辑 | `role_level` 不再明显失真 |
| 穿搭片段被环境/道具描述污染 | 证据隔离层 | 只在命中服装关键词的角色子句里记录 `costume_mentions` | 固化服装提示词窗口和角色子句绑定 | `costume_profile` 可解释 |
| 主合同改成知行合一后，字段/步骤仍留在平行 `references/` | 真源治理层 | 把字段主表、思行节点、输出合同收回主 `SKILL.md` | 对 `复杂链路的骨架 / 细则分层=false` 的技能，只保留迁移 stub，不保留平行 reference 真源 | 目录内不再出现并列演化的执行细则 |

## Repair Playbook

1. 先查输入文件是否符合 shared director schema。
2. 再查 `分镜组列表[] / 分镜明细[] / 角色及站位和穿搭` 三层结构是否齐全。
3. 逐镜检查角色名、穿搭子句和证据行是否能同时保留。
4. 聚合后复查 `roles[]`、`group_role_map[]` 与 `_manifest.json` 的统计是否一致。

## Reusable Heuristics

- 对当前仓的 design 清单链来说，最有价值的不是“研究得多深”，而是先把角色对象池做成下游可复用的 canonical JSON。
- 一旦导演 episode JSON 已经细化到 `分镜明细[]`，角色清单就必须站在镜级提取，再向上聚合；否则服装变体和群像关系都会被抹平。
- `角色及站位和穿搭` 里的角色名提取应偏保守，宁可保留 `unknown`，也不要把道具或动作词当成人名。
- 当用户显式要求知行合一且 `复杂链路的骨架 / 细则分层=false` 时，`1-清单` 的字段主表、判型和汇流门都应回收到主 `SKILL.md`，不再让 `references/` 承载并列步骤合同。

## Case Log

### Case-20260412-AIGC-DESIGN-ROLE-LIST-CONTRACT

- milestone_type: source_contract_change
- outcome: 基于旧仓 `角色清单` 参考脚本，为当前仓 `.agents/skills/aigc/4-Design/角色/1-清单` 建立了 shared-schema 对齐的新合同和提取脚本。
- root_cause_or_design_decision: 参考源的主输入是旧 `output/影片/...` 结构与合并研究链，但当前仓需要的是以 `director_episode_output.schema.json` 为上游真源、只产出 design-source 清单的角色叶子技能。
- final_fix_or_heuristic: 复用旧脚本中高价值的角色归并与穿搭子句提取逻辑，但把输入结构切到 `final_output.main_content.分镜组列表[].分镜明细[]`，输出收敛为 `角色清单.json + _manifest.json`。
- prevention_or_replication_checklist:
  - [x] shared schema 路径已写入合同
  - [x] 提取脚本已对齐镜级字段
  - [x] 输出文件数已收敛到 2 份
  - [x] 经验层已记录迁移口径
- evidence_paths:
  - `.agents/skills/aigc/4-Design/角色/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/角色/1-清单/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/角色/1-清单/scripts/extract_role_list.py`
- user_feedback_or_constraint: 用户明确要求参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/1-清单/角色清单`，但输入改为 `projects/[项目名]/3-Detail/第N集.json`，并与 shared director schema 匹配。

### Case-20260412-AIGC-DESIGN-ROLE-LIST-ZXY-REPACK

- milestone_type: source_contract_change
- outcome: 将 `1-清单` 重排为知行合一主合同，并把原 `references/` 降级为迁移 stub。
- root_cause_or_design_decision: 旧合同已经具备字段主表、执行流程和输出模板，但它们分散在 `references/` 中；用户又明确要求 `复杂链路的骨架 / 细则分层=false`，因此主 `SKILL.md` 必须成为唯一可执行真源。
- final_fix_or_heuristic: 保留 shared schema、脚本入口、输出路径和字段口径不变，只把业务分析、拓扑、变量、思行节点、汇流门、字段主表和输出合同全部收回 `SKILL.md`，旧 `references/` 只保留历史跳转说明。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已内收字段主表与输出合同
  - [x] 思行节点与汇流门已直接写在主合同
  - [x] `references/` 已降级为迁移 stub
  - [x] 经验层已记录本次知行合一收口策略
- evidence_paths:
  - `.agents/skills/aigc/4-Design/角色/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/角色/1-清单/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/角色/1-清单/references/chain-of-thought.md`
- user_feedback_or_constraint: 用户明确要求“内容和机制上全量参照现有配置，但根据知行合一规范编排”，并指定 `复杂链路的骨架 / 细则分层=false`。
