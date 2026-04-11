# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-明细/subtypes/4-场景氛围` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/3-明细/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 氛围补写越权成摄影说明 | sibling 边界层 | 回滚摄影、运镜、转场术语 | 在 `SKILL.md` 固化 sibling 边界与失败码 | 文本只保留环境语义 |
| 环境句很美，但与戏核脱节 | 叙事锚点层 | 先补锚点卡，再重选主路线 | 在 `SKILL.md` 固化“锚点先行”与 `景/境/物/留白` 顺序 | 每条新增句可回答环境任务 |
| `景 / 境 / 物` 同时乱开导致文本过满 | 路由策略层 | 收敛为单 dominant route，必要时最多一条 support route | 在 VSM 写清主辅路线与过密回退 | 单段主路线唯一 |
| 高留白场被写满，余波感消失 | 节奏层 | 回退到留白路径，只保留最小环境信号 | 在 `SKILL.md` 固化高留白密度上限 | 高留白场新增不超过 1 条 |
| 物件暗喻无来源或不可回收 | 母题层 | 改用场景已有物件，或降级为普通环境补写 | 在母题账本记录“首次 -> 变体 -> 回收” | 物件链可追溯 |
| 物镜有情调但没有时间刻度 | 暗喻层 | 给物件补状态变化，补不出来就降级为普通细节 | 在 `type-strategies.md` 固化 `时间刻度` 门禁 | 物镜能回答时间如何流逝 |
| 景镜/境镜只出现一次，回收链断掉 | 母题层 | 改记为一次性环境增强，或补成“首次 -> 变体 -> 回收” | 把景/境信号也纳入母题账本 | 环境母题可回查 |
| 氛围补写破坏对白、分镜或角色层 | 层级守恒层 | 回滚到当前终稿，再做邻接补句 | 在 `SKILL.md` 固化“只补写、不删改” | 对白/分镜/角色层保持稳定 |
| 标签式写法把故事写成说明书 | 文体层 | 去标签并改成段内自然融写 | 在 VSM 固化 `V-SAT-LABEL` 与去标签回退 | 标签命中数为 0 |
| 忽略 `writer.story` 预设，导致路线与题材失配 | 输入治理层 | 先补读 `世界卡 / 风格卡`，再重判 dominant route | bundle-first 写入 `SKILL.md` 与 `execution-flow.md` | 路由决议可回查预设来源 |
| 正文要求保持纯净，结果锚点卡和 QA 一起丢失 | 写位合同层 | 把锚点卡、路由决议、母题链与 QA 转移到侧车/CHANGELOG | 在 `output-template.md` 固化 pure-body traceability | 纯正文模式下仍能完整回查 |
| 思维链只剩字段表，缺少启发式工作链、工具后反思与 Gate Summary | 思维链合同层 | 重写 `references/chain-of-thought.md`，补齐运行模式、三轴三重、可见/隐藏分层与验收闭环 | 以后同类 `chain-of-thought.md` 默认按最新 `think-think` 合同维护，不再停留在“字段表 + pass 表”级别 | 模块内能直接回答“怎么判、判完落哪、失败回哪” |

## Repair Playbook

1. 先检查输入链是否同时覆盖 grouped source、当前终稿与组间 handoff。
2. 再看锚点卡是否足以支撑“环境任务”判断。
3. 再决定当前应走 `景 / 境 / 物 / 留白` 的哪条主路线。
4. 若出现越权、过密或断裂，先删回环境层最小增量，再重写。
5. 最后把母题链与下一入口写入侧车和 `CHANGELOG.md`。

## Reusable Heuristics

- 场景氛围不是“形容词加法”，而是“环境信号对戏核的增压”。
- 先想这段环境在推进什么，再想它看起来美不美。
- `景镜` 适合承情，`境镜` 适合施压，`物镜` 适合回收，`留白` 适合收束余波。
- 真正好的氛围补写，通常不会让读者明显看到“方法名”。
- 只要一句氛围句开始借摄影术语站位，本层就已经越权了。
- `4-场景氛围` 与 `5-摄影美学` 的最佳交接方式，不是替后者写结论，而是给出稳定的环境语义底座。
- `4-场景氛围` 的思维链先判“环境任务是什么”，再判“哪条路线成立”，最后才判“补到哪里”；顺序倒过来就很容易滑成形容词加法。
- `Gate Summary` 对本层不是装饰，而是防止氛围补写在验收时重新退化成“写完就算”的必要闭环。
- 高张力时刻不一定要跟着角色哭，写一个无动于衷的日常声源或物象，往往更能制造“景结情”的反差。
- 通感可以用，但必须落到味道、湿度、温度、触感、声场等可被下游消费的物理信号，不能只剩抽象抒情。
- `物镜` 真正稳的时候，通常都带着时间刻度；关系的变质，最好让物件替角色去感知。
- 先戏核后天气。先锁环境任务，再选雨、雾、走廊、旧物还是静默。
- 留白不是空白；只保留最小但最有张力的环境信号，反而比多写更满。
- 母题不只属于道具；景镜与境镜信号也应被允许进入回收链。
- `writer.story` 的 `世界卡 / 风格卡` 应作为本层默认预设护栏；legacy `project_preset.json` 只做兼容回退。
- 纯正文不等于无追溯。只要正文被要求保持干净，锚点卡、路由决议、母题链和 QA 就应外移到辅助写位。
- 粗裁决只回答“环境在推进什么”，优选层才回答“哪条路线最美”；把顺序倒过来，最容易把氛围写成装饰。
- 若后续 `3-明细` patch 家族建立 shared runtime profile，应让 `4-场景氛围` 的 canonical 写位、侧车与 fallback_chain 一起收口到 `writer.atmosphere`，避免多文档散落维护。

