# Context: aigc 道具 2-设计

本文件是 `$aigc-prop-design` 的经验层知识库，不是过程日志。它沉淀单道具细目设计、上游清单消费、初始化综合整合和提示词约束中的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: initial
recommended_action: keep-prop-design-heuristics-target-scoped
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-PROP-DESIGN-01` | 细目设计变成多个道具的总稿 | 单主体边界层 | 拆成每个道具一个文件 | 在 `SKILL.md` 与模板固定单主体输出 | 文件标题和来源只对应一个清单项 |
| `TM-PROP-DESIGN-02` | 研究考据像百科摘抄，无法转成可生成视觉 | 研究转译层 | 把考据压缩为材质、年代、工艺、磨损和使用痕迹 | 在 `references/` 固定“考据必须服务设计” | 考据之后能直接支撑解构字段 |
| `TM-PROP-DESIGN-03` | 物语只写功能说明，没有叙事生命 | 物语层 | 加入拥有者、行动痕迹、冲突或象征 | 模板要求“为什么它在故事里必须被看见” | 物语不新增上游矛盾事实 |
| `TM-PROP-DESIGN-04` | Photography 与 Prop Design 混在一段里 | 解构层 | 拆成拍摄可见语言与道具造型语言 | 模板固定两个字段 | 两字段均有可执行视觉词 |
| `TM-PROP-DESIGN-05` | 英文 prompt 太长、未引用画面基调或道具风格，或使用 `--no` | 提示词层 | 压缩到 1300 characters 内并显式引用 `画面基调.Global Style Prompt + 道具风格.Prop Style Prompt`；用自然语言负向约束替代 Midjourney 参数 | review gate 检查字符数、引用关系和 `--no` | prompt 为英文且可直接进入 Midjourney v8.1 |
| `TM-PROP-DESIGN-05A` | 解构区或文件名缺少主体 ID，或与 prompt 前缀不一致 | 结构投影层 | 在 `## 4. 解构` 下方补 `主体ID号：<主体ID>`，并同步文件名前缀、`## 5. 提示词设计` 与英文 prompt 前缀 | 模板和 review gate 固定四处 ID 一致性 | 文件名前缀、解构 ID、提示词字段 ID、prompt 开头完全一致 |
| `TM-PROP-DESIGN-05B` | 英文提示词只补前缀后缀，未整合解构主体 | Prompt 整合层 | 回到 `## 4. 解构`，逐项压缩 Photography 与 Prop Design 的镜头、形制、材料、工艺、年代、磨损、功能和尺度槽位进英文 prompt，并在 `deconstruction_coverage` 说明合并或剔除理由 | 模板和 review gate 固定“整合对象是解构全部有效信息” | final English prompt 可反查到镜头、形制、材质、工艺、磨损、功能和固定画面槽位 |
| `TM-PROP-DESIGN-06` | 初始化综合只被点名，未影响设计 | 初始化综合消费层 | 把冻结综合中的设计约束、启发和风险转译为材质、构图、年代感、动作性或留白策略 | steps 固定“初始化综合 -> 设计决策”证据 | 文件中能看到至少一条对应设计选择 |
| `TM-PROP-DESIGN-06A` | 初始化综合存在但仍触发顾问代入 | 初始化综合边界层 | 只读消费 `team.yaml.init_synthesis.stage_seed_summary."11-主体"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`，提炼当前道具节点可执行的约束、启发和风险 | `init_team_synthesis_context` 固定在 LLM 道具设计前消费，并记录 `node_ref / pass_ref / gate_ref`；禁止 team 身份调用、旧 stage profile 和伪顾问问答 | 可见指导改变当前节点的判断、执行取舍、局部 patch 或风险提示，且没有新增创作阶段顾问身份 |
| `TM-PROP-DESIGN-06B` | references 细则存在但未进入执行/验收 | 合同汇流层 | 把 reference 同步接入 Reference Loading Guide、steps 节点、review gate 和必要的机械 resolver | 新增硬规则 reference 时必须同时声明加载场景、消费节点和阻断门禁 | `rg` 能在 SKILL、steps、review、scripts/README 中找到该 reference 的消费点 |
| `TM-PROP-DESIGN-07` | 批量生成的 Skill 2.0 包只有文字合同，缺关键 Mermaid 拓扑 | 包治理层 | 在根 `SKILL.md` 补 `Visual Maps`，在 `references/`、`types/`、`review/` 补来源、分流和汇流图 | README 固定可视化入口索引，后续维护先检查图谱再改流程 | `rg '```mermaid'` 能看到根图、steps 图和关键分区图 |
| `TM-PROP-DESIGN-08` | 研究写了很多，但 prompt 看不出研究贡献 | 证据链层 | 把研究拆成 source cue、confidence、visual translation、prompt token | 模板固定研究证据链和 Prompt Evidence Chain | prompt 核心 token 能回指研究、物语或解构字段 |
| `TM-PROP-DESIGN-09` | 冷门考据被写成确定事实，后续美术和生成都跟着错 | 不确定性治理层 | 将事实分为 source_fact / inference / inspired_by / unknown | references 固定 confidence 和 risk_uncertainty 字段 | 不确定内容以 inspired by 或 uncertain 标注，不进入确定性 design lock |
| `TM-PROP-DESIGN-10` | Photography 或英文 prompt 写成局部特写、裁切特写或半截道具，只强调纯色背景但没有要求完整全貌、仅道具、无人物和无背景元素 | 固定画面约束层 | 补 full-view prop shot、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、no people、no background elements | 在 `SKILL.md`、模板、references、review gate 同步固定完整道具全貌约束，并禁止局部特写 | Photography 和英文 prompt 均明确完整展示道具全貌、完整轮廓和主要结构，仅展示道具 |
| `TM-PROP-DESIGN-11` | 道具只是“普通匕首、普通盒子、普通信件、普通令牌”，功能准确但不好看、无设计细节 | 审美设计层 | 回到 `N5-RESEARCH-CHAIN / N6-DESIGN`，补独特轮廓、材质记忆点、工艺/装饰细节、文化/身份符号、使用痕迹、功能结构和 signature detail | 在 `SKILL.md`、模板、types、review gate 固定 `design_detail_culture` | `Design Appeal Target`、`Signature Detail`、`Cultural Element Strategy`、prompt token 均可见 |
| `TM-PROP-DESIGN-12` | 文化元素像随机贴花，或把现代奢牌、战术、赛博、哥特奇幻符号硬套进历史/地域语境 | 文化语境层 | 删除错置元素，按项目时代、地域、阶层、职业、宗教/族群禁区和功能逻辑重做原创转译 | `knowledge-base/prop-design-corpus.md` 只做启发，必须配 `Period Context Guardrail` | `Prop Corpus Usage Trace` 说明语料种子、原创转译和 period/culture guardrail |
| `TM-PROP-DESIGN-13` | 触发道具审美或文化细节任务，但输出没有加载或记录语料库 | 语料库触发层 | 加载 `knowledge-base/prop-design-corpus.md`，补 `Prop Corpus Usage Trace` 和 prompt 证据 | `GATE-PROP-DESIGN-14` 阻断缺语料库或照搬语料 | 输出中有语料种子、原创转译、时代/文化 guardrail 与 prompt evidence |
| `TM-PROP-DESIGN-14` | 道具设计稿字段完整但像批量模板换名、换材质或换纹样 | 反模板伪差异层 | 废弃候选设计稿，回到研究、解构和 prompt 节点重做道具专属裁决 | `SKILL.md` 固定 `FAIL-PROP-DESIGN-PSEUDO-DIFF`，禁止用字段完整、长度合规、语料库加载或“细节很多”抵消 | 每个道具有不可互换的形制、材质工艺、使用痕迹、功能结构或文化语境裁决证据 |

