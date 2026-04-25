# Visual Unit Type Map

本文件定义画面句子的类型变量和镜头策略。

## Type Variables

| variable | values | use |
| --- | --- | --- |
| `visual_source` | label_match / semantic_match | 判断为何命中 |
| `visual_function` | establish / action / performance / reveal / object / group / transition / reaction | 选择镜头语言主策略 |
| `pressure_level` | low / medium / high / rupture | 决定运动强度和剪辑密度 |
| `information_density` | sparse / readable / layered / critical | 决定是否需要特写、焦点拉移或多分镜 |
| `continuity_need` | hold / cut / match_cut / sound_bridge | 决定是否使用转场或保持长镜 |
| `rhythm_profile` | converge / standard / expand / rupture | 决定镜头语言描述密度、运动复杂度和转场强度 |

## Type Matrix

| visual_function | typical fields | beat focus | technique bias | review risk |
| --- | --- | --- | --- | --- |
| `establish` | `环境描写`、空间型 `群像画面` | 空间锚点、威胁位置、角色分布 | 建立镜头、对称构图、高机位、深焦 | 写成氛围散文 |
| `action` | `角色动作`、`动作画面` | 预备、执行、结果、反应 | 跟拍、动作匹配、视线牵引、低角度 | 切太碎导致动作不清 |
| `performance` | `表演提示`、`表情特写` | 微表情、呼吸、沉默、身体压抑 | 特写、慢推、反应镜头、浅景深 | 把心理解释当画面 |
| `reveal` | `规则显影`、`系统画面`、文字型 `旁白画面` | 信息从不可见到可读 | 显影推进、焦点拉移、文字转场、微距 | 文字不可读或信息过载 |
| `object` | `道具特写`、物件状态变化 | 材质、颜色、异常、触碰关系 | 插入特写、微距、红色点光、形态匹配 | 道具脱离角色反应 |
| `group` | `群像画面`、多人反应 | 多焦点、秩序崩塌、恐惧传播 | 横移扫视、手持微晃、俯拍棋盘 | 群像没有主注意力 |
| `transition` | `转场`、声音承托画面、光变画面 | 画面接口、声画桥、形态咬合 | 声音先行、匹配剪辑、光变转场 | 炫技破坏表演停顿 |
| `reaction` | `对白画面`、`独白画面`、`音效画面` | 声音落到脸、手、肩、眼睛的反应 | 反打、压缩焦段、负空间 | 只是复述对白内容 |

## Routing

1. 先按字段标签确定候选类型。
2. 若标签与内容冲突，以内容的可见戏剧功能为准。
3. `visual_function` 决定 `beat-analysis-contract.md` 中优先检查哪些触发器。
4. `pressure_level` 和 `information_density` 决定分镜密度。
5. `rhythm_profile` 决定是否收敛、标准展开、发散强化或断裂发散。
6. `continuity_need` 决定是否读取高能转场条目。
