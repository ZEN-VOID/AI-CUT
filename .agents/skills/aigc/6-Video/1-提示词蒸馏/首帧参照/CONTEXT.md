# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-Video/1-提示词蒸馏/首帧参照` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在父级 `6-Video` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 直接照搬整组 `剧本正文` | 桥段提取层 | 回到目标 `分镜ID`，重做剧情桥段裁切 | 在 `FIELD-VID-FFR-02` 固化“剧情桥段只对应目标帧” | 剧情桥段与目标镜级事实对齐 |
| `全局风格` 被改写 | 固定文本层 | 恢复原文直贴 | 在输出契约里显式标记“fixed verbatim block” | 与上游逐字一致 |
| prompt 中暴露了字段标题 | 文本编排层 | 重写为无标题融合文本 | 在 `FIELD-VID-FFR-02` 固化只保留组ID/镜ID标签 | 除组ID/镜ID外无显式字段名 |
| 帧级请求没有带出所属 `分镜组ID` | 来源定位层 | 补回 `meta.group_id` 与显式 `分镜组` 标签 | 在字段表中要求 `group_id + source_shot_ids` 成对存在 | 可同时回链到组级与帧级 |
| 为了凑字数而虚构桥段细节 | 字数预算层 | 回退到保守桥段表达，允许 underflow | 在策略表中固化 `ambiguous/underflow` 保守退化规则 | manifest 中有原因备注且无新事实 |
| 规则散落在 `references/*.md` 导致主合同失真 | 真源治理层 | 把字段表、流程、类型策略、输出契约全部回收进 `SKILL.md` | 固化“`SKILL.md` 是唯一规范真源，`CONTEXT.md` 只保留经验层” | 执行无需再依赖 `references/` |
| `6-视频/subtypes/...` 与真实路径 `6-Video/...` 不一致 | 路径合同层 | 统一所有技能内路径与证据路径到真实目录 | 在案例与合同中持续使用真实路径，避免旧路径回潮 | 仓内不再残留命中的旧路径字符串 |
| 只把章节标题改成知行合一口径，但桥段判型、预算压缩、写回与汇流仍是旧线性说明书 | 思行网络层 | 把执行链重排为 `任务归位 -> 判型 -> 提取 -> 压缩 -> 写回 -> 汇流` 的节点网络 | 在 `SKILL.md` 固化 `Business Requirement Analysis + Topology + Thinking-Action Node + Convergence + One-Shot Output` 五层结构 | 关键链路可通过节点与 Mermaid 一眼定位 |
| 概述中的 canonical 路径漂到不存在的仓库根（如 `AIGC-DREAMER`） | 路径真源层 | 回收所有本地目录说明到当前真实技能树路径 | 在 leaf 合同、经验层与 changelog 中统一使用 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/` | 文档路径、evidence path 与仓内真实目录一致 |

## Repair Playbook

1. 先查目标 `分镜ID` 是否真实存在于某个 `分镜组`。
2. 再查 `剧情桥段` 是否只描述该目标分镜可支持的动作、状态或事件阶段。
3. 再查 `全局风格` 是否保持原文。
4. 再查其余组级与镜级字段是否已压缩进 prompt，且没有字段标题残留。
5. 最后查 `prompt_char_count`、双输出文件与 manifest 是否一致。

## Reusable Heuristics

- 帧级视频请求最容易失真在“把整组剧情搬过来”，而不是“文字不够华丽”。
- `剧情桥段` 的职责是把整组剧本正文切成目标镜头可见的一小段，不是重写剧情，也不是摘要整组剧情。
- 当一个分镜组只有 1 个分镜时，直接使用整段 `剧本正文` 作为剧情桥段，通常最稳。
- 当一个分镜组有多个分镜而桥段边界不够清晰时，优先锚定目标分镜的可见动作、人物状态和空间关系，保守缩写，不虚构过渡。
- 帧级 prompt 仍然需要组级空气层，所以最稳结构通常是：`剧情桥段 + 全局风格 + 压缩后的类型元素/导演意图 + 目标镜级字段`。
- 帧级提示词的字数窗应低于组级；若上游信息有限，允许 underflow，但必须把原因写进 manifest，而不是用空泛修辞补字数。
- 当叶子技能已经稳定时，字段表、流程、类型策略和输出契约应收束进单一 `SKILL.md`；经验层只保留 failure map、repair playbook 和 milestone case。
- 技能路径一旦完成真实目录切换，后续 case、evidence path 和默认加载路径都必须同步使用真实路径，不能继续沿用旧别名。
- 对帧级 `首帧参照` 做知行合一改造时，最稳的方式不是改变桥段/模板机制，而是把既有机制重织成更细的思行节点，让“判型、提取、预算、写回、汇流”全部显性化。
- 当用户明确要求 `复杂链路的骨架 / 细则分层 = false` 时，应把复杂度体现在节点粒度和 Mermaid 治理密度上，而不是再拆出第二份 references 真源。

## Case Log

### Case-20260410-AIGC-VIDEO-FIRST-FRAME-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `6-Video/1-提示词蒸馏/首帧参照` 建立了从 `3-Detail/第N集.json` 单一 `分镜ID` 到帧级视频请求 JSON 的叶子合同。
- root_cause_or_design_decision: 用户需求已明确要求“站在分镜帧颗粒度，按分镜ID组织提示词，并把剧本正文切成对应分镜帧的剧情桥段”；若仍沿用组级 `全能参照` 规则，会把最关键的帧级桥段提取问题留成隐式人工判断。
- final_fix_or_heuristic: 将“单帧定位、剧情桥段提取、全局风格固定保留、其余字段均匀压缩、双输出模式、参照图暂留空”的规则写成稳定的叶子执行合同，并让 `meta.source_shot_ids` 固定承载单一目标 `分镜ID`。
- prevention_or_replication_checklist:
  - [x] 帧级来源定位已写入合同
  - [x] `剧本正文 -> 剧情桥段` 规则已写入策略
  - [x] 双输出落点已写入合同
  - [x] `source_shot_ids` 已回链共享模板
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`
- user_feedback_or_constraint: 用户明确要求默认读取 `projects/<项目名>/3-Detail/第N集.json`，模板参照共享 JSON/TXT 模板，提示词以分镜组内容为基础，但当前站在分镜帧颗粒度，只处理单一 `分镜ID`，并将剧本正文调整为对应分镜帧的剧情桥段。

