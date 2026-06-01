# Visual Unit Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义画面句子的类型变量和镜头策略。

## Type Variables

| variable | values | use |
| --- | --- | --- |
| `visual_source` | label_match / semantic_match | 判断为何命中 |
| `visual_function` | establish / action / performance / reveal / object / group / handoff / scene_boundary / reaction / tactile_establish / dialogue_body_anchor / memory_insert | 选择分镜画面主策略 |
| `pressure_level` | low / medium / high / rupture | 决定运动强度和剪辑密度 |
| `information_density` | sparse / readable / layered / critical | 决定是否需要特写、焦点拉移或多分镜 |
| `continuity_need` | hold / cut / scene_boundary / handoff_required / sound_handoff | 决定是否需要记录交出锚点或保持长镜 |
| `rhythm_profile` | converge / standard / expand / rupture | 决定分镜画面描述密度、运动复杂度和边界清晰度 |
| `duration_bias` | instant / short / standard / held / long_hold | 为 `shot-duration-decision-contract.md` 提供初始时值倾向 |
| `dialogue_load` | none / short_line / standard_line / long_line / voiceover | 判断对白、旁白或画外音是否决定镜头最低时长 |
| `sequence_relation` | none / same_space / prop_chain / sound_chain / action_chain / memory_insert / motif_chain | 判断是否需要形成内部 `sequence_profile`，但不改变逐句归属 |
| `ownership_risk` | low / medium / high | 判断当前分镜是否容易被段落级流畅吞掉画面点归属 |

## Type Matrix

| visual_function | typical fields | beat focus | technique bias | review risk |
| --- | --- | --- | --- | --- |
| `establish` | `环境描写`、空间型 `群像画面` | 空间锚点、威胁位置、角色分布 | 建立镜头、对称构图、高机位、深焦 | 写成氛围散文 |
| `action` | `角色动作`、`动作画面` | 预备、执行、结果、反应 | 跟拍、动作匹配、视线牵引、低角度 | 切太碎导致动作不清 |
| `performance` | `表演提示`、`表情特写`、`心理反应`、`心理变化`、`情绪反应`、`思考反应`、`认知变化`、`内心反应` | 微表情、呼吸、沉默、身体压抑、心理/思考变化的可见外化 | 特写、慢推、反应镜头、浅景深、正面停顿 | 把心理解释或思考摘要当画面，或把心理/思考反应当非画面漏掉 |
| `reveal` | `规则显影`、`系统画面`、文字型 `旁白画面` | 信息从不可见到可读 | 显影推进、焦点拉移、文字转场、微距 | 文字不可读或信息过载 |
| `object` | `道具特写`、物件状态变化 | 材质、颜色、异常、触碰关系 | 插入特写、微距、红色点光、形态匹配 | 道具脱离角色反应 |
| `group` | `群像画面`、多人反应 | 多焦点、秩序崩塌、恐惧传播 | 横移扫视、手持微晃、俯拍棋盘 | 群像没有主注意力 |
| `handoff` | 声音承托画面、光变画面、注意力交出画面 | 画面接口、声画/形态/光色锚点 | 记录交出锚点、当前停点和下一画面进入提示 | 把锚点写成创意转场方案 |
| `scene_boundary` | 场景标题变化、空间/时间/叙事段落切换 | 上一场景交出点、下一场景进入提示、空间重置 | 建立当前镜头入口、明确最后一镜交出点 | 场景凭空开始，或在摄影阶段设计组间转场 |
| `reaction` | `对白画面`、`独白画面`、`音效画面`、承接台词/事件的 `心理反应`、`思考反应`、`认知变化` | 声音、事件或认知变化落到脸、手、肩、眼睛、呼吸、站姿、注意力停滞的反应 | 反打、压缩焦段、负空间、极慢推近 | 只是复述对白内容，或只写“害怕/震惊/犹豫/意识到”等心理标签 |
| `tactile_establish` | 材质密集型 `环境描写`、空间建立、道具环境关系 | 木纹、潮水、鱼鳞、衣摆、盐霜、雾、血、水痕等可触材料如何建立空间 | 深焦横移、低机位贴近、微距材质、前景遮挡 | 材质铺陈吞掉后文动作，当前画面点失主 |
| `dialogue_body_anchor` | `对白画面` 中含手、脚、眼、衣角、道具、身体停顿 | 台词如何落到身体锚点，而不是解释心理 | 静止近景、手部/脚部特写、浅景深停顿、听者反应 | 借用后文身体反应，或时值不够承托台词 |
| `memory_insert` | 闪回、记忆画面、柔焦插入、旧时画面 | 记忆进入/退出的可见接口和当前归属 | 轻柔焦、光色偏移、动作/物件触发、短停顿 | 凭空新增记忆段，或把记忆插入写到无承托字段下 |

## Routing

1. 先按字段标签确定候选类型。
2. 若标签与内容冲突，以内容的可见戏剧功能为准。
3. `心理反应/心理变化/情绪反应/思考反应/认知变化/意识变化/内心反应/内心活动` 默认路由到 `performance` 或 `reaction`：先形成 `psychological_reaction_visualization_map`，把心理词、思考词或认知变化绑定到眼神、呼吸、面部肌肉、肩颈、手指、站姿、身体距离、视线回避、注意力停滞、停顿或道具/环境接触；不得跳过，也不得把抽象心理结论、思考摘要或“意识到”直接写进 `分镜画面`。
4. `visual_function` 决定 `beat-analysis-contract.md` 中优先检查哪些触发器。
5. `pressure_level` 和 `information_density` 决定分镜密度。
6. `rhythm_profile` 决定是否收敛、标准展开、发散强化或断裂发散。
7. `duration_bias` 只是初始倾向，必须由 `references/shot-duration-decision-contract.md` 结合节拍、信息可读性、动作完成、表演停顿、高点、对白台词量和 15 秒分组风险复判。
8. `dialogue_load` 命中 `short_line / standard_line / long_line / voiceover` 时，必须形成 `dialogue_time_budget`；对白/旁白承托画面不得只按画面动作长短裁决。
9. `sequence_relation != none` 时，必须读取 `references/visual-sequence-alignment-contract.md`，形成内部 `sequence_profile` 和 `unit_ownership_map`；该画像只用于连续性，不改变当前画面句子的落盘边界。
10. `ownership_risk = high` 时，`shot_design_plan` 必须显式执行 `unit_ownership_check`，防止后文主体动作、对白反应、记忆段或道具揭示提前外溢。
11. `visual_function = scene_boundary` 或场景/空间/时间/叙事段落发生变化时，必须读取 `references/transition-design-contract.md` 并形成内部 `handoff_profile`。
12. `continuity_need` 决定是否记录交出锚点；`handoff_required` 和 `sound_handoff` 不代表本阶段要设计转场，只代表要给 `5-分组` 留可消费连接素材。
