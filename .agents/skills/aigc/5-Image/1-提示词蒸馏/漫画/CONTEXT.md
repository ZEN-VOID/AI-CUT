# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md` 之后加载本文件。
- 本技能当前已取消 `references/` 规范载体；经验层只保留在 `CONTEXT.md`。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
soft_limit_cases: 16
hard_limit_cases: 32
current_chars: 5898
current_lines: 111
current_cases: 3
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-12T20:25:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把图片落盘当主产物 | 输出合同层 | 回退到 `第N集.json` 漫画图像请求集合 | 在 `SKILL.md` 的 `Convergence Contract` 与 `One-Shot Output Contract` 固化“json 为主，生成后置” | 主产物指向 `第N集.json` |
| `prompt` 没有固定漫画前缀 | Prompt 合同层 | 重新按固定前缀 + `comic_page_group` 拼接 | 在 `SKILL.md` 的 `Prompt Assembly Rules` 固化前缀逐字保留 | `prompt` 开头逐字一致 |
| `comic_page_group` 漏掉组级或镜级内容 | 输入覆盖层 | 回到 shared schema 重新提取分镜组内容 | 在 `SKILL.md` 的 `Field Master` 与 `Mandatory Workflow` 固化完整覆盖要求 | 可回链 `剧本正文 + 组间设计 + 分镜明细[]` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 以 `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json` 为唯一模板真源 | `model` 骨架与共享模板一致 |
| 文档再次引用 `5-画面/subtypes/...` 或 `references/*.md` | 真源治理层 | 统一替换回当前真实路径，并保持单一 `SKILL.md` 真源 | 在 `SKILL.md` 固化 `Shared Canonical Sources`、`Context Preload` 与 `Root-Cause Execution Contract`，禁止重建第二套规范载体 | 技能目录内不再残留旧路径或已删除 references 引用 |
| 合同只剩字段表与 workflow 摘要，节点没有做到“想清楚即执行” | 编排表达层 | 把业务分析、思行节点网络、节点执行 playbook、汇流门和一次性输出门补回 `SKILL.md` | 在主合同显式声明 `skeleton_detail_split: false`，并要求每个节点写清输入、动作、证据、路由与完成信号 | 执行者无需查额外细则即可完成整条漫画蒸馏链 |

## Repair Playbook

1. 先核对当前父路径是否指向 `.agents/skills/aigc/5-Image/1-提示词蒸馏/`，不要再引用不存在的 `5-画面/subtypes/...`。
2. 再查目标分镜组是否能从 `3-Detail/第N集.json` 的 `分镜组列表[]` 唯一定位。
3. 再查 `prompt` 是否严格等于“固定前缀 + comic_page_group”。
4. 再查 `model` 是否仍保持共享模板骨架，且 `reference_images / image_markers` 未被删掉。
5. 最后查输出模式是 `json_only` 还是 `full_trace`，确认 `第N集.json` 与 `_manifest.json` 的落盘是否一致。
6. 若技能看起来“信息都在，但执行还是发虚”，回查 `SKILL.md` 是否具备 `Business Requirement Analysis / Thinking-Action Node Network / Node Execution Playbook / Convergence Contract / One-Shot Output Contract` 五段主脊梁。

## Reusable Heuristics

- 对这种确定性的叶子蒸馏技能，最稳的升格方式不是补 `team.md`，而是把规范内容收回单一 `SKILL.md` 真源。
- 只要 `references/` 承担了字段表、workflow、类型策略或输出合同，它就不再是“参考材料”，而是在偷渡第二套规范层。
- 阶段名称可以保留人类可读的“5-画面”语义，但文件路径必须以当前真实目录 `5-Image/1-提示词蒸馏/漫画/` 为准。
- 当前仓对本技能没有独立的 `5-Image/SKILL.md` 阶段根合同，因此加载顺序应直接落到 `1-提示词蒸馏` 父级。
- 漫画子技能最常见的漂移不是画风，而是把“漫画图像请求 JSON 蒸馏”误做成“直接页图落盘”。
- 对这种已经是叶子且又有多道判断门的蒸馏技能，最稳的知行合一改造不是继续拆 `references/`，而是把节点细则直接写进主 `SKILL.md`。
- 如果用户明确要求 `复杂链路的骨架 / 细则分层 = false`，就要把“可扫描性”交给 Mermaid 和节点表，而不是把执行细节外包给另一个文档。