## Case Log

### Case-20260409-AIGC-SCRIPT-ATMOSPHERE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/4-场景氛围` 建立了可执行合同与经验层，使其能在 `3-明细` 共享主文件上执行环境增强式 patch。
- root_cause_or_design_decision: 用户要求完善 `4-场景氛围`，并明确整个 `3-明细` 系列都要改成“以上游分组原文为底稿、按任务类型层层加权扩写、最终发酵为单一成稿”的前提；直接缺口是当前目录为空，无法承接该阶段里的氛围层职责。
- final_fix_or_heuristic: 参考 ZEN-VOID `6-氛围感` 的三镜法、锚点先行与留白门禁，但改写为当前 `3-明细` 阶段的 `patch-in-place` 合同，并显式把摄影术语边界留给 `5-摄影美学`。
- prevention_or_replication_checklist:
  - [x] 已建立 `4-场景氛围/SKILL.md`
  - [x] 已建立 `4-场景氛围/CONTEXT.md`
  - [x] 已固化 `景 / 境 / 物 / 留白` 路由矩阵
  - [x] 已固化 sibling 边界与密度门禁
  - [x] 已将主文件落点收回 `projects/<项目名>/3-明细/第N集.md`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/6-氛围感/SKILL.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
- user_feedback_or_constraint: 用户要求“整个 `.agents/skills/aigc/3-明细` 系列按照新的前提预设：对于上游分集分组好的原文，根据不同的任务类型进行层层加权扩写式任务，以其最终发酵为完善的融合组间层全部智慧的最终文件”。

### Case-20260409-AIGC-SCRIPT-ATMOSPHERE-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `references/chain-of-thought.md` 从“字段表 + pass 表”升级为符合最新 `think-think` 规范的完整思维链合同。
- root_cause_or_design_decision: 用户要求“按照最新的思维链设计规范”优化本模块；直接缺口是旧版文件虽有 `Field Master / Thought Pass Map / Pass Table`，但缺少 `设计立场`、`运行模式`、`启发式工作链`、`工具后反思`、`可见/隐藏分层` 与 `Gate Summary`，导致它更像静态表格而不是 reasoning 友好的执行合同。
- final_fix_or_heuristic: 以“环境任务先行、dominant route 唯一、patch-in-place 落位、Gate Summary 结案”为主线，重写 `chain-of-thought.md`，把 `4-场景氛围` 的思维链压实成可收窄、可回写、可返工的模块。
- prevention_or_replication_checklist:
  - [x] 已补 `设计立场与运行模式`
  - [x] 已补 `启发式工作链`
  - [x] 已补 `三轴三重裁决` 与 `层内自省`
  - [x] 已补 `可见 / 隐藏分层`
  - [x] 已补 `工具后反思` 与 `Gate Summary`
  - [x] 已保留并升级 `Field Master / Thought Pass Map / Pass Table`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/chain-of-thought.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/3-分组/references/chain-of-thought.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/references/chain-of-thought.md`
- user_feedback_or_constraint: 用户明确指定“按照最新的思维链设计规范，优化一下 `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/chain-of-thought.md`”。

### Case-20260409-AIGC-SCRIPT-ATMOSPHERE-JJW3-INTEGRATION

- milestone_type: source_contract_change
- outcome: 将 `JJW-3` 命名合同、题材化语料、bundle-first 预设护栏、物件时间刻度、景境回收与 pure-body traceability 融入 `4-场景氛围` 的多层真源。
- root_cause_or_design_decision: 当前 `4-场景氛围` 已有三镜法骨架，但还缺少更高分辨率的 `景/境/物` 属性定义、题材模板、`writer.story` 预设优先级，以及“正文纯净但证据不丢”的辅助写位合同，导致方法有框架却不够精细。
- final_fix_or_heuristic: `SKILL.md` 只补 `JJW-3` 命名合同与核心门禁，`references/type-strategies.md` 吸收题材模板、时间刻度与题材相容裁决，`references/chain-of-thought.md` 强化“先戏核后天气”与预设护栏，`execution-flow.md` 与 `output-template.md` 分别补 bundle-first 和 pure-body traceability，`CONTEXT.md` 沉淀高价值 heuristic。
- prevention_or_replication_checklist:
  - [x] 已补 `JJW-3` 命名与主门禁
  - [x] 已补 `writer.story` bundle-first 护栏
  - [x] 已补四类高频题材语料模板
  - [x] 已补 `物件时间刻度` 与 `景境回收` 规则
  - [x] 已补 `纯正文不等于无追溯` 的辅助写位合同
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/execution-flow.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“如已有相关内容不必赘述，仅作缺失补全；补全部分不得是直接大段插入的粗糙方式，而要做消化吸收后的融合和分配”。
