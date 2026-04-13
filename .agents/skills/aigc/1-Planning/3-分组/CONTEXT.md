# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/3-分组` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/3-分组/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 输入没有锁到 `2-剧本/第N集.md` | 输入真源层 | 回到规划主稿重新锁定当前集范围 | 在 `SKILL.md + validator` 固化输入根门禁 | 输入清单与当前集一致 |
| `3-分组` 重新依赖外部 planning specialist / reviewer | 真源治理层 | 收回到 `3-分组/SKILL.md` 的内部能力面 | 在 `SKILL.md + audit` 固化 `Internal Capability Fusion Contract` | 不再引用旧规划组文档 |
| 分组切口混用了 `分镜组ID` 与 `分镜ID` | ID 合同层 | 改回三段式 `分镜组ID` | 在模板、validator 与父 skill 固化“组三级、镜四级” | 标题语义稳定 |
| 量化规则只写在 reference，计算仍靠手填 | 计算真源层 | 回到 quantizer 重新计算 | 让 validator 直接消费 quantizer 结果 | `effective_text_chars` 不再只是说明字段 |
| 台词权重升级后 reference 与 quantizer 系数不一致 | 计算真源层 | 同轮更新 reference 表与 quantizer 常量，并回刷受影响 grouped output | 把 voice_text 系数视为单一计算真源变更，不允许只改文档或只改代码 | quantizer 输出、执行报告与 validator 重新一致 |
| reviewer gate 越权接管组边界 | 复核边界层 | reviewer 仅保留说明，不改 authoritative 数值 | 在 `SKILL.md` 固化 reviewer gate 的非 owned truth 边界 | grouped script 只由父 skill 写回 |
| 组尾重复借入下一组开端后污染字窗判定 | 展示增强层 | 先用 canonical 正文完成量化裁决，再在结果落定后追加隐藏 `尾钩借焰` | 在 `SKILL.md + reference + postprocess + quantizer + validator` 固化“先量化定组，后挂尾钩” | 尾钩存在时，本组 `effective_text_chars` 仍只对应 canonical 分组正文 |

## Repair Playbook

1. 先确认 `2-剧本/第N集.md` 是否是唯一输入主证据。
2. 再确认 quantizer 是否真的参与组界裁决。
3. 再看 grouped script 是否保持正文结构，只在切口处新增组标题。
4. 最后才检查 reviewer gate 是否被误开或越权。

## Reusable Heuristics

- `3-分组` 最稳的定位不是摘要板，而是“在 `2-剧本` 正文里切出组边界后的 grouped script”。
- 对当前阶段来说，最有效的抗漂移机制不是再造 specialist 文档，而是“主合同 digest + quantizer + validator”三件套。
- 节奏复核在规划阶段只应作为 reviewer gate 存在，除非用户明确要求，否则不要把它升级成单独执行面。
- 对 `3-分组` 来说，`effective_text_chars` 一旦进入 validator，就不应再允许人工说明替代 authoritative 结果。
- `voice_text` 系数一旦调整，必须同步回刷 reference、quantizer 和已落盘的 grouped output；这类变更会直接改变 `hard_text_window` 判断，不能只改未来项目。
- 若要增强组间牵引，优先用 `尾钩借焰` 借下一组的首个叙事拍点，而不是直接挪动组界；最稳口径是“先纯量化定组，再隐藏挂钩”，而不是把尾钩再塞回字窗判定。
- 对 `尾钩借焰`，最稳的思维·执行拆法仍是“两节点制”：先做 `eligibility gate`，再做 `inject`；但量化节点必须停在尾钩之前，不能与尾钩重新缠在一起。

## Case Log

### Case-20260412-AIGC-PLANNING-GROUPING-INTERNALIZATION

- milestone_type: source_contract_change
- outcome: 将 `3-分组` 从“stage-local parent + 外部 planning specialist/reviewer”重构为知行合一的单阶段内化网络。
- root_cause_or_design_decision: 用户要求删除旧规划组载体，因此 `3-分组` 不能继续依赖 shared specialist / reviewer 文档，必须把边界判断、量化裁决和节奏复核 gate 收回自身合同。
- final_fix_or_heuristic: 在 `3-分组/SKILL.md` 内建立 `Internal Capability Fusion Contract`，把分组边界判断、量化裁决、reviewer gate、写回与 validator 统一在一个 stage-local parent skill 中，外部 planning docs 彻底退出运行链。
- prevention_or_replication_checklist:
  - [x] `3-分组` 已不再引用旧规划组文档
  - [x] reviewer 只保留为内部 gate
  - [x] quantizer 与 validator 闭环保持不变
  - [x] grouped script 与执行报告仍是唯一 canonical 输出
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
- user_feedback_or_constraint: 用户明确要求旧规划组文档不再需要，相关能力必须重新整理吸回 `SKILL.md`。

