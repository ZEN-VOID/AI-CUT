# AIGC Visual Signal Matrix

> **契约地位**：本文件为 `2-编导` script layer 提供 AIGC 图像/视频生成的视觉信号映射规范，是 field-routing-and-audio-visual-contract.md §12 的扩展和深化。

---

## 1. 概述

本矩阵定义了**情绪/类型 → 视觉信号**的完整映射，供 AIGC 图像/视频生成时使用。

核心原则：
- **具体化**：避免泛化，使用具体可见描述
- **可感知化**：提供视觉/听觉可接收的信号
- **场景化**：包含空间、光线、道具等环境信息
- **分层化**：从背景到前景到主体分层描述

---

## 2. 字段 → 视觉参数映射

> **来源**：field-routing-and-audio-visual-contract.md §12

| 字段 | AIGC 生成参数 | 说明 |
|------|-------------|------|
| `环境描写` | `setting`, `lighting`, `atmosphere`, `color_temperature`, `weather`, `time_of_day` | 场景、光线、氛围、色温、天气、时间 |
| `角色动作` | `pose`, `gesture`, `facial_expression_hint`, `body_direction`, `speed_motion_blur` | 姿态、手势、表情提示、身体方向、运动模糊 |
| `场面调度` | `spatial_composition`, `character_placement`, `depth_relation`, `cinematic_framing` | 空间构图、人物位置关系、景深 |
| `表情特写` | `facial_detail`, `micro_expression`, `emotional_cue`, `eye_direction` | 面部细节、微表情、情绪信号、眼神方向 |
| `道具特写` | `prop_detail`, `texture`, `light_interaction`, `material`, `wear` | 道具细节、材质、光线互动 |
| `系统画面` | `ui_elements`, `text_display`, `glow_effect`, `digital_interface` | 界面元素、文字显示、发光效果 |
| `心理反应` | `actor_body_cue`, `subtle_movement`, `tension_line`, `physiological_response` | 演员身体信号、微动作、张力线 |
| `群像画面` | `crowd_composition`, `group_reaction`, `attention_direction`, `mass_movement` | 群体构图、群体反应、注意力方向 |
| `动作画面` | `action_sequence`, `movement_path`, `impact_frame`, `motion_direction` | 动作序列、运动路径、冲击帧 |
| `音效画面` | `sound_visual_sync`, `source_visibility`, `ripple_effect`, `environmental_reaction` | 声音视觉同步、声音源可见性、涟漪效应、环境反应 |

---

## 3. 情绪 → 视觉信号矩阵

### 3.1 恐惧（Fear）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 阴影拉长、闪烁忽明忽暗、底部反光、单点光源抖动 | `long shadows, flickering light, under-lighting, single point light source trembling` |
| **色彩** | 冷调、低饱和、局部高对比、蓝灰色调 | `cool color palette, desaturated, high local contrast, blue-gray tones` |
| **构图** | 留白增加、人物靠边/靠墙、被切割出画面、角落构图 | `more negative space, character pressed against wall, framing at edge, corner composition` |
| **身体** | 后退、手护住胸前/脸前、蜷缩、抱臂、膝盖弯曲 | `stepping back, hands protecting chest/face, curling up, crossing arms, bent knees` |
| **表情** | 瞳孔放大、眼睛睁大、嘴唇抿紧、下唇颤抖 | `dilated pupils, wide eyes, pressed lips, trembling lower lip` |
| **空间** | 封闭空间、门/窗在身后、身后有阴影、空旷中有孤立感 | `enclosed space, door/window behind, shadow behind figure, isolation in open space` |
| **道具** | 碎玻璃、破镜子、滴落的水滴、倒塌的物件 | `broken glass, shattered mirror, dripping water, fallen objects` |

