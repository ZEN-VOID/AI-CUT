# Grouping Workflow

本文件定义 `6-分组` 的思行一体执行拓扑。

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 将逐集摄影稿切成完整分镜组，供后续设计、图像和视频阶段稳定消费 |
| `business_object` | `projects/aigc/<项目名>/5-摄影/第N集.md` 与 `0-初始化/north_star.yaml` |
| `constraint_profile` | 组内显式时长累计优先接近 15 秒，通常约 12-18 秒可接受，且单组不得超过 18 秒；画面句子多分镜和对应对白承托不可截断，但不能作为超 18 秒放行理由；字数/对白只作辅助风险复核；相邻组具备 3-4 秒首尾帧连接件 |
| `success_criteria` | 每组 ID 真实、每组开头有入场镜头，且入场镜头说明入口源、入场触发、镜头/观看位置、主体入画状态和动态关系变化；首组从本组第一个原始分镜可见状态进入，第二组起从上一组末帧、上一组尾帧、上一组最后一帧或连接件抵达首态进入并牵引人物动作链；场景/环境信息只作为入场路径必要上下文；构图分区把角色、群体、关键道具和场景锚点整理为带属性、站位和关系变化的主体账本；风格整理含置顶于第 1 行最前的全局固定前置词和 300 字以内当前组全局风格句；正文保真、组间连接自然、统计 YAML 可复查 |
| `non_goals` | 不改剧情、不改对白、不重写原有分镜明细、不生成图像/视频提示词 |
| `complexity_source` | 边界裁决、组间首尾帧连接件、显式时长累计与完整性汇流 |
| `topology_fit` | 串行取证 + 场景内树形分组 + 相邻组 pairwise review + 统一验收 |

## Node Network

```mermaid
flowchart TD
    N1["N1-INTAKE<br/>锁定项目、集号、上游和 north_star"] --> N2["N2-PROJECT-STYLE<br/>整理三项风格字段"]
    N2 --> N3["N3-SCENE-MAP<br/>建立集/场/atomic unit 映射"]
    N3 --> N5["N5-GROUP-PLAN<br/>显式时长累计/atomic unit/密度风险裁决"]
    N5 --> N5E["N5E-SUBJECT-EVIDENCE<br/>主体/空间/镜头证据取证"]
    N5E --> N5A["N5A-ENTRY-SHOT<br/>入场镜头与构图分区裁决"]
    N5A --> N4["N4-VISUAL-TONE<br/>裁决组级画面属性"]
    N4 --> N6["N6-CONNECTOR<br/>组间首尾帧连接件设计"]
    N6 --> N7["N7-ASSEMBLE<br/>场景标题 + 入场镜头 + 组头 + 原正文 + YAML + 连接件"]
    N7 --> N8{"N8-REVIEW<br/>结构、连接件、保真验收"}
    N8 -->|"pass"| N9["N9-WRITE<br/>写入 6-分组/第N集.md 与执行报告.md"]
    N8 -->|"north_star 缺失或投影错误"| N2
    N8 -->|"场景/ID 异常"| N3
    N8 -->|"组内时长异常、对白/字数过载或 atomic unit 被截断"| N5
    N8 -->|"入场镜头缺失、构图分区缺失、主体站位错误、未还原上一组尾帧或未牵引动作链"| N5A
    N8 -->|"连接件缺失、断裂或新增剧情"| N6
    N8 -->|"YAML 统计漏项"| N7
```

