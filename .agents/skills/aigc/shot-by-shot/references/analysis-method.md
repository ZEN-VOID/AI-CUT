# Shot-by-Shot Analysis Method

本文件定义 `shot-by-shot` 的基础解析维度。它只提供逐镜分析方法，不拥有最终输出路由权；最终输出以 `SKILL.md` 和 `templates/output-template.md` 为准。

## Minimum Shot Record

| field | requirement |
| --- | --- |
| `shot_id` | 使用 `S001` 起顺序编号；若绑定目标集/组，可附 `episode/scene/group` |
| `timecode_in` / `timecode_out` | 可见素材必须记录；若只有截图或描述，写 `inferred` |
| `observable_event` | 只写画面和声音中能观察到的事件 |
| `entry_point` | 本镜从哪个主体、动作、声音、光色、文字或空间进入 |
| `exit_point` | 本镜把注意力交给哪里 |
| `shot_function` | 建立空间、揭示信息、压迫人物、制造反应、兑现高点、转场交出等 |

## Analysis Dimensions

| dimension | core question | output hint |
| --- | --- | --- |
| 口播论点 | 旁白、字幕或讲解明确提出了什么因果方法、禁忌、操作步骤或审美判断 | `spoken_method_note` |
| 导演调度 | 谁被放在空间权力中心，谁被压迫、遮挡、孤立或召唤 | `blocking_power_note` |
| 表演任务 | 演员在镜头里要达成什么、隐藏什么、用什么身体策略绕过去 | `performance_task` |
| 摄影语法 | 景别、视角、景深、焦点、镜头类型、运镜速度如何服务观看任务 | `camera_grammar` |
| 构图空间 | 线条、门窗、桌椅、前后景、空位、遮挡如何组织压力 | `composition_logic` |
| 光影色彩 | 光源、明暗、色相、材质如何塑造信息和情绪 | `light_color_logic` |
| 剪辑节奏 | 切点、停顿、反应镜头、声画提前或滞后如何控制呼吸 | `rhythm_logic` |
| 声音接口 | 台词、环境声、音效、静默如何引导注意力或交接镜头 | `sound_bridge` |
| 类型母题 | 该镜头承担何种类型承诺或视觉母题 | `genre_motif` |
| AIGC 可行性 | 后续图像/视频生成能否执行，是否需要拆解或简化 | `aigc_feasibility` |

## Method Rules

- 先写观察，再写解释；没有观察证据的解释只能标记为 `inference`。
- 教程型、拆解型、经验分享型视频必须先抽取口播论点，再用画面例子验证；旁白中的因果规则、反例、操作步骤和审美判断是第一证据源，不得只看截图归纳。
- 口播与画面不一致时必须分层记录：`spoken_claim` 写讲解者主张，`visual_example` 写画面是否支持，`transferable_principle` 只采纳被证据支撑且可迁移的部分。
- 先判断镜头功能，再选择临摹原则；不要从技法名倒推出意义。
- 对长镜头或复杂运动镜头，拆成 `phase_1 / phase_2 / phase_3`，但不要伪造剪辑点。
- 对快切片段，先找注意力接力和声音接口，再统计镜头数量。
- 对参考片的独特表达，必须抽象成“可迁移语法”，不得保留原片具体表达。
