# Anti-Abstract Language Contract

## Purpose

本共享合同定义 `2-编导`、`3-运动`、`4-摄影`、`5-分组` 与 `6-设计` 共同适用的反抽象语言规范。它要求所有创作判断、阶段报告、设计描述和下游提示词在进入 canonical 输出前，先把抽象判断转译为可见、可听、可演、可拍、可生成或可审查的具象材料。

本合同不是替代各阶段的业务细则；它只提供跨阶段语言门、预设规则、抽象到具象的学习例子和验收映射。各阶段仍按自己的 `SKILL.md`、`references/`、`steps/`、`review/` 与输出合同裁决具体字段。

## Core Rule

任何抽象词、审美词、心理词、主题词、关系结论、风格口号、方法分类或 prompt token，只有在同一句、同一字段或同一证据项中绑定了可执行承托时，才允许保留。否则必须删除、替换或降级为内部判断，不得进入 canonical 正文。

最小判断句固定为：

```text
这句话离开解释后，摄影机能看见什么，演员能做什么，空间/道具如何承托，声音能听见什么，生成器能画出什么？
```

若答案仍是“观众会理解什么”“氛围是什么”“主题是什么”“关系发生了什么”，则尚未完成反抽象。

## Preset Rules

| rule_id | rule | fail signal | required projection |
| --- | --- | --- | --- |
| `AAL-R01` | 抽象情绪必须落到身体、面部、呼吸、声线、视线、手部、姿态或动作节拍 | `紧张`、`压抑`、`崩溃`、`克制` 独立成句 | 肩颈、咬肌、指节、呼吸、停顿、退让、抓握、避视 |
| `AAL-R02` | 抽象关系必须落到空间距离、朝向、遮挡、触碰、视线线、权力站位或行动-反应 | `权力压迫`、`关系反转`、`疏离感` | 谁靠近/后退，谁挡住谁，谁先动作，谁被迫反应 |
| `AAL-R03` | 抽象审美必须落到材质、光线、色彩、构图、镜头位置、运动速度或环境声 | `高级感`、`电影感`、`宿命感`、`诗意` | 冷光压低脸部、玻璃反光切断视线、低机位压住门框 |
| `AAL-R04` | 抽象动作方向必须落到起点、路径、终点、参照系和最终状态 | `向压迫感移动`、`带着气势逼近` | 从桌右沿绕过椅背，沿墙边阴影走到对方面前半步处 |
| `AAL-R05` | 抽象摄影策略必须落到镜头起点、景别/机位、运镜路径、焦点、停点、光线结果和观看变化 | `镜头更有冲击力`、`节奏更紧` | 近景从手背推到眼睛，焦点在停顿时从纸角转到咬紧的下颌 |
| `AAL-R06` | 抽象分组/连接分类必须落到首帧、尾帧、主体运动、透视适应和可生成变化过程 | `流动型连接`、`高能转场` | 上组水面反光吞没画面，下组白色门缝从同一亮区中打开 |
| `AAL-R07` | 抽象设计词必须落到形制、比例、材质、工艺、磨损、地域年代、功能逻辑和 prompt evidence token | `古典气质`、`高级服装`、`神秘道具` | 青灰麻布立领、磨亮袖口、铜扣氧化绿痕、45 度完整轮廓 |
| `AAL-R08` | 风格、主题、类型和 north star 可以作为内部裁决来源，但落盘必须转译成当前对象的具体材料 | 直接粘贴全局风格口号 | 当前场景/角色/道具自己的光色、材质、结构、镜头和负向约束 |
| `AAL-R09` | 不得用具象化新增上游没有的剧情事实、对白、人物动机、规则、道具或场景 | 为了具象而补新事件 | 只使用上游事实、项目记忆和已授权推断；新增必须标注来源或退回上游 |
| `AAL-R10` | 脚本只能检查抽象残留、示例覆盖和字段完整性，不得自动主创替换句 | 正则把抽象词批量替换成模板句 | LLM 按当前上下文完成具象投影，脚本只做审计辅助 |

## Projection Ladder

遇到抽象表达时，按下列顺序处理：