### 3.2 压迫（Oppression）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 顶部直射、地面反光、暗角、顶灯压下 | `overhead lighting, ground reflection, vignette, ceiling light pressing down` |
| **色彩** | 灰色基调、降低饱和度、统一色调 | `gray color base, reduced saturation, unified tone` |
| **构图** | 低顶棚感、人物俯视、广角近距离仰拍、密集排列 | `low ceiling feeling, worm's-eye view, wide angle close-up low angle, dense arrangement` |
| **身体** | 肩膀下沉、头部低垂、重心下降、手压住桌面 | `drooping shoulders, head bowed, lowered center of gravity, hand pressing desk` |
| **表情** | 眉心下压、眼睛向下看、嘴角下拉、眉头紧锁 | `furrowed brow, eyes looking down, downturned mouth, knitted eyebrows` |
| **空间** | 拥挤、狭窄通道、多人逼近、高墙 | `crowded, narrow corridor, multiple people approaching, high walls` |
| **道具** | 天花板吊灯、讲台高台、审判桌、铁栅栏 | `ceiling lamp, elevated platform, judge's bench, iron bars` |

### 3.3 紧张（Tension）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 硬光、边缘光、追光、局部高光 | `hard light, rim light, follow light, selective highlight` |
| **色彩** | 高对比、局部色彩饱和、强调色 | `high contrast, local color saturation, accent color emphasis` |
| **构图** | 中心聚集、四角压暗、对称构图被打破 | `center aggregation, dark corners, symmetry broken` |
| **身体** | 身体前倾、重心前移、手指敲击、手心出汗 | `leaning forward, forward weight shift, finger tapping, sweaty palms` |
| **表情** | 眼神游离、眨眼频繁、咬唇、深呼吸 | `darting eyes, frequent blinking, lip biting, deep breathing` |
| **空间** | 面对面、近距离、无退路 | `face to face, close distance, no escape route` |
| **道具** | 计时器、倒计时屏幕、绷紧的绳子、武器 | `timer, countdown screen, taut rope, weapon` |

### 3.4 温暖/亲密（Warmth/Intimacy）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 柔光、暖色温、散射光、边缘柔化 | `soft light, warm color temperature, diffused light, soft edges` |
| **色彩** | 暖色调、高饱和、自然色、金色/橙色点缀 | `warm color palette, high saturation, natural colors, gold/orange accents` |
| **构图** | 人物靠近、框架内构图、亲密距离、对称或三分法 | `characters close together, framed composition, intimate distance, rule of thirds` |
| **身体** | 靠近、肩膀接触、手握手、头靠头 | `leaning in, shoulder contact, holding hands, heads together` |
| **表情** | 眼角皱纹、真笑、放松的眉毛、自然眼神 | `crow's feet, genuine smile, relaxed eyebrows, natural eye contact` |
| **空间** | 柔和背景、居家环境、自然场景 | `soft background, home environment, natural setting` |
| **道具** | 烛光、热饮、毯子、窗边阳光 | `candlelight, hot drink, blanket, sunlight through window` |

### 3.5 孤独（Loneliness）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 单点光源、轮廓光、阴影占主导、背光剪影 | `single light source, rim light, shadow dominant, backlit silhouette` |
| **色彩** | 蓝灰调、降低饱和、弱对比、冷暖对比 | `blue-gray tones, reduced saturation, low contrast, cool-warm contrast` |
| **构图** | 人物远离、留白占主导、大量负空间、角落位置 | `figure distant from others, negative space dominant, vast empty space, corner position` |
| **身体** | 身体蜷缩、单人背影、侧脸、低头 | `curled up body, single figure from behind, profile, head down` |
| **表情** | 空洞眼神、无表情、望向远方 | `hollow eyes, blank expression, gazing into distance` |
| **空间** | 空旷、巨大空间、窗外无人 | `vast emptiness, huge space, no one outside window` |
| **道具** | 空椅子、空酒杯、熄灭的蜡烛、窗外夜色 | `empty chair, empty glass, extinguished candle, night view outside window` |

### 3.6 悬疑（Suspense）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 侧光、低角度、阴影覆盖半边脸、明暗对比 | `side lighting, low angle, shadow covering half face, chiaroscuro` |
| **色彩** | 蓝绿调、降低饱和、单色调倾向 | `blue-green tones, reduced saturation, monochromatic倾向` |
| **构图** | 三分法、重点在边缘、框架内框架、窥视感 | `rule of thirds, subject at edge, frame within frame, voyeuristic feel` |
| **身体** | 侧身、隐藏姿势、手放在暗处、身体紧绷 | `side view, hidden posture, hand in shadow, body tense` |
| **表情** | 半遮脸、眯眼、困惑眼神、一只眼在光中 | `half-covered face, squinting, confused gaze, one eye in light` |
| **空间** | 半开着的门、窗帘缝隙、钥匙孔、阴影角落 | `half-open door, curtain gap, keyhole, shadowy corner` |
| **道具** | 模糊的文字、破碎照片、半张脸、镜中倒影 | `blurred text, torn photo, half face, mirror reflection` |

