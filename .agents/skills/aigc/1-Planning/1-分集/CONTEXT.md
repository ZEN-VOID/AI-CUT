# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/1-分集` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/1-分集/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

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
| 输入根没有锁到 `projects/<项目名>/Story/` | 输入真源层 | 回到故事目录重新锁定输入范围 | 在 `SKILL.md` 固化故事目录优先，manifest 只作索引证据 | 输入清单与用户口径一致 |
| readiness 未通过仍继续正式分集 | gate 层 | 停止执行并返回缺口 | 把 blocked / incremental / full_season 写成强门禁 | 不再出现 blocked 仍落盘正式结果 |
| 把 storyboard / hybrid 中的镜头语言清洗掉 | 源文本保真层 | 恢复原文切分，不做小说化改写 | 在 `SKILL.md` 固化“只切分，不清洗镜头语言” | 输出仍保留源文本结构证据 |
| 漏写 `source_profile` 或 `bootstrap_output` handoff | 下游交接层 | 重建父级 patch | 在字段主表与模板中固定 handoff 字段 | `2-Global` 可直接消费 handoff |
| `episode-split-plan.json` 与 `1-分集/第N集.md` 漂移 | 机读一致性层 | 回读模板并重建索引 | 强制模板化生成机读文件 | 索引与上游原文真源一致 |
| 为单一分集裁决单元保留孤立 subagent | 结构治理层 | 将边界判断、落盘与 handoff 全部收回 `1-分集` skill 本体 | 在父 skill、leaf skill、入口元数据与审计脚本中固化“`1-分集` 直达执行” | 不再存在 `.codex/agents/aigc/规划组/分集.md` 回指 |

## Repair Playbook

1. 先确认 `projects/<项目名>/Story/` 的实际输入范围。
2. 再确认主路由是否真的遵守 `P1>P2>P3`。
3. 再看候选边界是否有结构/戏剧证据，而不是字数硬切。
4. 最后才检查 `episode-split-plan.json` 与 handoff patch。

## Reusable Heuristics

- 在 DREAMER 里，`1-分集` 的 canonical 输出应是 `projects/<项目名>/1-Planning/1-分集/第N集.md`，由 `2-剧本` 再继续整理成主稿。
- 只要 `story-source-manifest.yaml` 已经把 `storyboard_script` 和锁轴写清，分集阶段就应保留这些结构信号，而不是先清洗再切分。
- `episode-split-plan.json` 的价值不是替代正文，而是给 `2-剧本`、父 skill、规划组其他角色和 `2-Global` 一个稳定机读入口。
- `1-分集` 的证据侧车最多保留一份 `projects/<项目名>/1-Planning/1-分集/执行报告.md`；逐集报告会把证据层拆碎，不利于规划阶段收口。
- 在 `1-分集` 里，不要为了单一裁决面额外保留 subagent；边界判断、落盘、索引更新和 QA 应统一留在 skill。
- 若某个 leaf 当前只有一个命中的角色且没有独立变体路由价值，应直接融合回 skill 本体，而不是再维护一层 team/agent 合同。

## Case Log

### Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-DIRECT-LEAF

- milestone_type: source_contract_change
- outcome: 将 `1-分集` 从“单 subagent 投影 + skill 收束”收敛为直接 leaf skill 执行。
- root_cause_or_design_decision: 当前匹配面只有一个 `.codex/agents/aigc/规划组/分集.md`，并不存在真正的多角色编排价值；继续保留会让 skill、team 与 audit 多维护一层无效真源。
- final_fix_or_heuristic: 删除 `规划组/分集.md`，把边界裁决、执行闭环与入口摘要全部收回 `1-分集/SKILL.md + agents/openai.yaml`，并同步修正父级规划合同、team 拓扑与 audit 必填项。
- prevention_or_replication_checklist:
  - [x] `1-分集` 已改为 direct leaf
  - [x] 父 skill 已移除 `规划组/分集.md` 回指
  - [x] 规划组 `team.md` 已撤掉 `分集` 角色
  - [x] 审计脚本已不再要求 `规划组/分集.md`
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.codex/agents/aigc/规划组/team.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求“当前匹配的 subagents 就孤零零一个，没有必要走 subagents 模式，直接完整融合在现有 SKILL 中”。

### Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-MIGRATION

- milestone_type: source_contract_change
- outcome: 参照 `AIGC-ZEN-VOID` 的 `1-故事分集`，在 DREAMER runtime 下重建 `1-分集` 的 leaf 合同。
- root_cause_or_design_decision: 仓内原 `1-Planning/1-分集` 目录为空，且现有规划组与 registry 还在回指不存在的 `1-规划` 路径；若直接照搬 `writer` 产物结构，会与 DREAMER 的 `projects/<项目名>/Init + 规划 + 编导` 运行时冲突。
- final_fix_or_heuristic: 保留 `ZEN-VOID` 的字段链、边界证据和 QA 闭环，但把输入真源改为 `projects/<项目名>/Story/`，把 canonical 输出改为 `projects/<项目名>/1-Planning/1-分集/第N集.md`，机读侧车改为 `projects/<项目名>/1-Planning/episode-split-plan.json`，并把执行报告收束为唯一的全剧集 `执行报告.md`。
- prevention_or_replication_checklist:
  - [x] 已固定 `Story/` 输入根
  - [x] 已固定 `1-Planning/1-分集/` 输出
  - [x] 已新增 `episode-split-plan.template.json`
  - [x] 已把 `source_profile + bootstrap_output` 固化进 handoff
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/1-分集/templates/episode-split-plan.template.json`
  - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
- user_feedback_or_constraint: 用户要求全面参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/1-故事分集` 的相关配置进行升级。
