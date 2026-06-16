# Cinematic Lighting TOP10 Knowledge Base

本知识库服务 `.agents/skills/aigc/backup/9-光影/SKILL.md`，用于在逐分镜光影美学注入时提供“可转译为正文的光影表现技巧”。它不是第二执行合同，不拥有输出路径、完成门或主链裁决权；调用时必须回到主入口 `N2-LIGHT-UNDERSTAND`、`N5-LIGHT-SHOT-FUNCTION`、`N6-LIGHT-DESIGN` 和 `N8-LIGHT-REVIEW-REPAIR`。

## Source Set

| source_id | source | reusable_value |
| --- | --- | --- |
| `SRC-ASC-QUALITY` | [ASC Shot Craft: Light Quality 101](https://theasc.com/article/shot-craft-light-quality-101/) | 光的强度、颜色、质量；硬光/柔光由光源相对大小和距离决定，关键落点是阴影边缘与质感呈现。 |
| `SRC-ASC-PRACTICALS` | [ASC: Fargo - Cold-Blooded Scheming](https://theasc.com/article/fargo-cold-blooded-scheming/) | Roger Deakins 的 location/practical 思路：先让场景内灯具有资格成为光源，再让隐藏灯补足可拍性。 |
| `SRC-ASC-LOGICAL` | [ASC: Spectral Strife - Shining Vale](https://theasc.com/article/spectral-strife-shining-vale/) | logical lighting：窗、实景灯和房间功能决定光源逻辑；亮房间与阴影房间可承担不同叙事职能。 |
| `SRC-ASC-NYKVIST` | [ASC Salutes Sven Nykvist](https://theasc.com/article/asc-salutes-sven-nykvist/) | Nykvist 将光看作叙事语言：柔、死、雾、暴烈、低角度、感性等光质都改变观众感受。 |
| `SRC-STUDIOBINDER` | [StudioBinder: Film Lighting Techniques](https://www.studiobinder.com/blog/film-lighting-techniques/) | motivated lighting、practicals、natural light、diffusion、hard light、low-key 等基础技法的电影化使用。 |
| `SRC-ADORAMA` | [Adorama/42West: Types of Lighting in Film](https://www.adorama.com/alc/basic-cinematography-lighting-techniques/) | key/fill/backlight、low-key、motivated lighting、gel/window shadow 等可操作的布光角色与情绪用途。 |
| `SRC-BACKSTAGE-COLOR` | [Backstage: Color Temperature in Film](https://www.backstage.com/magazine/article/what-is-color-temperature-75608/) | 色温和色彩对情绪、角色状态和叙事语气的影响。 |
| `SRC-LEARNABOUTFILM` | [Learn About Film: Using Light in Your Movie](https://www.learnaboutfilm.com/film-language/picture/light-and-colour/) | 三点布光原则、rim/backlight、光影连续性和自然光替代方案。 |

## TOP10 Technique Matrix

| rank | technique | use_when | inject_as | avoid |
| --- | --- | --- | --- | --- |
| `T01` | 动机光与实景灯锚定 | 场景中有窗、灯、火、屏幕、街灯、车灯、烛光、门缝或可见环境光源 | 先写“光从哪里被观众相信”，再写隐藏增强后的受光结果：窗光切过人物侧脸、餐桌吊灯压出眼窝阴影、屏幕冷光贴住指尖 | 无 source 支撑时新增光源；把 practical 变成道具清单 |
| `T02` | Key/Fill/Back 分工与光比 | 需要控制主体可读性、阴影深度和轮廓分离 | 写主光定义观看方向，填充光控制阴影保留量，背光/轮廓光把主体从背景里切出来 | 机械写“三点布光”；让填充光把冲突抹平 |
| `T03` | 硬光/柔光与阴影边缘 | 分镜需要质感、威胁、审讯、温柔、梦感或无方向环境光 | 硬光写清锐利投影、纹理凸显、亮暗切线；柔光写清渐变阴影、低反差、皮肤/布料/雾气的柔化 | 用“柔和/强烈”替代可见阴影边缘；每条都体积光 |
| `T04` | Low-key / High-key / Contrast Ratio | 想让画面显得悬疑、温暖、公开、压迫、轻松或临床化 | low-key 写阴影占比、局部可见、暗部吞没；high-key 写低反差、亮面连贯、几乎无威胁暗角 | 把 low-key 误写成“曝光不足”；把 high-key 写成无层次平光 |
| `T05` | 阴影设计与负填充 | 需要让危险、隐瞒、权力不对称或孤立感进入画面 | 写“不给光”的区域：脸的一半沉入暗部、背景被吸黑、前景遮挡制造压迫、墙角无填充形成空洞 | 只给主体加光，不设计暗部；让阴影遮掉关键表演信息 |
| `T06` | 自然光、反射与遮挡控制 | 外景、窗边、走廊、白墙、雪地、水面、车内等可用环境光强 | 写 bounce、反射、旗板/遮挡的画面结果：白墙漫反射托起下颌，窗帘削弱顶光，雪地反光冷冷托亮眼眶 | 输出器材操作；无视自然光方向和时间 |
| `T07` | 色温与混合色光 | 场景有情绪对立、内外空间冲突、时代质感或不同光源共存 | 写暖光/冷光/绿偏/钠灯/霓虹/屏幕光如何分区：暖灯留住亲密，窗外冷光压进肩线，绿偏荧光让办公室显得病态 | 把色彩当滤镜；无动机地堆红蓝紫 |
| `T08` | 逆光、侧光、轮廓光与剪影 | 需要分离主体、制造神秘、隐藏身份、表现孤独或增强空间深度 | 写边缘亮线、头发/肩线被切开、人物成为黑形、背景亮面吞掉细节、侧光雕出脸部骨相 | 剪影时仍描写面部细节；轮廓光没有背景对比 |
| `T09` | 空气介质与材质反射 | 场景有雾、烟、雨、尘、玻璃、水面、金属、湿地、织物或强光穿透 | 写光在介质中显形：尘埃浮在窗光里，雨幕把街灯拉成长线，水面晃光扫过天花板，玻璃反射把人物切成双层 | 没有介质也写体积光；把反射写成新增道具 |
| `T10` | 动态光源与光色接力 | 角色移动、镜头运动、门开合、火焰、屏幕、车灯、警灯、霓虹、水面或窗帘变化 | 写时间中的变化：车灯扫过脸又退走，火光在墙上摇，屏幕蓝光随手指滑动跳变，人物从暖光走进冷光 | 高频炫技；动态光源无 source anchor；破坏相邻分镜连续性 |

## Runtime Trigger Rules

| trigger_signal | load_this_kb | return_to_node | required_output_evidence |
| --- | --- | --- | --- |
| 用户要求“电影光影表现技巧”“TOP10”“参考网络资料”“知识库” | yes | `N2-LIGHT-UNDERSTAND` | `knowledge_source_matrix`、`top10_technique_selection` |
| `N6-LIGHT-DESIGN` 出现泛化套词、光源随机、动态光源不足、多光源无主次 | yes | `N6-LIGHT-DESIGN` | `technique_applied_map`，每条失败分镜至少绑定 1 个 `Txx` |
| `FAIL-LIGHT-GENERIC` 或 `FAIL-LIGHT-MOTIVATION-RANDOM` | yes | `R1/R2 -> N5/N6` | `generic_phrase_scan`、`lighting_reason_samples` |
| `FAIL-LIGHT-DYNAMIC-EMPTY` 或 `FAIL-LIGHT-CONTINUITY-BREAK` | yes | `R1/R2 -> N4/N6` | `dynamic_light_map`、`light_state_timeline` |

## Application Formula

逐分镜注入时不要把 `Txx` 名称写进正文。内部可按以下顺序消化：

```text
source fact -> scene light logic -> selected Txx -> visible light result -> camera/movement alignment -> continuity handoff
```

正文句式建议：

```text
可见光源/可信光源 + 明暗结构 + 色温/材质/空气作用 + 动态变化或静态理由 + 与主体/运镜的关系。
```

示例骨架：

```text
窗外冷光从侧后方压入，人物正面只留桌灯的低位暖反射，眼下阴影被保留，随着镜头缓慢靠近，玻璃上的蓝色反光轻轻滑过脸侧，让压抑感从空间过渡到表演。
```

## Review Notes

- 每条光影句至少能回指一个 source fact 或场景风格事实。
- 大师/作品参照只能贡献光影原则，不能变成照搬画面。
- 多技巧可以叠加，但每条分镜优先 1 个主技巧、1 个辅助技巧；超过 3 个技巧通常会变成堆词。
- 若 source 没有动态光源，优先用 `T03/T04/T05/T08` 做静态明暗，不强行套 `T10`。
