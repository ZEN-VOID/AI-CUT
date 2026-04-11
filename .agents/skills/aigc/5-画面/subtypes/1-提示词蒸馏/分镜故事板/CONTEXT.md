# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-画面/subtypes/1-提示词蒸馏/分镜故事板` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在父级 `5-画面` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把图片落盘当主产物 | 输出合同层 | 回退到 `第N集.json` 图像请求集合 | 在 `SKILL.md + references/output-template.md` 固化“json 为主，生成后置” | 主产物指向 `第N集.json` |
| prompt 没有固定英文前缀 | Prompt 合同层 | 重新按固定前缀 + `storyboard_group` 拼接 | 在 `references/output-template.md` 固化前缀逐字保留 | prompt 开头逐字一致 |
| `storyboard_group` 漏掉组级或镜级内容 | 输入覆盖层 | 回到 director schema 重新提取分镜组内容 | 在 `FIELD-SB-SHEET-02` 固化完整覆盖要求 | prompt 可回链 `剧本正文 + 组间设计 + 分镜明细[]` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `5-画面/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |

## Repair Playbook

1. 先查 `编导/第N集.json` 的 `分镜组列表[]` 是否稳定。
2. 再查 `prompt` 是否严格等于“固定英文前缀 + storyboard_group”。
3. 再查 `storyboard_group` 是否已经覆盖 `剧本正文 + 组间设计 + 分镜明细[]`。
4. 最后查单集 JSON 是否仍以共享模板骨架承接，并确认后续 handoff 字段完整。

## Reusable Heuristics

- `分镜故事板` 的消费单位是“组”，不是“帧”。
- 上游进入 `分镜故事板` 时，优先把 `projects/<项目名>/编导/第N集.json` 视为第一事实源；`3-明细/第N集.md` 只作为人工可读 sidecar。
- 对本子技能来说，最常见漂移不是画风，而是把“图像请求 JSON 蒸馏”误做成“直接图片落盘”。
- 先把 `1-提示词蒸馏` 收口到稳定 JSON，再把一致性和真实生成交给后续子技能，职责边界最清晰。
- 当 prompt 结构已经被固定为“英文前缀 + storyboard_group”时，最稳的做法是不再在子技能里并行维护第二套私有 prompt 模板。
- 当子技能已经稳定后，优先把流程、VSM 与输出骨架下沉到 `references/*.md`，主 `SKILL.md` 只保留入口合同与边界摘要。
- 当 `分镜故事板` 升级思维链时，优先保留 `FIELD-SB-SHEET-*` 接口，再把判断补成 `组边界 -> storyboard_group -> 固定前缀 -> 模板骨架 -> handoff`。

## Case Log

### Case-20260409-AIGC-STORYBOARD-SHEET-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `5-画面/subtypes/1-提示词蒸馏/分镜故事板` 建立了面向当前仓的组级 storyboard 合同与经验层。
- root_cause_or_design_decision: 参考源来自 ZEN-VOID 的 `4-分镜/分镜故事板/生成`，但当前仓的第一事实源已经改成 `projects/<项目名>/3-明细/第N集.md`，因此必须重写输入与落点口径。
- final_fix_or_heuristic: 保留“组级多格 storyboard + episode JSON + manifest”的骨架，把输入改写为 `3-明细` 分镜锚点，把落点改写为 `projects/<项目名>/画面/分镜故事板/`。
- prevention_or_replication_checklist:
  - [x] 输入口径已改写到当前仓
  - [x] 组级输出合同已补齐
  - [x] 单集 JSON / manifest 已固定
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/CONTEXT.md`
- user_feedback_or_constraint: 用户要求参照旧仓分镜故事板能力，但落到当前 `aigc/5-画面` 子技能体系。

### Case-20260409-AIGC-STORYBOARD-SHEET-LATEST-NORM

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板` 子技能重构为“主合同 + references 模块细则”的最新规范结构。
- root_cause_or_design_decision: 原 `SKILL.md` 同时承载边界、workflow、字段表、VSM 与输出骨架，已不符合当前仓同类技能的 canonical 模块化结构。
- final_fix_or_heuristic: 保留“组级 storyboard sheet + episode JSON + manifest”的内容骨架与落点不变，只把字段主表、执行流程、类型策略和输出模板拆入 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已回到摘要式入口合同
  - [x] 四个 `references/*.md` 已补齐
  - [x] 原有落点、对象边界与输出骨架未改变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/output-template.md`
- user_feedback_or_constraint: 用户要求加载最新规范重构，但不改变内容基础。

### Case-20260409-AIGC-STORYBOARD-SHEET-CHAIN-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板/references/chain-of-thought.md` 从旧版三张表升级为最新版 `think-think` 叶子子技能合同。
- root_cause_or_design_decision: 旧版文件虽保留 `FIELD-SB-SHEET-01` 到 `04`，但没有显式写出“为什么先锁组、为什么必须是 multi-panel、何时回退、何时判定输出追溯面成立”，导致对象边界与返工闭环不透明。
- final_fix_or_heuristic: 保持组级字段接口不变，把叶子层思维链升级为“`group_id` -> multi-panel prompt -> 参考锚点 -> episode JSON/manifest -> Gate Summary”的 reasoning-friendly 可见合同。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补 `Think-Think Design Snapshot`
  - [x] 已补 `工具后反思与 Gate Summary`
  - [x] 已保留 `FIELD-SB-SHEET-01` 到 `04` 不变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按最新思维链设计规范优化 `分镜故事板`，同时保持原有组级对象与输出骨架不变。

### Case-20260410-AIGC-STORYBOARD-SHEET-SHARED-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板` 的上游输入合同从 `3-明细/第N集.md` 同步到 `projects/<项目名>/编导/第N集.json + director_episode_output.schema.json`。
- root_cause_or_design_decision: 上游统一输出内容模板已经收口到 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，但 `分镜故事板` 仍把 `3-明细/第N集.md` 与旧本地字段壳当成第一输入真源，导致 shared schema 回链缺位。
- final_fix_or_heuristic: 当时先保留本地 `第N集_storyboard.json + _manifest.json + 图片` 这套消费侧落点，并显式增加 shared schema 回链；该口径已在后续 `Case-20260410-AIGC-STORYBOARD-SHEET-IMAGE-REQUEST-CONTRACT` 中升级为 `第N集.json` 图像请求合同。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已改成 shared schema 输入口径
  - [x] `references/execution-flow.md` 已改成 `编导/第N集.json` 工作流
  - [x] `references/output-template.md` 已补 shared source 回链字段
  - [x] `references/chain-of-thought.md` 与 `references/type-strategies.md` 已同步 shared group list 口径
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/output-template.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/type-strategies.md`
- user_feedback_or_constraint: 用户要求由于上游输出模板改为 shared schema，因此同步调整 `分镜故事板` 相关配置。

### Case-20260410-AIGC-STORYBOARD-SHEET-IMAGE-REQUEST-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板` 从“图片/故事板落盘中心”重定义为“每个分镜组对应 1 条图像生成请求 JSON”的提示词蒸馏合同。
- root_cause_or_design_decision: 若全面对齐 `6-视频/subtypes/1-提示词蒸馏/全能参照` 的配置方式，`1-提示词蒸馏` 阶段的主产物应是可 handoff 的请求 JSON，而不是图片文件；图片生成和一致性处理应后移到独立子技能。
- final_fix_or_heuristic: 在 `5-画面/_shared` 新增共享 `image-generation-input.template.json`，并把 `分镜故事板` 改成“固定英文前缀 + storyboard_group + 图像侧 model 骨架 + 第N集.json”的单输出合同。
- prevention_or_replication_checklist:
  - [x] 共享 JSON 模板已落到 `5-画面/_shared`
  - [x] 主 `SKILL.md` 已改为图像请求 JSON 合同
  - [x] `references/output-template.md` 已改为共享模板填充规则
  - [x] `references/execution-flow.md` 已改为 `json_only/full_trace` 输出逻辑
  - [x] `references/chain-of-thought.md` 与 `references/type-strategies.md` 已同步 handoff 口径
- evidence_paths:
  - `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/output-template.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/references/type-strategies.md`
- user_feedback_or_constraint: 用户明确确认“如果全面对齐 `6-视频/全能参照`，就不该继续把图片落盘当主产物，而应该把每个分镜组对应的图像生成请求 JSON 当主产物”；`2-一致性处理` 与 `3-图像生成` 将后续单独补充。