```mermaid
flowchart LR
    subgraph THINK["思维判断"]
        T1["输入真源判断"]
        T2["场景和组号判断"]
        T4["边界时长判断"]
        T5E["主体/空间/镜头证据判断"]
        T5["入场镜头与构图分区判断"]
        T5V["画面属性判断"]
        T6["首尾帧连接判断"]
        T7["统计证据判断"]
    end
    subgraph EXEC["执行产物"]
        E1["input manifest"]
        E2["scene unit table"]
        E4["group boundary plan"]
        E5E["subject layout evidence table"]
        E5["group entry shot + composition ledger"]
        E5V["group visual tone list"]
        E6["connector list"]
        E7["episode group draft"]
    end
    T1 --> E1 --> T2 --> E2 --> T4 --> E4 --> T5E --> E5E --> T5 --> E5 --> T5V --> E5V --> T6 --> E6 --> T7 --> E7
```

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、集号、上游和 north_star | 用户请求、项目目录 | 定位 `5-摄影/第N集.md`、`north_star.yaml`、项目记忆和上下文 | input manifest | `N2-PROJECT-STYLE` | 必需输入可读 |
| `N2-PROJECT-STYLE` | 整理三项风格字段 | north_star、当前组场景证据 | 抽取 `全局风格.全局风格提示词`、`类型元素.类型元素提示词`、`细分风格.画面风格`；把全局风格当作作品全集总风格母稿，根据每个候选组的场景类型、空间、时间、动作、光源、色彩、材质、空气、摄影和负面约束证据整理当前组专属全局风格句，并把固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。` 放在第 1 行最前；第 2、3 行直引类型元素和画面风格 | style_organization、group_style_projection list | `N3-SCENE-MAP` | 三项字段齐全；每组全局风格整理句 300 字以内、匹配当前组证据，且固定前置词已置顶于第 1 行最前 |
| `N3-SCENE-MAP` | 建立集/场/atomic unit 映射 | 摄影稿正文 | 提取场景标题、字段、分镜明细块、显式 `分镜N（约X秒）` 和对白数 | scene unit table | `N5-GROUP-PLAN` | atomic unit 不跨场景 |
| `N5-GROUP-PLAN` | 裁决组边界 | scene unit table、style_organization | 按显式时长累计形成组计划：优先接近 15 秒，通常约 12-18 秒可接受；低于约 10 秒做回填复核，超过 18 秒必须拆分、重组或回退 `5-摄影` 修复，不能例外放行；字数/对白只作辅助风险检查 | group boundary plan | `N5E-SUBJECT-EVIDENCE` | 每组时长接近 15 秒、完整且 `<=18` 秒 |
| `N5E-SUBJECT-EVIDENCE` | 建立主体/空间/镜头证据表 | group boundary plan、scene unit table、上一组末帧、组间连接件预期首态、`5-摄影` 画面/角色动作/镜头设计/分镜明细/对白主体/道具特写 | 为每组抽取可见或需要生成主体、群体、关键道具、场景锚点、姿态、动作链、朝向、视线、左右关系、前后纵深、内外关系、靠近/拉开/转向/遮挡等变化趋势、光影、色彩、氛围、前景遮挡、背景压迫和镜头观看位置；合并同一主体，不因镜头景别或状态变化拆分；标注证据来源，无法从上游推断的位置不得臆造 | subject layout evidence table、composition_axis_profile | `N5A-ENTRY-SHOT` | 每个主体有来源证据；至少可确定一条空间轴和一条关系变化线索；第二组起已回看上一组尾帧 |
| `N5A-ENTRY-SHOT` | 为每组重建开头入场镜头并落盘构图分区主体账本 | subject layout evidence table、composition_axis_profile、group boundary plan、上一组末帧、组间连接件预期首态、`references/group-entry-shot-contract.md`、`../_shared/scene-shot-identity-contract.md`、`../_shared/action-first-continuity-contract.md` | 为每个分镜组写 `入场镜头：`，说明本组从哪里进入、因什么触发进入、镜头/观看位置如何进入空间、哪些主体如何入画，以及主体之间的距离、遮挡、视线、朝向或动作相位如何开始变化。首组从本组第一个原始分镜的可见状态进入；第二组及之后从上一组末帧、上一组尾帧、上一组最后一帧或连接件抵达首态进入，具体复现主体位置、姿态、朝向、视线、身体接触、道具关系、光线、烟雾、水纹、碎片、衣袍或发丝等仍在延续的可见状态，并说明本组如何以不同景别、机位、焦点、构图或观看距离进入。场景身份和环境身份只保留进入路径所需的空间功能、固定锚点、材质、氛围、光影、色彩和声音底色，不得写回旧式静态定场段落。随后写 `画面构图：` 概述进入后的主体布局逻辑，再按固定顺序完整输出 `左侧：`、`中间：`、`右侧：`、`前景：`、`中景：`、`背景：` 六个构图分区。每个分区必须落到具体可见主体、环境锚点、遮挡、光影材质或空场压力；每个重要主体必须带形容属性、状态属性、站位属性、姿态、朝向/视线、与其他主体或关键道具的关系，以及该分区如何引入、压住、牵引、遮挡、靠近、拉开或改变主体关系；不得使用泛化占位句或静态站位清单，不另列 `角色：` / `场景：` / `道具：` 组头清单，不写成单纯人物动作摘要，不新增剧情、人物、道具互动或无互动道具氛围镜头 | group entry shot list、composition_partition_ledger、tail_frame_replay_entry、entry_source_profile、action_first_continuity_check | `N4-VISUAL-TONE` | 每组都有入场镜头、入口源、入场触发、观看位置、主体入画状态、`画面构图：` 和固定顺序六个非空、非泛化构图分区；主体位置和关系变化能回指上游、本组正文、上一组末帧或组间连接件证据 |
| `N4-VISUAL-TONE` | 裁决并输出组级画面属性 | group boundary plan、group entry shot list、上游摄影稿镜头设计、`references/group-visual-tone-contract.md`、`../5-摄影/knowledge-base/摄影构图/` | 从组内镜头设计中提炼每组的画面属性自然语句：构图布局核心选择、构图方式关键子维度（形状感/线条感/影调感/虚实感/节奏感/纹理质感/气势中选取 2-3 个）、光源效果、色彩基调和关键摄影技术参数；画面属性从镜头设计中提炼，不是从 north_star 投影，也不是从 5-摄影 内部约束直接搬运；裁决时参考 `knowledge-base/摄影构图/` 确保审美维度有摄影构图理论支撑 | group_visual_tone list | `N6-CONNECTOR` | 每组都有画面属性语句，且与组内镜头设计一致 |
| `N6-CONNECTOR` | 设计组间首尾帧连接件 | 相邻组首尾 atomic unit、style_organization、场景标题 | 在第 N+1 组完成后回看第 N 组原尾帧与第 N+1 组原首帧，逐对设计 3-4 秒连接件并判断同场景/跨场景连接，内部选择依赖型/流动型/变形型/复合型/无连接方法论，先落盘场景标题行：同场景重复同一标题，跨场景写 `场景标题A ➡️ 场景标题B`；再落盘三项风格行：第 1 行根据连接件首尾场景和运动过程整理 300 字以内连接件风格句，第 2、3 行直引类型元素和画面风格；随后写具体画面连接办法；不复述端点，改写为变化过程、主体运动、运镜设计和透视适应，末尾用 `避免元素` 写负面约束，连接件 ID 固定为 `上一个分镜组ID~下一个分镜组ID` | connector list | `N7-ASSEMBLE` | 相邻组都有连接件，且不新增剧情、不使用旧入场/出场尾钩、不输出 `连接件提示：` |
| `N7-ASSEMBLE` | 组装分组稿 | group plan、group_entry_shot list、composition_partition_ledger、group_visual_tone list、connector list、style_organization、scene title list | 每个分镜组标题后先写当前场景标题行，再写入场镜头、画面构图和构图分区，再写画面属性语句（从 `group_visual_tone` 提炼），再写组头（三项风格行：当前组全局风格整理句、类型元素、画面风格）、原正文、YAML 统计，并把组间连接件物理夹放在对应上下两个相邻分镜组之间；场景标题行、入场镜头、画面构图、构图分区和画面属性语句计入 YAML `字数统计`，不计入 `时长估算`；YAML fenced block 本身不计入字数；YAML `道具` 先做同物识别、归一合并和去重 | episode group draft | `N8-REVIEW` | 正文同步原换行；道具统计不过细、不重复 |
| `N8-REVIEW` | 验收结构和质量 | 分组稿、上游、validator | 运行机械检查或人工 review，记录报告 | review result | `N9-WRITE` 或返工 | 所有 gate pass |
| `N9-WRITE` | 落盘交付 | accepted draft | 写 `6-分组/第N集.md` 与 `执行报告.md` | output files | done | 输出可复查 |

## Failure Routes

```mermaid
flowchart TD
    F0["N8-REVIEW 发现失败"] --> F1{"失败类型"}
    F1 -->|"north_star 三项缺失"| R2["返回 N2-PROJECT-STYLE"]
    F1 -->|"场景标题缺失或 ID 不连续"| R3["返回 N3-SCENE-MAP"]
    F1 -->|"画面属性缺失或与镜头设计不一致"| R4["返回 N4-VISUAL-TONE"]
    F1 -->|"组内时长异常未复核、字数/对白风险失控或分镜明细被截断"| R5["返回 N5-GROUP-PLAN"]
    F1 -->|"入场镜头缺失、构图分区缺失、主体站位错误、未还原上一组尾帧或未牵引动作链"| R5A["返回 N5A-ENTRY-SHOT"]
    F1 -->|"连接件位置/ID错误或新增剧情"| R6["返回 N6-CONNECTOR"]
    F1 -->|"YAML 统计漏项"| R7["返回 N7-ASSEMBLE"]
    R2 --> F0
    R3 --> F0
    R4 --> F0
    R5 --> F0
    R5A --> F0
    R6 --> F0
    R7 --> F0