### 3.7 暴力/危险（Violence/Danger）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 硬边光、红橙色调、闪烁、血色反光 | `hard edge lighting, red-orange tones, flickering, blood-red reflection` |
| **色彩** | 高对比、红蓝冷暖对比、强调红/黑色 | `high contrast, red-blue warm-cool contrast, red/black emphasis` |
| **构图** | 低角度仰拍、广角夸张、速度线、冲击感 | `low angle, wide angle distortion, speed lines, impact feel` |
| **身体** | 动态姿势、出拳/挥砍动作、肢体伸展、翻滚 | `dynamic pose, punching/swinging motion, limbs extended, tumbling` |
| **表情** | 扭曲的脸、咬牙、张嘴喊叫、血溅 | `twisted face, clenched teeth, mouth open screaming, blood splatter` |
| **空间** | 碎片四散、尘土飞扬、烟雾、破碎物 | `debris scattered, dust flying, smoke, shattered objects` |
| **道具** | 武器、血迹、破碎玻璃、火焰 | `weapon, blood stain, broken glass, flames` |

### 3.8 悲伤/失落（Grief/Loss）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 暗淡、柔光、无明确光源、灰白色调 | `dim, soft light, no clear light source, gray-white tones` |
| **色彩** | 冷色调、低饱和、蓝灰、褪色感 | `cool tones, low saturation, blue-gray, faded feel` |
| **构图** | 中央构图但孤立、单人占比小、背景模糊 | `centered but isolated, small figure proportion, blurred background` |
| **身体** | 垂下手臂、头部低垂、跪地、单膝跪 | `hanging arms, head bowed, kneeling, on one knee` |
| **表情** | 眼眶泛红、空洞眼神、眼泪、嘴唇颤抖 | `red-rimmed eyes, hollow gaze, tears, trembling lips` |
| **空间** | 空旷空间、雨天、落叶、废墟 | `empty space, rainy, fallen leaves, ruins` |
| **道具** | 破碎的照片、遗物、葬礼花束、熄灭的灯 | `broken photo, keepsake, funeral flowers, extinguished lamp` |

### 3.9 愤怒（Anger）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 红色色调叠加、高对比、闪烁光源 | `red color overlay, high contrast, flickering light source` |
| **色彩** | 红/黑强调、高饱和、暖色冲突 | `red/black emphasis, high saturation, warm color clash` |
| **构图** | 广角近距离、不平衡构图、压迫感 | `wide angle close-up, unbalanced composition, pressing feel` |
| **身体** | 拳头紧握、身体前冲、颤抖、站直僵硬 | `clenched fists, leaning forward aggressively, trembling, rigid stance` |
| **表情** | 眉头紧皱、瞪眼、咬牙切齿、脸红、颈静脉怒张 | `furrowed brow, glaring, teeth grinding, flushed face, neck vein bulging` |
| **空间** | 狭小空间、被逼到角落、对峙 | `small space, cornered, confrontation` |
| **道具** | 被砸的物品、破碎的玻璃、推倒的椅子 | `smashed items, broken glass, overturned chair` |

### 3.10 期待/希望（Anticipation/Hope）

| 维度 | 信号 | AIGC 提示词 |
|------|------|-------------|
| **光线** | 曙光、透光、暖色边缘光 | `dawn light, light penetrating, warm rim light` |
| **色彩** | 渐变暖色、蓝色转金色、向上色彩 | `gradient warm colors, blue to gold, upward color shift` |
| **构图** | 向上看、望向远方、地平线 | `looking up, gazing into distance, horizon line` |
| **身体** | 手放在胸前、抬头、伸展、准备起跑姿势 | `hand on chest, head tilted up, stretching, ready-to-run stance` |
| **表情** | 眼中希望之光、轻微微笑、屏息 | `light in eyes, slight smile, held breath` |
| **空间** | 开阔视野、地平线、门/窗打开 | `open view, horizon, door/window open` |
| **道具** | 日出/日落、开启的门、种子发芽、地图 | `sunrise/sunset, open door, seed sprouting, map` |

