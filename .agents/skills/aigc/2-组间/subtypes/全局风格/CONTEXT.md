# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `2-组间/全局风格` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时，应自动预加载本文件。
- 优先级固定为：用户显式请求 > 根 `AGENTS.md` > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 项目级风格写成 moodboard 标签堆 | SKILL 合同层 | 重写为“一句话命题 + 观演关系 + 风格母体” | 在字段主表固定统一根文件中的 `全局风格` 字段区块，并补 sidecar/Gate 落点 | 下游能直接复述风格口径 |
| `全局风格` 字段混入角色、服装、道具细节 | 阶段边界层 | 把对象级信息下放到后续阶段 | 在 SKILL 明确“不拥有”边界 | 风格真源不再替对象拍板 |
| 类型与导演意图继承的风格不一致 | handoff 层 | 回写 `下游继承提示` | 要求所有下游都引用该区块 | 子技能不再各写一套风格解释 |
| 题材容易串味但没有禁区 | 污染防护层 | 补写 `污染防护` | 把禁区设为固定输出区块 | 风格文档能明确说出“不是什么” |
| 风格合同只有气氛词，没有媒介、技术栈与美学范式 | 输出契约层 | 补写 `风格基础协议`，显式锁定 `媒介属性 / 渲染技术栈 / 美学范式 / 服务叙事理由` | 在 `output-template.md` 和字段主表中为这组协议单独设区块与失败码 | 风格真源能回答“用什么实现、为何这样实现” |
| 项目节奏锚定与 `1-规划/3-分组` 字窗口径互相打架 | 跨阶段接口层 | 把 `全局风格` 的节奏结论改写为项目级解释基线，而非回写规划结果 | 在流程与类型策略里显式声明“可解释、不可反向改规划” | `全局风格` 字段中的节奏锚定与分组产物可并存且不冲突 |
| 集级 `导演意图` 缺少统一上游导演协议 | 跨子技能共享层 | 在 `全局风格` 固定输出项目级 `director_intent` 母合同 | 在 output-template / chain-of-thought 中把它设成强制区块和字段 | `导演意图` 子技能能继承到统一项目级观看法则 |
| 用户要求原文直通，却仍被蒸馏成净化版 | 路由识别层 | 触发 `Canonical Style Lock`，保留用户原文并停止默认净化 | 在 VSM 增加 `exact lock` 情况，并在输出合同中单列条件区块 | `全局风格` 字段中的原文锁定可保真且无误净化 |

## Repair Playbook

1. 先看统一根文件中的 `全局风格` 字段是否真的是项目级，而不是某一集或某一对象的说明。
2. 再看 `项目风格一句话` 与 `观演关系` 是否能支撑整份文档。
3. 再看 `风格基础协议`、`节奏锚定` 与 `风格母体` 是否互相支撑，而不是各写各的。
4. 再看 `污染防护` 是否充分。
5. 最后检查 `下游继承提示` 是否能被 `类型元素 / 导演意图 / 3-明细` 直接消费。

## Reusable Heuristics

- 最稳的全局风格不是“参考 A + 参考 B + 参考 C”，而是“观众如何被带进这部片”的一句总命题。
- `全局风格` 最常见的越权不是写太少，而是提前替角色、道具、镜头细节拍板。
- 当下游协同增多时，`下游继承提示` 的价值和 `风格母体` 一样高，不应省略。
- 当内容合同已经稳定时，优先把 VSM、workflow、输出区块与 field map 下沉到 `references/`，能减少主合同膨胀而不改变风格语义。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 对内容输出型子技能，字段系统不能只覆盖主正文区块；若 sidecar 与验收记录是 canonical runtime 的一部分，也要被 field map 和 Gate 明确接住。
- 在当前仓的统一根文件 `全局风格` 字段中，`style_motherbody.style_backbone_en` 最稳的落法不是单独另起第二真源，而是嵌入 `风格母体` 子区块，作为项目级稳定项的英文蒸馏骨架。
- `style_prompt` 适合被定义为 `Legacy 兼容视图`，它服务旧消费者，不应反客为主变成新的项目真源。
- 项目级 `director_intent` 应作为 `导演意图` 子技能的上游母合同，而不是把 episode-level 导演构思提前写完。
- 项目级节奏锚定最适合承担“解释基线”角色：它要告诉下游项目整体更偏慢/中/快，但不应反向重写 `1-规划/3-分组` 已稳定的组级字窗公式。

## Case Log

