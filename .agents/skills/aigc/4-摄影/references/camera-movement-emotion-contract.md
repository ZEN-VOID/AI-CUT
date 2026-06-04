# Camera Movement Emotion Contract

本文件定义运镜的情绪语义。每种运镜不只是技术选择，而是观众情绪的调节器。运镜的速度、方向、稳定性直接决定观众"被迫"感受到什么。

## Core Rule

运镜 = 情绪工具，不是技术炫技。每一个运镜决定必须回答：这个运动让观众感到什么？这种情绪是否服务于当前叙事情绪？

没有情绪语义的运镜是机械运动。观众不会记得一个"稳定跟拍"，但会记得一个"镜头逼近令人窒息"的感觉。

## Movement Emotion Mapping Table

### 基础情绪语义表

| movement_id | 运镜动作 | emotional_semantics（情绪语义） | audience_effect（观众感受） | use_when |
| --- | --- | --- | --- | --- |
| `ME-01` | 慢推向主体 | 靠近审视 / 揭示压迫 / 强迫性逼近 | 观众被迫与角色距离拉近，产生亲密或不安 | 秘密逼近 / 威胁接近 / 审视真相 / 心理压迫加深 |
| `ME-02` | 快速拉远 | 逃离 / 揭示尺度失控 / 被迫撤退 | 观众感到被推开，尺度感放大（空间或情绪） | 角色突然发现危险 / 真相揭示后倒吸冷气 / 压迫解除 |
| `ME-03` | 轻微手持晃动 | 不安 / 真实 / 在场感 | 观众感到画面"抓不住"，不确定感上升 | 监控视角 / 角色内心崩溃 / 事件突发 / 恐惧感建立 |
| `ME-04` | 稳定三脚架 | 权威 / 冷静 / 全知 / 审判 | 观众感到被审视、被观察，或感到安全（取决于场景情绪） | 规则宣判 / 全知视角 / 平静观察 / 权力对峙前的静默 |
| `ME-05` | 环绕主体旋转 | 困境 / 眩晕 / 混乱 / 失去方向 | 观众视线跟随旋转，失去对空间的确定性 | 角色内心混乱 / 困境中的挣扎 / 信息过载 / 威胁包围 |
| `ME-06` | 从低到高升起（升镜） | 希望 / 超越 / 发现 / 仰望 | 观众被迫从俯视转为仰视，主体变得高大或被升华 | 突破时刻 / 希望重燃 / 角色站立 / 真相浮出 |
| `ME-07` | 从高到低下降（降镜） | 压迫 / 下沉 / 绝望 / 俯视控制 | 观众被迫俯视，主体被压缩或被压制 | 角色被压垮 / 压迫加剧 / 规则强化 / 失败确认 |
| `ME-08` | 静止长镜头 | 凝视 / 留白 / 时间感 / 直面 | 观众被迫直视，无处躲藏；时间被拉长 | 压抑高潮 / 角色崩溃 / 规则对峙 / 需要观众承受的时刻 |
| `ME-09` | 快速甩镜 | 惊觉 / 紧迫 / 转移注意力 | 观众被迫快速跟随镜头运动，紧张感上升 | 突发事件 / 惊吓 / 注意力强制转移 / 节奏加速 |

### 进阶情绪语义表（运镜组合）

| combination | 组合效果 | narrative_use |
| --- | --- | --- |
| 推 + 手持晃动 | 侵犯感 | 逼近的同时不稳定，让观众感到被侵入而不只是被接近 |
| 拉 + 稳定三脚架 | 抽离观察 | 被推远但镜头稳定，角色变成被冷静审视的对象（而非逃离） |
| 推 + 固定 | 逼近凝视 | 镜头逼近但稳定，恐惧来自逼近本身而非画面晃动 |
| 环绕 + 推 | 螺旋困境 | 不断缩小圈子同时旋转，增强压迫感和迷失感 |
| 升 + 拉 | 升华抽离 | 升起的同时拉远，让情绪既被升华又被拉回观察距离 |
| 降 + 推 | 下沉压迫 | 下降的同时推进，让角色被压进画面深处 |
| 长镜头 + 静止 | 凝视深渊 | 镜头不动+时间延伸，让观众与角色一起承受 |
| 甩镜 + 固定 | 惊觉后静止 | 先用甩镜快速抓取注意力，然后立即静止形成反差 |