1. `label`: 标出抽象词或抽象句的类型：情绪、关系、审美、主题、动作、摄影、分组、设计、prompt。
2. `source_function`: 判断它在当前阶段承担的功能：保真转译、表演提示、运动连续、镜头设计、组间连接、设计识别或提示词压缩。
3. `anchor`: 找到上游事实或当前对象证据：人物、位置、道具、材质、光源、声音、身体状态、清单行、设计字段。
4. `projection`: 用可见/可听/可演/可拍/可生成材料替换或承托抽象表达。
5. `boundary`: 检查是否新增事实、越权到下游、污染 prompt、或把内部判断泄露为正文。
6. `evidence`: 在阶段报告或 review 证据中记录抽象风险、具象投影、目标字段和返工 owner。

## Stage Binding Matrix

| stage | mandatory consumption | evidence key | local rework owner |
| --- | --- | --- | --- |
| `2-编导` | visual language pass、导演判断、表演工艺、声画字段、报告证据 | `anti_abstract_language_evidence` + `concrete_visual_language_evidence` | `N5-BD-VISUAL-LANGUAGE` / `N6R-BD-REPAIR` |
| `3-运动` | 运动候选、参照系选择、起点/路径/终点扩写、连续性报告 | `anti_abstract_motion_projection` | `N4-MOTION-ENRICHMENT` / `N5R-MOTION-REPAIR` |
| `4-摄影` | `shot_design_plan`、`分镜画面：`、抽象情绪转译、光源/运镜/景深叙事 | `anti_abstract_cinematography_check` | `N7-INJECT` / `N8R-DIRECT-REPAIR` |
| `5-分组` | 入场镜头、出场画面、连接件、画面属性、north star 风格整理 | `anti_abstract_grouping_check` | `PASS-GROUP-02A` / `PASS-GROUP-02B` / `PASS-GROUP-04` |
| `6-设计` | 场景/角色/道具设计稿的研究转译、解构、摄影字段和英文 prompt | `anti_abstract_design_projection` | 命中域级 `2-设计` 的 design/review 节点 |

## Learning And Growth Protocol

本合同允许通过“抽象 -> 具象”例子持续成长，但必须区分项目局部经验和跨阶段共享规则。

1. 单次项目中出现的抽象/具象对，先写入项目根 `CONTEXT/` 或命中技能同目录 `CONTEXT.md`，作为经验候选。
2. 同类抽象在至少两个阶段或两个项目中反复出现，且具象修复被 review 通过，才允许晋升到本文件的 `Seed Example Bank` 或 `Learned Example Bank`。
3. 晋升时必须保留 `abstract_pattern`、`concrete_projection`、`stage_scope`、`source_evidence`、`boundary_check` 和 `review_gate` 六项；不得只追加好句子。
4. 示例只能指导判断，不得成为模板灌写。执行具体项目时必须回到当前上游真源、项目 `MEMORY.md`、项目 `CONTEXT/` 和阶段合同重新裁决。
5. 若示例与用户显式指令、上游事实、项目禁区或阶段输出合同冲突，示例失效。

## Seed Example Bank

| abstract_pattern | concrete_projection | stage_scope | boundary_check | review_gate |
| --- | --- | --- | --- | --- |
| `压迫感增强` | 对方往前半步，椅脚抵住地砖发出短响；被压迫者后背贴住门框，手指停在门把上没有拧下去 | `2-编导` / `4-摄影` | 不新增对话和新动作结果，只显化已存在的压力关系 | `GATE-AAL-01` |
| `情绪崩溃但克制` | 下颌线绷紧，呼吸先断一拍；他把杯沿按回桌面，指腹发白，却没有抬高声音 | `2-编导` / `4-摄影` | 情绪词只作为内部标签，正文写身体和声线 | `GATE-AAL-01` |
| `带着气势逼近` | 角色从桌角阴影外迈入灯下，右肩先越过桌沿，脚步停在对方膝前半步处 | `3-运动` / `4-摄影` | 必须有起点、路径、终点和参照系 | `GATE-AAL-02` |
| `高级感镜头` | 低机位贴近冷玻璃桌沿，白色顶光在划痕上断成三截，焦点从纸角移到手背青筋 | `4-摄影` | 镜头技术服务信息和观看变化，不只堆摄影名词 | `GATE-AAL-03` |
| `流动型连接` | 上一组结尾的雨线贴着镜头滑下，下一组首帧的门缝白光从同一竖线位置亮起 | `5-分组` | 连接方法必须写变化过程，不只写分类名 | `GATE-AAL-04` |
| `神秘古物` | 暗青铜圆牌边缘有两圈不均匀刻痕，孔洞内残留黑色蜡渍，45 度全貌能看出一侧被长期手握磨亮 | `6-设计` | 研究/物语必须转为形制、材料、工艺和使用痕迹 | `GATE-AAL-05` |

