# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划/subtypes/2-格式` 的经验层知识库，不是过程日志。
- 进入 `2-格式` 时，应在父级 `1-规划/CONTEXT.md` 之后预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 父级 `SKILL.md` > 本 `SKILL.md` > 父级 `CONTEXT.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 主 `SKILL.md` 同时承载流程、模板、判模细节，开始变成第二真源 | 真源治理层 | 把执行流、VSM、模板拆到 `references/` | 固化“主合同 + references 模块层”结构 | 主 `SKILL.md` 不再重复整套细则 |
| 只有 `标准剧/解说剧` 空目录，没有父级变体路由 | 父子路由层 | 先补 `2-格式` 父级合同与路由矩阵 | 固化“父级裁决变体，子级细写合同” | 从父级能唯一进入某个变体 |
| 直接复制参考仓的“正文改写技能”，导致规划阶段越权 | 阶段边界层 | 收回为“格式合同 + 样例 + 验证报告” | 在父子技能中显式声明“不直接代写整集正文” | 产物是规划合同，而不是成片正文 |
| `标准剧` 成了默认却没写清原因 | 判模层 | 在父级写明默认分支逻辑 | 固化“未显式解说则默认标准剧” | 未给出解说信号时不会误入旁白主导 |
| 无序 sibling 被误解为可以正式双开 | 调度语义层 | 在父级显式声明“分析可并行，正式落盘只取唯一主变体” | 将该规则写成父级硬门槛 | 不再同时产出两套正式主格式 |
| 样例只讲概念，不给下游可直接照抄的骨架 | 交接层 | 增补最小格式样例 | 固化“合同 + 样例”双轨输出 | 下游能直接按样例续跑 |
| 顾问团已启用，但 `2-格式` 没继承 `1-规划` 的阶段顾问运行时 | 继承层 | 明确本父技能继承上层 `1-规划` 的 `Council Runtime Contract` | 子技能不再重复发明第二套顾问团规则 | 进入 `2-格式` 时会先遵守项目根 `team.yaml` 判定 |
| `2-格式` 只产出合同/样例，不产出实际格式化正文 | 结果物真源层 | 改为默认产出 `规划/2-格式/第N集.md` 结果稿 | 固化“合同留在技能源层，项目 runtime 只落结果稿” | 打开 `2-格式` 产物时能直接读到该集正文 |
| 混合源的 `source_profile` 只存在于 manifest / handoff，`2-格式` 结果稿看不出 mixed 属性，且把镜号误升为场景号 | 格式写位层 | 在 `2-格式/第N集.md` 顶部显式写出来源画像，并规定 `场景号` 只按连续时空编号、`镜号/锚点` 独立保留 | 用父级模板、执行流与标准剧模板固化“source profile 可见化 + scene/shot 去混淆” | 打开 `2-格式/第N集.md` 就能看到 mixed 属性，同一连续时空跨组时使用 `场景X（续）` |
| `2-格式/第N集.md` 提前长出 `## G01 / G02 ...`，导致与父级主稿几乎同稿 | 父子职责边界层 | 收回为 scene-first draft，只保留场景边界与锚点；组级投影延后到 `3-分组` 和父级聚合 | 固化“2-格式不写组容器，父级主稿才写 compact group projection” | `2-格式/第N集.md` 与 `规划/第N集.md` 不再只有一行差异 |
| `2-格式` 把原文改写成转述版正文，用户要求“不得改变原文，只附加字段标题” | 结果稿生成层 | 回退到原文保真模式，仅补 `场景标题 / 动作画面 / 对白 / 对白画面` 等字段标题 | 在父级合同、执行流和标准剧模板中固化“仅附加字段标题，不改正文” | 格式稿中的正文与主故事源逐段可回查，不再出现同义改写 |
| 分镜脚本来源进入 `2-格式` 后，镜头语言没有被优先保留，或被当成普通叙事源去补画面 | source_profile 投影层 | 在父级 `2-格式` 合同中补“优先保留镜头语言 / 规范化整理 / 优先复用原结构 / 禁止脑补新增” | 把 storyboard special case 固化到父级 `SKILL.md + references`，并要求两个叶子同步承接 | 分镜源结果稿能看见原镜头语言与原结构证据，而不是二次改写稿 |
| 条件字段被模板写成硬字段，导致普通叙事源也出现 `镜头语言预设 / 镜号范围 / 锚点继承` 占位 | 模板写位层 | 删除当前结果稿中的占位字段，并把父级模板改成“仅在上游显式提供或锁轴要求时输出” | 在 `references/output-template.md + execution-flow.md` 固化“条件字段不占位”规则 | 普通叙事源结果稿不再出现无证据的镜头/锚点占位字段 |