### 辅助情绪语义表

| movement_id | 运镜动作 | emotional_semantics | audience_effect | use_when |
| --- | --- | --- | --- | --- |
| `ME-10` | 极慢速运动（微速推/拉/移） | 悬念 / 等待 / 缓慢逼近 | 观众感到"要发生什么"但还没发生，紧张感积累 | 规则将要宣布 / 危险将要出现 / 角色将要崩溃 |
| `ME-11` | 横向平移（不含推拉） | 空间扫描 / 观察 / 冷静移动 | 观众视线跟随横向扫描，像在审视或观察 | 展示空间关系 / 群像扫描 / 信息收集 |
| `ME-12` | 倾斜构图移动 | 失衡 / 失控 / 失衡感强化 | 观众感到画面"不对劲"，暗示心理失衡 | 角色内心崩溃 / 空间异常 / 规则失控 |
| `ME-13` | 垂直升降（不含推拉） | 权力升降 / 心理高度 | 镜头升降位置决定视角权力感 | 角色被抬高（权力增强）或被压低（权力剥夺） |
| `ME-14` | 轨道运动（侧向推/拉） | 空间进入 / 接近 / 退离 | 侧面推入空间，让观众感到"进入"或"离开" | 进入房间 / 沿走廊接近 / 沿队列移动 |
| `ME-15` | 俯仰（不含推拉） | 仰望/俯视转换 | 视角的上下转换改变权力关系 | 角色抬头（反抗/希望）或低头（服从/绝望） |

## Movement Combination Emotion Matrix

运镜的情绪效果可以通过组合叠加或对比形成更复杂的情绪语义：

| 基础运镜 | + | 组合运镜 | = | 合成情绪语义 |
| --- | --- | --- | --- | --- |
| 慢推 (ME-01) | + | 固定 (ME-04) | = | 压迫性逼近（冷静的逼近更令人窒息） |
| 快速拉远 (ME-02) | + | 手持 (ME-03) | = | 惊恐逃离（既被推开又感到画面失控） |
| 环绕 (ME-05) | + | 轻微手持 (ME-03) | = | 迷失眩晕（旋转的同时画面不稳） |
| 长镜头 (ME-08) | + | 静止 (无运动) | = | 凝视深渊（完全静止让观众无处躲藏） |
| 甩镜 (ME-09) | + | 固定 (ME-04) | = | 惊觉钉定（快速定位后锁定，紧张凝固） |

## Emotional Alignment with Scene Tone

运镜情绪语义必须与场景整体情绪基调对齐：

| scene_tone | 适配运镜 | 不适配运镜 | rationale |
| --- | --- | --- | --- |
| 恐怖/惊悚 | 手持 (ME-03)、慢推 (ME-01)、环绕 (ME-05)、甩镜 (ME-09) | 稳定 (ME-04)、长镜头 (ME-08) | 恐怖需要不稳定感和逼近感，稳定的镜头与恐怖基调矛盾 |
| 悬疑/紧张 | 极慢速 (ME-10)、长镜头 (ME-08)、稳定 (ME-04) | 快速拉远 (ME-02)、甩镜 (ME-09) | 悬疑需要张力积累，快速运动会破坏悬念 |
| 揭示/高潮 | 稳定 (ME-04)、长镜头 (ME-08) | 手持 (ME-03)、倾斜 (ME-12) | 高潮需要清晰度，手持晃动会干扰信息传递 |
| 动作/高能 | 甩镜 (ME-09)、快速拉远 (ME-02) | 极慢速 (ME-10)、长镜头 (ME-08) | 动作需要节奏感，缓慢镜头会拖慢节奏 |
| 心理/内省 | 长镜头 (ME-08)、静止、降 (ME-07) | 甩镜 (ME-09)、环绕 (ME-05) | 内省需要时间和凝视，快速运动破坏内省感 |
| 温暖/希望 | 升 (ME-06)、稳定 (ME-04) | 降 (ME-07)、手持 (ME-03) | 希望需要升华和稳定，手持和不稳定会削弱希望感 |

## Speed Emotion Correlation

运镜速度本身是情绪参数：

