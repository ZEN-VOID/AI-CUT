# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/1-场景/1-清单` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `.agents/skills/aigc/SKILL.md` 之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把 `1-清单` 误写成研究链 | 阶段边界层 | 回退到 scene catalog 最小输出壳 | 在 `SKILL.md + references/output-template.md` 固化“只输出 scenes[] / group_scene_map[]” | 主产物不含研究字段 |
| `scene_name` 与 `scene_variant` 拆分不稳 | 抽取规则层 | 保守只锁 `scene_name`，其余回收到 `scene_variant` 或空 | 在脚本中固定“先主场景、后方位变体”的 earliest-marker 规则 | 同一主场景不再裂成多个伪场景 |
| 上游 episode JSON 缺少 shared schema 壳 | 输入合同层 | 停止并报告缺失字段 | 在 `references/execution-flow.md` 固化最小必需字段 | 不在缺壳情况下伪造清单 |
| 输出落回旧 `output/影片/...` 路径 | runtime 落点层 | 改回 `projects/<项目名>/4-Design/1-场景/1-清单/第N集/` | 在脚本默认落点和输出模板里固定当前任务口径 | 输出目录符合当前技能合同 |

## Repair Playbook

1. 先查上游 episode JSON 是否存在 `final_output.main_content.分镜组列表[]`。
2. 再查每个 `分镜明细[]` 是否含 `分镜ID` 与 `场景及方位`。
3. 再查 `scene_name / scene_variant` 是否按“主场景优先”保守收口。
4. 最后查 `第N集.json` 是否同时具备 `scenes[] + group_scene_map[] + summary`。

## Reusable Heuristics

- `1-清单` 的目标不是“把场景写得更完整”，而是“把场景主键锁稳，让下游不用重新从镜头文本里猜场景”。
- 对本链路来说，最重要的不是方位词拆得多细，而是 `scene_name` 足够稳定，能把同一主场景的多个镜头聚到一起。
- 当 `场景及方位` 句子既含空间实体又含朝向描述时，先保住空间实体，方位描述宁可全留在 `scene_variant`，不要反过来把方位短语误升为新场景。
- 参照仓的研究/bridge 资产适合设定阶段，不适合当前这个只做场景清单的叶子技能；输入 schema 和下游落点变了，就不能机械平移旧输出合同。

## Case Log

### Case-20260412-AIGC-DESIGN-SCENE-LIST-CREATION

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/1-场景/1-清单` 补齐了面向当前仓的场景清单子技能包、reference 模块与提取脚本。
- root_cause_or_design_decision: 参照仓 `场景清单` 绑定旧的 `output/影片/.../3-设定` runtime，并同时负责研究与 bridge；当前任务则明确要求消费 `projects/<项目名>/3-Detail/第N集.json` 并只输出 `4-Design/1-场景/1-清单/` 下的场景清单。
- final_fix_or_heuristic: 保留“镜级场景抽取 + 主场景聚合”的核心能力，把输出收口为 `第N集.json + 可选 _manifest.json`，去掉研究链与旧 runtime 假设。
- prevention_or_replication_checklist:
  - [x] shared director schema 已成为输入真源
  - [x] `projects/<项目名>/4-Design/1-场景/1-清单/` 已成为当前技能默认落点
  - [x] `scenes[] / group_scene_map[]` 已固定为主输出字段
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/1-场景/1-清单/scripts/extract_scene_catalog.py`
- user_feedback_or_constraint: 用户明确要求参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/1-清单/场景清单`，但输入改为 `projects/<项目名>/3-Detail/第N集.json`，输出改为 `projects/<项目名>/4-Design/1-场景/1-清单/`。
