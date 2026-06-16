# AIGC Video Lighting Vocabulary

本知识库服务 `.agents/skills/aigc/backup/9-光影/SKILL.md`，用于把逐分镜光影描述写成 AIGC 视频模型更容易实现的具象词库。它不是第二执行合同，不拥有输出路径、完成门或主链裁决权；调用时必须回到主入口 `N6-LIGHT-DESIGN` 和 `GATE-LIGHT-09-CONCRETE-AIGC`。

## Source Set

| source_id | source | usable_rule |
| --- | --- | --- |
| `SRC-RUNWAY-GEN4` | [Runway Gen-4 Video Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide) | 单次生成更适合作为单场景、5-10 秒短片；输入图锁定主体、构图、颜色、光影和风格，文字应描述运动和变化。 |
| `SRC-RUNWAY-92` | [Runway AI Video Prompting Guide](https://runwayml.com/resources/ai-video-prompting-guide) | 视频 prompt 应清晰描述镜头、场景、动作和细节；使用正向表达，避免“不要晃动”等负向写法。 |
| `SRC-RUNWAY-CAMERA` | [Runway Camera Terms, Prompts, Examples](https://help.runwayml.com/hc/en-us/articles/47313504791059-Camera-Terms-Prompts-Examples) | 视频模型可消费“backlit, rim light, silhouette, golden hour, dusty, warm amber, high contrast shadows”等具象光影词。 |
| `SRC-LUMA-PROMPT` | [Luma Prompting Guide](https://docs.agents.lumalabs.ai/guides/prompt-guide/) | Prompt anatomy 中 lighting 是独立字段；推荐描述 light quality and direction，例如 golden hour、dramatic side lighting、soft diffused。避免 keyword soup。 |
| `SRC-SORA-2` | [OpenAI Sora 2 Prompting Guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | 光影应同时描述光质和颜色锚点；不要写“brightly lit room”，应写 soft window light、warm lamp fill、cool rim 等具体混合光源。 |
| `SRC-KLING` | [Kling Text-to-Video Prompt Guide](https://kling.ai/quickstart/text-to-video-prompt-guide) | Kling prompt 公式把 Lighting + Atmosphere 放在 Subject、Movement、Scene、Camera 后；5 秒视频应使用简洁、可显示的场景描述。 |
| `SRC-SEEDANCE-OFFICIAL` | [ByteDance Seed: Seedance 2.0](https://seed.bytedance.com/en/seedance2_0) | Seedance 2.0 是默认最优工具标准：支持 text/image/audio/video 多模态输入，强调 motion stability、audio-video joint generation，并允许创作者控制 performance、lighting、shadow、camera movement。 |
| `SRC-SEEDANCE-MODEL-CARD` | [Seedance 2.0: Advancing Video Generation for World Complexity](https://arxiv.org/abs/2604.14148) | 作为模型能力边界参考：公开模型卡描述其支持 4-15 秒音视频生成、480p/720p 原生输出，以及多图、多视频、多音频参考；光影句应适合短片段、参考承接和稳定运动。 |
| `SRC-SEEDANCE-PRACTICAL` | [Seedance 2.0 Prompt Guide 2026](https://www.seedance.tv/blog/seedance-2-0-prompt-guide) | 非 ByteDance 规格书，仅作实践参考：稳定写法是 shot / subject / action / environment / lighting / style，失败时只改 camera、motion 或 lighting 一个变量。 |

## Primary Tool Standard: Seedance 2.0

未指定其他下游视频工具时，`9-光影` 的 AIGC 可实现性默认按 `Seedance 2.0` 审查。这里的“工具标准”不是要求输出 Seedance prompt，而是要求每条中文光影句天然可被 Seedance 2.0 式视频模型转译为稳定画面。

| standard_slot | required_light_description | why_it_matters | fail_signal |
| --- | --- | --- | --- |
| `single_shot_visibility` | 每条分镜的光影变化必须能在 4-15 秒内看见：光扫过、火光跳动、屏幕冷光脉动、雨幕拉光、玻璃反射滑过 | Seedance 2.0 面向短片段生成，过长的光影演化会丢失重点 | 写成“情绪逐渐升华”“氛围层层递进”但没有可见变化 |
| `multimodal_reference_ready` | 若 source 有参考图、视频、音频或上游画面，光影句应说明哪些光色/阴影/材质需要继承，而不是重造场景 | Seedance 2.0 支持多模态参考，光影应利于参考承接 | 新增不存在的窗、火、霓虹、雨水、屏幕或光源 |
| `motion_stability` | 动态光只写 1 个主变化：光带滑过脸、门缝光延伸到手背、车灯扫过墙面、屏幕冷光轻微脉动 | 过多同步变化会让主体、背景、光色漂移 | 同一镜同时写火光、车灯、霓虹、屏幕、镜头旋转 |
| `lighting_shadow_camera_control` | 光源方向、阴影落点和运镜关系要绑定：推近时亮带压到眼睛，横移时玻璃反射从脸侧滑开 | 官方能力口径强调 lighting、shadow、camera movement 可控 | 只写“电影级光影”“强烈明暗对比”，没有光从哪里来 |
| `audio_visual_compatibility` | 有声音/节奏来源时，光影可写轻微同步：警灯脉动、屏幕闪烁、火光随风跳动；无声音依据时不强写节奏 | Seedance 2.0 支持音视频联合生成，但 `9-光影` 只做视觉内联 | 无声音/设备依据却写“随音乐频闪” |
| `positive_concrete_language` | 用可见正向描述：`门缝暖光切住鞋尖`、`冷蓝屏幕光贴住眼睛`、`湿地反射霓虹色带` | 视频模型更稳定消费明确对象和可见结果 | 用“不凌乱、不廉价、不塑料感”等负向抽象词 |

### Seedance 2.0 Light Payload Template

在 `lighting_aesthetic_plan` 内部按以下顺序形成可执行 payload；写入 canonical 正文时只保留自然中文光影句，不输出字段名。

```text
shot_duration_visibility -> trusted_light_source -> direction_and_shadow -> color_temperature -> material_or_air_medium -> one_motion_change -> camera_alignment
```

示例内部 payload：

```text
5-8秒可见 -> 门缝暖光 -> 从低位切到鞋尖和手背，脸部保留暗面 -> 暖黄对冷蓝走廊 -> 尘埃在光束里可见 -> 镜头推近时光线从手背滑到袖口
```

正文落地示例：

```text
门缝暖光从低位切住鞋尖和手背，脸部仍压在冷蓝走廊暗面里，镜头推近时细窄光线沿手背滑到袖口，光束中的尘埃短暂浮起。
```

## Usage Rules

1. 词库只提供可见光影词，不替代 `source`、`2-美学` 和分镜事实。
2. `Seedance 2.0` 是默认最优工具标准；若用户指定 Runway、Sora、Kling、Luma 或其他工具，则用户指定工具优先。
3. 每条分镜最多选择 1 个主光影词组 + 1-2 个辅助词组；超过 3 组通常会变成 keyword soup。
4. 先写中文正文，再按需要映射为英文 prompt phrase；不要把英文词直接堆进中文 canonical 正文。
5. 禁止使用无法画出来的概念词：`destiny feeling`、`premium look`、`soulful lighting`、`strong emotion`、`cinematic vibe`。
6. AIGC 视频更稳定地理解：光源位置、光色、受光对象、阴影形状、空气介质、材质反射、光随时间变化。

## Core Vocabulary Matrix

| category | zh_term | english_prompt_phrase | visible_result | use_when | avoid |
| --- | --- | --- | --- | --- | --- |
| light_source | 窗光 | `soft window light from camera left` | 一侧脸、肩线或桌面被窗外柔光托亮，另一侧保留暗部 | 室内、清晨、黄昏、安静对话 | 无窗场景硬写窗光 |
| light_source | 门缝漏光 | `thin warm light leaking through the doorway` | 一条窄光切在地面、鞋尖、手背或墙边 | 门外未知空间、悬疑、即将进入 | 把门缝光写成大面积照明 |
| light_source | 屏幕冷光 | `cool blue screen light on the face and fingers` | 蓝白光贴住眼睛、鼻梁、指尖，背景保持暗 | 手机、电脑、监控、夜间室内 | 无屏幕或电子设备时新增 |
| light_source | 烛火/火光摇曳 | `flickering candlelight / firelight` | 暖橙光在脸和墙上轻微跳动，阴影不稳定 | 古装、停电、仪式、营火 | 高频闪烁造成视频不稳 |
| light_source | 霓虹反射 | `neon reflections on wet pavement and glass` | 粉、蓝、绿等色光在湿地、玻璃、车窗上拉出反射 | 夜城、雨巷、赛博、酒吧外 | 干燥无反射面时乱写 |
| light_source | 车灯扫光 | `headlights sweep across the subject` | 亮带从脸、墙或地面快速扫过又退走 | 街道、车内、逃亡、夜路 | 没有车辆或道路事实时新增 |
| direction | 侧光 | `dramatic side lighting` | 一侧受光，一侧沉入暗部，脸部骨相更明显 | 冲突、审讯、犹豫、权力对峙 | 把侧光写成均匀照亮 |
| direction | 逆光 | `strong backlight` | 主体正面变暗，边缘被亮光勾出 | 隐藏身份、入场、离别、强轮廓 | 还要求看清正面细节 |
| direction | 轮廓光 | `thin rim light along the shoulders and hair` | 肩线、发丝、侧脸边缘出现细亮线 | 主体从暗背景里分离 | 背景过亮导致轮廓消失 |
| direction | 顶光 | `overhead light casting eye-socket shadows` | 眼窝和颧骨下方形成压迫阴影 | 审讯室、办公室、医院、走廊 | 爱情/柔和表演场景滥用 |
| direction | 低位光 | `low angle warm light rising from below` | 下巴、鼻底和手部被低位光托起，面部出现不安阴影 | 火光、地灯、门缝、仪式 | 无低位光源时写成恐怖脸 |
| quality | 柔光 | `soft diffused light` | 阴影边缘长而缓，皮肤和布料质感被柔化 | 亲密、回忆、清晨、梦感 | 抹掉关键明暗层次 |
| quality | 硬光 | `hard directional light with sharp shadow edges` | 墙面、脸部、道具上出现清晰投影和强反差 | 罪案、正午、审讯、危险 | 每条都硬光导致疲劳 |
| quality | 斑驳光 | `dappled light filtering through leaves / blinds` | 光斑切在脸、衣服、墙面，随遮挡轻微变化 | 树影、百叶窗、窗帘、监牢感 | 无遮挡结构时乱写 |
| contrast | 低调高反差 | `low-key lighting with deep shadows` | 暗部占多数，只保留局部脸、手或道具可见 | 悬疑、恐惧、秘密、压迫 | 误写成曝光不足 |
| contrast | 高调低反差 | `high-key soft even lighting` | 画面明亮、阴影浅，空间开放 | 喜剧、公开空间、广告、轻松日景 | 让画面没有主体层次 |
| contrast | 负填充吸黑 | `negative fill deepening the shadow side` | 背景或脸侧暗部被压深，主体更立体 | 黑房间、暗墙、权力压迫、孤立 | 把表演眼神完全吞掉 |
| color | 暖灯填充 | `warm lamp fill` | 琥珀/钨丝暖光托住脸侧或桌面 | 家庭、餐馆、怀旧、私密 | 每个夜景都暖黄 |
| color | 冷色边缘光 | `cool rim light from the hallway / window` | 肩线或脸侧出现蓝冷边缘，和暖主光分区 | 门外、窗外、夜间、空间对立 | 无冷光源时强行混色 |
| color | 绿偏荧光 | `greenish fluorescent overhead light` | 皮肤偏灰绿，空间显得病态、机构化 | 医院、办公室、地下室、工厂 | 美颜或浪漫场景慎用 |
| color | 钠灯橙光 | `sodium-vapor orange streetlight` | 街面和皮肤染成脏橙，暗部发棕 | 夜街、停车场、旧城、警匪 | 室内无街灯入口时乱用 |
| atmosphere | 体积光束 | `volumetric light beams through haze` | 光束在烟、雾、尘中显形 | 仓库、教堂、窗光、舞台、清晨雾 | 没有空气介质时写体积光 |
| atmosphere | 尘埃浮光 | `dust particles visible in the shaft of light` | 光柱里有细小颗粒漂浮 | 旧屋、仓库、阳光斜射、静默场景 | 大风动作戏中过密颗粒 |
| atmosphere | 雨幕拉光 | `rain streaks catching streetlight` | 雨线被街灯拉亮，背景反射变长 | 雨夜、街巷、车窗、逃亡 | 无雨事实时新增天气 |
| material | 湿地反光 | `wet ground reflecting neon light` | 地面映出拉长色带，人物脚边有光色晃动 | 雨后、酒吧街、赛博、夜景 | 干燥地面写湿反光 |
| material | 玻璃双层反射 | `layered reflections on glass` | 人脸和环境光在玻璃上叠出双影 | 窗边、车内、观察、隔离 | 无玻璃面时新增 |
| material | 金属冷反射 | `cool highlights on metal surfaces` | 刀、门把手、机械、栏杆出现冷亮边 | 武器、工业、审讯、科幻 | 金属面积过小还强写 |
| motion | 光线滑过 | `light slides across the face as the camera moves` | 随镜头或人物移动，亮带从脸侧滑过 | 推轨、横移、人物穿过光区 | 静止镜头无原因滑光 |
| motion | 光影脉动 | `subtle pulsing colored light` | 屏幕/霓虹/警灯让亮度或颜色轻微变化 | 电子屏、警灯、夜店、故障灯 | 高频闪烁、过强频闪 |
| motion | 火光跳动 | `flickering amber firelight on the wall` | 墙面和脸上暖光不稳定地跳动 | 火盆、蜡烛、营火、爆燃余光 | 无火源新增火 |
| motion | 阴影扫过 | `moving shadow passes over the subject` | 门、窗帘、人影、车辆遮挡造成暗影掠过 | 有遮挡体移动、悬疑转折 | 无运动物体时乱写 |
| stability | 光源主次清晰 | `primary window light, subtle warm practical fill` | 主光决定脸，辅助光只托暗部或边缘 | 多光源场景 | 多个强光源互相打架 |
| stability | 背景降亮 | `background falls into soft darkness` | 主体可读，背景不过曝或不抢戏 | 特写、心理戏、低调场景 | 背景完全黑导致空间丢失 |
| stability | 光色锚点 | `palette anchors: amber, steel blue, deep brown` | 3-5 个颜色稳定整场视觉 | 多镜头同场景、Sora/Runway 连续生成 | 颜色过多导致漂移 |

## Scene Recipe Pack

| scene_type | zh_recipe | english_recipe | notes |
| --- | --- | --- | --- |
| 雨夜街巷 | 湿地反光 + 霓虹反射 + 冷色轮廓光 + 雨幕拉光 | `neon reflections on wet pavement, cool rim light, rain streaks catching streetlight` | 适合夜城、追逐、孤独；必须有雨/湿地事实。 |
| 室内悬疑 | 门缝漏光 + 低调高反差 + 负填充吸黑 + 侧光 | `thin warm doorway light, low-key contrast, negative fill, dramatic side lighting` | 适合开门、等待、偷听；不要新增门外事件。 |
| 家庭温暖 | 窗光 + 暖灯填充 + 柔光 + 背景轻暗 | `soft window light, warm lamp fill, diffused shadows, background falls softly dark` | 适合餐桌、卧室、回忆；避免过度金黄。 |
| 工业/医院 | 顶光 + 绿偏荧光 + 金属冷反射 + 浅暗部 | `greenish fluorescent overhead light, cool metal highlights, shallow shadows` | 适合机构感、病态、冷酷；人脸不要完全失真。 |
| 古装/仪式 | 烛火摇曳 + 低位暖光 + 轮廓暗影 + 尘埃浮光 | `flickering candlelight, low warm light, rimmed darkness, dust in light shafts` | 适合密谈、祠堂、祭祀；必须有火/烛/灯事实。 |
| 清晨外景 | 金色低角度光 + 轻雾 + 柔背光 + 长阴影 | `golden hour low-angle sunlight, soft haze, gentle backlight, long shadows` | 适合启程、回忆、希望；避免“全身都金黄”。 |
| 科幻监控 | 屏幕冷光 + 蓝绿边缘光 + 玻璃双层反射 + 微弱脉动 | `cool screen light, cyan rim light, layered glass reflections, subtle pulsing light` | 适合控制室、监控墙、实验室；屏幕必须存在。 |
| 战斗/追逃 | 硬光 + 阴影扫过 + 车灯扫光 + 暗部保留 | `hard directional light, moving shadows, headlights sweep across, deep shadow pockets` | 适合动作片；不要同时堆太多动态光。 |

## Abstract-to-Visible Conversion

| abstract_bad | concrete_replace |
| --- | --- |
| 宿命感更强 | 顶灯熄掉一半，门缝暖光只切住鞋尖，人物正脸沉入暗部 |
| 高级电影感 | 背景降亮，侧后方细窄轮廓光勾肩线，玻璃反光在脸侧轻滑 |
| 压迫感拉满 | 顶光压出眼窝阴影，墙角不补光，人物身后的暗面吞掉空间 |
| 诗意光影 | 清晨斜窗光落在桌面尘埃里，白纱反射出柔暖边缘 |
| 灵魂被照亮 | 屏幕冷光只点亮眼睛和指尖，其他面部保留低调暗部 |
| 梦幻氛围 | 柔雾中有低反差逆光，发丝边缘泛开，背景高光轻微散射 |

## Prompt Assembly Formula

中文光影句内部先按这个顺序组织：

```text
可信光源 -> 光的方向/质量 -> 受光对象 -> 阴影/色温/材质 -> 动态变化 -> 与镜头/动作的关系
```

如需转成英文 AIGC 视频 prompt，可压成：

```text
[light source + direction], [light quality], [color/palette anchors], [material/atmosphere interaction], [motion of light], [camera alignment]
```

示例：

```text
thin warm doorway light from floor level, low-key contrast, cool hallway rim light, dust visible in the light beam, the warm line slides across his hand as the camera slowly pushes in
```

## Review Checklist

- 是否能在 5-10 秒短视频里看见该光影变化？
- 是否有明确光源或可信环境光？
- 是否说明了光照到哪个主体、哪一面、哪种材质？
- 是否避免了负向 prompt 和 keyword soup？
- 是否最多 3-5 个颜色锚点？
- 是否与相机运动、角色运动或场景运动同步？
