# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/服装/3-面板` 的经验层知识库，不是过程日志。
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
| `3-面板` 目录存在但没有可执行合同 | 叶子技能层 | 补齐 `SKILL.md + CONTEXT.md + template + runner` | 固化“空目录不算 active 技能”原则 | 目录可执行且有最小 runner |
| 面板阶段回头重扫 `角色清单 / 编导` | 输入真源层 | 锁定 `2-设计` 产物为唯一输入 | 在 `SKILL.md` 和 runner 同时固定输入根 | runner 只读取 `2-设计/第N集/` |
| prompt sidecar 缺失导致 panel prompt 变短 | 降级策略层 | 回退 `服装设计.json.prompt_anchor` 并标记 degraded mode | manifest 永远记录 sidecar 缺失 | `_manifest.json.degraded_costumes` 非空 |
| 每集被写成单一 panel 文件 | 输出契约层 | 按 `costumes[]` 逐服装输出 layout | 在命名合同中固定 `<costume_id>-<canonical_label>-CostumePanel-layout.json` | episode 输出文件数等于 costume 数 |
| 模板结构从 reference 漂移 | 模板真源层 | 回退当前目录 template，禁止脚本内再造第二套结构 | 把 layout contract 锁在 template 文件，不在脚本复制模块定义 | prompt 中能回链 mandatory rules |
| 叶子合同只说流程，不足以支撑 degraded mode 和 packet 级闭环 | 思行网络层 | 把输入门、sidecar 退化、模板锁定、逐服装 packet 组装和 manifest 汇流都收回主 `SKILL.md` | 固化 `Node Network + Capability Detail + Convergence` | `3-面板` 可直接按节点执行 |

## Reusable Heuristics

- 服装面板最稳定的输入不是角色清单，而是已经收束好的 `服装设计.json + costume_design_prompt.json`。
- 若当前仓库还没有稳定共享 panel engine，先固定 layout JSON 停点，比仓促接回自动生图更稳。
- 逐服装 layout 比整集单文件更适合后续审阅、回修和图像工具消费。
- 对 `3-面板` 做知行合一改造时，最重要的是把 degraded mode 也当成正式节点，而不是只在脚本里静默兜底。

## Case Log

### Case-20260412-AIGC-COSTUME-PANEL-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/服装/3-面板` 建立了可执行 skill 包，并将输入锁定为 `2-设计` 产物。
- root_cause_or_design_decision: 服装链若只做到 `2-设计`，其 panel handoff 仍然悬空；若直接从角色清单或导演 JSON 拼 panel，又会产生新的第二真源。
- final_fix_or_heuristic: 将 `3-面板` 升级为 active leaf，并把输入固定为 `服装设计.json + costume_design_prompt.json`，本轮只生成 layout JSON + manifest。
- prevention_or_replication_checklist:
  - [x] 叶子 skill 合同已存在
  - [x] 模板与 runner 已落地
  - [x] 当前 runtime 路径已 canonicalized
  - [x] 降级路径已进入 manifest
- evidence_paths:
  - `.agents/skills/aigc/4-Design/服装/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/服装/3-面板/templates/服装面板-提示词.json`
  - `.agents/skills/aigc/4-Design/服装/3-面板/scripts/generate_costume_panels.py`
- user_feedback_or_constraint: 用户要求参照现有 `角色 / 场景 / 道具` 家族，把 `3-服装` 一次性补齐到完整链路。

### Case-20260412-AIGC-COSTUME-PANEL-ZHI-XING-NETWORK

- milestone_type: source_contract_change
- outcome: 在保持 design-master-first、template 真源和 layout packet 停点不变的前提下，将 `3-面板` 重排为知行合一叶子技能。
- root_cause_or_design_decision: 原合同已有字段表和流程，但对 degraded mode、identity badge、逐服装 packet 组装和 manifest 汇流的节点化表达还不够强，难以满足“每一步足够细”的质量要求。
- final_fix_or_heuristic: 将 `3-面板` 改写为 `Business Requirement Analysis -> Topology -> Thinking-Action Node Network -> Capability Detail -> Convergence -> One-Shot Output`，并把 sidecar 缺失的退化处理纳入正式节点。
- prevention_or_replication_checklist:
  - [x] 输入根仍固定为 `2-设计` 产物
  - [x] template 真源与 runner 未变
  - [x] degraded mode 已进入节点网络和 manifest 合同
- evidence_paths:
  - `.agents/skills/aigc/4-Design/服装/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/服装/3-面板/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/服装/3-面板/templates/服装面板-提示词.json`
- user_feedback_or_constraint: 用户要求“复杂链路的骨架 / 细则分层：false”，并要求每一个思维·执行节点一步一步足够细致。