### Case-20260412-AIGC-VIDEO-FIRST-FRAME-SINGLE-SOURCE-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `首帧参照` 从“`SKILL.md` 摘要 + `references/*.md` 规范外置”升级为单一 `SKILL.md` 主合同，并补齐 `CHANGELOG.md` 与 `agents/openai.yaml`。
- root_cause_or_design_decision: 原结构把字段表、执行流程、类型策略和输出契约拆散到 `references/*.md`，同时继续保留旧路径 `6-视频/subtypes/...`，导致执行者必须跨文件拼合同，且实际目录与文档入口漂移。
- final_fix_or_heuristic: 将字段表、workflow、variable register、case-to-strategy、output contract 与 audit contract 全部回收进 `SKILL.md`，同步把路径口径统一到 `6-Video/1-提示词蒸馏/首帧参照`，并新增 interface metadata 与 changelog 作为稳定交付面。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已成为唯一规范真源
  - [x] `CONTEXT.md` 只保留经验层与里程碑案例
  - [x] `agents/openai.yaml` 已补齐
  - [x] `CHANGELOG.md` 已记录升格与迁移
  - [x] 目标目录不再依赖 `references/*.md`
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CHANGELOG.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“针对 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照` 执行全量升格重构，references 内容整合到 `SKILL.md` 内，不再以 references 作为载体引用”。

### Case-20260412-AIGC-VIDEO-FIRST-FRAME-ZHI-XING-NETWORK

- milestone_type: source_contract_change
- outcome: 在不改变 `首帧参照` 现有输入输出、桥段判型、共享模板、字数窗和三件套机制的前提下，将其重排为知行合一的 inline-full-spec 单技能网络。
- root_cause_or_design_decision: 现有 `首帧参照` 虽然已经是单一 `SKILL.md` 主合同，但表达形态仍偏传统“workflow + field tables”说明书，且节点粒度不足，无法把用户要求的“每一个思维·执行节点从哪些方面着手，一步一步足够细致”显性化。
- final_fix_or_heuristic: 保留现有帧级机制，只把结构重排为 `Business Requirement Analysis -> Total Input -> Topology -> N0-N9 思行节点 -> Convergence -> One-Shot Output`，并显式写出 `bridge_mode`、`budget_state`、汇流门与 `思考过程` closure。
- prevention_or_replication_checklist:
  - [x] 未改变 `projects/<项目名>/6-Video/首帧参照/第N集/` 三件套落点
  - [x] 保留 `FIELD-VID-FFR-01` 到 `FIELD-VID-FFR-04`
  - [x] 已把桥段判型、预算压缩、模板骨架与写回汇流改为细粒度节点
  - [x] 已显式写明 `复杂链路的骨架 / 细则分层 = false`
  - [x] 已修正概述中的仓库根路径漂移
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CHANGELOG.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“重构 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照` 下相关子技能包，内容和机制上全量参照现有配置，但根据知行合一的规范进行编排；‘复杂链路的骨架 / 细则分层’: false；每一个思维·执行节点一步一步足够细致”。