---

## 4. 类型片视觉标准（Genre Visual Standards）

### 4.1 校园规则怪谈

| 视觉元素 | 信号 | 说明 |
|----------|------|------|
| **空间** | 教室、走廊、门框、窗边、讲台 | 规则怪谈核心空间 |
| **光线** | 荧光灯管、白炽灯、窗帘过滤光、忽明忽暗 | 人工光源为主，暗示控制 |
| **色彩** | 冷白、灰色校服、红色强调（高跟鞋、口红、血迹） | 对比色制造不安 |
| **构图** | 规则几何、课桌排列、行列秩序、俯视/平视交替 | 秩序感与压抑 |
| **道具** | 黑板规则、课桌编号、点名册、教鞭、广播 | 规则显影载体 |
| **声音视觉** | 高跟鞋声、广播声、铃声、机械提示 | 规则声音化 |
| **群像** | 整齐校服、集体低头、同一动作、脸被遮挡 | 去个性化 |

### 4.2 战斗/动作

| 视觉元素 | 信号 | 说明 |
|----------|------|------|
| **速度** | 运动模糊、速度线、慢动作定格 | 速度感 |
| **冲击力** | 尘土/水花/碎片、冲击波、变形 | 物理反馈 |
| **空间** | 开阔/封闭对比、空中/地面、垂直位移 | 空间变化 |
| **身体** | 伸展/蜷缩交替、重心转移、旋转 | 身体力学 |
| **道具** | 武器轨迹、光效、碰撞 | 道具动态 |
| **光线** | 金属反光、追光、剪影 | 动作光效 |

### 4.3 悬疑/推理

| 视觉元素 | 信号 | 说明 |
|----------|------|------|
| **观察视角** | 第一人称视角、窥视框架、镜子反射 | 主观观察 |
| **信息载体** | 文字特写、照片、痕迹、指纹 | 线索可视化 |
| **光影** | 明暗对比、阴影中的线索、手电筒光柱 | 光线引导 |
| **空间** | 狭窄通道、楼梯、门/抽屉内部 | 隐藏空间 |
| **构图** | 三分法、边缘构图、框架内框 | 视觉谜题 |
| **细节** | 特写放大、时间痕迹、磨损、裂缝 | 微物证据 |

### 4.4 情感/亲密

| 视觉元素 | 信号 | 说明 |
|----------|------|------|
| **距离** | 亲密距离、身体靠近、视线交汇 | 空间亲密 |
| **光线** | 柔光、暖色、散射、单点光 | 亲密氛围 |
| **身体** | 手部接触、头部靠近、拥抱、依赖 | 身体语言 |
| **表情** | 真笑、眼部细节、泪光、呼吸同步 | 微表情 |
| **道具** | 共同持有的物件、信物、礼物 | 情感连接 |
| **构图** | 封闭框架、中心构图、浅景深 | 聚焦主体 |

### 4.5 恐怖/惊悚

| 视觉元素 | 信号 | 说明 |
|----------|------|------|
| **黑暗** | 深阴影、仅部分照亮、完全黑暗 | 未知恐惧 |
| **异常** | 比例失调、位置异常、动作诡异 | 恐怖谷效应 |
| **声音视觉** | 嘴张开无声、震动、静音符号 | 声音断点 |
| **反射** | 镜中异常、玻璃倒影、水面扭曲 | 反射恐怖 |
| **空间** | 封闭、狭窄、出口被堵、身后威胁 | 空间压迫 |
| **身体** | 僵硬、抽搐、不自然姿态、后退 | 恐惧身体化 |

### 4.6 科幻/赛博朋克

