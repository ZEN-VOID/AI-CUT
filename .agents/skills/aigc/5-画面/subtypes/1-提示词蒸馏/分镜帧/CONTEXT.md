# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-画面/subtypes/1-提示词蒸馏/分镜帧` 的经验层知识库，不是过程日志。
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
| `分镜ID` 仍是局部编号 | ID 归一层 | 重新归一为四段式 canonical ID | 在输入合同中固化四段式要求 | 单帧条目可全局回链 |
| 下游仍按 `3-明细/第N集.md` 读取上游 | 输入真源层 | 切换到 `projects/<项目名>/编导/第N集.json` 并按 shared schema 锁定目标分镜 | 在 `SKILL.md + references/*.md` 固化 `final_output.main_content.分镜组列表[].分镜明细[]` 取数路径 | 单帧条目能回链 shared director schema |
| `single_frame_shot` 混入整组剧情或大段对白 | 内容归纳层 | 收缩到当前目标分镜与其必要组级上下文 | 把 `single_frame_shot` 定义为单帧内容块，而非整组剧情摘要 | 内容块不再复述整段台词 |
| prompt 没有固定单帧前缀 | Prompt 合同层 | 重新按固定前缀 + `single_frame_shot` 拼接 | 在 `references/output-template.md` 固化前缀逐字保留 | prompt 开头逐字一致 |
| 仍把图片落盘当主产物 | 输出契约层 | 回退到 `第N集.json` 单帧图像请求集合 | 将 JSON 视为必要 completeness carrier | 主产物指向 `第N集.json` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `5-画面/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |

## Repair Playbook

1. 先锁唯一 `分镜ID`。
2. 再检查 `prompt` 是否严格等于“固定单帧前缀 + single_frame_shot”。
3. 再确认 `single_frame_shot` 是否只服务当前目标分镜与其必要组级上下文。
4. 最后确认 JSON 是否为主产物，manifest 是否按需成立。

## Reusable Heuristics

- 单帧技能最容易漂移的不是画风，而是“对象边界”。
- 先锁 ID，再写 `single_frame_shot`，否则所有单帧内容块都会失真。
- 当上游导演真源已切到 `director_episode_output.schema.json` 后，`分镜帧` 必须先从 `final_output.main_content.分镜组列表[].分镜明细[]` 取镜，再做本地单帧投影。
- 对单帧技能来说，JSON / manifest 比图片更能证明这张图到底对应哪一镜。
- 当固定前缀已经定义“单帧、无多格、无文字覆盖”的页面约束时，最稳的做法是不再在子技能里并行维护第二套私有 prompt 模板。
- 当单帧子技能已经稳定后，优先把 workflow、VSM 与输出骨架下沉到 `references/*.md`，主 `SKILL.md` 只保留入口、边界与门禁。
- 当 `分镜帧` 升级思维链时，优先保留 `FIELD-SB-FRAME-*` 接口，再把判断补成 `唯一 ID -> single_frame_shot -> 固定前缀 -> 模板骨架 -> handoff`。

## Case Log

### Case-20260409-AIGC-STORYBOARD-FRAME-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `5-画面/subtypes/1-提示词蒸馏/分镜帧` 建立了单帧合同与经验层。
- root_cause_or_design_decision: 参考源来自 ZEN-VOID 的 `分镜帧`，但当前仓要服务的是 `projects/<项目名>/3-明细` 的分镜锚点体系，因此必须把“单帧单位”改写为当前仓四段式 `分镜ID`。
- final_fix_or_heuristic: 保留“单帧条目 + 单帧 JSON + manifest”的骨架，把输入改写为脚本内联分镜，把 ID 合同改写为四段式 canonical。
- prevention_or_replication_checklist:
  - [x] 四段式 `分镜ID` 已固定
  - [x] `分镜情节` 已定义为画面摘要
  - [x] JSON / manifest 追溯面已固定
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/CONTEXT.md`
- user_feedback_or_constraint: 用户要求当前仓 `5-画面` 下要有与旧仓相对应的单帧子技能，但不再沿用旧阶段路径真源。

### Case-20260409-AIGC-STORYBOARD-FRAME-LATEST-NORM

- milestone_type: source_contract_change
- outcome: 将 `分镜帧` 子技能重构为“主合同 + references 模块细则”的最新规范结构。
- root_cause_or_design_decision: 原 `SKILL.md` 同时承载单帧入口、workflow、字段表、类型策略与输出骨架，结构上已经过重，不利于后续继续沿当前仓规范维护。
- final_fix_or_heuristic: 保留“四段式 `分镜ID` + 单帧 JSON + manifest + 图片”的能力骨架与路径不变，只把字段主表、执行流程、类型策略和输出模板下沉到 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已回到摘要式单帧入口合同
  - [x] 四个 `references/*.md` 已补齐
  - [x] 原有单帧对象边界、ID 规则与追溯骨架未改变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/output-template.md`
- user_feedback_or_constraint: 用户要求加载最新规范重构，但不改变内容基础。

### Case-20260409-AIGC-STORYBOARD-FRAME-CHAIN-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `分镜帧/references/chain-of-thought.md` 从旧版三张表升级为最新版 `think-think` 叶子子技能合同。
- root_cause_or_design_decision: 旧版文件虽保留 `FIELD-SB-FRAME-01` 到 `04`，但没有显式写出“唯一 `分镜ID` 为什么是第一门”“何时摘要已越界成整组剧情”“何时单帧台账才算成立”，导致单帧对象边界与返工路径不透明。
- final_fix_or_heuristic: 保持单帧字段接口不变，把叶子层思维链升级为“唯一 `分镜ID` -> 当前帧画面 -> 单帧锚点 -> single_frame JSON/manifest -> Gate Summary”的 reasoning-friendly 可见合同。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补 `Think-Think Design Snapshot`
  - [x] 已补 `工具后反思与 Gate Summary`
  - [x] 已保留 `FIELD-SB-FRAME-01` 到 `04` 不变
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按最新思维链设计规范优化 `分镜帧`，同时保持原有四段式 `分镜ID` 与单帧输出骨架不变。

### Case-20260410-AIGC-STORYBOARD-FRAME-SHARED-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `分镜帧` 的上游输入合同从旧 `3-明细/第N集.md` 同步到 `projects/<项目名>/编导/第N集.json` 的 shared director schema。
- root_cause_or_design_decision: 上游内容输出模板已经统一收口到 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，但 `分镜帧` 叶子合同仍按旧 `3-明细` 文本主稿描述取数，导致输入真源与字段投影发生漂移。
- final_fix_or_heuristic: 保留本地 `meta + groups` 单帧汇总骨架不变，把上游锁镜路径显式改为 `final_output.main_content.分镜组列表[].分镜明细[]`，并在 `SKILL.md + references/*.md + CONTEXT.md` 中统一回指 shared schema。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已写明上游输入真源与 shared schema
  - [x] `references/execution-flow.md` 已切换为 `编导/第N集.json` 输入合同
  - [x] `references/output-template.md` 已补 shared schema 输入投影说明
  - [x] `references/chain-of-thought.md` 已补字段级上游映射
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/output-template.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/CONTEXT.md`
- user_feedback_or_constraint: 用户要求因为上游输出内容模板已调整为 shared schema，所以同步修正 `5-画面/subtypes/1-提示词蒸馏/分镜帧` 的相关配置。

### Case-20260410-AIGC-STORYBOARD-FRAME-IMAGE-REQUEST-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `分镜帧` 从“单帧图片/单帧台账中心”重定义为“单一 `分镜ID` 对应 1 条图像生成请求 JSON”的提示词蒸馏合同。
- root_cause_or_design_decision: 若 `分镜帧` 要对齐 `6-视频/subtypes/1-提示词蒸馏/首帧参照` 的上下文范式，就不应继续把图片落盘当 `1-提示词蒸馏` 阶段主产物；主产物必须前移到可 handoff 的请求 JSON。
- final_fix_or_heuristic: 复用 `5-画面/_shared/image-generation-input.template.json`，并把 `分镜帧` 改成“固定单帧前缀 + single_frame_shot + 图像侧 model 骨架 + 第N集.json”的单输出合同。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已改为单帧图像请求 JSON 合同
  - [x] `references/output-template.md` 已改为共享模板填充规则
  - [x] `references/execution-flow.md` 已改为 `json_only/full_trace` 输出逻辑
  - [x] `references/chain-of-thought.md` 与 `references/type-strategies.md` 已同步 handoff 口径
  - [x] 固定单帧前缀已固化
- evidence_paths:
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/output-template.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/execution-flow.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/chain-of-thought.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/references/type-strategies.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜帧/CONTEXT.md`
- user_feedback_or_constraint: 用户要求 `分镜帧` 按 `6-视频/首帧参照` 的上下文范式重构，并由我直接补固定前缀后全量执行。