## Repair Playbook

1. 先确认问题属于输入取证、单主体边界、研究转译、物语、解构、提示词、初始化综合消费还是输出落盘。
2. 若缺上游清单，回到 `道具/1-清单`；不要从分镜正文自行扩充完整道具表。
3. 若缺 `3-美学/画面基调/全局风格协议.md`、`3-美学/道具风格/道具风格协议.md`、`north_star.yaml` 或 `team.yaml.init_synthesis`，保留道具设计可执行部分，但在文件或报告中标注画面基调、道具风格或初始化综合缺口。
4. 若 prompt 超过 1300 characters，优先删解释性短语，保留主体、材质、使用痕迹、构图、光线、风格锚点和自然语言禁止项。
5. 生成或修复英文 prompt 前，先确认 `## 4. 解构` 下方已有 `主体ID号：<主体ID>`，且与文件名前缀、提示词字段和 prompt 前缀一致。
6. 若研究过多，删掉不能改变造型、材质、工艺、年代、磨损或拍摄方式的事实。
7. 若 prompt token 像凭空出现，回到研究证据链补 source cue、confidence、visual translation 和 design lock。
8. 若道具看起来平凡，先不加剧情，先加可见设计：轮廓比例、材料对比、工艺痕迹、封缄/铭文/徽记、旧损、功能结构和 signature detail。
9. 若需要文化元素，先判断时代、地域、阶层、职业、宗教/族群禁区和道具功能，再从 `knowledge-base/prop-design-corpus.md` 取启发做原创转译。
10. 执行初始化综合消费时，先锁定当前 `node_id / pass_id / gate_id`，再把冻结综合转译为节点级判断、局部 patch 或风险提示；不要补造顾问问答、身份扮演或固定字段问卷。
11. 若一个道具存在多状态，先判断是同一主体状态版本还是不同叙事道具；必要时按 `types/prop-design-type-map.md` 分流命名。
12. 若不使用外部初始化综合消费 或 reviewer，按 `SKILL.md` 的初始化综合消费 Execution Contract 直接执行本地 checklist。
13. 若维护本技能包结构，先确认根 `SKILL.md#Visual Maps` 与关键分区 Mermaid 图仍然覆盖输入、类型、创作、审查和落盘主链。
14. 若发现研究、物语、解构或 prompt 只是替换道具名、材质、纹样、年代或形容词，不局部润色；整稿作废并从 LLM 研究/解构/prompt 节点重做。