| 视觉元素 | 信号 | 说明 |
|----------|------|------|
| **界面** | 全息投影、AR界面、数字纹理 | 数字元素 |
| **光线** | 霓虹、LED、数据流、光纤 | 科技光效 |
| **色彩** | 青色、紫色、橙红色、数字绿 | 赛博色调 |
| **空间** | 高层建筑、垂直城市、网络空间 | 赛博空间 |
| **身体** | 机械增强、神经接口、发光部件 | 身体改造 |
| **质感** | 金属、玻璃、数字网格、电路纹理 | 科技材质 |

---

## 5. 场景状态 → 视觉参数

### 5.1 进入状态（Entry State）

| 状态类型 | 视觉参数 | 说明 |
|----------|----------|------|
| **建置入场** | 宽镜头、全景、establishing shot | 建立空间全貌 |
| **角色入场** | 中景跟随、视线引导、身体局部 | 引导关注角色 |
| **紧张入场** | 低角度仰拍、压迫构图、暗角 | 建立压迫感 |
| **发现入场** | 特写推进、景深变化 | 引导发现 |

### 5.2 压力状态（Pressure State）

| 状态类型 | 视觉参数 | 说明 |
|----------|----------|------|
| **持续压迫** | 稳定镜头、硬光、紧凑构图 | 压迫持续 |
| **压迫升级** | 推进镜头、加速剪辑暗示、光线变暗 | 升级信号 |
| **压迫顶点** | 特写、极简构图、寂静暗示 | 顶点时刻 |

### 5.3 转折状态（Turning Point State）

| 状态类型 | 视觉参数 | 说明 |
|----------|----------|------|
| **上行转折** | 光线变亮、暖色进入、空间打开 | 希望/突破 |
| **下行转折** | 光线变暗、冷色进入、空间收缩 | 危机/失去 |
| **揭示转折** | 特写聚焦、信息载体突出 | 信息揭晓 |

### 5.4 退出状态（Exit State）

| 状态类型 | 视觉参数 | 说明 |
|----------|----------|------|
| **压力释放** | 镜头拉远、柔光、放松构图 | 释放完成 |
| **悬念留存** | 镜头静止、阴影留存、声音余韵 | 悬念延续 |
| **情绪落点** | 人物近景、表情定格、环境呼应 | 情绪收尾 |

---

## 6. AIGC 提示词生成规范

### 6.1 生成原则

| 原则 | 说明 | 错误示例 | 正确示例 |
|------|------|----------|----------|
| **具体化** | 避免泛化，使用具体可见描述 | `scary atmosphere` | `dim corridor, flickering fluorescent light, dust particles in light beam` |
| **可感知化** | 提供视觉/听觉可接收的信号 | `feels nervous` | `slight tremor in hand, gulping, eyes darting to the door` |
| **场景化** | 包含空间、光线、道具等环境信息 | `character scared` | `character backed against wall, one hand near face, cold sweat on forehead` |
| **分层化** | 从背景到前景到主体分层描述 | `scary scene` | `background: abandoned classroom, midground: overturned desks, foreground: character crouching` |
| **情绪锚定** | 包含情绪可读的身体/空间信号 | `tension` | `shoulders hunched, fingers gripping desk edge, ceiling light casting harsh shadows` |

### 6.2 分层结构

```
AIGC Prompt Structure:

[光线/色温] + [空间/场景类型] + [主体位置/姿势] + [表情/情绪信号] + [道具/细节] + [构图/景别]

示例：
Warm amber light, school classroom with rows of empty desks, female teacher standing at elevated platform, slight unnatural smile, wooden pointer in hand, wide-angle low-angle shot, cinematic
```

### 6.3 禁止模式

| 禁止 | 原因 | 修正 |
|------|------|------|
| 泛化情绪词 | AIGC 难以理解抽象概念 | 用具体身体/空间信号替代 |
| 无空间上下文 | 缺少场景信息 | 必须包含空间/环境描述 |
| 矛盾光线描述 | 产生视觉噪声 | 统一光源方向和色温 |
| 过长的复合句 | AIGC 解析困难 | 拆分为简洁的描述单元 |
| 缺少对比元素 | 画面平淡 | 加入光影对比、色彩对比、动静对比 |

### 6.4 类型化提示词模板

#### 校园规则怪谈

