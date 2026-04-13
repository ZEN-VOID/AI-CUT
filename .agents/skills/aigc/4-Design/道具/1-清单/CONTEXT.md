# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/道具/1-清单` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在根 `aigc` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按旧仓 `3-设定/道具清单` 路径推断输入或输出 | 路径契约层 | 改为优先消费 `3-Detail/第N集.json`，并兼容 `3-Detail/第N集.json` | 把路径推断固化进 runner 脚本与 `SKILL.md` | 输入不存在时能正确回退 |
| `道具及状态` 被整句吞掉，无法收束 canonical prop | 抽取层 | 先做 clause 级拆分，再用 noun suffix 收束 prop name | 在抽取脚本固化 `prop_name + state` 二分结构 | `道具清单.json.props[]` 能稳定聚合同名道具 |
| 研究层只有抽象评语，没有设计可消费字段 | 输出桥接层 | 强制输出 `structure_modules / material_and_finish / shot_route / physical_character` | 把 bridge 字段写成叶子技能主产物，而非可选 sidecar | `prop_design_bridge.json` 字段完整 |
| 关键剧情道具在研究/bridge 中被压平成普通功能道具 | 研究桥接层 | 为 research 与 bridge 同步补写 `narrative_significance` | 将“是否具有特殊叙事意义”固定成 `1-清单` 的必答问题，而不是留给 `2-设计` 自由猜测 | `道具研究.json` 与 `prop_design_bridge.json` 都含 `narrative_significance` |
| 用户给的是 `3-Detail` 路径，但项目仍保留 `编导` 真源 | runtime 兼容层 | 支持双路径解析，优先命中用户给定路径 | 在 runner 中内建 `3-Detail <-> 编导` 回退，不要求用户改命令 | 同一命令可在两种项目布局中运行 |
| 叶子合同必须依赖 references 才能看懂执行顺序 | 合同真源层 | 把输入锁定、抽取、聚合、研究、bridge、写回验证全部收回主 `SKILL.md` | 固化“1-清单的核心节点在主文档直写”规则 | 只读 `SKILL.md` 也能完整执行该叶子技能 |

## Repair Playbook

1. 先验证输入 JSON 是否存在 `final_output.main_content.分镜组列表`。
2. 再检查 `道具及状态` 是否被拆成 `prop_name + state`。
3. 再检查每个 canonical prop 是否能回链 `group_id + shot_id + raw_prop_text`。
4. 再检查研究层是否已经回答“它是否具有特殊叙事意义”，而不是只给材质和功能。
5. 再检查桥接层是否把叙事意义转成 `visual_obligation / continuity_guard` 一类可执行约束。
6. 最后检查输出目录是否稳定落到 `4-Design/道具/1-清单/第N集/`。

## Reusable Heuristics

- 道具链的第一事实不是“这个物件看起来多酷”，而是“它在第几个镜头、以什么状态出现”。
- 只要上游已经把道具信息落在 `道具及状态`，设计阶段就不该再回到旧 markdown 分镜块里猜。
- 对 `4-Design` 来说，研究不是终点；研究必须在同一轮里产出 bridge 字段，否则下游仍然会退回手工理解。
- 当某个道具承担身份确认、记忆回收、关键动作触发或持续空间限制时，应在 `1-清单` 就判定为特殊叙事道具，而不是留给 `2-设计` 后补。
- 用户显式给阶段路径时，叶子技能应优先兼容那个路径，而不是强迫用户接受仓内另一套 runtime 口径。
- 对抽取型叶子技能来说，最稳的知行合一写法是把“抽取 -> 聚合 -> 研究 -> bridge -> 写回”直接写成主文档节点，而不是把关键执行顺序藏进 references。

## Case Log

