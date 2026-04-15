# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/道具/1-清单` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在根 `aigc` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按旧仓 `3-设定/道具清单` 路径推断输入或输出 | 路径契约层 | 改为优先消费 `3-Detail/第N集.json`，并兼容 legacy `编导/第N集.json` | 把路径推断固化进 runner 脚本与 `SKILL.md` | 输入不存在时能正确回退 |
| `3-Detail` canonical 与 legacy `编导` 路径被各 leaf 各自解释 | 真源治理层 | 固定 `3-Detail/第N集.json` 为第一输入根，`编导/第N集.json` 仅作 fallback | 在 `1-清单/_shared` 共享消费合同里统一路径与字段映射 | 道具链与角色/场景链的 detail 输入规则一致 |
| `道具及状态` 被整句吞掉，无法收束 canonical prop | 抽取层 | 先做 clause 级拆分，再用 noun suffix 收束 prop name | 在抽取脚本固化 `prop_name + state` 二分结构 | `道具清单.json.props[]` 能稳定聚合同名道具 |
| 研究层只有抽象评语，没有设计可消费字段 | 输出桥接层 | 强制输出 `design_context.design_handoff.structure_modules / material_and_finish / shot_route / physical_character` | 把 bridge 字段折叠进 canonical catalog，而不是默认拆成第二真源 | `道具清单.json.props[].design_context` 字段完整 |
| 关键剧情道具在研究/bridge 中被压平成普通功能道具 | 研究桥接层 | 为 `design_context` 同步补写 `narrative_significance` | 将“是否具有特殊叙事意义”固定成 `1-清单` 的必答问题，而不是留给 `2-设计` 自由猜测 | `道具清单.json.props[].design_context` 含 `narrative_significance` |
| 用户给的是 `3-Detail` 路径，但项目仍保留 `编导` 真源 | runtime 兼容层 | 支持双路径解析，优先命中用户给定路径 | 在 runner 中内建 `3-Detail <-> 编导` 回退，不要求用户改命令 | 同一命令可在两种项目布局中运行 |
| 道具链 runner 在相对路径输入下把输出误落到 `3-Detail/4-Design-道具-1-清单/` | 输出路径解析层 | 改为按 `Path.parts` 直接定位 `projects/aigc/<项目名>` 项目根，而不是依赖 `\"/projects/\"` 字符串命中 | 默认输出根统一从项目根推断到 `4-Design/道具/1-清单/第N集/`，并保留误落盘清理步骤 | 相对路径与绝对路径输入都落到同一 canonical 输出目录 |
| 清单阶段只有三份业务 JSON，没有统一 `_manifest.json`，导致 sibling leaf 审计层不齐 | canonical output 治理层 | 让 runner 默认补写 `_manifest.json`，并在共享合同中明确其 audit sidecar 身份 | 统一到 `<领域>清单.json + _manifest.json + 按需派生 sidecar` | 道具链与角色/服装/场景的清单阶段输出层级一致 |
| 叶子合同必须依赖 references 才能看懂执行顺序 | 合同真源层 | 把输入锁定、抽取、聚合、研究、bridge、写回验证全部收回主 `SKILL.md` | 固化“1-清单的核心节点在主文档直写”规则 | 只读 `SKILL.md` 也能完整执行该叶子技能 |
| 用户要求道具与场景/角色统一三真源 | 输出治理层 | 将 `道具研究.json / prop_design_bridge.json` 改为默认业务真源成员 | 明确清单管对象池，研究管证据与属性，bridge 管设计直参；脚本默认写三份 JSON | 默认输出三份业务 JSON |

## Repair Playbook

1. 先验证输入 JSON 是否存在 `final_output.main_content.分镜组列表`。
2. 再检查 `道具及状态` 是否被拆成 `prop_name + state`。
3. 再检查每个 canonical prop 是否能回链 `group_id + shot_id + raw_prop_text`。
4. 再检查 `design_context` 是否已经回答“它是否具有特殊叙事意义”，而不是只给材质和功能。
5. 再检查 `design_handoff` 是否把叙事意义转成 `visual_obligation / continuity_guard` 一类可执行约束。
6. 最后检查输出目录是否稳定落到 `4-Design/道具/1-清单/第N集/`。

## Reusable Heuristics

- 道具链的第一事实不是“这个物件看起来多酷”，而是“它在第几个镜头、以什么状态出现”。
- 只要上游已经把道具信息落在 `道具及状态`，设计阶段就不该再回到旧 markdown 分镜块里猜。
- 对 `4-Design` 来说，研究不是终点；研究必须在同一轮里折叠成 `design_context`，否则下游仍然会退回手工理解。
- 当某个道具承担身份确认、记忆回收、关键动作触发或持续空间限制时，应在 `1-清单` 就判定为特殊叙事道具，而不是留给 `2-设计` 后补。
- 一旦 `2-设计/道具` 的 source-layer 已回迁，`1-清单/道具` 的默认 handoff 就应直接回到该叶子，不必继续维持“条件存在才可进入”的过渡表述。
- 用户显式给阶段路径时，叶子技能应优先兼容那个路径，而不是强迫用户接受仓内另一套 runtime 口径。
- 对抽取型叶子技能来说，最稳的知行合一写法是把“抽取 -> 聚合 -> 研究 -> bridge -> 写回”直接写成主文档节点，而不是把关键执行顺序藏进 references。
- 当多个 sibling leaf 共用同一上游 `3-Detail` episode JSON 时，路径 alias 和字段 fallback 应优先上收到共享合同，而不是在每个叶子脚本里各写一遍局部解释。
- 只要 runner 允许相对路径输入，项目根定位就必须基于 `Path.parts` 或等价结构判断，不能依赖带前导斜杠的字符串模式。
- 对道具链来说，三真源不等于三份总稿；`道具清单.json` 管 identity，`道具研究.json` 管研究事实，`prop_design_bridge.json` 管设计 handoff，`_manifest.json` 仍只做审计。