## Repair Playbook

1. 先检查父级 `1-规划` 是否已把任务正确路由到 `2-格式`。
2. 再在 `标准剧 / 解说剧` 间做唯一主变体裁决。
3. 先写变体合同，再写样例，不要反过来。
4. 正式落盘前补父级 `validation-report.md`，解释为何采用该变体。
5. 若参考仓内容与当前规划阶段职责冲突，以当前阶段边界为真源。

## Reusable Heuristics

- `2-格式` 最容易犯的错不是“写得太少”，而是把下游正文创作职责提前带进规划层。
- 对格式规划来说，父级最重要的价值是做“唯一变体裁决”；子级最重要的价值是把该变体写成可消费合同。
- 如果用户没明确说要旁白主导，先走 `标准剧`，通常比默认提升旁白密度更稳。
- 只给格式原则不够；必须同时给出最小样例，下游才能真正复用。
- 对 `2-格式` 来说，顾问团机制应该继承自 `1-规划` 根级，不应在父变体层再复制一套独立运行时。
- 对已进入稳定维护的技能来说，`references/` 最适合承接流程图、VSM 四件套与模板骨架；主 `SKILL.md` 只保留判定门槛与回链。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 对混合源格式化来说，最常见失真不是漏掉某句台词，而是把“镜头/锚点证据层”错误升格为“场景编号层”。
- `2-格式` 的正确交付是“scene-first draft”，不是“半聚合后的总稿”；一旦它提前长出 `G01 / G02 ...`，父级 `1-规划` 就几乎失去聚合空间。
- 若用户要求“不要改原文”，`2-格式` 的最稳做法是把原文整段挂到字段标题下，而不是先理解后复述。
- 当主故事源已经是分镜脚本时，`2-格式` 的重点不是“补齐画面”，而是“把已有分镜表达规范化投影给下游继续消费”。
- `镜头语言预设 / 镜号范围 / 锚点继承` 都是证据型条件字段；没有上游显式证据时，最稳做法是完全省略，而不是写“未预置”。

### Case-20260411-AIGC-PLAN-FORMAT-STORYBOARD-CAMERA-PRESERVE

- milestone_type: source_contract_change
- symptom_or_outcome: 用户明确要求当前仓 `2-格式` 对 `storyboard_script` 同步承接参考仓的四条特别机制：优先保留镜头语言、画面从补齐改为规范化整理、场景标题优先复用原分镜结构、禁止脑补新增镜头提示。
- root_cause_or_design_decision: 直接技术原因不是根级 `source_profile` 缺失，而是 `2-格式` 父级与两个叶子变体只写了 `镜号范围 / 锚点继承`，没有把 storyboard special case 升成正文格式合同。
- final_fix_or_heuristic: 在 `2-格式` 父级 `SKILL.md + references` 中建立统一 storyboard 特别处理，再由 `标准剧 / 解说剧` 同步投影 `镜头语言预设` 条件字段、原场景结构优先复用与规范化整理规则。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补 storyboard source 四条硬规则
  - [x] 父级 `references/type-strategies.md` 已补镜头语言保留变量
  - [x] 父级 `references/execution-flow.md` 已补优先保留与规范化整理步骤
  - [x] 父级 `references/output-template.md` 已补 `镜头语言预设`
  - [x] 两个叶子变体已同步承接该规则
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“优先保留镜头语言、规范化整理既有分镜表达、场景标题优先复用原结构、禁止脑补新增，这些都要有”。

