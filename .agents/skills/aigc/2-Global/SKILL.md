---
name: aigc-global
description: Use when the global directing stage must read one episode's planning group script plus init presets, then write `projects/aigc/<项目名>/2-Global/第N集.json` as the only creative business output for that episode.
governance_tier: full
---

# aigc 2-Global

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 本 `SKILL.md` 只咬定入口输入、出口输出、关键门禁、真源边界与目录导引；过程细则不得继续堆回主文件。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本目录 `references/ steps/ review/ types/` > `templates/README.md` > 本 `CONTEXT.md`。

## Positioning

`2-Global` 是 `1-Planning` 与 `3-Detail` 之间的导演前置收束阶段。

本阶段只做一件事：把当前集规划分组结果与初始化预设收束为**按集 JSON seed**。

- 输出文件固定为：`projects/aigc/<项目名>/2-Global/第N集.json`
- 填写模板固定为：`.agents/skills/aigc/2-Global/templates/episode-root.template.json`
- `第N集.json` 是本阶段唯一 creative business truth
- `validation-report.md` 是治理/验收侧车，不是创作业务输出物
- `全局风格.md / 全集类型元素.md / 分组类型元素.md / 导演意图.md` 不再生成，也不得作为新链路输入真源

## Mode Selection

| mode | 进入条件 | 允许动作 | 禁止动作 |
| --- | --- | --- | --- |
| `episode-bootstrap` | 当前集尚无 `2-Global/第N集.json` | 从必需输入首写按集 JSON | 先写 Markdown 再抽 JSON |
| `incremental-patch` | 当前集已有 `2-Global/第N集.json`，只修局部组或字段 | 仅 patch 命中 `group / field / advisory scope` | 无 scope 全量覆盖 |
| `blocked` | 必需输入缺失、集数不明或上游分组未稳定 | 写阻塞说明到治理侧车或最终回复 | 猜测生成业务 JSON |

旧 Markdown 投影已从默认模式移除。若旧项目确需读取历史 Markdown，只能在项目迁移任务中按既有 JSON 另行派生，不能进入本阶段主合同。

## Input Contract

### Required Runtime Inputs

