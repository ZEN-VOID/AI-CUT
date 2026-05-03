# Review Contract

本文件定义 `3-摄影` 的质量门禁。

若本轮启动 subagents 模式，review gate 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`：是否从项目 `team.yaml` 解析监制组相关智能顾问团、是否基于当前 `PASS-CINE-*` / `N*-*` 思维·执行节点派生顾问问题、是否要求顾问代入角色意识/创作风格/专业水准参与节点判断和执行取舍、是否形成 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写 `2-编导` 原文。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 落盘前或修复时 | 检查 `分镜明细：` 覆盖、`分镜N` 连续、路径和命名 |
| `cinematic_quality_review` | 交付前 | 检查构图、运镜、转场、光影、色彩是否服务戏剧 |
| `transition_design_review` | 交付前 | 检查场景变化是否形成交出点/进入点，其他转场是否具备空间、注意力、动作、声音、形态、光色、文字或高点断裂接口 |
| `shot_plan_projection_review` | 交付前 | 检查 references 细则是否汇流为 `shot_design_plan`，以及每个 `分镜N` 是否能反推节拍、节奏、连续性、技法和交出点 |
| `functional_projection_review` | 交付前 | 检查每个 `分镜N` 是否有影视功能、运镜策略和下游 AIGC 可消费 payload，而不是随机好看句 |
| `thinking_action_node_review` | 交付前 | 检查 `PASS-CINE-*` / `N*-*` 是否完成真源锁定、类型画像、节拍、节奏、高点、连续性、摄影语法、功能投影、计划汇流、自然注入和阶段内修复闭环 |
| `camera_grammar_review` | 交付前 | 检查景别梯度、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化是否有节拍、空间、信息或情绪动机 |
| `camera_design_scope_review` | 交付前 | 检查 `分镜明细：` 是否只承载运镜手法、摄影美学和有动机转场特效，没有抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 |
| `natural_language_review` | 交付前 | 检查 `分镜明细：` 是否读起来像自然中文镜头文字，而不是参数清单、模板填空或连续同构句 |
| `shot_count_distribution_review` | 交付前 | 检查同一集或同一场分镜数量是否被模板化为固定 2 镜；抽样确认 1/2/3/4 镜均来自真实节拍 |
| `faithfulness_review` | 有改写风险时 | diff 上游 `2-编导`，确认正文事实、对白、顺序未被改写 |

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/cinematography-workflow.md` 的 `N8R-DIRECT-REPAIR`，由 `3-摄影` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `3-摄影/第N集.md`。
- 允许直接修复的范围：`分镜明细：` 覆盖、`分镜N` 连续编号、节拍数量、画面节奏、`shot_design_plan` 汇流、镜头连续性、专业可执行性、动态表达、峰值分镜、执行报告和 review 证据。
- 禁止直接修复的范围：改写 `2-编导` 原文、对白、场景标题、字段顺序、剧情事实或上游 source truth。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何覆盖、编号、保真、空间连续性、专业可执行或 LLM-first 问题不得降级为 followup。

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-CINE-01` | 输入回指 | frontmatter 或报告记录 `source_directing_path` |
| `GATE-CINE-02` | 画面覆盖 | 所有命中画面性句子下方就近有 `分镜明细：` |
| `GATE-CINE-03` | 分镜编号 | 每个分镜明细块从 `分镜1:` 开始，连续编号，无跳号 |
| `GATE-CINE-04` | 节拍合理 | 分镜数量与当前画面句子的动作、信息、情绪节拍匹配 |
| `GATE-CINE-04A` | 数量去模板化 | 1/2/3/4 镜来自 `shot_count_decision`；同一集或同一场若 2 镜占比异常集中，已抽样复判并修正低信息硬撑、关键信息压平或模板继承 |
| `GATE-CINE-05` | 画面节奏 | 低信息/过场句收敛，关键揭示/强情绪/空间重置句发散，描述密度与信息重要性匹配 |
| `GATE-CINE-06` | 连续性回看 | 当前分镜明细已在内部承接临近至少前 3 个画面单位；不足 3 个时承接已有画面单位，输出不机械展示回看过程 |
| `GATE-CINE-07` | 专业可执行 | 内部锁定景别、景深、镜头视角、镜头类型、运镜速度等必要参数；成稿只显式写当前节拍最关键的摄影选择，并按需要补充构图、机位、运动、光影、色彩或转场中的有效选择 |
| `GATE-CINE-08` | 动态流畅 | 分镜明细能反推出起点、路径、速度变化和注意力转移，不是静态标签列表，也不是机械套句 |
| `GATE-CINE-09` | 分镜计划投影 | 每个 `visual_unit` 输出前已有 `shot_design_plan`；最终 `分镜N` 的数量、顺序、入口、摄影语法、运镜路径、停点、落点和交出点可反推 beat/rhythm/continuity/transition/camera/function/handoff |
| `GATE-CINE-10` | 字段语义纯度 | `分镜明细：` 是兼容字段名，内容按运镜摄影设计写作；不输出抽象主题、心理结论、世界观解释、导演阐释或不可执行的气氛口号 |
| `GATE-CINE-11` | 空间一致 | 没有无动机跳轴、反向运动、景别断崖、光色突变或风格断裂 |
| `GATE-CINE-12` | 戏剧服务 | 技法服务角色、危险、信息揭示或空间压迫，不是孤立炫技 |
| `GATE-CINE-13` | 原文保真 | 除新增 frontmatter/report 和 `分镜明细` 外，不改写 `2-编导` 正文 |
| `GATE-CINE-14` | 高潮分镜 | 上游存在 `peak_visual_policy`、`peak_visual_pass` 或明显高潮/爽点/高光画面时，摄影稿完成峰值分镜强化，且不新增事实、对白或动作结果 |
| `GATE-CINE-15` | 功能性投影 | 每个 `分镜N` 可抽取 shot_function、visible_subject、action_phase、camera_movement_plan、composition_anchor、light_color_material、continuity_handoff 和下游消费点 |
| `GATE-CINE-16` | 摄影语法变化 | 景别、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化服务节拍、空间、信息、情绪或交接；不存在随机换技法、无动机大远景跳大特写或视角乱跳 |
| `GATE-CINE-17` | 思维·执行节点完整 | 产物能回指 `PASS-CINE-00..12` 与 `N1/N2/N3/N4/N5/N5.5/N5.6/N6/N6.1/N6.2/N6.4/N6.5/N7/N8/N8R/N9` 的关键判断：真源、类型、节拍、节奏、高点、顾问、连续性、转场、摄影语法、功能投影、计划、注入、审查修复 |
| `GATE-CINE-18` | 自然成稿 | 连续分镜不出现重复句法骨架、参数清单腔或“高级/丝滑/电影感”等空泛效果词；读起来先是画面，再是摄影 |
| `GATE-CINE-19` | 输出路径 | 写入 `projects/aigc/<项目名>/3-摄影/第N集.md` 和 `执行报告.md` |
| `GATE-CINE-20` | 顾问请教 | 启动 subagents 模式时，已完成 `team.yaml` 监制顾问请教；顾问问题同步于当前思维·执行节点，并沉淀为后续上下文，或记录上层阻断降级 |
| `GATE-CINE-21` | 转场动机 | 场景变化已处理上一画面交出点和下一画面进入点；其他显式转场能回指空间重置、注意力转交、动作承接、声音先行、形态/颜色匹配、光变、文字显影或高点断裂接口，且强度不抢表演/信息 |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-CINE-02` | 漏掉画面性句子 | `references/visual-matching-contract.md` |
| `FAIL-CINE-03` | 分镜过粗、过碎或固定模板化 | `references/beat-analysis-contract.md` |
| `FAIL-CINE-03A` | 分镜数量塌缩为固定 2 镜或同数分布异常，无法证明每个 `分镜2` 的真实观看策略 | `references/beat-analysis-contract.md`、`references/visual-rhythm-analysis-contract.md`、`references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-04` | `分镜明细` 缺失或编号断裂 | `templates/output-template.md`、`scripts/validate_cinematography_markup.py` |
| `FAIL-CINE-05` | 分镜明细空泛 | `references/cinematic-technique-library.md` |
| `FAIL-CINE-05A` | 分镜明细混入抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 | `SKILL.md` Output Contract、`templates/output-template.md` |
| `FAIL-CINE-05B` | 分镜明细静态呆板，没有变化和组合运镜 | `references/dynamic-lens-language-contract.md` |
| `FAIL-CINE-05C` | 当前分镜明细与临近镜头断裂、跳轴、跳色或空间跳跃 | `references/shot-continuity-contract.md` |
| `FAIL-CINE-05D` | 分镜明细不分轻重，低信息过度发散或重信息过度收敛 | `references/visual-rhythm-analysis-contract.md` |
| `FAIL-CINE-05E` | 上游高点被按普通画面压平，或高潮强化缺少分镜/运镜/停顿/余波策略 | `references/peak-shot-language-contract.md` |
| `FAIL-CINE-05F` | references 被引用但未汇流成 `shot_design_plan`，导致分镜数量随机、上下不接或输出过短 | `references/shot-planning-integration-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05G` | 分镜明细出现参数清单、连续同构句、模板填空腔或过度显式化内部计划 | `references/natural-shot-detail-writing-contract.md`、`steps/cinematography-workflow.md#N7-INJECT` |
| `FAIL-CINE-05H` | 分镜明细表达顺滑但缺少影视功能、运镜策略、主体/动作/构图/光色/空间锚点或下游 AIGC 可消费 payload | `references/functional-cinematic-projection-contract.md`、`steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05I` | 景别、镜头视角、景深/焦点、镜头类型或构图变化随机，无法回指节拍、空间、信息、情绪或连续性交接 | `references/cinematic-technique-library.md`、`steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` |
| `FAIL-CINE-05K` | 场景变化没有交出点/进入点，或显式转场缺少空间、注意力、动作、声音、形态、光色、文字或高点断裂接口 | `references/transition-design-contract.md`、`references/shot-continuity-contract.md`、`steps/cinematography-workflow.md#N6.5-SHOT-PLAN` |
| `FAIL-CINE-05J` | 思维·执行节点缺环：未完成类型画像、摄影语法、功能投影、计划汇流或阶段内修复闭环，却直接写出 `分镜明细` | `steps/cinematography-workflow.md`、`SKILL.md#Thought Pass Map` |
| `FAIL-CINE-06` | 改写原编导稿 | `SKILL.md` Output Contract 和本文件 `faithfulness_review` |
| `FAIL-CINE-07` | 启动 subagents 模式时缺少顾问请教、节点同步问题、角色意识/创作风格/专业水准参谋、上下文沉淀或降级说明 | `../../_shared/team-advisor-consultation-contract.md` + `../SKILL.md#Subagents Execution Mechanism` |

## Review Output

执行报告至少记录：

- 输入文件与输出文件。
- 处理集号。
- 画面性句子数量。
- `分镜明细` 块数量。
- 机械校验结果或人工 review 结果。
- 画面节奏张弛结果。
- 分镜数量分布与 2 镜集中抽样复判结果。
- 高潮分镜强化结果。
- `shot_design_plan` 汇流与投影检查结果。
- 转场动机检查结果：场景变化交出点/进入点、显式转场接口、转场强度与表演/信息保护。
- 摄影语法变化检查结果：景别梯度、镜头视角、景深/焦点、镜头类型、构图、光色和运镜变化。
- 功能性影视投影与 AIGC 下游可消费性检查结果。
- 顾问请教 roster 来源、问题类型、可执行指导或降级说明。
- 镜头连续性、空间一致性和风格一致性结果。
- 运镜摄影设计纯度检查结果。
- 自然成稿检查结果。
- 需要返工的行号或字段标签。
- repair actions、复审 verdict、未修复风险和是否允许进入下游阶段。