### Case-20260409-AIGC-DIRECTING-GLOBAL-STYLE-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `2-组间/全局风格` 建立了项目级内容输出合同与经验层；当前真源已迁为统一根文件中的 `全局风格` 字段区块。
- root_cause_or_design_decision: 参考仓的 `1-风格基座` 很强，但当前仓的 `2-组间` 阶段仍是空壳；直接复制旧仓 JSON 与路径会破坏当前 `projects/<项目名>/` 体系，因此只继承“项目级风格母体 + 污染防护 + handoff”能力，不照搬旧路径。
- final_fix_or_heuristic: 将当前仓的 canonical 输出收束为统一根文件 `projects/<项目名>/编导/第N集.json` 中的 `全局风格` 字段区块，并固定六区块输出。
- prevention_or_replication_checklist:
  - [x] canonical 输出路径已改写到 `projects/<项目名>/`
  - [x] 明确项目级边界
  - [x] 固定 `污染防护` 与 `下游继承提示`
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/1-风格基座/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参照 `1-风格基座`，但当前仓必须落到 `2-组间` 的内容输出型子技能体系。

### Case-20260409-AIGC-DIRECTING-GLOBAL-STYLE-REFERENCES

- milestone_type: source_contract_change
- outcome: 将 `全局风格` 重构为“主合同 + references 模块细则”结构，保留既有风格区块、路径与项目级边界。
- root_cause_or_design_decision: 单文件版 `SKILL.md` 已覆盖完整内容，但最新内容输出型规范要求把思维链、流程、策略和输出契约拆进模块载体，避免主合同和细则纠缠在一起。
- final_fix_or_heuristic: 保留根本语义不变，仅将 field map、workflow、VSM、固定区块拆进 `references/*.md`，主 `SKILL.md` 收束为边界、回指和 Root-Cause 合同。
- prevention_or_replication_checklist:
  - [x] 已建立 `references/` 四件套
  - [x] 主 `SKILL.md` 已保留唯一主合同
  - [x] 统一根文件中的 `全局风格` 字段区块已成为 canonical 真源字段区块
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/chain-of-thought.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/execution-flow.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/type-strategies.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
- user_feedback_or_constraint: 用户要求在不改变内容基础的前提下按最新规范重构。

### Case-20260409-AIGC-DIRECTING-GLOBAL-STYLE-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `全局风格` 的思维链模块升级为符合最新 `think-think` 规范的可见思维合同。
- root_cause_or_design_decision: 旧版 `references/chain-of-thought.md` 只有字段表、pass map 与返工入口，缺少启发式工作链、三轴三重、可见快照、工具后反思和 Gate Summary；同时 `视听气候` 未被字段系统显式接住，导致输出契约与思维链真源轻微错位。
- final_fix_or_heuristic: 将模块重写为 `Think-Think Design Snapshot + 三轴三重自省流 + 工具后反思合同 + Field Master(01-08) + Gate Summary` 结构，并把统一根文件中的 `全局风格` 六区块、`thinking/project.md` 快照、`validation-report.md` Gate 一并纳入字段系统。
- prevention_or_replication_checklist:
  - [x] 启发式工作链已显式化
  - [x] `视听气候` 已接入字段系统
  - [x] sidecar 与 Gate 已进入 field map
  - [x] 主 `SKILL.md` 的字段摘要已同步
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/chain-of-thought.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/CONTEXT.md`
- user_feedback_or_constraint: 用户要求按最新思维链设计规范优化 `references/chain-of-thought.md`，且默认交互语言为中文。

### Case-20260409-AIGC-DIRECTING-GLOBAL-STYLE-FOUNDATION-PROTOCOL

- milestone_type: source_contract_change
- outcome: 将旧 `1-风格基座` 规范中的高价值能力提炼并适配进当前仓 `2-组间/全局风格`，补齐了媒介/渲染/美学协议、项目级节奏锚定、项目级 `director_intent` 母合同、`style_backbone_en -> style_prompt` 双视图蒸馏链，以及显式锁定模式。
- root_cause_or_design_decision: 当前 `全局风格` 已具备项目级风格母体、污染防护与 handoff 基线，但缺少“风格如何被技术与媒介实现、如何形成项目级导演协议、如何和现有规划节奏字窗体系共存”的明示合同；若继续沿用旧 `style-bible.md` 主稿叙述，会与当前统一根文件真源冲突。
- final_fix_or_heuristic: 保持 `全局风格` 字段区块为唯一真源，把新增能力拆分吸收到 `SKILL.md / execution-flow / type-strategies / output-template / chain-of-thought / agents/openai.yaml` 各自职责位，并把 `Canonical Style Lock` 设计为条件区块而非另起并行真源。
- prevention_or_replication_checklist:
  - [x] 媒介/渲染/美学协议已成为固定区块
  - [x] 项目级 `director_intent` 已被声明为上游母合同，而非集级替代品
  - [x] `style_backbone_en -> style_prompt` 已写成默认蒸馏链
  - [x] 与 `1-规划/3-分组` 节奏字窗的关系已显式化，避免跨阶段打架
  - [x] 显式锁定模式已用条件区块承接，避免误净化
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/execution-flow.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/type-strategies.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/references/chain-of-thought.md`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/agents/openai.yaml`
  - `.agents/skills/aigc/2-组间/subtypes/全局风格/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“识别类型和属性后进行消化吸收式融合”，不能粗暴大段插入，也不能照搬旧仓模板。
