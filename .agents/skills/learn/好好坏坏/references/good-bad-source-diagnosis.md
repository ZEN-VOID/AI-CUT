# Good/Bad Source Diagnosis

本文件定义 `好好坏坏` 的核心诊断规则：从用户给出的好/坏示例出发，回看目标技能配置、任务要求和资料来源，找到应调优的源层 owner。

## Evidence Package

每次诊断至少建立以下证据包：

| evidence | required | owner |
| --- | --- | --- |
| `target_skill_contract` | yes | 目标 `SKILL.md + CONTEXT.md` |
| `task_stage_or_output` | yes | 用户输入 / 任务文件 |
| `good_examples` | yes | 用户输入 / 输出文件 |
| `bad_examples` | yes | 用户输入 / 输出文件 |
| `task_requirements` | no, but required for normative judgment | prompt / issue / 阶段合同 / PRD |
| `source_materials` | no, but required for factual judgment | 项目资料 / 参考文本 / 输入数据 |
| `current_outputs` | no | 现有产物或中间文件 |

缺少 `task_requirements` 时，只能判断相对好坏，不得把判断写成硬性验收规则。缺少 `source_materials` 时，不得对事实忠实度做最终裁决。

## Contrast Dimensions

| dimension | good signal examples | bad signal examples | likely source owner |
| --- | --- | --- | --- |
| requirement coverage | 覆盖用户显式要求、阶段合同、输出字段 | 漏字段、漏阶段、跑题、误解任务 | `SKILL.md` Input/Output Contract、`steps/` |
| source fidelity | 引用资料准确、边界清楚、不过度发挥 | 幻觉、错引、忽略输入证据 | `references/`、`steps/`、`review/` |
| routing and typing | 选对类型包、分支和模式 | 错分支、默认路线错误、模式漂移 | `types/`、`SKILL.md` Mode Selection、`steps/` |
| reasoning sequence | 先读资料、再判型、再生成、再验收 | 顺序倒置、未留证据、跳过 gate | `steps/` |
| output schema | 字段完整、命名稳定、路径正确 | schema 破坏、路径漂移、格式不可消费 | `templates/`、`SKILL.md` Output Contract |
| quality gate | 能拦截坏结果、解释风险 | review 口号化、漏检、无 verdict | `review/` |
| style and taste | 风格服务任务，口吻与项目一致 | 泛化套话、过度营销、风格错位 | 目标 `CONTEXT.md`、项目 `MEMORY.md`、`references/` |
| script boundary | 脚本只做机械辅助 | 脚本主创、启发式拼正文、静默改写判断 | `scripts/`、`SKILL.md` Critical Gates |

## Source Owner Decision Rules

1. 改变“什么时候触发、接受什么输入、输出必须是什么”时，优先落 `SKILL.md`。
2. 改变“具体如何按顺序判断和执行”时，优先落 `steps/`。
3. 改变“不同对象、场景、风格或输出形态怎么分流”时，优先落 `types/`。
4. 改变“长规则、详细规范、资料解释原则”时，优先落 `references/`。
5. 改变“如何验收、如何拦截坏结果、如何给 verdict”时，优先落 `review/`。
6. 改变“输出字段、报告结构、命名样板”时，优先落 `templates/`，并同步 `SKILL.md` Output Contract。
7. 改变“机械读取、diff、校验、投影”时，才落 `scripts/`；脚本不得承接核心创作判断。
8. 一次性经验、失败模式和可复用 heuristic 先落目标 `CONTEXT.md`；跨 skill 通用经验落本技能 `CONTEXT.md` 或 `knowledge-base/`。
9. 改变发现、路由或触发语义时，必须检查 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml`。

## Anti-Overfitting Rules

- 不把好示例的表面措辞固定成唯一模板，除非任务本身要求逐字风格。
- 不把坏示例中的单次错误扩展成全局禁令，除非能证明同类任务稳定复发。
- 不把用户当次偏好写入目标 `SKILL.md`；长期偏好才进入项目 `MEMORY.md`，稳定跨任务规则才晋升源层合同。
- 不因好示例“更长”就要求输出更长；先判断是否因为证据更完整、结构更清晰或字段更齐。
- 不因坏示例“更短”就要求扩写；先判断是否漏需求、漏资料、漏 gate。

## Diagnosis Matrix Shape

| contrast_id | good_signal | bad_signal | requirement_or_source_basis | direct_output_cause | source_owner | patch_action | validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `C1` |  |  |  |  |  |  |  |

每一行都必须能回答：好在哪里、坏在哪里、为什么源层应改这里，以及改完如何验证。
