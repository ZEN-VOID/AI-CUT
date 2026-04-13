# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/角色/3-面板` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `aigc` 根技能 > 本 `SKILL.md` > 本 `CONTEXT.md`。

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
| 面板 prompt 直接吃整份 Markdown，混入 `物语 / 解构` | prompt 提取层 | 只抽 `**prompt整合**` 段作为 `design_subject` | 在脚本与 `SKILL.md` 固化“prompt整合-only”规则 | `design_subject_source=markdown_prompt_integration` |
| `2-设计` 缺少 Markdown 或 `prompt整合` | 输入回退层 | 从 `character_design.json.roles[]` 合成保守版 `design_subject` | 在 packet 中记录 fallback 来源，避免 silent drift | `design_subject_source=fallback_json_synthesis` |
| 模板被平行改写成第二真源 | 模板治理层 | 固定只读 `templates/角色面板-提示词.json` | 把 layout、critical requirements 与 prompt segments 统一从模板继承 | packet 中 `template_path` 指向同一路径 |
| crowd 角色仍被当成单人 turnaround 处理 | 角色层级策略层 | `role_tier=crowd` 时自动打 `group_portrait=true` | 在类型策略中固化 crowd 群像策略 | manifest 统计到 `group_portrait_count` |
| 父级合同仍把 `3-面板` 写成 pending | 路由状态层 | 同步更新 `2-角色` 与 `4-Design` 父级状态 | 每新增 active leaf 同步回写父级真源与经验层 | 父级合同不再出现 stale pending |
| 主合同改成知行合一后，prompt 来源/类型策略仍留在并列 `references/` | 真源治理层 | 把 prompt 来源判型、role tier 策略、输出合同收回主 `SKILL.md` | 对 `复杂链路的骨架 / 细则分层=false` 的面板技能，只保留迁移 stub，不保留并列 reference 真源 | 当前目录不再出现平行执行真源 |

## Repair Playbook

1. 先确认 `character_design.json` 是否存在且 `roles[]` 非空。
2. 再确认逐角色 Markdown 是否存在，并优先抽 `prompt整合`。
3. 若 `prompt整合` 缺失，回退到 JSON synthesis，但必须在 packet 中留痕。
4. 再检查模板路径、layout 和 critical requirements 是否完整继承。
5. 最后检查 packet 命名、episode 路径和 `_manifest.json` 是否一致。

## Reusable Heuristics

- 角色面板最稳的 prompt 源不是整份设计卡，而是 `prompt整合` 这个已经被 `2-设计` 压好的下游消费段。
- panel 阶段最怕的不是“文案不华丽”，而是把设计事实、layout 规则和出图执行混成一层；因此本阶段只做 packet，停在写回。
- 如果上游设计稿还不完整，宁可保守 fallback 到 JSON synthesis，也不要把 `物语 / 解构` 之类分析段直接灌给下游。
- crowd 角色的 panel 更像“同一阶层群像设计板”，不是单人 front/side/back 转身图。
- 当用户显式要求知行合一且 `复杂链路的骨架 / 细则分层=false` 时，`3-面板` 的 prompt 来源策略、群像策略、reference image 规则和 output contract 都应回收到主 `SKILL.md`，不再让 `references/` 承载并列步骤真源。

## Case Log

### Case-20260412-AIGC-ROLE-PANEL-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/角色/3-面板` 建立了主合同、经验层、shared I/O、模板、入口元数据与最小 packet 生成脚本。
- root_cause_or_design_decision: 当前仓 `3-面板` 只有空目录，父级合同仍把它视为 pending；同时参考仓的成熟能力没有迁移到当前 runtime 与 `2-设计` 真源之上。
- final_fix_or_heuristic: 以当前 `2-设计/character_design.json + [角色名].md` 为第一输入根，把参考仓的角色面板模板与 prompt 收束逻辑迁成当前仓的 machine-first layout packet 方案。
- prevention_or_replication_checklist:
  - [x] `SKILL.md + CONTEXT.md + CHANGELOG.md` 已建立
  - [x] `_shared/IO_CONTRACT.md`、`references/`、`templates/` 已建立
  - [x] `scripts/build_character_panel_packets.py` 已建立
  - [x] 父级状态已从 pending 同步到 active
- evidence_paths:
  - `.agents/skills/aigc/4-Design/角色/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/角色/3-面板/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/4-Design/角色/3-面板/scripts/build_character_panel_packets.py`
  - `.agents/skills/aigc/4-Design/角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
- user_feedback_or_constraint: 用户要求完善当前仓 `.agents/skills/aigc/4-Design/角色/3-面板`，并参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/4-面板/角色面板`。

### Case-20260412-AIGC-ROLE-PANEL-ZXY-REPACK

- milestone_type: source_contract_change
- outcome: 将 `3-面板` 重排为知行合一叶子技能，并把 `references/` 降级为迁移 stub。
- root_cause_or_design_decision: 现有 `3-面板` 已具备模板、runner 与 packet 结构，但 `design_subject` 策略、role tier 判型和输出结构仍分散在 `references/` 中；用户明确要求 `复杂链路的骨架 / 细则分层=false`，因此主 `SKILL.md` 必须成为唯一可执行真源。
- final_fix_or_heuristic: 保留 `character_design.json -> prompt整合 -> template -> packet` 这条业务链和 runner/template 机制不变，只把 prompt 来源判型、role tier / reference image 策略、思行节点、字段主表和 output contract 全部收回 `SKILL.md`，旧 `references/` 只保留迁移跳转。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已内收类型策略与输出合同
  - [x] 思行节点与 handoff gate 已直接写在主合同
  - [x] `references/` 已降级为迁移 stub
  - [x] 经验层已记录本次知行合一收口策略
- evidence_paths:
  - `.agents/skills/aigc/4-Design/角色/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/角色/3-面板/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/角色/3-面板/references/type-strategies.md`
- user_feedback_or_constraint: 用户明确要求“内容和机制上全量参照现有配置，但根据知行合一规范编排”，并指定 `复杂链路的骨架 / 细则分层=false`。