| speed | emotional_semantics | use_when |
| --- | --- | --- |
| 极慢（超过 5 秒的推/拉） | 压抑积累 / 等待 / 悬念 | 规则将要宣布 / 危险将要发生 |
| 慢速（3-5 秒） | 逼近 / 审视 / 压迫加深 | 秘密接近 / 威胁靠近 |
| 中速（1.5-3 秒） | 自然过渡 / 观察 | 常规叙事过渡 / 空间建立 |
| 快速（0.5-1.5 秒） | 紧迫 / 惊觉 | 突发转移 / 节奏加速 |
| 极快（0.5 秒以内） | 惊吓 / 打断 | 强烈惊吓 / 节奏爆发 |

## Migrated Dynamic Technique Layer

本节承接原 `cinematic-technique-library.md` 中的动态内容。凡涉及运镜、速度、焦点转移、景别切换、方向参照、组合连招、高点动态处理和边界交出锚点，都必须在本合同内裁决；`cinematic-technique-library.md` 只保留静态构图与画面组织。

### Shot Size Switching Dynamics

同一画面主体在不同景别之间切换时，必须变更镜头角度或给出动作链连续性例外；不得把景别切换写成假变焦。

| dynamic_rule | emotional_or_rhythm_reason | exception |
| --- | --- | --- |
| 同一主体景别切换时，角度应有可见变化 | 避免产生“变焦而非摄影”的虚假感 | 极端快节奏动作链中为保持节奏连贯，可临时借用轴线连续性 |
| 景别越近，越倾向正面/微侧 | 方便捕捉微表情、眼神和瞳孔变化 | 侧脸或 3/4 脸用于表现隐瞒、闪躲或分裂 |
| 景别越远，越倾向中立/客观 | 建立空间、权力关系和群体处境 | 主观恐惧镜头可借用低角度大远景 |

| film_genre | shot_size_switch_pattern | rhythm_requirement | example |
| --- | --- | --- | --- |
| 舒缓温情类 | 景别相邻过渡，不跳级 | 渐变式，避免同一镜头内从极远跳到极近 | 全景 -> 中景 -> 近景 -> 特写 |
| 快节奏武侠 / 动作类 | 大跨度景别切换，大远景与特写可用 | 短促剪辑，景别落差产生视觉冲击 | 大远景 -> 特写 -> 大远景 |
| 高能战斗 / 追逐 | 景别快速切换并保持方向清晰 | 保持运动感但不丢空间方向 | 跟拍近景 -> 反应特写 -> 环境全景 |
| 强叙事压迫类 | 景别从宽到紧递进 | 速度与压迫感同步升级 | 中全景 -> 中景 -> 近景 -> 特写 |
| 群像恐慌类 | 个体反应与群体扩散跳切 | 每跳一次，恐惧层级递增一档 | 特写 -> 全景 -> 特写 |

节奏判断标准：

- `rhythm_profile=conserve / measured / recovery` 时，景别切换偏保守，只在必要揭示点才切近。
- `rhythm_profile=burst / peak_slot / set_piece_chain_slot` 时，允许大跨度景别切换以释放视觉冲击。

### Focus Movement And Perception Dynamics

| technique | use when | execution cue |
| --- | --- | --- |
| 焦点拉移 | 同镜头完成信息转交 | 从人物眼神拉到规则字、道具、门缝或反应对象 |
| 失焦再合焦 | 眩晕、醒来、规则显影、感知异常 | 失焦不能太久，合焦点必须落在新信息上 |
| 焦点追随 | 动态跟踪、视线引导 | 焦点跟随运动主体，背景流动模糊 |

焦点运动必须说明观众获得了什么新信息；只写“背景虚化”“焦点变化”但没有信息转交，按 `FAIL-CINE-05X` 返工。

### Movement Speed Palette

| speed | use when | execution cue |
| --- | --- | --- |
| 静止 | 宣判、僵持、被迫服从 | 镜头不救角色，压力由表演和声音累积 |
| 极慢 | 危险无声逼近、意识慢慢发现 | 推拉摇移速度低于观众警觉阈值 |
| 慢速 | 观察、悬疑、信息揭示 | 让观众有时间读文字、看反应、感受空间 |
| 中速 | 普通动作承接、视线转交 | 不炫耀运动，清楚把注意力送到目标 |
| 快速 | 突发、惊吓、动作冲击 | 只用于强节拍，之后给反应镜头落地 |
| 急停 | 危险确认、人物被点名、规则锁定 | 运动突然停止在眼睛、手、字或门口 |
| 变速 | 感知异常、规则显影、心理断裂 | 加速/减速必须对应可见信息变化 |

