# Visual Point And Beat Contract

本文件融合旧 `4-摄影/references/visual-matching-contract.md` 与 `beat-analysis-contract.md`，改写为 `6-分镜` 的 step1/step2 细则。它只授权画面点识别与画面节拍法，不授权旧 `4-摄影` 的 `3-运动` source、原字段正文改写或 `[起始秒-结束秒]` 输出格式。

## Core Rule

从 `5-导演/第N集.md` 或用户指定文稿中找出所有需要内联分镜处理的画面点。每个画面点保持原字段归属，分镜列表只追加在该字段下方。

本文件中的“画面化/可视化”默认按白描式可拍材料处理：画面点必须落到主体、起始状态、空间层次、动作相位、视线、声音、光线、道具、文字或时间变化；不得用明喻、隐喻、象征或概念标签替代可执行画面。

节拍在本阶段等价于“分镜切换触发点”：单个画面点内，任何会让观众观看策略、注意力对象、动作相位、信息可读性、情绪压力、空间关系或声画打点发生变化的瞬间，都可以触发一条新的 `分镜N（N-N秒）`。其中时码 `N-N秒` 由时值合同投影到 0.5 秒网格，不要求整数秒。

## Beat Calculation Protocol

`beat=N` 必须由“候选触发点 -> 观看状态变化聚类 -> 有效 beat 计数”得到，不得由字段类型、段落类型、动作复杂度标签或预设数量表直接推出。

计算步骤：

1. 锁定当前画面点的 `ownership_boundary`：只处理当前字段拥有的信息，不吞入上一字段或下一字段的动作、反应、结果或转场。
2. 建立 `candidate_trigger_set`：从当前字段中列出可能触发分镜切换的观看变化，并用 `BT-01..BT-15` 标记依据。
3. 建立 `state_change_cluster_map`：把候选触发点按“是否造成同一次独立观看状态变化”聚类。多个 `BT` 若共同支撑同一观看状态变化，只算 1 个 cluster。
4. 建立 `merged_trigger_log`：记录被合并的触发点及合并理由，例如“同一声画打点同时造成主体切换和情绪转折，观众只需要一次观看策略变化”。
5. 建立 `rejected_trigger_log`：删除无独立观看结果的候选触发点，例如“环境陪体只强化同一空间压迫，不改变注意力对象或信息可读性”。
6. 得出 `beat_count_formula`：`beat=N = count(state_change_cluster_map.valid_clusters)`。
7. 校验 `beat=N == shot_count_decision == actual_storyboard_lines`；不一致时回到本协议第 1 步，不得只改数字凑格式。

禁止口径：

- 不得写成“静态氛围/反应点多为 1 个 beat，复杂武器/护送调度/双重危险多为 2-3 个 beat”等类型到数量的经验映射。
- 不得把 `BT` 数量直接等同于 beat 数量；`BT` 是证据标签，cluster 才是有效 beat 的数量真源。
- 不得为了控制篇幅把多个独立观看状态变化压成 1 个 beat。
- 不得为了显得密集把同一观看状态变化拆成多个 beat。
- 不得让脚本、字段标签、关键词、行长、标点数量或固定镜头序列裁决 beat 数。

## Visual Point Match

默认命中字段：

| keyword | typical fields |
| --- | --- |
| `画面` | `画面`、`动作画面`、`对白画面`、`音效画面`、`旁白画面`、`系统画面`、`氛围画面` |
| `动作` | `角色动作`、`动作画面` |
| `表演` | `表演提示` |
| `心理` | `心理反应`、`心理变化`、`内心反应` |
| `思考/认知` | `思考反应`、`角色思考`、`认知变化`、`意识变化` |
| `描写/特写/显影` | `环境描写`、`道具特写`、`规则显影`、`系统显影` |

字段标签未命中但内容含人物造型、姿态、视线、微表情、呼吸、手部动作、身体距离、场景空间、光线、文字、屏幕、道具状态、异常物理变化或可视化插入段时，也可命中。

## Psychological And Audio-Visual Overlay

- `心理反应/思考反应/认知变化` 不得默认排除，必须先白描式转译为眼神、呼吸、咬肌、肩颈、手指、站姿、身体距离、视线回避、停顿、注意力停滞或与环境/道具的可见关系；删除“像/仿佛/宿命感/压迫感”等词后仍应可分镜。
- `音效画面` 和 `旁白画面` 不能只写声音本体；必须判断声音对应的可见主体、反应落点、空间变化、系统文字或环境承托。
- `系统画面` 必须判断文字/图标/屏幕/规则显影的可读时值和反应镜头。

## Beat Trigger Matrix

