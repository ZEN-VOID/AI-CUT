# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划/subtypes/2-格式/subtypes/标准剧` 的经验层知识库，不是过程日志。
- 进入 `标准剧` 变体时，应在父级 `2-格式/CONTEXT.md` 之后预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 上层 `SKILL.md` > 本 `SKILL.md` > 上层 `CONTEXT.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 主 `SKILL.md` 一边讲规则一边塞模板，细则和主合同混成一层 | 真源治理层 | 把模板、流程、类型策略拆到 `references/` | 固化“子技能主合同 + references”结构 | 主 `SKILL.md` 不再重复整块模板 |
| 标准剧合同被写成高旁白密度 | 体裁边界层 | 收回到“表演优先、旁白从严” | 把“允许整场景零旁白”写成硬规则 | 样例中不再默认堆旁白 |
| 样例只有对白，没有动作画面承载 | 字段合同层 | 补 `动作画面` 为默认可用字段 | 固化“动作画面承载无台词推进” | 样例能体现无台词推进 |
| 直接照搬参考仓的正文改写规则 | 阶段边界层 | 重写为规划层合同和样例 | 显式声明本技能不代写整集正文 | 产物落为 `格式合同.md` 与 `格式样例.md` |
| 旁白主体口径漂移 | 字段一致性层 | 若启用旁白，统一规划为 `讲述者` | 在合同中固定主体口径 | 合同与样例口径一致 |
| 混合源下把镜号逐条升格为场景号，导致同一连续时空被错误拆成多个场景 | 场景骨架层 | 标准剧结果稿改为“场景号按连续时空，镜号范围单列” | 在叶子模板和执行流中固化 `场景X（续） + 镜号范围 / 锚点继承` | 同一寿堂日连续段会写成 `场景2（续）`，而不是 6、7、8、9 连续新场景 |
| 分镜脚本来源下镜头语言被当成可删可不删的备注，而非应优先保留的上游证据 | 分镜源保真层 | 把 `镜头语言预设` 升为 storyboard source 下的优先字段，并要求紧跟相关 `*画面` | 在标准剧叶子合同、流程、模板中统一固化“只整理上游明确提示，禁止脑补新增” | 分镜源结果稿里可见原镜头语言，且挂位稳定 |
| 普通叙事源结果稿出现 `镜头语言预设 / 镜号范围 / 锚点继承` 占位行 | 叶子模板写位层 | 删除占位行，并把叶子模板改成“命中条件才输出” | 在 `标准剧/references/output-template.md + execution-flow.md` 固化条件字段启用规则 | 普通叙事源标准剧结果稿不再出现“未预置 / 无上游显式提示” |

## Repair Playbook

1. 先确认父级已把任务裁决到 `标准剧`。
2. 先锁“表演优先、旁白从严”，再写字段。
3. 样例至少覆盖 `动作画面 + 对白 + 对白画面`，必要时再加独白。
4. 若样例里已经能靠表演表达，就不要额外补旁白。
5. 若参考仓细节超出规划层职责，只保留其高价值格式原则。

## Reusable Heuristics

- `标准剧` 的规划核心不是“字段越多越好”，而是“默认让表演和动作画面工作”。
- 对规划层来说，最稳的旁白规则不是“禁止旁白”，而是“只有必要时才允许启用旁白”。
- 如果一份标准剧样例读起来像讲解稿，通常不是文笔问题，而是变体判模已经跑偏了。
- 对 `标准剧` 这类叶子技能，模板、局部流程和变量策略很适合下沉到 `references/`；主 `SKILL.md` 只要守住变体边界与质量门槛。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 对混合源标准剧转写来说，`场景号` 是连续时空层，`镜号` 是证据层；两层必须并存，不能互相替代。
- 对分镜脚本来源标准剧来说，`镜头语言预设` 不是装饰性字段；只要上游明确写了，就应作为优先保留的证据字段继续传递。
- 对普通叙事源标准剧来说，条件字段宁可不出现，也不要用“未预置 / 无显式提示”占位。

### Case-20260411-AIGC-PLAN-FORMAT-STANDARD-STORYBOARD-CAMERA

- milestone_type: source_contract_change
- symptom_or_outcome: 用户要求当前仓 `标准剧` 对分镜脚本来源完整承接参考仓的四条特别处理，不再只是保留 `镜号范围 / 锚点继承`。
- root_cause_or_design_decision: 直接技术原因是当前标准剧叶子只有 mixed source 场景编号规则，没有把“镜头语言优先保留、画面规范化整理、标题优先复用原结构、禁止脑补新增”写成局部合同。
- final_fix_or_heuristic: 为 `标准剧` 增补 `FIELD-STD-CAMERA-05`，并在局部 VSM、执行流、模板中统一声明 storyboard source 下优先保留 `镜头语言预设`。
- prevention_or_replication_checklist:
  - [x] `标准剧/SKILL.md` 已补 storyboard special case 与 camera field
  - [x] `标准剧/references/type-strategies.md` 已补 `CASE-STD-STORYBOARD`
  - [x] `标准剧/references/execution-flow.md` 已补镜头语言保留步骤
  - [x] `标准剧/references/output-template.md` 已补 `镜头语言预设`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“优先保留镜头语言、规范化整理、场景标题优先复用原结构、不能脑补新增，这些都要有”。

## Case Log

### Case-20260409-AIGC-PLAN-FORMAT-STANDARD-REFERENCE-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `标准剧` 子技能重构为“主合同 + references 模块层”，并把局部流程、VSM 四件套与模板拆出主 `SKILL.md`。
- root_cause_or_design_decision: `标准剧` 已同时承载变体边界、详细模板与执行步骤，若继续堆叠会让局部模板与主合同发生双真源漂移。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留变体边界、字段主表、硬门槛与回链；详细模板和类型策略以下沉的 `references/` 为真源。
- prevention_or_replication_checklist:
  - [x] `references/` 已建立 4 个核心模块
  - [x] 输出模板已迁入 `references/output-template.md`
  - [x] VSM 四件套已迁入 `references/type-strategies.md`
  - [x] 主 `SKILL.md` 已保留边界与字段主表
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
- user_feedback_or_constraint: 用户要求按最新 `skill-内容输出型` 规范重构整个 `2-格式` 子树。

### Case-20260409-AIGC-PLAN-FORMAT-STANDARD

- milestone_type: source_contract_change
- outcome: 为 `1-规划/2-格式/subtypes/标准剧` 建立了规划层格式合同与经验层，并把参考仓的“标准剧”能力改写为当前仓可消费的规划真源。
- root_cause_or_design_decision: 用户指定参考 `AIGC-ZEN-VOID` 的 `标准剧`，但当前仓所需不是正文改写技能，而是先为后续脚本阶段规划标准剧格式边界。
- final_fix_or_heuristic: 继承参考仓的核心边界，包括“表演优先、旁白从严、同命题配对、动作剥离”，同时把产物改写为 `格式合同.md + 格式样例.md + validation-report.md`。
- prevention_or_replication_checklist:
  - [x] 已明确标准剧为默认变体
  - [x] 已写明允许整场景零旁白
  - [x] 已把动作画面保留为核心字段
  - [x] 已显式声明规划层不直接代写正文
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/标准剧/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `AIGC-ZEN-VOID` 的 `标准剧`，同时当前仓默认交互与合同表达使用中文。

### Case-20260411-AIGC-PLAN-FORMAT-STANDARD-HYBRID-SCENE-CHAIN

- milestone_type: source_contract_change
- symptom_or_outcome: 标准剧结果稿在混合源模式下把寿堂日的连续段按镜号拆成多个新场景，导致“场景号”和“镜号”概念混淆。
- root_cause_or_design_decision: 叶子模板只写了 `### 场景X` 骨架，没有约束“混合源场景号必须绑定连续时空”，执行流也没要求显式列出 `镜号范围 / 锚点继承`。
- final_fix_or_heuristic: 标准剧叶子模板新增 `来源画像`、`镜号范围`、`锚点继承`，并规定同一连续时空跨组续写时使用 `场景X（续）`。
- prevention_or_replication_checklist:
  - [x] `标准剧/SKILL.md` 已补混合源场景骨架硬规则
  - [x] `标准剧/references/execution-flow.md` 已补场景编号粒度步骤
  - [x] `标准剧/references/output-template.md` 已补 `场景X（续） + 镜号范围 / 锚点继承`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
  - `projects/嫡母重生：过继局/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确指出“相关空间场景和时间状态被错误分到不同场景号下”，要求从源层修正而不是只改一稿。

### Case-20260411-AIGC-PLAN-FORMAT-STANDARD-CONDITIONAL-FIELDS

- milestone_type: source_contract_change
- symptom_or_outcome: 当前项目标准剧结果稿把 `镜头语言预设 / 镜号范围 / 锚点继承` 当成固定骨架，即使上游没有对应证据也照样输出。
- root_cause_or_design_decision: 叶子模板把这些证据型字段直接写进了默认骨架，执行时容易机械保留占位文本。
- final_fix_or_heuristic: 把这些字段全部降回条件字段，只有上游显式提供或锁轴要求保留时才输出；否则整段省略。
- prevention_or_replication_checklist:
  - [x] `标准剧/references/output-template.md` 已改成条件字段模板
  - [x] `标准剧/references/execution-flow.md` 已补“无证据则省略”
  - [x] 当前项目标准剧结果稿已删除无证据占位
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/execution-flow.md`
  - `projects/晴深不渝/规划/2-格式/第1集.md`
- user_feedback_or_constraint: 用户明确指出这些行“不应该硬加”。
