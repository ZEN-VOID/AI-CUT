# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/1-场景/3-面板` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc -> 4-Design -> 1-场景` 根链之后加载本文件。

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
| `3-面板` 跳过 `2-设计` 直接拼场景 prompt | 输入真源层 | 强制回到 `场景设计.json` 与 `panel_handoff` | 在 `SKILL.md` 与脚本中固化 `2-设计` 为第一输入根 | 不再从导演 JSON 直接生 panel |
| 面板 carrier 只有单个 `layout.json`，没有 episode 级聚合真源 | 输出治理层 | 补回 `场景面板.json` 作为 machine-first canonical carrier | 在 `output-template` 中固定 episode + per-scene 双层同源结构 | `场景面板.json` 与逐场景 layout 一一可回链 |
| negative constraints 在场景设计有记录，面板阶段丢失 | handoff 合同层 | 将 `reverse_taboos` 与模板 negative prompt 汇总进 `negative_prompt` | 在脚本里固定 negative 合成函数 | per-scene layout 不再遗漏禁区 |
| 面板阶段越权做图片生成 | 阶段边界层 | 停在 panel carrier 落盘，不调用生图 | 在 `SKILL.md`、脚本 CLI 与输出契约中固定 JSON-only 边界 | 运行后只生成 JSON |
| identity badge 漂移，导致场景面板无法稳定追溯 | 命名合同层 | 固定 `<scene_key> + <scene_name>` identity badge | 在模板与脚本中统一 badge 生成规则 | 每个 layout 都有稳定 badge |

## Repair Playbook

1. 先查 `2-设计/场景设计.json` 是否存在且 `scene_designs[]` 完整。
2. 再查每个场景是否具备 `scene_key / final_scene_prompt / panel_handoff`。
3. 再查模板是否保持 `16:9 + 3x3 + prompt_segments` 结构。
4. 然后检查 `场景面板.json` 与 `<scene_key>-layout.json` 是否同源。
5. 最后确认运行结果停在 JSON，而不是越权进入出图。

## Reusable Heuristics

- 场景面板最稳的上游不是导演 JSON，而是已经被 `2-设计` 收束过的 `final_scene_prompt + panel_handoff`。
- 只要 `panel_handoff` 已经存在，`3-面板` 就不应该重新解释世界观和空间逻辑，而应该把它们整理成更稳定的展示布局 prompt。
- `场景面板.json` 负责 machine-first 批量消费，逐场景 `*-layout.json` 负责局部追溯与下游 handoff；两者必须同源，不能各自生长。
- 面板阶段最容易越权到“直接生图”，但当前仓的真边界是 `4-Design` 负责 carrier，`5-Image` 负责图像生成。

## Case Log

### Case-20260412-AIGC-SCENE-PANEL-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为空壳的 `.agents/skills/aigc/4-Design/1-场景/3-面板` 建立了可执行 skill package、模板、脚本与入口元数据，并把场景类目父级从 pending 面板状态升级为 active。
- root_cause_or_design_decision: 参照仓存在旧 `3-设定/4-面板/场景面板`，但当前仓 `4-Design/1-场景/3-面板` 目录为空，导致 `2-设计` 的 `panel_handoff` 没有实际接收方；若直接搬旧合同，又会把旧 runtime 与自动生图边界带入当前仓。
- final_fix_or_heuristic: 保留参照仓“scene design -> layout carrier”的核心思路，但把输入收口到当前仓的 `场景设计.json`，输出收口为 `场景面板.json + <scene_key>-layout.json`，并把阶段边界固定在 JSON carrier，不越权生图。
- prevention_or_replication_checklist:
  - [x] `3-面板` 主合同已建立
  - [x] `CONTEXT.md` 已沉淀根因与 heuristic
  - [x] `references/` 与模板已建立
  - [x] 最小执行脚本已建立
  - [x] 父级 `1-场景` 与 `4-Design` 路由状态已同步
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/templates/scene-panel-layout.template.json`
  - `.agents/skills/aigc/4-Design/1-场景/3-面板/scripts/generate_scene_panels.py`
  - `.agents/skills/aigc/4-Design/1-场景/SKILL.md`
- user_feedback_or_constraint: 用户明确要求完善 `.agents/skills/aigc/4-Design/1-场景/3-面板`，并参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/4-面板/场景面板`。