| input_id | path | must_contain | fail_if_missing |
| --- | --- | --- | --- |
| `IN-GLOBAL-01` | `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` | 当前集全部分组正文、分镜组 ID、组序 | 阻塞，不生成 `第N集.json` |
| `IN-GLOBAL-02` | `projects/aigc/<项目名>/0-Init/north_star.yaml` | 项目级目标、风格方向、核心约束 | 阻塞，除非用户显式提供等价替代 |
| `IN-GLOBAL-03` | `projects/aigc/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段 handoff、长期约束、下游边界 | 阻塞，除非用户显式提供等价替代 |

### Optional Runtime Inputs

| input_id | path | use |
| --- | --- | --- |
| `IN-GLOBAL-04` | `projects/aigc/<项目名>/MEMORY.md` | 项目长期偏好、禁区与稳定口味 |
| `IN-GLOBAL-05` | `projects/aigc/<项目名>/CONTEXT/` 相关文件 | 项目共享附加上下文 |
| `IN-GLOBAL-06` | `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml` | 源文本、预设、保真模式证据 |
| `IN-GLOBAL-07` | `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md` | 当前集格式化剧本主稿 |
| `IN-GLOBAL-08` | `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md` | 分组决议、组序与时长 handoff |
| `IN-GLOBAL-09` | `projects/aigc/<项目名>/team.yaml` | 仅作前置 advisory；不得接管写回 owner |
| `IN-GLOBAL-10` | `projects/aigc/<项目名>/2-Global/第N集.json` | 增量 patch 的现存按集 JSON |
| `IN-GLOBAL-11` | 用户显式指定的风格、类型或导演偏好 | 当前轮最高优先级补充约束 |

### Forbidden Inputs

- `2-Global/*.md` 作为新链路业务真源。
- 与当前项目无关的外部参考文本。
- 外置导演组 team、agent、creative method 文档作为业务真源。
- 任何要求本阶段直接写 shot-level 字段、分镜列表或镜头 JSON 的输入。

## Output Contract

### Required output

- 必需创作业务输出：`projects/aigc/<项目名>/2-Global/第N集.json`
- 必需治理侧车：`projects/aigc/<项目名>/2-Global/validation-report.md`，或在阻塞时于最终回复中明确说明未写入原因。

### Output format

- 创作业务输出格式：JSON。
- JSON 结构必须同构于 `.agents/skills/aigc/2-Global/templates/episode-root.template.json`。
- 治理侧车格式：Markdown。

### Output path

- 按集 JSON：`projects/aigc/<项目名>/2-Global/第N集.json`
- 阶段验收：`projects/aigc/<项目名>/2-Global/validation-report.md`

### Naming convention

- `<项目名>` 必须等于当前项目根目录名。
- `第N集.json` 的 `N` 必须等于输入分组正文中的当前集号。
- 不得使用固定 `episode_root.json` 作为项目运行时创作输出名。

### Completion gate

- 只有 `第N集.json` 已按模板落盘且字段通过 `Output Field Gate`，本阶段才可判定完成。
- 若必需输入缺失或 JSON 未写入，只能返回 blocked verdict。

### Creative Business Output

| output_id | path | owner | schema_source | must_contain |
| --- | --- | --- | --- | --- |
| `OUT-GLOBAL-01` | `projects/aigc/<项目名>/2-Global/第N集.json` | `aigc-global` | `.agents/skills/aigc/2-Global/templates/episode-root.template.json` | `meta + project_global + groups[].global` |

`OUT-GLOBAL-01` 是本阶段唯一 creative business output。每一集一份 JSON，不使用固定 `episode_root.json` 作为项目运行时输出名。

### Governance Sidecar

| output_id | path | owner | role |
| --- | --- | --- | --- |
| `OUT-GLOBAL-02` | `projects/aigc/<项目名>/2-Global/validation-report.md` | `aigc-global` | 记录验收、阻塞、根因上溯、handoff 与可续跑状态 |

`validation-report.md` 可以写回，但它不是创作业务真源，不替代 `第N集.json`。

### Explicitly Removed Outputs

- `projects/aigc/<项目名>/2-Global/全局风格.md`
- `projects/aigc/<项目名>/2-Global/全集类型元素.md`
- `projects/aigc/<项目名>/2-Global/分组类型元素.md`
- `projects/aigc/<项目名>/2-Global/导演意图.md`
- `projects/aigc/<项目名>/2-Global/episode_root.json` 作为运行时业务输出名

历史项目中已有这些文件时，视为 legacy artifacts；新执行不得更新它们作为主链输出。

## Output Field Gate

`第N集.json` 最低必须满足：

| field_id | target_path | requirement | detail_owner |
| --- | --- | --- | --- |
| `FIELD-GLOBAL-01` | `meta.剧名 / 集数 / 组数 / 总时长` | 与当前项目和当前集严格一致 | `references/字段与验收映射.md` |
| `FIELD-GLOBAL-02` | `project_global.全局风格` | 项目级统一视觉风格前缀；真人古装影视默认遵循写实摄影基线 | `references/全局风格词最佳实践.md` |
| `FIELD-GLOBAL-03` | `project_global.全集类型元素` | 项目级类型总则，不混入单组临场打法 | `references/字段与验收映射.md` |
| `FIELD-GLOBAL-04` | `groups[].分镜组ID` | 与分组正文一一对应 | `references/字段与验收映射.md` |
| `FIELD-GLOBAL-05` | `groups[].global.剧本正文` | 完整整理命中组正文，不摘要 | `references/字段与验收映射.md` |
| `FIELD-GLOBAL-06` | `groups[].global.全局风格` | 默认继承 `project_global.全局风格` | `references/字段与验收映射.md` |
| `FIELD-GLOBAL-07` | `groups[].global.类型元素` | 对齐当前组类型信号 | `references/字段与验收映射.md` |
| `FIELD-GLOBAL-08` | `groups[].global.导演意图` | 至少具备观看策略、执行抓手、禁用方向 | `scripts/validate_director_intent.py`、`review/review-contract.md` |

## Reference Loading Guide

- 先读本 `SKILL.md + CONTEXT.md`，锁定本轮 input/output 与 mode。
- 需要字段细则时读 [references/字段与验收映射.md](references/字段与验收映射.md)。
- 需要节点、scope、汇流或阻塞回路时读 [references/思行网络.md](references/思行网络.md)。
- 需要增量 patch 或 legacy 投影处理时读 [references/增量写回与兼容投影.md](references/增量写回与兼容投影.md)。
- 需要真人古装写实风格词时读 [references/全局风格词最佳实践.md](references/全局风格词最佳实践.md) 与 [steps/全局风格词生成流程.md](steps/全局风格词生成流程.md)。
- 需要类型分流时读 [types/type-map.md](types/type-map.md)。
- 需要交付审计时读 [review/review-contract.md](review/review-contract.md)。
- `templates/` 不再承载 Markdown 业务输出内容模板；读 `templates/README.md` 确认边界，实际 JSON 填写只使用 `templates/episode-root.template.json`。

## Directory Guidance

过程细节按需进入以下 owner，不在 `SKILL.md` 展开：

| need | read |
| --- | --- |
| 输入输出、命名、JSON 写回边界 | `references/io-contract.md`、`references/writeback-contract.md` |
| 字段槽位、验收映射、JSON 最低结构 | `references/字段与验收映射.md` |
| 思行节点、scope、汇流、阻塞回路 | `references/思行网络.md` |
| 增量 patch 与 legacy 投影处理 | `references/增量写回与兼容投影.md` |
| 真人古装写实全局风格词 | `references/全局风格词最佳实践.md`、`steps/全局风格词生成流程.md` |
| 风格类型冲突或非真人媒介例外 | `types/type-map.md` |
| 交付审计、review verdict、降级口径 | `review/review-contract.md` |
| 可复用经验与修复打法 | `CONTEXT.md`、`knowledge-base/global-style-heuristics.md` |
| 模板目录边界确认 | `templates/README.md`；业务输出模板只允许是 `templates/episode-root.template.json` |

## Internal Capability Fusion Contract (Mandatory)

本节只声明能力归属，不展开过程。

| capability | input | output_field | detail_owner |
| --- | --- | --- | --- |
| `global_style_engine` | `north_star / init_handoff / MEMORY / user style` | `project_global.全局风格`、`groups[].global.全局风格` | `references/全局风格词最佳实践.md` |
| `type_bible_engine` | `north_star / init_handoff / 第N集分组正文` | `project_global.全集类型元素` | `references/字段与验收映射.md` |
| `group_type_engine` | `project_global.全集类型元素 / 第N集分组正文` | `groups[].global.类型元素` | `references/思行网络.md` |
| `director_intent_engine` | `groups[].global.剧本正文 / 类型元素 / project_global.*` | `groups[].global.导演意图` | `references/字段与验收映射.md`、`review/review-contract.md` |
| `json_writeback_engine` | 全部已定稿字段 | `projects/aigc/<项目名>/2-Global/第N集.json` | `references/io-contract.md` |
| `convergence_audit_engine` | `第N集.json` | `validation-report.md` verdict | `review/review-contract.md` |

## Field Mapping

字段真源与详细规则见 `Output Field Gate` 及 [references/字段与验收映射.md](references/字段与验收映射.md)。本节保留 `Field Mapping` 标记供审计器识别；不得在此复制完整字段细则。

### Field Master

字段 owner 以 `Output Field Gate` 为主，详细字段约束由 [references/字段与验收映射.md](references/字段与验收映射.md) 承载。

## Thought Pass Map

主文件只保留 pass 首尾映射；节点细节见 [references/思行网络.md](references/思行网络.md)。

| pass_id | input | output |
| --- | --- | --- |
| `P1-input-lock` | 必需输入、可选输入、用户偏好 | `mode + scope + invariant_brief` |
| `P2-synthesis` | 已锁定输入、项目记忆、风格/类型规则 | `project_global.* + groups[].global.*` |
| `P3-writeback` | 全部已定稿字段、`templates/episode-root.template.json` | `projects/aigc/<项目名>/2-Global/第N集.json` |
| `P4-validation` | `第N集.json` | `validation-report.md` 或 blocked verdict |

## Pass Table

| pass | direct_write_target | detail_owner |
| --- | --- | --- |
| `input-lock` | 无业务写回 | `references/思行网络.md` |
| `project-global` | `project_global.全局风格 / 全集类型元素` | `references/全局风格词最佳实践.md`、`references/字段与验收映射.md` |
| `group-global` | `groups[].global.*` | `references/字段与验收映射.md` |
| `json-writeback` | `2-Global/第N集.json` | `references/io-contract.md` |
| `validation` | `validation-report.md` | `review/review-contract.md` |

## One-Shot Output Contract (Mandatory)

一次执行的闭环输出为：

1. 必须写入或 patch：`projects/aigc/<项目名>/2-Global/第N集.json`
2. 必须写入、更新或在最终回复中说明阻塞：`projects/aigc/<项目名>/2-Global/validation-report.md`
3. 必须明确下一入口：`projects/aigc/<项目名>/3-Detail/`

若 `第N集.json` 未能写入，本阶段不得宣称完成，只能返回 blocked verdict。

## Acceptance Checklist

完成本技能前，必须确认：

1. `第N集.json` 已按 `templates/episode-root.template.json` 同构落盘。
2. `groups[].global.剧本正文` 是完整组正文，不是摘要。
3. `groups[].global.类型元素 / 导演意图` 与当前 `分镜组ID` 严格对齐。
4. `project_global.全局风格` 已通过全局风格词门禁；真人古装项目不得滑向动画描线、赛璐璐分层或夸张残影。
5. 本阶段没有生成或更新四个旧 Markdown 作为业务输出。
6. `validation-report.md` 已记录验收、阻塞或 handoff；若被上层策略阻断真实 reviewer/subagent，必须记录降级来源与实际路径。

## Root-Cause Execution Contract (Mandatory)

若本阶段失败，必须按以下链路上溯：

`Symptom -> Direct Cause -> Rule Source -> Meta Rule Source`

常见定位：

- `Symptom`: `第N集.json` 缺失、字段缺失、跨组混写、旧 Markdown 反客为主、组正文被摘要。
- `Direct Cause`: 输入未锁定、输出路径未按集命名、JSON 写回未对齐模板、legacy 投影被误当真源。
- `Rule Source`: 本 `SKILL.md` 的 `Input Contract`、`Output Contract`、`Output Field Gate`、`Directory Guidance`。
- `Meta Rule Source`: 根 `AGENTS.md` 的 `LLM-first creative authorship`、Skill 2.0 分区职责、复合型技能输出治理合同。
