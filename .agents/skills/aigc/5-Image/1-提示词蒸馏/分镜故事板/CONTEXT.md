# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在根 `.agents/skills/aigc/SKILL.md` 与父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 之后加载本文件。
- 当前仓没有独立的 `.agents/skills/aigc/5-Image/SKILL.md` 阶段根合同；若再次出现该旧回链，应视为源层漂移。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把图片落盘当主产物 | 输出合同层 | 回退到 `第N集.json` 图像请求集合 | 在 `SKILL.md` 固化“json 为主，生成后置” | 主产物指向 `第N集.json` |
| prompt 没有固定英文前缀 | Prompt 合同层 | 重新按固定前缀 + `storyboard_group` 拼接 | 在 `N4` 与 `FIELD-SB-SHEET-02` 固化前缀逐字保留与拼接顺序 | prompt 开头逐字一致 |
| `storyboard_group` 漏掉组级或镜级内容 | 输入覆盖层 | 回到 director schema 重新提取分镜组内容 | 在 `N3` 固化字段覆盖检查 | prompt 可回链 `剧本正文 + 组间设计 + 分镜明细[]` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `.agents/skills/aigc/5-Image/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |
| 规范又被拆回 `references` 或其他副本 | 真源治理层 | 回收规范到当前 `SKILL.md` | 固化“单文件真源 + `复杂链路的骨架 / 细则分层: false`” | 目录下不再存在第二套规范载体 |
| 节点只有动作没有路由与门禁 | 思行网络层 | 给对应节点补 `route_out / gate` | 在 `Thinking-Action Node Contract` 强制六槽位 | 每个关键节点都可回退或汇流 |
| 仍引用不存在的 `5-Image/SKILL.md` | 上游回链层 | 改回根 `aigc` + 父级 `1-提示词蒸馏` 加载顺序 | 在 `Total Input Contract` 固化真实加载链 | 本包内不再出现旧路径引用 |

## Repair Playbook

1. 先查 `N0` 是否锁定了“组级 storyboard 请求 JSON 蒸馏”而不是其他对象。
2. 再查 `N1` 的 shared schema 与 `分镜组列表[]` 是否成立。
3. 再查 `N2` 的 `group_id + source_shot_ids` 是否唯一且有序。
4. 再查 `N3` 是否已经覆盖 `剧本正文 + 组间设计 + 分镜明细[]`。
5. 再查 `N4` 是否严格等于“固定英文前缀 + storyboard_group”。
6. 再查 `N5` 是否仍以共享模板骨架承接，并确认 `reference_images / image_markers` 没被删。
7. 最后查 `N6` 是否正确落 `第N集.json`，以及 `full_trace` 时 `_manifest.json` 是否与之互相追溯。

## Reusable Heuristics

- `分镜故事板` 的消费单位始终是“组”，不是“帧”。
- 对这个叶子技能而言，复杂度主要来自节点门禁与汇流，而不是多角色协作；优先用单技能知行网络，不要过早升格为 subagents。
- 上游进入 `分镜故事板` 时，优先把 `projects/<项目名>/3-Detail/第N集.json` 视为第一事实源；`3-Detail/evidence/` 只作为人工可读证据。
- 当 `复杂链路的骨架 / 细则分层` 固定为 `false` 时，复杂节点细则必须直接留在 `SKILL.md`，不能再借 `references/` 旁路外包。
- 对本技能来说，最常见漂移不是画风，而是把“图像请求 JSON 蒸馏”误做成“直接图片落盘”或“只写线性步骤不写汇流门”。
- 最稳的节点主干是：`组边界 -> storyboard_group -> 固定前缀 -> 模板骨架 -> 落盘汇流`。
- `思考过程` 应留在调用侧摘要或 `full_trace` 侧车，不要写进 canonical JSON 业务真源。

## Case Log

### Case-20260409-AIGC-STORYBOARD-SHEET-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `分镜故事板` 建立了面向当前仓的组级 storyboard 合同与经验层。
- root_cause_or_design_decision: 参考源来自旧仓，但当前仓的第一事实源已经改成 `projects/<项目名>/3-Detail/第N集.json` 与 `3-Detail/evidence/` 下相关 sidecar，因此必须重写输入与落点口径。
- final_fix_or_heuristic: 保留“组级多格 storyboard + episode JSON + manifest”的骨架，把输入改写为 `3-Detail/第N集.json`，把落点改写为 `projects/<项目名>/5-Image/分镜故事板/`。
- prevention_or_replication_checklist:
  - [x] 输入口径已改写到当前仓
  - [x] 组级输出合同已补齐
  - [x] 单集 JSON / manifest 已固定
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/CONTEXT.md`
- user_feedback_or_constraint: 用户要求参照旧仓分镜故事板能力，但落到当前 `aigc/5-Image` 子技能体系。

