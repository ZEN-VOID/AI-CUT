# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-画面/subtypes/1-提示词蒸馏/漫画` 的经验层知识库，不是过程日志。
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
| 仍把图片落盘当主产物 | 输出合同层 | 回退到 `第N集.json` 漫画图像请求集合 | 在 `SKILL.md + references/output-template.md` 固化“json 为主，生成后置” | 主产物指向 `第N集.json` |
| prompt 没有固定漫画前缀 | Prompt 合同层 | 重新按固定前缀 + `comic_page_group` 拼接 | 在 `references/output-template.md` 固化前缀逐字保留 | prompt 开头逐字一致 |
| `comic_page_group` 漏掉组级或镜级内容 | 输入覆盖层 | 回到 director schema 重新提取分镜组内容 | 在 `FIELD-SB-COMIC-02` 固化完整覆盖要求 | prompt 可回链 `剧本正文 + 组间设计 + 分镜明细[]` |
| `1 shot = 1 panel` 或文字归属约束未进入 prompt | 页面语言层 | 回到 `comic_page_group` 补漫画硬门槛 | 在固定前缀与内容块同时固化漫画约束 | prompt 明确一镜一格和文字归属 |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `5-画面/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |

## Repair Playbook

1. 先查当前页是否能唯一回链原分镜组。
2. 再查 `prompt` 是否严格等于“固定漫画前缀 + comic_page_group”。
3. 再查 `comic_page_group` 是否已经覆盖 `剧本正文 + 组间设计 + 分镜明细[]`，并写入 `1 shot = 1 panel` 与文字归属约束。
4. 最后查单集 JSON 是否仍以共享模板骨架承接，并确认后续 handoff 字段完整。

## Reusable Heuristics

- 漫画子技能最常见的漂移不是画风，而是把“漫画图像请求 JSON 蒸馏”误做成“直接页图落盘”。
- 对漫画子技能来说，最关键的硬门槛是 `1 shot = 1 panel` 与文字系统必须显式约束到对应 panel。
- 当固定前缀已经定义页面语言时，最稳的做法是不再在子技能里并行维护第二套私有 prompt 模板。
- 当漫画页合同已经稳定后，优先把 workflow、VSM 与输出骨架下沉到 `references/*.md`，主 `SKILL.md` 只保留入口、边界与硬门槛摘要。
- 当 `漫画` 升级思维链时，优先保留 `FIELD-SB-COMIC-*` 接口，再把判断补成 `组边界 -> comic_page_group -> 固定前缀 -> 模板骨架 -> handoff`。
- 当上游导演集输出已经收束到 shared schema 时，`漫画` 应优先消费 `projects/<项目名>/编导/第N集.json` 的 `final_output.main_content.分镜组列表[]`，把 `3-明细/第N集.md` 降为补充对白与上下文证据，而不是继续把它当第一结构化真源。

## Case Log

### Case-20260409-AIGC-STORYBOARD-COMIC-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `5-画面/subtypes/1-提示词蒸馏/漫画` 建立了漫画页改编合同与经验层。
- root_cause_or_design_decision: 参考源来自 ZEN-VOID 的 `漫画故事板`，但当前仓需要服务 `projects/<项目名>/3-明细` 内联分镜与当前 `5-画面/漫画/` 落点，因此不能直接沿用旧阶段路径与旧父子关系。
- final_fix_or_heuristic: 保留“分镜组 -> 漫画页”的消费骨架，把输入重写为当前仓脚本分镜锚点，把输出收口到 `projects/<项目名>/5-画面/漫画/`，并显式固化 `1 shot = 1 panel`。
- prevention_or_replication_checklist:
  - [x] 当前仓输入真源已改写
  - [x] `1 shot = 1 panel` 已固化
  - [x] 页级 JSON / manifest 已固定
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/CONTEXT.md`
- user_feedback_or_constraint: 用户要求保留旧仓漫画能力的方向，但必须转成当前 `aigc/5-画面/subtypes/1-提示词蒸馏/漫画` 的治理结构。

### Case-20260409-AIGC-STORYBOARD-COMIC-LATEST-NORM

- milestone_type: source_contract_change
- outcome: 将 `漫画` 子技能重构为“主合同 + references 模块细则”的最新规范结构。
- root_cause_or_design_decision: 原 `SKILL.md` 同时承载漫画页入口、workflow、字段表、类型策略与输出骨架，已不符合当前仓同类技能的 canonical 模块化结构。
- final_fix_or_heuristic: 保留“分镜组 -> 漫画页 + `1 shot = 1 panel` + 页级 JSON/manifest”的能力骨架与路径不变，只把字段主表、执行流程、类型策略和输出模板拆入 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已回到摘要式漫画页入口合同
  - [x] 四个 `references/*.md` 已补齐
  - [x] 原有页面语言硬门槛与追溯骨架未改变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/output-template.md`
- user_feedback_or_constraint: 用户要求加载最新规范重构，但不改变内容基础。

### Case-20260409-AIGC-STORYBOARD-COMIC-CHAIN-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `漫画/references/chain-of-thought.md` 从旧版三张表升级为最新版 `think-think` 叶子子技能合同。
- root_cause_or_design_decision: 旧版文件虽保留 `FIELD-SB-COMIC-01` 到 `04`，但没有显式写出“为什么先锁组、何时 `1 shot = 1 panel` 才成立、何时页面仍是漫画页而非 storyboard 排格”，导致页面语言与返工闭环不透明。
- final_fix_or_heuristic: 保持漫画页字段接口不变，把叶子层思维链升级为“`group_id` -> panel 对位与文字落点 -> layout_plan -> comic JSON/manifest -> Gate Summary”的 reasoning-friendly 可见合同。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补 `Think-Think Design Snapshot`
  - [x] 已补 `工具后反思与 Gate Summary`
  - [x] 已保留 `FIELD-SB-COMIC-01` 到 `04` 不变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按最新思维链设计规范优化 `漫画`，同时保持原有漫画页对象边界与 `1 shot = 1 panel` 硬门槛不变。

### Case-20260410-AIGC-STORYBOARD-COMIC-SHARED-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `漫画` 子技能的上游结构化输入从旧的 `3-明细/第N集.md` 口径同步到 `.agents/skills/aigc/_shared/director_episode_output.schema.json`。
- root_cause_or_design_decision: 上游导演集输出模板已统一收束到 `projects/<项目名>/编导/第N集.json + director_episode_output.schema.json`，但 `漫画` 仍把 `3-明细/第N集.md` 写成第一输入真源，并在输出契约里保留了旧的平行顶层骨架说明，形成源层漂移。
- final_fix_or_heuristic: 将 `漫画/SKILL.md` 与 `references/*.md` 统一改为“先消费 shared schema 的 `分镜组列表[]`，再生成本地漫画页台账”，并显式禁止再定义第二份与 shared schema 平行竞争的 episode 顶层模板。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已改写为 shared schema 输入口径
  - [x] `output-template.md` 已改成“上游 shared schema + 本地页级台账”双层说明
  - [x] `execution-flow.md` / `chain-of-thought.md` / `type-strategies.md` 已切到 `编导/第N集.json`
  - [x] `3-明细/第N集.md` 已降级为补充证据而非第一结构化真源
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/output-template.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/CONTEXT.md`
- user_feedback_or_constraint: 用户要求由于上游输出内容模板已经调整为 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，将 `5-画面/subtypes/1-提示词蒸馏/漫画` 相关配置同步调整。

### Case-20260410-AIGC-STORYBOARD-COMIC-IMAGE-REQUEST-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `漫画` 从“漫画页图片/页级台账中心”重定义为“每个分镜组对应 1 条漫画图像生成请求 JSON”的提示词蒸馏合同。
- root_cause_or_design_decision: 既然 `漫画` 要与 `分镜故事板` 共享 `1-提示词蒸馏` 的上下文范式和 `5-画面/_shared` 的图像模板真源，就不应继续把页图落盘当主产物；主产物必须前移到可 handoff 的请求 JSON。
- final_fix_or_heuristic: 复用 `5-画面/_shared/image-generation-input.template.json`，并把 `漫画` 改成“固定漫画前缀 + comic_page_group + 图像侧 model 骨架 + 第N集.json”的单输出合同。
- prevention_or_replication_checklist:
  - [x] 共享 JSON 模板已升级为由各子技能填充 `prompt_style.type`
  - [x] 主 `SKILL.md` 已改为漫画图像请求 JSON 合同
  - [x] `references/output-template.md` 已改为共享模板填充规则
  - [x] `references/execution-flow.md` 已改为 `json_only/full_trace` 输出逻辑
  - [x] `references/chain-of-thought.md` 与 `references/type-strategies.md` 已同步 handoff 口径
- evidence_paths:
  - `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/output-template.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/references/type-strategies.md`
- user_feedback_or_constraint: 用户要求 `漫画` 按 `分镜故事板` 的上下文范式重构，基本范式一致，仅把固定前缀换成漫画专属版本。