## Reusable Heuristics

- 单道具设计的好坏不在信息量，而在“能否让生成和美术执行者稳定复现同一个物件”。
- 上游 `原文描述（关键词式）` 是约束，不是天花板；可以深化材质和视觉逻辑，但不得新增与上游冲突的叙事事实。
- 冷门考据应以“可见特征”收束：形制、材料、工艺、年代、磨损、携带方式、使用痕迹。
- 道具“好看”不是加一堆装饰，而是让轮廓、材质、工艺、文化符号、磨损和功能结构形成统一设计；普通工具也可以通过比例、手作痕迹、材料记忆点和使用痕迹变得有设计感。
- 文化元素要像从时代和人物关系里长出来：纹样、铭文、徽记、封缄、器型、材质和装饰必须说明语境，不能把不相干的现代潮流、奢侈品、战术风、赛博风或泛奇幻符号贴上去。
- `knowledge-base/prop-design-corpus.md` 的最佳用法是“选轴不选句”：选取类型、文化元素、材质/工艺和短语结构，再按当前项目原创转译。
- 研究进一步升级的关键不是增加资料量，而是建立 `source cue -> confidence -> visual translation -> design lock -> prompt token` 的短链路。
- `confirmed` 才能变成硬锁定；`probable` 和 `inferred` 应写进设计倾向；`uncertain` 更适合成为风险注记或 inspired-by 表达。
- `Photography` 关注镜头如何让物件被看见；`Prop Design` 关注物件本身如何被制造、持握、老化和辨认。
- `Photography` 和英文 prompt 必须同时锁定完整道具全貌与单主体隔离：full-view prop shot、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、no people、no background elements，避免生成局部特写、裁切特写、半截道具、人物手持或场景化背景。
- 物语不应替代剧情扩写；它只说明该道具的叙事压力、象征和使用痕迹。
- 初始化综合要落到动作：例如材质克制、构图距离、颜色禁区、年代错位、手作痕迹、功能暴露。
- 初始化综合消费的最佳产物不是固定字段答案或大师名字清单，而是能改变当前思维·执行节点判断、取舍、局部 patch 或风险提示的短指令。
- prompt 的英文 1300 characters 限制是硬门禁；中文解释可以在正文中充分，但最终 prompt 必须紧凑可投喂，且不得使用 Midjourney `--no` 参数。
- 主体 ID 是单道具设计稿的结构锚点；`PROP-###` 应同时出现在文件名前缀、解构区、提示词字段和英文 prompt 开头。
- Mermaid 图不是装饰；根图负责主链，分区图负责来源汇入、类型分流和 review 汇流，流程变化时先更新对应 owner 图再更新 README 入口索引。