### Dynamic Parameter Composition

执行时不要把参数写成清单，也不要机械套“从/以/变化到/最终”句式。先在内部选参数，再把它们压成自然运动句。

| static parameter list | dynamic expression |
| --- | --- |
| `近景、浅景深、长焦、慢推` | 从中景的课桌边缘慢慢压成近景，长焦把后排空间挤扁，景深逐步收窄到人物眼睛 |
| `特写、微距、焦点拉移` | 先让关键表面占满画面，再把焦点从反光拉到异常痕迹 |
| `俯拍、深景深、慢速横移` | 从棋盘式空间俯拍开始慢速横移，让每一排人物像被规则逐格扫描 |

### AI Video Direction References

涉及人物移动、镜头跟随、入画退场或视线方向时，必须把方向绑定到镜头、摄像机、画面边界或空间锚点。方向参照优先进入内部计划，影响下游视频阶段时应自然进入 `时间段` 正文。

| direction case | weak cue | executable cue |
| --- | --- | --- |
| 朝向镜头 | 人物向前走 | 人物朝镜头走来，课桌边缘从两侧后退 |
| 远离镜头 | 人物往后退 | 人物背对镜头缓慢离开，身体逐渐远离摄像机 |
| 横向入画 | 人物从左边进入 | 人物从画面左侧进入，穿过前景，停在右侧三分之一处 |
| 空间深处 | 走到前面 | 沿课桌通道向画面深处走，最后停在黑板字下方 |
| 跟随移动 | 镜头跟着他 | 镜头保持在他右后方半步跟随，直到门框阴影压住肩线 |

### Advanced Movement Techniques

| technique | use when | execution cue |
| --- | --- | --- |
| 隐形推轨 | 危险或信息慢慢逼近 | 推进速度低于观众意识阈值，结尾落在眼睛、手、文字 |
| 视线牵引摇镜 | 注意力从角色视线转向目标物 | 先给眼神，再沿视线摇到门、黑板、道具 |
| 焦点拉移 | 同一镜头内完成主体切换 | 前景人物虚化，后景规则或危险变清晰 |
| 轴线压缩 | 角色退无可退、空间变窄 | 长焦压扁空间距离，让环境像被折叠 |
| 甩镜/急摇 | 惊吓、骤停、突发入场 | 只用于强节拍，不覆盖需要冷静压迫的段落 |
| 手持微晃 | 人群恐惧、失控边缘 | 控制晃动幅度，保留信息可读性 |
| 静止长镜 | 权力碾压、规则宣判 | 镜头不动，让演员和声音造成压力 |

### Peak Movement Treatments

这些技法只在上游画面已经是 `peak_visual_unit` 或明显高点时使用。它们用于服务 `peak-shot-language-contract.md`，不得为制造高潮感新增事实。

| peak_treatment | use when | execution cue |
| --- | --- | --- |
| 峰值读秒 | 认知翻转、规则显影、艰难判断 | 静止或极慢推轨，让文字、眼神或手部动作保持可读 1-2 秒 |
| 结果钉镜 | 行动结果、胜负变化、任务成败 | 运动结束后急停在结果物、对手反应或角色身体代价上 |
| 反应回声 | 规则压迫、奇观、公开打脸、群体恐慌 | 事件后切 1 个群像或关键旁观者反应，作为余波落点 |
| 技术显影 | 高超对决、推理、谈判、规则漏洞 | 用视线牵引、过肩构图、焦点拉移或轴线压缩展示“如何赢/如何识破” |
| 断裂入侵 | 怪异、惩罚、惊吓、灾变 | 声音先行、光变、急摇或甩镜后必须给清楚落点，不能只制造混乱 |
| 温柔停顿 | 关系暖点、治愈、状态修复、风景高点 | 少运动、浅景深或慢速横移，把距离变化、手部动作、物件交换留住 |

### Boundary Handoff Anchors

本节只提供 `4-摄影` 可记录的动态交出素材，不提供组间或跨场景创意转场方案。场景变化时，`4-摄影` 只处理上一画面交出点和下一画面进入提示；连接强度、匹配方式和 3-4 秒连接件提示由 `5-分组` 裁决。具体边界遵守 `transition-design-contract.md`。