## Case Log

### Case-20260410-AIGC-STORYBOARD-COMIC-IMAGE-REQUEST-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `漫画` 从“漫画页图片中心”重定义为“每个分镜组对应 1 条漫画图像请求 JSON”的提示词蒸馏合同。
- root_cause_or_design_decision: 既然 `漫画` 要与 `1-提示词蒸馏` 共享上下文范式和 `5-Image/_shared` 的图像模板真源，就不应继续把页图落盘当主产物。
- final_fix_or_heuristic: 复用 `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`，把 `漫画` 固化为“固定漫画前缀 + comic_page_group + 图像侧 model 骨架 + 第N集.json”的单输出合同。
- prevention_or_replication_checklist:
  - [x] 主产物已固定为 `第N集.json`
  - [x] 共享模板已作为唯一图像模板真源
  - [x] `1 shot = 1 panel` 已固化到 prompt 合同
- evidence_paths:
  - `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`
- user_feedback_or_constraint: 用户要求 `漫画` 与同层提示词蒸馏技能保持共享模板与请求 JSON handoff 口径。

### Case-20260412-AIGC-STORYBOARD-COMIC-SINGLE-SOURCE-ELEVATION

- milestone_type: source_contract_change
- outcome: 将 `漫画` 从“`SKILL.md + references/*` 平行规范”升格为“单一 `SKILL.md` 真源”，并补齐 `agents/openai.yaml` 与 `CHANGELOG.md`。
- root_cause_or_design_decision: 原 `references/*.md` 已实际承担字段表、workflow、类型策略和输出合同，形成第二套规范层；同时目录内残留旧路径 `5-画面/subtypes/...`，与当前真实树 `5-Image/1-提示词蒸馏/...` 发生漂移。
- final_fix_or_heuristic: 将四个 `references` 文件的规范内容全部并入 `SKILL.md`，在 `CONTEXT.md` 只保留经验层；同步补建入口元数据、变更记录，并删除废弃 `references/` 载体。
- prevention_or_replication_checklist:
  - [x] `references/*` 规范内容已内联到 `SKILL.md`
  - [x] 本技能不再保留第二套规范载体
  - [x] 已补 `agents/openai.yaml`
  - [x] 已补 `CHANGELOG.md`
  - [x] 技能目录内旧路径已同步到真实目录结构
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CHANGELOG.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“references 内容整合到 SKILL.md 内，不再以 references 作为载体引用”，并按 `skill-subagents` 执行全量升格重构。

### Case-20260412-AIGC-STORYBOARD-COMIC-ZHIXING-PLAYBOOK-REFRAME

- milestone_type: source_contract_change
- outcome: 在不改动漫画蒸馏业务机制的前提下，将 `漫画` 重编排为知行合一单技能网络，并明确 `skeleton_detail_split: false`。
- root_cause_or_design_decision: 旧版 `漫画` 虽已收回单一 `SKILL.md` 真源，但仍偏“字段表 + workflow 摘要”表达；用户要求每个思维·执行节点一步一步足够细、且不把复杂细则下沉到 `references/`，因此必须补齐业务分析、节点网络、逐节点 playbook、汇流门与一次性输出门。
- final_fix_or_heuristic: 保留现有 `prompt / model / landing / manifest` 机制不变，只重写合同表达层：新增 `Business Requirement Analysis Contract`、四张 Mermaid 图、九个思行节点、逐节点 `aspect` 细化表、`Convergence Contract` 与 `One-Shot Output Contract`，并在主合同声明 `skeleton_detail_split: false`。
- prevention_or_replication_checklist:
  - [x] 已显式声明 `skeleton_detail_split: false`
  - [x] 已补 `Thinking-Action Node Network`
  - [x] 已补逐节点 `Node Execution Playbook`
  - [x] 已补 `Convergence Contract`
  - [x] 已补 `One-Shot Output Contract`
  - [x] 未新增 `references/` 或第二套真源
- evidence_paths:
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CHANGELOG.md`
- user_feedback_or_constraint: 用户明确要求“根据知行合一规范进行编排”“复杂链路的骨架 / 细则分层：false”“每一个思维·执行节点从哪些方面着手，一步一步要足够细致，确保高品质”。