```
[光线] fluorescent flickering light, [空间] typical classroom, [主体] teacher in red heels standing at blackboard, [道具] pointer, [构图] elevated view, [氛围] oppressive, [风格] cinematic, desaturated
```

#### 战斗动作

```
[光线] hard rim light, [空间] open arena with debris, [主体] character mid-air with weapon extended, [动作] motion blur trail, [特效] dust particles, [构图] low angle wide shot, [风格] dynamic, high contrast
```

#### 情感亲密

```
[光线] soft warm diffused light from window, [空间] intimate close-up frame, [主体] two characters with foreheads touching, [道具] hands intertwined, [表情] genuine smile with crow's feet, [构图] shallow depth of field, [风格] intimate, golden hour
```

---

## 7. 交叉引用索引

| 本文件章节 | 对应规则/文档 | 说明 |
|-----------|-------------|------|
| §2 字段映射 | field-routing §12 | 正式编导字段的 AIGC 参数 |
| §3 情绪矩阵 | hollywood-quality-spec.md §6 | 10种情绪的完整视觉信号 |
| §4 类型片标准 | hollywood-quality-spec.md §4 | 6种类型的视觉要求 |
| §5 场景状态 | hollywood-quality-spec.md §5 | 4种场景状态参数 |
| §6 提示词规范 | novel-to-screen-language-contract.md | 转换方法论的 AIGC 落地 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 字段到视觉参数的映射是否仍以 `环境描写`、`角色动作`、`表情特写`、`心理反应`、`音效画面` 等正式编剧字段为源，而不是另造第二套视觉字段或把抽象情绪直接交给 AIGC？ | `GATE-SCRIPT-10` | `FAIL-CONCRETE-VISUAL` | `steps/directing-workflow.md#N4-FIELD` | `aigc_visual_signal_matrix.field_parameter_trace` 记录每个视觉参数回指的正式字段与源句 |
| 情绪/类型视觉信号是否被转成可见、可听、可感知的身体、空间、光线、道具或群体信号，而不是停留在 `scary atmosphere`、`tension` 等泛化情绪词？ | `GATE-SCRIPT-10` | `FAIL-CONCRETE-VISUAL` | `steps/directing-workflow.md#N4-FIELD` / `steps/directing-workflow.md#N5-SCRIPT-DRAFT` | `aigc_visual_signal_matrix.concrete_signal_audit` 列出抽象词替换为具体信号的证据 |
| `表情特写` 对应的视觉信号是否只写眉、眼、嘴角、咬肌、下颌、喉头等面部细节，并能回指上游触发或当前声画压力？ | `GATE-SCRIPT-18` | `FAIL-FACIAL-EXPRESSION-FIELD` | `steps/directing-workflow.md#N4-FIELD` | `facial_expression_anchor_evidence` 记录触发源、主体、面部分区和风险检查 |
| 场景状态、类型片标准和提示词结构是否补足空间、光线、道具、主体位置与前中后景层次，避免无空间上下文或矛盾光线描述？ | `GATE-SCRIPT-10` | `FAIL-CONCRETE-VISUAL` | `steps/directing-workflow.md#N4-FIELD` | `aigc_visual_signal_matrix.layered_prompt_evidence` 记录空间、光源、主体、道具和构图层次 |
| 声音视觉化是否仍保持声音字段与 `音效画面` / `旁白画面` 等画面字段就近配对，而不是把声音类别、时间说明或叙述概括写成声音本体？ | `GATE-SCRIPT-05` / `GATE-SCRIPT-11` | `FAIL-PAIRING` / `FAIL-SOUND-LITERAL` | `steps/directing-workflow.md#N4-FIELD` | `audio_visual_pairing_map` 与 `sound_literal_risk_map` 记录声音源、声音本体和对应画面 |
| 场景入场、压力、转折和退出状态是否服务 `scene_rhythm_profile`，而不是把镜头方案、剪辑节奏或导演级分镜提前写入编剧层？ | `GATE-SCRIPT-20` | `FAIL-SCENE-RHYTHM` | `steps/directing-workflow.md#N3-SCENE` / `steps/directing-workflow.md#N5-SCRIPT-DRAFT` | `scene_rhythm_profile` 记录 entry / pressure / turning / exit 状态及转出方式 |