### Case-20260412-AIGC-4DESIGN-PROP-LIST-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为空的 `.agents/skills/aigc/4-Design/道具/1-清单/` 建立了首份可执行叶子合同与脚本链。
- root_cause_or_design_decision: 参照来源仍绑定旧仓 `3-设定/道具清单` 与 markdown 分镜块，而当前仓共享真源已经切到 `director_episode_output.schema.json`；若直接平移旧技能，会在输入、输出与阶段语义上同时失配。
- final_fix_or_heuristic: 保留“抽取 -> 研究 -> bridge”三段式结构，但把上游改为 `3-Detail/第N集.json`，把下游改为 `4-Design/道具/1-清单/第N集/`，并在 runner 中兼容 `3-Detail/第N集.json`。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已改为当前仓路径语义
  - [x] runner 已支持 `3-Detail <-> 编导` 双路径回退
  - [x] 默认主产物已收口为三份 JSON
  - [x] `CONTEXT.md` 已登记本轮路径迁移 heuristic
- evidence_paths:
  - `.agents/skills/aigc/4-Design/道具/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/道具/1-清单/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/道具/1-清单/scripts/run_prop_list_pipeline.py`
- user_feedback_or_constraint: 用户明确要求“参照 AIGC-ZEN-VOID 的道具清单，但要匹配当前仓的 `director_episode_output.schema.json`，输入为 `projects/[项目名]/3-Detail/第N集.json`，输出为 `projects/[项目名]/4-Design/道具/1-清单/`”。

### Case-20260412-AIGC-PROP-LIST-ZHIXING-REFRACTOR

- milestone_type: source_contract_change
- outcome: 将 `1-清单` 重构为知行合一叶子技能，主 `SKILL.md` 直接承载抽取、聚合、研究、bridge 与写回节点。
- root_cause_or_design_decision: 旧版 `1-清单` 已有内容，但强依赖 `references/chain-of-thought.md` 与 `execution-flow.md` 才能看清真实执行顺序，不满足用户要求的“每个思维·执行节点足够细”。
- final_fix_or_heuristic: 保留脚本、路径、输出结构与 fail code，不动机制；只把关键执行链收回主 `SKILL.md`，让节点槽位、着手面与返工门在主合同可单读。
- prevention_or_replication_checklist:
  - [x] 主文档已写明六个思行节点
  - [x] 研究层和 bridge 不再依赖 references 才能理解
  - [x] 经验层已记录“抽取型叶子技能主文档直写节点” heuristic
- evidence_paths:
  - `.agents/skills/aigc/4-Design/道具/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/道具/1-清单/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按 `$skill-知行合一` 重构 `4-道具` 相关子技能包，且关闭“骨架 / 细则分层”，要求逐节点细写。

### Case-20260412-AIGC-PROP-LIST-NARRATIVE-SIGNIFICANCE

- milestone_type: source_contract_change
- outcome: 将“是否具有特殊叙事意义”前移到 `1-清单` 的研究与 bridge 合同，形成 `narrative_significance` 结构化字段。
- root_cause_or_design_decision: 道具设计脚本层已有零散 `narrative_function` 信号，但上游 bridge 没有显式回答“这个道具是否是关键剧情道具”，导致 `2-设计` 只能事后猜测。
- final_fix_or_heuristic: 在 `道具研究.json` 与 `prop_design_bridge.json` 同步加入 `narrative_significance`，并要求 `1-清单` 把特殊叙事意义转译成 `visual_obligation / continuity_guard` 等下游可执行约束。
- prevention_or_replication_checklist:
  - [x] `1-清单/SKILL.md` 已把叙事意义写入研究与 bridge 节点
  - [x] `build_prop_research.py` 已生成 `narrative_significance`
  - [x] 输出模板已同步该字段
- evidence_paths:
  - `.agents/skills/aigc/4-Design/道具/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-Design/道具/1-清单/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/道具/1-清单/scripts/build_prop_research.py`
  - `.agents/skills/aigc/4-Design/道具/1-清单/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求为 `.agents/skills/aigc/4-Design/道具` 技能包的思维·执行节点加入“是否具有特殊叙事意义”的考虑，并允许转化为更好的表达与节点布局。