### Case-20260411-AIGC-PLAN-FORMAT-PRESERVE-ORIGINAL-TEXT

- milestone_type: source_contract_change
- symptom_or_outcome: 当前项目 `projects/晴深不渝/规划/2-格式/第1集.md` 把原文改写成了标准剧式转述，用户明确要求“进行时，不得改变原文，仅附加相关字段标题”。
- root_cause_or_design_decision: 直接技术原因是 `2-格式` 父级与 `标准剧` 子技能合同都仍把结果稿定义成“转写/整理”后的正文，导致执行默认走向改写而非保真挂载。
- final_fix_or_heuristic: 把 `2-格式` 根技能、执行流、父级模板与 `标准剧` 模板统一收敛到“原文保真 + 字段标题附加”模式；项目侧把现有结果稿回退为原文原样挂载版本。
- prevention_or_replication_checklist:
  - [x] `2-格式/SKILL.md` 已补“仅附加字段标题，不改正文”硬规则
  - [x] `2-格式/references/output-template.md` 已补“默认只加标题，不改正文”
  - [x] `2-格式/references/execution-flow.md` 已补原文改写即返工规则
  - [x] `标准剧/SKILL.md` 与模板已改为原文保真模式
  - [x] 当前项目 `规划/2-格式/第1集.md` 已回退为原文保留版
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
  - `projects/晴深不渝/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确要求“`.agents/skills/aigc/1-规划/subtypes/2-格式` 进行时，不得改变原文！仅附加相关字段标题”。

### Case-20260411-AIGC-PLAN-FORMAT-VS-PARENT-MASTER

- milestone_type: source_contract_change
- symptom_or_outcome: 当前项目中 `规划/第1集.md` 几乎与 `规划/2-格式/第1集.md` 完全相同，父级主稿几乎没有承接 `3-分组` 的额外价值。
- root_cause_or_design_decision: 直接技术原因不是父级不会汇总，而是 `2-格式` 子产物越权提前写成了带 `G01/G02...` 的半聚合稿，导致父级只能原样搬运。
- final_fix_or_heuristic: 把 `2-格式` 重新锁回 scene-first draft，只保留场景、镜号范围与锚点；父级主稿则额外投影 compact group summary，使两者职责明确分层。
- prevention_or_replication_checklist:
  - [x] `2-格式/SKILL.md` 已补“不写组容器”硬规则
  - [x] `2-格式/references/output-template.md` 已禁止 `## Gxx`
  - [x] 当前项目 `规划/2-格式/第1集.md` 将回退为纯场景稿
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/CONTEXT.md`
  - `projects/嫡母重生：过继局/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确指出 `projects/嫡母重生：过继局/规划/第1集.md` 几乎与 `projects/嫡母重生：过继局/规划/2-格式/第1集.md` 完全一样。

## Case Log

### Case-20260409-AIGC-PLAN-FORMAT-REFERENCE-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `2-格式` 父技能重构为“主合同 + references 模块层”，把思维链、执行流、VSM 四件套与输出模板从主 `SKILL.md` 下沉到 `references/`。
- root_cause_or_design_decision: 随着 `2-格式` 父技能不断补细则，主 `SKILL.md` 已开始同时承担流程、判模、模板三类说明，存在演化成隐藏第二真源的风险。
- final_fix_or_heuristic: 保留父级 `SKILL.md` 的边界、路由、字段门禁与闭环，把 `chain-of-thought / execution-flow / type-strategies / output-template` 作为唯一细则承载层。
- prevention_or_replication_checklist:
  - [x] 父级 `references/` 已建立 4 个核心模块
  - [x] 主 `SKILL.md` 已回链到模块真源
  - [x] VSM 四件套已迁入 `references/type-strategies.md`
  - [x] 输出模板已迁入 `references/output-template.md`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“加载最新规范”并重构 `.agents/skills/aigc/1-规划/subtypes/2-格式`。

