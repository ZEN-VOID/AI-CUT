# Cinematography Workflow

本文件定义 `3-摄影` 的思行一体化执行节点。

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 给 `2-编导` 逐集稿的每个画面句子注入可执行的大师级运镜摄影设计；`镜头语言：` 仅作为下游兼容字段名 |
| `business_object` | Markdown 编导稿中的字段化画面句子 |
| `constraint_profile` | 保真、逐集落盘、LLM 主创、动态引用、下游可执行、subagents 摄影监制上下文沉淀 |
| `success_criteria` | 每个命中句子下有按节拍生成的 `镜头语言：分镜N`，内容聚焦运镜手法、摄影美学和有动机转场特效，且专业、克制、服务剧情 |
| `non_goals` | 不改剧情、不改对白、不生成图像提示词、不替代下游视频阶段 |
| `complexity_source` | 画面匹配覆盖率、节拍判断、画面节奏张弛、高潮分镜强化、监制顾问参谋汇流、shot_design_plan 汇流、技法选择、连续性和保真约束 |
| `topology_fit` | 串行主干 + 类型分流 + subagents 顾问分支 + review 汇流 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、集号、输入真源和上下文 | 用户请求、`2-编导/第N集.md`、项目 `MEMORY.md` | 定位文件，读取相关上下文，确认不改原文 | source path、episode list | `N2-TYPE` | 输入可读且有画面性正文 |
| `N2-TYPE` | 判断画面句子类型与处理策略 | `types/visual-unit-type-map.md` | 建立 visual category 和审美策略 | type_profile | `N3-MATCH` | 类型能覆盖主要字段 |
| `N3-MATCH` | 执行 step1 画面匹配 | `references/visual-matching-contract.md`、正文行 | 找出所有 visual_unit，记录场景锚点和匹配理由 | visual_unit list | `N4-BEAT` | 命中行覆盖画面性字段 |
| `N4-BEAT` | 执行 step2 节拍分析 | visual_unit、`references/beat-analysis-contract.md` | 判断节拍点和分镜数量 | beat_map | `N5-RHYTHM` | 每个 visual_unit 至少 1 个节拍点 |
| `N5-RHYTHM` | 执行 step2.5 画面节奏分析 | visual_unit、beat_map、上下文密度、`references/visual-rhythm-analysis-contract.md` | 判断收敛/发散、描述密度、运动复杂度、转场强度 | rhythm_profile | `N5.5-PEAK-SHOT` | 当前画面有张弛策略 |
| `N5.5-PEAK-SHOT` | 执行 step2.6 高潮分镜强化判断 | visual_unit、beat_map、rhythm_profile、上游 `peak_visual_policy` 或高点证据、`references/peak-shot-language-contract.md` | 识别 `peak_visual_unit`，决定分镜密度、镜头运动、景别尺度、停顿/断裂和余波交接 | peak_shot_profile | `N5.6-ADVISOR` | 高点强化可回指上游，不新增事实 |
| `N5.6-ADVISOR` | subagents 摄影监制参谋汇流 | `team.yaml`、共享顾问合同、visual_unit、beat_map、rhythm_profile、peak_shot_profile、项目 `MEMORY.md`、`north_star.yaml` 与相关 `CONTEXT/` | 启动或按阻断报告处理 team.yaml 中明确的监制组相关智能顾问团；要求顾问代入专业视角和个人风格，对镜头连续性、节拍密度、运镜、光影、色彩、峰值镜头和转场动机提出参谋指导；主 agent 汇流为后续任务上下文 | `advisor_consultation_packet` 或降级报告 | `N6-CONTINUITY` | packet 已包含 roster 来源、问题类型、可执行镜头指导、风险提示和 `execution_brief` |
| `N6-CONTINUITY` | 回看临近镜头语言并建立连续性策略 | rhythm_profile、peak_shot_profile、`advisor_consultation_packet`、前 3 个 visual_unit、`references/shot-continuity-contract.md` | 建立轴线、运动方向、景别梯度、光色和注意力交接策略，并吸收顾问参谋但不改写上游原文 | continuity_profile | `N6.5-SHOT-PLAN` | 当前镜头有进入点和交出点 |
| `N6.5-SHOT-PLAN` | 汇流 references 形成逐分镜计划 | visual_unit、type_profile、beat_map、rhythm_profile、peak_shot_profile、continuity_profile、`advisor_consultation_packet`、`references/shot-planning-integration-contract.md`、动态表达合同与技法库 | 为每个 visual_unit 形成内部 `shot_design_plan`；裁决分镜数量、顺序、入口、路径、落点、技法和交出点；删除没有新观看策略的随机分镜 | shot_design_plan | `N7-INJECT` | 每个计划分镜可回指 beat/rhythm/continuity/technique/handoff |
| `N7-INJECT` | 执行 step3 运镜摄影设计注入 | `shot_design_plan`、`advisor_consultation_packet`、`references/dynamic-lens-language-contract.md`、`references/cinematic-technique-library.md` | LLM 直写 `镜头语言：` 与 `分镜N`，严格投影 `shot_design_plan`，吸收顾问参谋上下文但不改写上游真源；字段内容不得输出抽象主题、心理结论、世界观解释、导演阐释或不可执行气氛口号 | enriched episode draft | `N8-REVIEW` | 原文保留，注入块紧跟命中句子；字段语义纯度通过；每个分镜有起点、路径、速度、落点、动机和交出点；顾问上下文未越权 |
| `N8-REVIEW` | 执行质量与机械门禁 | candidate enriched draft、`review/review-contract.md`、可选 validator | 检查覆盖、连续编号、节奏张弛、shot_design_plan 投影、连续性、保真、专业性，定位 repair target | review result、repair targets | `N8R-DIRECT-REPAIR` 或 `N9-WRITE` | 无阻断项才可写回 |
| `N8R-DIRECT-REPAIR` | 阶段内直接修复阻断项 | repair targets、candidate enriched draft、上游编导稿 | 最小修复 `镜头语言`、`分镜N`、连续性、节奏张弛、峰值分镜、专业可执行或报告证据；不改上游原文 | repaired draft、repair actions | `N8R-REVIEW-AGAIN` | 修复范围不越权 |
| `N8R-REVIEW-AGAIN` | 复审修复稿 | repaired draft、repair actions、上游编导稿 | 复跑阻断 gate；通过则准入写回，失败则回最早责任节点 | re-review verdict | `N9-WRITE` 或 `N3/N4/N5/N5.5/N6/N7/N8R` | 复审通过或明确阻断 |
| `N9-WRITE` | 落盘与报告 | enriched draft、review result | 写入 `3-摄影/第N集.md`，更新报告 | output path、report path | done | 路径和命名符合 Output Contract |