| handoff_anchor | use when | execution cue |
| --- | --- | --- |
| 场景边界落点 | 场景、空间或时间段变化 | 上一画面的落点清楚交出，下一画面只给进入提示 |
| 声音余波 | 声音可作为连接素材 | 高跟鞋、铃声、教鞭、日光灯嗡鸣在当前画面末端保留 |
| 形态/颜色锚点 | 两个画面可能共享轮廓、色块或运动方向 | 白光、红珠、黑板波纹、瞳孔反光等状态在当前画面末端可见 |
| 动作落点 | 一个动作的方向或速度可供下游连接 | 推门、翻页、抬眼、教鞭点地成为当前画面落点 |
| 光变状态 | 过曝、熄灯、显影、冷光闪动 | 光线吞没、露出或停住信息，但不写如何转入新画面 |
| 文字/符号锚点 | 规则、系统字、板书成为画面接口 | 字体、波纹、小字停在可被下游连接的位置 |
| 反应落点 | 事件结果需要落到被击中的脸或手 | 恐惧不直接展示完，停在指尖、瞳孔、肩膀 |

## Failure Modes

### FM-01: 运镜只有技术理由无情绪语义

**症状**：分镜画面中只有"用 50mm 镜头推"，没有说明"推"让观众感到什么。

**诊断**：每个运镜描述必须包含情绪语义说明。如果只写了技术参数，这就是 FM-01。

**修复**：为每个运镜补充 `emotional_semantics` 和 `audience_effect`。格式参考"运动情绪语义表"。

### FM-02: 运镜与场景情绪不符

**症状**：一个需要内心冷静审视的场景用了手持晃动（ME-03），或者一个恐怖压迫场景用了稳定三脚架（ME-04）。

**诊断**：检查运镜的情绪语义与场景整体情绪基调的匹配度。

**修复**：参考"情绪对齐表"调整运镜选择，或在分镜画面中明确说明为何用反差性运镜（如"用稳定镜头反衬内心混乱"）。

### FM-03: 运镜速度与叙事节奏矛盾

**症状**：高潮爆发场景用了极慢推，节奏拖沓；或者内心独白场景用了快速甩镜。

**诊断**：检查运镜速度是否服务于叙事节奏。速度是情绪参数，不是偏好。

**修复**：参考"速度情绪关联表"，让运镜速度与叙事节奏匹配。

### FM-04: 运镜组合没有形成新情绪语义

**症状**：写了"推+手持"，但没有说明这个组合比单独的推或手持多了什么情绪效果。

**诊断**：运镜组合必须产生 1+1>2 的效果，而不是简单叠加。

**修复**：参考"组合情绪语义表"，为运镜组合明确其合成情绪语义。

### FM-05: 长镜头静止被滥用为"高级感"

**症状**：到处用长镜头静止，因为觉得"长镜头=专业电影感"，但与场景情绪不匹配。

**诊断**：长镜头（ME-08）的情绪语义是"凝视/直面"，不是"高级感"。如果场景不需要观众直面，长镜头只是拖沓。

**修复**：只在需要观众直视承受的场景（心理对峙、崩溃时刻、规则宣判）使用长镜头。

## Per-Shot Movement Emotion Field Specification

每个 `shot_design_plan` 中的运镜部分必须包含情绪语义字段：

| field | type | required | description |
| --- | --- | --- | --- |
| `movement_emotion` | enum | 是 | 使用 ME-01 至 ME-15 编码，不得只写技术参数 |
| `emotional_semantics` | string | 是 | 一句话说明这个运镜让观众感到什么（不得只写"推进"或"拉远"，必须写具体的情绪） |
| `audience_effect` | string | 是 | 这个运镜对观众情绪产生的具体影响（可以用被动语态："观众被迫..."） |
| `speed_reason` | string | 否 | 为什么用这个速度（如果速度与常规不同） |
| `combination_emotion` | string | 否 | 如果是运镜组合，这个组合产生什么合成情绪语义 |

## Reusable Heuristics