| trigger_id | 节拍触发 | 判断问题 | 分镜响应 |
| --- | --- | --- | --- |
| `BT-01` | 主体切换 | 注意力是否从人物转向物、群体转向个体、前景转向背景？ | 新分镜、焦点/景别切换 |
| `BT-02` | 动作分相 | 动作是否包含预备、执行、结果、反应？ | 多分镜覆盖动作链 |
| `BT-03` | 信息揭示 | 文字、道具、眼神、异常细节是否首次可读？ | 显影/特写/焦点落点 |
| `BT-04` | 情绪转折 | 表情、身体、呼吸、沉默是否发生压力变化？ | 正面近景、正面双眼特写、停顿 |
| `BT-05` | 空间关系 | 人物与危险源、门窗、讲台、座位关系是否需要重定位？ | 建立镜头、轴线重置 |
| `BT-06` | 声画驱动 | 声音是否先行、骤停、变形或牵引画外注意力？ | 声画切点 + 可见反应 |
| `BT-07` | 视觉形态变化 | 光、色、文字、物体状态是否变化？ | 光变/形态锚点 |
| `BT-08` | 权力关系变化 | 谁控制场面、谁被凝视、谁被孤立是否改变？ | 高低机位、构图压迫 |
| `BT-09` | 摄影参数变化 | 景别、景深、视角或运动是否必须改变才清楚？ | 分镜切换或构图重设 |
| `BT-10` | 声音打点 | 撞击、拟声、笑声骤停等是否形成“一声一结果”？ | 每声对应可见结果 |
| `BT-11` | 平台钩子 | 当前 1-3 秒是否需要新视觉刺激或强问题感？ | 异常细节、遮挡揭示 |
| `BT-12` | 微动作跳点 | 眼神、呼吸、手指、肩膀等是否形成可见变化？ | 近景/特写/短反应 |
| `BT-13` | 文字可读点 | 系统字、字幕、屏幕、标签是否需要读清？ | 读秒分镜 |
| `BT-14` | 物理接触点 | 碰到、拿起、推开、撕开、激活道具是否产生结果？ | 接触点 + 结果 |
| `BT-15` | 构图刺激点 | 是否需要角度、前景、遮挡、突然留白制造观看变化？ | 新构图分镜 |

## Beat-To-Shot Mapping

- 分镜数必须等于当前画面点内的有效画面节拍数。
- 每个有效画面节拍生成 1 条 `分镜N（N-N秒）`，时码按 0.5 秒网格连续落盘。
- 分镜展开前必须先在正文写入 `节拍量化：beat=N（beat1: BT-xx 触发依据；beat2: BT-xx 触发依据）`。
- `beat=N` 等同于当前画面点的有效画面节拍数，并且必须匹配 `shot_count_decision` 和下方实际 `分镜` 条数。
- 括号内 `BT` 是各有效 beat 的判定依据，不是独立数量真源；多个 BT 若共同支撑同一个观看状态变化，应合并为同一个 beat 的依据。
- 不设置任何分镜数量上下限。
- 只有当两个候选触发点不构成独立观看状态变化时，才可判定为同一有效画面节拍。
- 不得为了控制数量而压缩有效节拍，也不得为了显得密集而把同一节拍拆成多条分镜。

## Evidence

每个画面点至少保留：

| field | meaning |
| --- | --- |
| `source_line` | 原文稿行文本 |
| `label` | 字段标签 |
| `match_reason` | 标签命中或语义命中原因 |
| `scene_anchor` | 所在场景标题 |
| `ownership_boundary` | 当前画面点拥有的信息边界 |
| `beat_map` | 每个有效 beat 对应的 BT 触发依据 |
| `candidate_trigger_set` | 当前画面点的候选触发点及对应 BT 依据 |
| `state_change_cluster_map` | 候选触发点按独立观看状态变化聚类后的有效 beat 真源 |
| `merged_trigger_log` | 合并多个候选触发点为同一 beat 的理由 |
| `rejected_trigger_log` | 删除无独立观看结果候选触发点的理由 |
| `beat_count_formula` | `beat=N = count(valid_clusters)` 的计算证据 |
| `shot_count_decision` | 有效画面节拍数与分镜数量一致性 |
| `beat_quant_line` | 正文 `节拍量化：beat=N（BT-xx...）` 及其与分镜条数的一致性 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 所有画面点是否被识别并保留归属？ | `GATE-SB-02` | `FAIL-SB-VISUAL-POINT` | `N3-VISUAL-POINTS` | `visual_point_inventory` |
| 心理/思考/认知字段是否被白描式画面化，没有停留在抽象结论、比喻、象征或概念标签？ | `GATE-SB-02` | `FAIL-SB-VISUAL-POINT` / `FAIL-SB-PLAIN-VISUALIZATION` | `N3/N5` | psychological visualization samples、`plain_visualization_audit` |
| 每条分镜是否来自有效画面节拍，且分镜数匹配有效画面节拍数即正文 `beat=N`、`shot_count_decision` 和实际分镜条数？ | `GATE-SB-04` | `FAIL-SB-BEAT` | `N4-BEAT-SPLIT` | `beat_map`、`beat_quant_line`、`shot_count_decision` |
| 分镜数量是否避免固定模板化？ | `GATE-SB-04` | `FAIL-SB-SHOT-COUNT` | `N4-BEAT-SPLIT` | count distribution and repairs |
| `beat=N` 是否由候选触发点聚类后的独立观看状态变化数量得到，而不是字段类型、动作复杂度标签、经验数量范围、BT 标签数量或脚本规则得到？ | `GATE-SB-23` | `FAIL-SB-BEAT-CALCULATION-DRIFT` | `N4-BEAT-SPLIT` | `candidate_trigger_set`、`state_change_cluster_map`、`merged_trigger_log`、`rejected_trigger_log`、`beat_count_formula` |
| `节拍量化` 行是否位于原字段正文和第一条分镜之间？ | `GATE-SB-21` | `FAIL-SB-BEAT-QUANT-LINE` | `N4-BEAT-SPLIT` / `N8-INLINE-INJECT` | `beat_quant_line`、format samples |