### Case-20260412-AIGC-PLANNING-GROUPING-VOICE-TEXT-COEF-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `voice_text` 的有效字数系数从 `1.0` 升级到 `1.2`，并同步要求回刷受影响 grouped output。
- root_cause_or_design_decision: 用户明确要求提高台词文本在 `effective_text_chars` 中的权重；若只改 reference 或只改 quantizer，会立刻造成计算双真相，并让已有分组报告过期。
- final_fix_or_heuristic: 同轮修改 `scene-order-duration-strategy.md` 与 `grouping_quantizer.py`，再对当前项目重跑 quantizer/validator，必要时重切过载分组。
- prevention_or_replication_checklist:
  - [x] reference 系数已从 `1.0` 改为 `1.2`
  - [x] quantizer 常量已同步改为 `1.2`
  - [ ] 受影响 grouped output 已回刷
  - [ ] validator 已按新系数重新通过
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/references/scene-order-duration-strategy.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
  - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“对白(*) / 独白(*) / 内心独白(*) / 旁白(*) / 【旁白】：1.0 调整为 1.2”。

### Case-20260412-AIGC-PLANNING-GROUPING-TAIL-HOOK-PREVIEW

- milestone_type: source_contract_change
- outcome: 为 `3-分组` 增加 `尾钩借焰` 机制，在每个非末组尾部预映下一组开端的首个叙事拍点，同时保持 canonical span 与量化口径不漂移。
- root_cause_or_design_decision: 用户要求在分组尾部重复附加下一组开端，以增强组间牵引；若直接裸复制正文而不加标记，会把 grouped script 从纯切分真相污染成重复计数的双真相。
- final_fix_or_heuristic: 以 `尾钩借焰` 作为显式标记名，统一约束为“先量化定组，后隐藏挂钩”：`postprocess` 负责在结果落定后自动写入隐藏标记，`quantizer` 始终只统计 canonical 分组正文，`validator` 强制其仅能出现在非末组尾部且必须回指下一组。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已定义 `尾钩借焰` 的展示/量化边界
  - [x] reference 已收录落盘格式与硬规则
  - [x] `postprocess_grouping_output.py` 可自动注入该区块
  - [x] `grouping_quantizer.py` 不再把借入段落计入本组量化
  - [x] `validate_grouping_output.py` 会校验尾钩位置与回指关系
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/references/scene-order-duration-strategy.md`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/postprocess_grouping_output.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
  - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
- user_feedback_or_constraint: 用户要求“在每个分镜组末端，额外再重复附加下一个分镜组的开端部分；是什么就附加什么，只要一段”。

### Case-20260412-AIGC-PLANNING-GROUPING-TAIL-HOOK-NODE-NETWORK

- milestone_type: source_contract_change
- outcome: 将 `尾钩借焰` 正式纳入 `3-分组` 的思维·执行节点网络，而不再只是散落在 step 文案中的附加动作。
- root_cause_or_design_decision: 用户要求“思维·执行节点也要加入考虑尾钩处理”；若只在 `Execution Workflow / Thought Pass Map` 中提一笔，`尾钩门禁` 与 `尾钩注入` 会继续混在一个模糊步骤里，不利于返工和稳定复用。
- final_fix_or_heuristic: 在 `SKILL.md` 中补齐 `Thinking-Action Node Contract + Thinking-Action Node Network + Convergence Contract`，并把 `尾钩借焰` 拆成 `N5-TAIL-HOOK-DECIDE` 与 `N6-TAIL-HOOK-INJECT` 两个节点：前者专管启用条件与首拍可得性，后者专管隐藏注入；authoritative 量化仍固定停在 `N3-CANONICAL-QUANTIZE`。
- prevention_or_replication_checklist:
  - [x] `3-分组` 已显式声明节点合同
  - [x] `尾钩借焰` 已拆成判断节点与执行节点
  - [x] validator 失败已能回指到边界/尾钩/量化的最小必要节点
- evidence_paths:
  - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
  - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“分组技能包中 思维·执行节点 也要加入考虑 尾钩处理（具体思维和执行方式你设计）”。
