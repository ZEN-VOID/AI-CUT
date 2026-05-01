# CHANGELOG

## 2026-04-30

- 明确 `2-编导` 启动 subagents 模式时的执行机制：以项目 `team.yaml` 中明确的监制组相关智能顾问团作为编导监制。
- 新增 `Subagents Execution Mechanism`，要求顾问代入专业视角和个人风格，对已知上下文提出编导方向参谋指导，并由主 agent 汇流为 `advisor_consultation_packet`。
- 在 workflow 中新增 `N4.6-ADVISOR`，将顾问参谋沉淀为 LLM 剧本化投影、阶段内修复和复审的后续上下文。
- 同步更新 review gate 与 CONTEXT 经验层，阻断“泛泛顾问意见”“本地模拟顾问”和“顾问意见越权改写上游真源”。

## 2026-04-29

- 新增阶段末 `Stage-End Review-Repair Contract`，将候选编导稿固定为 `candidate -> review -> direct repair -> re-review -> canonical writeback` 闭环。
- 在 workflow 中新增 `N6R-DIRECT-REPAIR` 与 `N6R-REVIEW-AGAIN`，要求 review 阻断项在 `2-编导` 阶段内最小修复并复审后才能交给下游。
- 更新 review gate、CONTEXT 和执行报告字段，明确保真、对白、声画、slugline、具像化和高点承托问题不得降级为交付后 followup。

## 2026-04-28

- 新增 `references/climax-visual-treatment-contract.md`，将 `story/2-卷章/3-章级` 的爽点设计思想投影为 `2-编导` 的高潮画面处理机制。
- 在 workflow 中新增 `N4.5-PEAK` / `peak_visual_pass`，要求从上游逐集正文识别 1-3 个高点或最强 `micro_payoff`，并落实为既有画面、声音、表演字段。
- 在 review gate 中新增 `FAIL-PEAK-VISUAL`，检查高点可回指、可拍承托、状态差/余波与不新增事实。
- 同步更新模板、README、CONTEXT 与 frontmatter policy，明确高潮强化不得新增剧情事实、对白或因果。

## 2026-04-25

- 初始化 `aigc/2-编导` Skill 2.0 包。
- 固定上游为 `projects/aigc/<项目名>/1-分集/第N集.md`，下游为 `projects/aigc/<项目名>/2-编导/第N集.md`。
- 新增忠实剧本化投影、对白冻结、声画配对、slugline 稳定和好莱坞级质量规范。
- 新增机械校验脚本 `scripts/validate_script_projection.py`；脚本只做结构与字段检查，不替代 LLM 主创。
- 强化“剧本化 = 可见 / 可听 / 可执行”源层定义，新增具像化、画面化、反抽象、反概念、反比喻门禁。
- 强化声音本体规则：`音效` 字段只写可听声音，不写时间说明、事件概括或描述性句子。
- 扩展 `validate_script_projection.py`，开始检查高频抽象画面词与描述性音效词。
- 移除 `镜头语言预设` 字段，避免 `2-编导` 越权到下游摄影/分镜；相关意图必须转化为可见画面、动作、表演或声音字段。