1. **每一个运镜都有情绪代价**：观众不会忘记一个逼近镜头的窒息感，也不会忘记被快速推远的失控感。运镜不是中性工具。
2. **速度即情绪**：极慢意味着积累，快速意味着紧迫。在决定运镜速度前，先问"此刻需要积累还是释放"。
3. **组合不是叠加**：推+手持不是"又推又晃"，而是"入侵性的不稳定"。每个组合必须有新的情绪语义。
4. **手持不是万能恐惧工具**：手持晃动（ME-03）适合恐惧，但不适合需要清晰观察的场景。在需要冷静审视的场景用手持，会让观众感到"镜头自己也在害怕"。
5. **长镜头是双刃剑**：静止长镜头（ME-08）让观众无法逃避，但如果用错场景，会让观众感到"无聊"而非"直面"。
6. **运镜方向即权力方向**：推=入侵（谁推谁强势），拉=抽离（谁拉谁掌控距离），升=升华（谁升谁被抬高），降=压低（谁降谁被压制）。
7. **甩镜后要静止**：快速甩镜（ME-09）后紧跟固定，让紧张感在静止中凝固，形成"惊觉钉定"效果。
8. **运镜情绪对齐是强制约束**：运镜与场景情绪不匹配是结构性错误，不是风格偏好。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does every important movement choice state the emotional semantics and audience effect rather than only naming push, pull, pan, handheld or static technique? | `GATE-CINE-29` | `FAIL-CINE-05X` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | `camera_movement_emotion_plan` samples with `movement_emotion`, `emotional_semantics` and `audience_effect` |
| Is the movement aligned with the scene tone, or is a deliberate contrast justified by the current narrative task? | `GATE-CINE-29` / `GATE-CINE-16` | `FAIL-CINE-05X` / `FAIL-CINE-05I` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | scene tone to movement alignment notes and contrast exceptions |
| Does the movement speed serve accumulation, release, shock, observation or pressure instead of contradicting the shot rhythm or duration decision? | `GATE-CINE-29` / `GATE-CINE-04B` | `FAIL-CINE-05X` / `FAIL-CINE-05L` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` / `steps/cinematography-workflow.md#N5.2-DURATION` | speed reason samples and duration/movement consistency checks |
| If movement is combined, does the combination produce a new emotional meaning rather than a stack of techniques? | `GATE-CINE-29` | `FAIL-CINE-05X` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | `combination_emotion` samples and rewritten combination shots |
| Are static or long-held shots used only when the viewer must observe, endure or face something, not as a generic "premium cinema" marker? | `GATE-CINE-29` / `GATE-CINE-12` | `FAIL-CINE-05X` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | long/static shot justification and deleted decorative long-take examples |
| Does the internal movement field set include at least `movement_emotion`, `emotional_semantics` and `audience_effect` for shots whose movement matters? | `GATE-CINE-17` / `GATE-CINE-29` | `FAIL-CINE-05J` / `FAIL-CINE-05X` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | node completion evidence and movement field coverage samples |
| When changing shot size on the same subject, does the shot also change angle or preserve a justified action-chain exception, avoiding fake zoom-like coverage? | `GATE-CINE-16` | `FAIL-CINE-05I` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | shot-size transition samples with angle/rhythm motivation |
| Does genre/rhythm context decide whether shot-size switching is conservative, wide-jump, compression-based or high-energy, instead of applying one default style? | `GATE-CINE-16` / `GATE-CINE-05` | `FAIL-CINE-05I` / `FAIL-CINE-05D` | `steps/cinematography-workflow.md#N5-RHYTHM` / `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | `rhythm_profile` and shot-size pattern evidence |
| Are movement, entry, exit and sightline directions tied to camera, frame edge or spatial anchor so downstream video does not drift? | `GATE-CINE-15A` / `GATE-CINE-26` | `FAIL-DIRECTION-REF-01` / `FAIL-CINE-05N` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | direction-reference samples such as toward camera, away from camera, frame-left entry or spatial-depth movement |
| Are peak movement treatments used only for upstream high points and without adding facts, dialogue, action results or false climax treatment? | `GATE-CINE-14` | `FAIL-CINE-05E` | `steps/cinematography-workflow.md#N5.5-PEAK-SHOT` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | peak evidence, peak-shot strategy and no-new-fact checks |
| Are boundary handoff anchors limited to visible exit material for `5-分组`, without writing full cross-scene transition solutions inside `4-摄影`? | `GATE-CINE-21` | `FAIL-CINE-05K` | `steps/cinematography-workflow.md#N6.1-HANDOFF` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | handoff anchor samples and no-overreach checks |