### Case-20260409-AIGC-PLAN-FORMAT-PARENT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划/subtypes/2-格式` 建立了父级格式规划合同，并把 `标准剧 / 解说剧` 两个空壳目录接回到可路由的父级入口。
- root_cause_or_design_decision: 用户要求完善 `标准剧`、`解说剧` 两个子目录，但直接技术阻塞是 `2-格式` 父级合同缺失，导致两个变体即使补齐也仍是孤岛。
- final_fix_or_heuristic: 先补 `2-格式/SKILL.md + CONTEXT.md`，再让父级显式承担变体裁决、验证汇总和下游交接；子技能只承接各自变体的格式合同与样例。
- prevention_or_replication_checklist:
  - [x] 父级变体路由矩阵已建立
  - [x] 已明确 `标准剧` 为默认分支
  - [x] 已明确“分析可并行、正式落盘只取唯一主变体”
  - [x] 已建立父级 `validation-report.md` 输出合同
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/标准剧/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `AIGC-ZEN-VOID` 的 `2-对白·独白·旁白` 双变体结构，同时补齐当前 `1-规划` 下的源层路由。

### Case-20260411-AIGC-PLAN-FORMAT-HYBRID-SCENE-GRANULARITY

- milestone_type: source_contract_change
- symptom_or_outcome: `2-格式/第1集.md` 把同一连续时空的混合源镜号逐条写成新场景号，同时结果稿顶部完全看不出当前集是 `hybrid_story_text`。
- root_cause_or_design_decision: 直接技术原因是 `2-格式` 父级模板只有 `### 场景X` 骨架，没有读取 `source_profile` 来决定场景编号粒度，也没有要求把 `镜号范围 / 锚点继承` 投影到正文。
- final_fix_or_heuristic: `2-格式` 先根据 `story-source-manifest.yaml` 或 `metadata.source_profile` 锁定来源画像；若 `scene_boundary` 被锁定，则 `场景号` 只按连续时空编号，并在每个场景下显式列出 `镜号范围 / 锚点继承`。
- prevention_or_replication_checklist:
  - [x] `2-格式/references/type-strategies.md` 已补来源粒度覆盖规则
  - [x] `2-格式/references/execution-flow.md` 已补来源画像与场景编号步骤
  - [x] `2-格式/references/output-template.md` 已补 `来源画像`、`镜号范围`、`锚点继承`
  - [x] 当前项目 `规划/2-格式/第1集.md` 已按新口径回写
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
  - `projects/嫡母重生：过继局/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确指出当前任务已选混合模式，但最终执行结果“看不出来保留了分镜脚本属性”。

### Case-20260411-AIGC-PLAN-FORMAT-CONDITIONAL-FIELDS

- milestone_type: source_contract_change
- symptom_or_outcome: 当前项目 `规划/2-格式/第1集.md` 在没有上游显式镜头提示和镜号锚点的情况下，仍硬写了 `镜头语言预设：无上游显式镜头提示` 与 `镜号范围：未预置`。
- root_cause_or_design_decision: 直接技术原因不是判模错误，而是父级与 `标准剧` 模板把条件字段写成了默认骨架，执行时即使没有证据也会机械落占位。
- final_fix_or_heuristic: 把 `镜头语言预设 / 镜号范围 / 锚点继承 / 当前集继承锚点` 全部收回为条件字段；只有上游显式提供或锁轴要求保留时才允许写入。
- prevention_or_replication_checklist:
  - [x] 父级 `references/output-template.md` 已改为条件字段模板
  - [x] 父级 `references/execution-flow.md` 已补“条件字段不占位”
  - [x] `标准剧/references/output-template.md` 已改为条件字段模板
  - [x] `标准剧/references/execution-flow.md` 已补条件启用规则
  - [x] 当前项目 `规划/2-格式/第1集.md` 已删除无证据占位字段
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/execution-flow.md`
  - `projects/晴深不渝/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确指出“`镜头语言预设：无上游显式镜头提示` 和 `镜号范围：未预置` 这种不应该硬加”。