## Branch Rules

- `N3-MATCH` 中标签命中和语义命中可以并行思考，但必须汇总为单一 visual_unit list。
- `N4-BEAT` 先给每个 visual_unit 独立判断，不允许跨句共用分镜编号。
- `N5-RHYTHM` 必须判断当前画面句子该收敛还是发散；不允许所有画面句子同等华丽。
- `N5.5-PEAK-SHOT` 只强化上游已有高点或明显 `micro_payoff`，不得把普通画面硬拔成高潮；强化必须体现为分镜密度、运镜速度、景别尺度、停顿、转场或余波交接的有动机变化。
- 若启动 subagents 模式，`N5.6-ADVISOR` 必须在 `N6-CONTINUITY` 和 `N7-INJECT` 前完成；顾问参谋只转化为 `advisor_consultation_packet` 上下文，不直接写镜头语言，不替换上游事实、对白或场景顺序。
- `N6-CONTINUITY` 必须回看临近至少前 3 个画面单位；不足 3 个时回看已有全部单位并建立本场景的初始轴线。
- `N6.5-SHOT-PLAN` 是 references 进入最终输出的硬门：不得跳过；分镜数量增加必须来自新的注意力、信息、动作相位、空间关系、情绪压力或转场接口。
- `N6.5-SHOT-PLAN` 必须保证同一 `visual_unit` 内相邻分镜首尾相接：上一条的落点必须成为下一条的入口、反应或转场接口。
- `N7-INJECT` 的技法选择可同时参考构图、运镜、转场、光影、色彩，但最终输出必须凝成可执行、连贯、张弛得当的动态分镜句。
- 若 `N7-INJECT` 把 `镜头语言：` 写成抽象阐释，必须回退：把抽象判断翻译为可见的景别、机位、镜头类型、运镜速度、焦点、构图、光影、色彩或有动机转场；无法转译的内容删除。
- 若 `N7-INJECT` 输出太简略，无法反推起点、路径、速度、落点、动机或交出点，必须回到 `N6.5-SHOT-PLAN` 重建计划后再写。
- 任一节点发现需要改写剧情或对白才能成立，必须回退：镜头语言应服务原句，而不是修补原句。
- 若 review 发现 subagents 启用但缺 `team.yaml` 监制顾问请教、个人风格参谋或上下文沉淀，回到 `N5.6-ADVISOR`。
- 若 review 发现上游高点被压平，回到 `N5.5-PEAK-SHOT`；若发现高潮强化导致跳轴、跳色或风格断裂，继续回到 `N6-CONTINUITY`。
- 若 review 发现分镜随机、上下衔接差、数量多但无递进、输出过短或 references 未真实汇流，回到 `N6.5-SHOT-PLAN`。
- 若 review 发现可由本阶段修复的覆盖、编号、节拍、张弛、计划汇流、连续性或专业性问题，先进入 `N8R-DIRECT-REPAIR` 并复审；不得跳过复审写回。

## Output Shape Per Visual Unit

```markdown
动作画面：林寂猛地睁开眼，身体在座位上僵住，视线从白光里落回现实。
镜头语言：
分镜1: 从白光残影还压在林寂瞳孔里的近景起，以长焦浅景深极慢推近到他僵住的眼角，冷白光从过曝慢慢回落，焦点最终停在瞳孔重新合焦的一瞬。
分镜2: 承接上一镜的瞳孔落点，镜头以低幅度手持后撤到中近景，让他的肩膀和课桌边缘一起进入压迫构图，最后把注意力交给他视线落向的教室前方。
```

不同画面句子的 `分镜N` 均从 `分镜1` 重新编号。