## Learned Example Bank

新晋升的跨项目、跨阶段例子追加到此表。每条必须来自已通过 review 的修复案例。

| abstract_pattern | concrete_projection | stage_scope | source_evidence | boundary_check | review_gate |
| --- | --- | --- | --- | --- | --- |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 输出是否仍用抽象情绪、审美、主题、关系或心理结论替代可见、可听、可演、可拍、可生成材料？ | `GATE-AAL-01` / `GATE-BD-13` / `GATE-CINE-15A` | `FAIL-ANTI-ABSTRACT-LANGUAGE` / `FAIL-BD-VISUAL-LANGUAGE` / `FAIL-CINE-19C` | `2-编导/steps/directing-workflow.md#N5-BD-VISUAL-LANGUAGE`；`4-摄影/steps/cinematography-workflow.md#N7-INJECT` | `anti_abstract_language_evidence`、抽象残留清单、具象投影和目标字段 |
| 运动或动作描述是否缺少主体、起点、路径、终点、参照系或最终状态，仍停留在气势/方向/感觉？ | `GATE-AAL-02` / `PASS-MOTION-04` | `FAIL-ANTI-ABSTRACT-MOTION` / `FAIL-MOTION-ELEMENTS` / `FAIL-MOTION-REFERENCE-SELECTION` | `3-运动/references/motion-five-elements-contract.md`；`N4-MOTION-ENRICHMENT` | `anti_abstract_motion_projection`、`motion_state_ledger`、`reference_frame_basis` |
| 摄影语言是否只写效果词、技法名或导演阐释，没有镜头起点、运镜路径、焦点、光线结果和观看变化？ | `GATE-AAL-03` / `FIELD-CINE-04` / `FIELD-CINE-14` | `FAIL-ANTI-ABSTRACT-CINEMATOGRAPHY` / `FAIL-CINE-04` / `FAIL-CINE-05G` | `4-摄影/steps/cinematography-workflow.md#N7-INJECT` / `#N8R-DIRECT-REPAIR` | `anti_abstract_cinematography_check`、`shot_design_plan`、`paraphrase_subtraction_check` |
| 分组入场、出场、连接件或画面属性是否使用静态概括、连接分类或风格口号，没有首尾帧、主体运动、空间和变化过程？ | `GATE-AAL-04` / `PASS-GROUP-02A` / `PASS-GROUP-02B` / `PASS-GROUP-04` | `FAIL-ANTI-ABSTRACT-GROUPING` / `FAIL-GROUP-07` / `FAIL-GROUP-10` / `FAIL-GROUP-11` / `FAIL-GROUP-12` | `5-分组/references/group-entry-shot-contract.md`、`group-exit-shot-contract.md`、`bridge-shot-contract.md` | `anti_abstract_grouping_check`、`entry_source_profile`、`group_exit_picture_tail_hook`、`inter_group_connector` |
| 设计稿、解构或 prompt 是否停留在风格标签、百科摘抄、身份口号或抽象美学，没有转成形制、材料、工艺、姿态、光线、构图和 prompt evidence token？ | `GATE-AAL-05` / `GATE-SCENE-DESIGN-03` / `GATE-CHAR-DESIGN-06` / `GATE-PROP-DESIGN-09` | `FAIL-ANTI-ABSTRACT-DESIGN` / `FAIL-SCENE-DESIGN-03` / `FAIL-RESEARCH-FLAT` / `FAIL-PROP-DESIGN-08` | 命中域级 `6-设计/*/2-设计` 的 research/design/review 节点 | `anti_abstract_design_projection`、`research_brief`、`visual_translation`、`prompt_evidence_chain` |
| 新增或晋升抽象/具象示例时，是否有跨阶段或跨项目证据、边界检查和 review 通过记录，而不是把项目一次性好句子写成共享模板？ | `GATE-AAL-06` | `FAIL-ANTI-ABSTRACT-LEARNING` | 本文件 `Learning And Growth Protocol`；命中技能同目录 `CONTEXT.md` | 示例来源、复用范围、通过的 review gate、未晋升原因或晋升记录 |