### Case-20260410-AIGC-STORYBOARD-SHEET-SHARED-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板` 的上游输入合同同步到 `projects/<项目名>/3-Detail/第N集.json + director_episode_output.schema.json`。
- root_cause_or_design_decision: 上游统一输出内容模板已经收口到 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，不能再把旧 sidecar 当成第一输入真源。
- final_fix_or_heuristic: 明确 shared schema 为输入壳体真源，同时保留 `3-Detail/evidence/` 为人工可读校对证据。
- prevention_or_replication_checklist:
  - [x] 主 `SKILL.md` 已改成 shared schema 输入口径
  - [x] 工作流已改成 `3-Detail/第N集.json`
  - [x] 字段系统与类型策略已同步 shared group list 口径
- evidence_paths:
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/SKILL.md`
- user_feedback_or_constraint: 用户要求由于上游输出模板改为 shared schema，因此同步调整 `分镜故事板` 相关配置。

### Case-20260410-AIGC-STORYBOARD-SHEET-IMAGE-REQUEST-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板` 从“图片/故事板落盘中心”重定义为“每个分镜组对应 1 条图像生成请求 JSON”的提示词蒸馏合同。
- root_cause_or_design_decision: 与视频链路保持一致时，`1-提示词蒸馏` 阶段的主产物应是可 handoff 的请求 JSON，而不是图片文件。
- final_fix_or_heuristic: 在 `5-Image/_shared` 采用共享 `image-generation-input.template.json`，并把 `分镜故事板` 改成“固定英文前缀 + storyboard_group + 图像侧 model 骨架 + 第N集.json”的单输出合同。
- prevention_or_replication_checklist:
  - [x] 共享 JSON 模板已落到 `5-Image/_shared`
  - [x] 主 `SKILL.md` 已改为图像请求 JSON 合同
  - [x] 输出模式已固定为 `json_only / full_trace`
- evidence_paths:
  - `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/SKILL.md`
- user_feedback_or_constraint: 用户明确确认应把每个分镜组对应的图像生成请求 JSON 当主产物；`2-一致性处理` 与 `3-图像生成` 后续单独补充。

### Case-20260412-AIGC-STORYBOARD-SHEET-SINGLE-SOURCE-CONSOLIDATION

- milestone_type: source_contract_change
- outcome: 将 `分镜故事板` 从“主合同 + references 模块细则”全量升格为单文件 `SKILL.md` 真源。
- root_cause_or_design_decision: 历史模块化结构把字段主表、执行流程、类型策略与输出契约外包给旧分文件载体，导致规范真源分裂；同时目录实际已迁移到 `5-Image`，但文档中仍残留 `5-画面/subtypes/...` 旧路径。
- final_fix_or_heuristic: 回收四份分文件合同内容到 `SKILL.md`，删除旧细则文件，同步补 `CHANGELOG.md` 与 `agents/openai.yaml`，并把相关路径统一到 `.agents/skills/aigc/5-Image/...`。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已成为唯一规范真源
  - [x] `CONTEXT.md` 只保留经验层
  - [x] 旧细则文件已删除
  - [x] `CHANGELOG.md` 已记录迁移映射
  - [x] `agents/openai.yaml` 已补齐
  - [x] 与目标技能直接相关的旧路径引用已同步修正
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/CHANGELOG.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“针对 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` 执行全量升格重构，references 内容整合到 `SKILL.md` 内，不再以 references 作为载体引用”。

### Case-20260412-AIGC-STORYBOARD-SHEET-ZHIXING-REFRAME

- milestone_type: source_contract_change
- outcome: 在保持既有输入、模板、字段和落盘机制不变的前提下，将 `分镜故事板` 重构为知行合一单文件思行网络。
- root_cause_or_design_decision: 旧单文件合同虽已收回真源，但仍偏“线性规则堆叠”，节点没有完整的 `route_out / gate`，且残留了对不存在 `5-Image/SKILL.md` 的旧回链；这会让复杂节点执行后难以收束。
- final_fix_or_heuristic: 以 `N0-N6` 思维·执行节点重写主合同，显式补齐 `Total Input Contract / Topology Contract / Thinking-Action Node Contract / Convergence Contract / One-Shot Output Contract`，并把复杂节点细则留在 `SKILL.md` 内，不再做 skeleton/reference 分层。
- prevention_or_replication_checklist:
  - [x] 每个关键节点具备 `objective / inputs / actions / evidence / route_out / gate`
  - [x] Mermaid 主干图、分支回退图、关系图、状态图均已补齐
  - [x] 旧的 `5-Image/SKILL.md` 回链已移除
  - [x] 业务真源仍保持 `第N集.json`
  - [x] `思考过程` 已被收编进调用侧摘要或 `full_trace` 侧车，而非污染业务真源
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求使用 `$skill-知行合一` 重构该包，并指定“复杂链路的骨架 / 细则分层: false”，且要求每个思维·执行节点足够细致。
