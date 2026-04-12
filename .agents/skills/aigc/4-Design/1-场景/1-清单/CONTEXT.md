# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/1-场景/1-清单` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc -> 4-Design -> 1-场景` 根链之后加载本文件。
- 当前技能采用知行合一单合同；经验层只存放复用知识，不再承载并行规则真源。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把 `1-清单` 误写成研究链或设计链 | 阶段边界层 | 回退到 scene catalog 最小输出壳 | 在 `SKILL.md` 固化“只输出 scenes[] / group_scene_map[] / summary” | 主产物不含研究与设计字段 |
| `scene_name` 与 `scene_variant` 拆分不稳 | 抽取规则层 | 保守只锁 `scene_name`，其余回收到 `scene_variant` 或整句 | 在 `SKILL.md + 脚本` 固定 earliest-marker 与 keep-raw 回退 | 同一主场景不再裂成多个伪场景 |
| 上游 episode JSON 缺少 shared schema 壳 | 输入合同层 | 停止并报告缺失字段 | 在 `SKILL.md` 中把 `N1` 作为硬门槛 | 不在缺壳情况下伪造清单 |
| 输出落回旧 `output/影片/...` 路径 | runtime 落点层 | 改回 `projects/<项目名>/4-Design/1-场景/1-清单/第N集/` | 在 `SKILL.md` 和脚本默认落点里固定当前仓口径 | 输出目录符合当前技能合同 |
| 主文档与 `references/` 规则漂移 | 真源治理层 | 把有效规则全部收回 `SKILL.md` | 删除或退役明细 `references/`，避免第二真源 | 当前目录只剩单一规则主合同 |

## Repair Playbook

1. 先查上游 episode JSON 是否存在 `final_output.main_content.分镜组列表[]`。
2. 再查每个 `分镜明细[]` 是否含 `分镜ID` 与 `场景及方位`。
3. 再查 `scene_name / scene_variant` 是否按“主场景优先”保守收口。
4. 最后查 `第N集.json` 是否同时具备 `summary / scenes[] / group_scene_map[] / acceptance_notes`。

## Reusable Heuristics

- `1-清单` 的高质量标准不是“写得更丰富”，而是“把下游要复用的场景主键锁稳”。
- 当 `场景及方位` 同时含空间实体和朝向短语时，优先保住空间实体；方位信息宁可全部留在 `scene_variant`。
- 对本链路来说，`unknown` 是合格回退，不是失败遮羞布；真正的失败是静默跳过镜头。
- 若规则已经收回单一 `SKILL.md`，经验层只补 heuristics，不再额外复制流程、表格和输出契约。

## Case Log

### Case-20260412-AIGC-DESIGN-SCENE-LIST-CREATION

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/1-场景/1-清单` 建立了面向当前仓的场景清单子技能包与提取脚本。
- root_cause_or_design_decision: 参照仓 `场景清单` 绑定旧 runtime，并同时负责研究与 bridge；当前任务则明确要求消费 `projects/<项目名>/3-Detail/第N集.json` 并只输出 `4-Design/1-场景/1-清单/` 下的场景清单。
- final_fix_or_heuristic: 保留“镜级场景抽取 + 主场景聚合”的核心能力，把输出收口为 `第N集.json + 可选 _manifest.json`，去掉研究链与旧 runtime 假设。
- prevention_or_replication_checklist:
  - [x] shared director schema 已成为输入真源
  - [x] `projects/<项目名>/4-Design/1-场景/1-清单/` 已成为当前技能默认落点
  - [x] `scenes[] / group_scene_map[]` 已固定为主输出字段
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/scripts/extract_scene_catalog.py`
- user_feedback_or_constraint: 用户明确要求参照旧场景清单能力，但输入改为 `projects/<项目名>/3-Detail/第N集.json`，输出改为 `projects/<项目名>/4-Design/1-场景/1-清单/`。

### Case-20260412-AIGC-DESIGN-SCENE-LIST-ZXY-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `1-清单` 重构为知行合一单合同技能，取消 `references/` 细则分层，所有规则收束到 `SKILL.md`。
- root_cause_or_design_decision: 旧结构把思维链、执行流、类型策略和输出模板拆到 `references/`，虽然可用，但已不符合用户要求的“复杂链路骨架/细则分层=false”与单一真源口径。
- final_fix_or_heuristic: 采用 `N0-N7` 思行节点，把边界、输入、抽取、聚合、写出、验收全部写进主合同；经验层只保留失败模式与复用 heuristics。
- prevention_or_replication_checklist:
  - [x] 主合同已覆盖输入、拓扑、节点、输出、字段表和 root-cause 合同
  - [x] `references/` 已不再承载规则真源
  - [x] 下游仍可沿原输出路径消费 `scene catalog`
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求基于 `$skill-知行合一` 重构本技能，并指定 `复杂链路的骨架 / 细则分层: false`，且每个思维·执行节点必须足够细致。
