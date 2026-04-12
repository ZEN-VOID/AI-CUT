# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-Image/1-提示词蒸馏/分镜帧` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md` 之后加载本文件。
- 当前知识沉淀已与 `skill-知行合一` 对齐：优先记录节点边界、回退入口、汇流门和可复用 heuristics，而不是记录一次性过程描述。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
soft_limit_cases: 16
hard_limit_cases: 32
status: ok
last_checked_at: 2026-04-12T21:20:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `分镜ID` 仍是局部编号 | ID 归一层 | 重新归一为四段式 canonical ID | 在 `SKILL.md` 输入合同中固化四段式要求 | 单帧条目可全局回链 |
| 下游仍按旧 detail markdown sidecar 读取上游 | 输入真源层 | 切换到 `projects/<项目名>/3-Detail/第N集.json` 并按 shared schema 锁定目标分镜 | 在 `SKILL.md` 固化 `final_output.main_content.分镜组列表[].分镜明细[]` 取数路径 | 单帧条目能回链 shared director schema |
| `single_frame_shot` 混入整组剧情或大段对白 | 内容归纳层 | 收缩到当前目标分镜与其必要组级上下文 | 把 `single_frame_shot` 定义为单帧内容块，而非整组剧情摘要 | 内容块不再复述整段台词 |
| prompt 没有固定单帧前缀 | Prompt 合同层 | 重新按固定前缀 + `single_frame_shot` 拼接 | 在 `SKILL.md` 固化前缀逐字保留 | prompt 开头逐字一致 |
| 仍把图片落盘当主产物 | 输出契约层 | 回退到 `第N集.json` 单帧图像请求集合 | 将 JSON 视为必要 completeness carrier | 主产物指向 `第N集.json` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `5-Image/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |
| 叶子 skill 规范被切碎到多个 `references/*.md` | 真源治理层 | 把思维链、workflow、VSM、输出契约回收到单一 `SKILL.md` | 将 `SKILL.md` 设为叶子技能唯一规范真源，`CONTEXT.md` 只保留经验层 | 不再需要依赖 `references/` 才能完整执行 |
| 步骤不少，但每一步没有 `route_out` 或回退入口 | 节点合同层 | 把线性步骤改写为知行合一思行节点 | 在 `SKILL.md` 固化 `Topology + Node Network + Convergence` 三联合同 | 出错时能准确回到具体节点 |
| 汇流前已经写回，导致 JSON 和 manifest 口径漂移 | 汇流审计层 | 在落盘前增加统一审计门，先判 `json_only/full_trace` 再写回 | 将 `N7-CONVERGENCE-AUDIT` 固化为写回前硬门槛 | 输出模式与落盘文件保持一致 |

## Repair Playbook

1. 先锁唯一 `分镜ID`。
2. 再检查 `single_frame_shot` 是否只服务当前目标分镜与其必要组级上下文。
3. 再检查 `prompt` 是否严格等于“固定单帧前缀 + single_frame_shot”。
4. 再确认共享模板骨架是否完整，尤其是 `reference_images / image_markers`。
5. 最后确认 JSON 是否为主产物，manifest 是否按需成立。
6. 若步骤无法说明“为什么能继续往下走”，优先修 `Topology / Node Network / Convergence Contract`，而不是继续堆补文字说明。

## Reusable Heuristics

- 单帧技能最容易漂移的不是画风，而是“对象边界”。
- 先锁 ID，再写 `single_frame_shot`，否则所有单帧内容块都会失真。
- 当上游导演真源已切到 `director_episode_output.schema.json` 后，`分镜帧` 必须先从 `final_output.main_content.分镜组列表[].分镜明细[]` 取镜，再做本地单帧投影。
- 对单帧技能来说，JSON / manifest 比图片更能证明这张图到底对应哪一镜。
- 当固定前缀已经定义“单帧、无多格、无文字覆盖”的页面约束时，最稳的做法是不再并行维护第二套私有 prompt 模板。
- 对这种边界稳定、字段数有限的叶子技能，`思行节点 + 汇流门 + 一次性输出` 通常比“长 checklist + 多张表”更抗漂移。
- 若一个节点不能同时回答“我处理了什么事实”和“我为什么可以流向下一步”，它通常还不是合格的叶子思行节点。

## Case Log

### Case-20260410-AIGC-STORYBOARD-FRAME-SHARED-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `分镜帧` 的上游输入合同同步到 `projects/<项目名>/3-Detail/第N集.json` 的 shared director schema。
- root_cause_or_design_decision: 上游内容输出模板已经统一收口到 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，但 `分镜帧` 仍按旧 detail sidecar 思路描述取数，导致输入真源漂移。
- final_fix_or_heuristic: 把上游锁镜路径显式改为 `final_output.main_content.分镜组列表[].分镜明细[]`，并在本地合同与经验层中统一回指 shared schema。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已写明上游输入真源与 shared schema
  - [x] 字段级上游映射已并入叶子主合同
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/CONTEXT.md`
- user_feedback_or_constraint: 用户要求随着上游 shared schema 收口，同步修正 `分镜帧` 的取数合同。

### Case-20260410-AIGC-STORYBOARD-FRAME-IMAGE-REQUEST-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `分镜帧` 重定义为“单一 `分镜ID` 对应 1 条图像生成请求 JSON”的提示词蒸馏合同。
- root_cause_or_design_decision: 若 `分镜帧` 要对齐后续下游消费链，就不应继续把图片落盘当 `1-提示词蒸馏` 阶段主产物；主产物必须前移到可 handoff 的请求 JSON。
- final_fix_or_heuristic: 复用 `5-Image/_shared/image-generation-input.template.json`，并把 `分镜帧` 改成“固定单帧前缀 + single_frame_shot + 图像侧 model 骨架 + 第N集.json”的单输出合同。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已改为单帧图像请求 JSON 合同
  - [x] 固定单帧前缀已固化
  - [x] 输出模式已收束为 `json_only/full_trace`
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/CONTEXT.md`
- user_feedback_or_constraint: 用户要求 `分镜帧` 按首帧参照类上下文范式重构，并由我直接补固定前缀后全量执行。

### Case-20260412-AIGC-STORYBOARD-FRAME-INLINE-SKILL-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `分镜帧` 从“主合同 + references 模块”重构为单一 `SKILL.md` 真源，并补齐 `agents/openai.yaml` 与 `CHANGELOG.md`。
- root_cause_or_design_decision: 该叶子技能的字段表、执行流程、类型策略与输出契约被拆到四份 `references/*.md`，导致修改 prompt、路径、共享模板或取数规则时需要多点同步。
- final_fix_or_heuristic: 把四类规范全部内联回 `SKILL.md`，删除 `references` 载体，新增 interface metadata 与结构变更记录，并把本技能的 path contract 统一到 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧`。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已成为唯一规范真源
  - [x] `references/` 已退场
  - [x] `agents/openai.yaml` 已补建
  - [x] `CHANGELOG.md` 已补建
  - [x] 旧路径与旧 references 引用已回扫
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/CHANGELOG.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求对 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧` 执行全量升格重构，并把 `references` 内容整合进 `SKILL.md`，不再以 `references` 为载体引用。

### Case-20260412-AIGC-STORYBOARD-FRAME-THINKING-ACTION-REORCHESTRATION

- milestone_type: source_contract_change
- outcome: 在不改变现有业务机制的前提下，将 `分镜帧` 从“线性叶子合同”重排为知行合一式思行节点网络。
- root_cause_or_design_decision: 旧合同虽然已经是单文件真源，但仍主要表现为 `Mandatory Workflow + Type Table + Field Table` 的线性组织；对“每一步从哪些方面着手、为何能流向下一步、何时应该回退到哪个节点”的表达不足，无法满足知行合一的节点密度要求。
- final_fix_or_heuristic: 保持 `json_only/full_trace`、固定前缀、共享模板、单帧对象边界与落盘路径不变，只把执行真源重写为 `Total Input Contract + Topology Contract + Thinking-Action Node Network + Convergence Contract + One-Shot Output Contract`，并为每个节点补齐“从哪些方面着手 + 一步一步怎么做 + 未达标信号”。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已包含至少 3 张 Mermaid 图
  - [x] `SKILL.md` 已包含节点六槽位网络
  - [x] `SKILL.md` 已补齐汇流审计门与思考过程输出说明
  - [x] 未重新引入 `references/` 第二真源
  - [x] 业务输出机制仍保持 `第N集.json + 可选 manifest`
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/CHANGELOG.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求该技能按 `skill-知行合一` 重编排，且指定“复杂链路的骨架 / 细则分层”为 `false`，并要求每一个思维·执行节点都写清楚从哪些方面着手、一步一步如何执行。