```

| failure | return_to |
| --- | --- |
| north_star 三项缺失 | `N2-PROJECT-STYLE`，先修复或请求授权 |
| 场景标题缺失或重复异常 | `N3-SCENE-MAP`，回上游摄影稿修复 |
| 画面属性缺失或与镜头设计不一致 | `N4-VISUAL-TONE`，重新从组内镜头设计提炼画面属性 |
| 组内累计时长低于约 10 秒，或高于 18 秒 | `N5-GROUP-PLAN`，移动完整 atomic unit；若单个 atomic unit 超 18 秒，回退 `5-摄影` 修复 |
| 入场镜头缺失、缺少入口源/入场触发/镜头观看位置/主体入画状态/动态关系变化、写回旧式静态定场段落、主体信息退化为 `角色/场景/道具` 清单、缺少 `画面构图：`，缺少 `左侧/中间/右侧/前景/中景/背景` 六字段任一字段，六字段乱序或内容泛化，主体未带形容属性/状态属性/站位属性、未覆盖全部角色站位姿态朝向和关系变化、构图关系退化为静态站位清单、第二组起未从上一组尾帧或连接件首态进入、未牵引人物动作链，或新增无互动道具氛围镜头 | `N5E-SUBJECT-EVIDENCE` -> `N5A-ENTRY-SHOT`，回上一组末帧、本组正文和上游分镜重建可进入、可承接、可变化的连续空间起始状态 |
| 场景标题行、入场镜头、画面构图、构图分区、画面属性加正文超 1680 字、对白过载或旧稿缺少显式秒数 | `N5-GROUP-PLAN`，做密度风险复核或回到 `5-摄影` 补时长 |
| 同一分镜明细被截断 | `N5-GROUP-PLAN`，恢复 atomic unit |
| 连接件缺失、无法从尾帧抵达首帧，或连接件新增剧情 | `N6-CONNECTOR`，重写 3-4 秒连接件 |
| YAML 统计漏项 | `N7-ASSEMBLE`，重抽统计 |
| validator 失败 | `N8-REVIEW`，按 fail_code 返工 |
