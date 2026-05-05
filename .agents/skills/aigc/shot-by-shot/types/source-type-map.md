# Source Type Map

| source_type | trigger | handling | risk |
| --- | --- | --- | --- |
| `video_file` | 用户提供本地视频文件 | 直接逐镜观察，记录时间码 | 文件不可读或格式不支持时需截图/描述补证 |
| `stills_sequence` | 用户提供截图序列 | 按截图顺序建立 inferred shot map | 不能推断完整运镜，只能分析构图和可能切点 |
| `timecoded_notes` | 用户提供时间码描述 | 用描述建立 partial shot map | 必须标注用户描述来源 |
| `public_clip_link` | 用户给出公开视频链接 | 能访问则观察；不能访问则要求截图或描述 | 链接失效或地区限制 |
| `memory_reference` | 用户只说“像某片某段” | 不做逐镜强结论，只给通用 craft 假设和补证需求 | 误记、过度概括、版权边界不清 |

## Stage Bridge Route

| bridge_target | trigger | load |
| --- | --- | --- |
| `0-初始化` | 用户要临摹或补强 north star 的全局风格、细分风格、类型元素 | `.agents/skills/aigc/0-初始化/SKILL.md + CONTEXT.md` |
| `2-编导` | 用户要临摹场面、表演、导演调度、人物压力 | `.agents/skills/aigc/2-编导/SKILL.md + CONTEXT.md` |
| `3-摄影` | 用户要临摹镜头语言、运镜、构图、光影、节奏 | `.agents/skills/aigc/3-摄影/SKILL.md + CONTEXT.md` |
| `5-设计` | 用户要临摹角色造型、空镜场景、道具资产、材质和美术秩序 | 按目标加载 `5-设计/角色/2-设计`、`5-设计/场景/2-设计`、`5-设计/道具/2-设计` |
| `0+2+3+5` | 用户要融合 north star 画面风格、编导、摄影和设计可套用结果 | 同时加载 `0-初始化`、`2-编导`、`3-摄影` 与对应 `5-设计` 子技能 |
| `research_only` | 用户只要分析，不绑定项目阶段 | 不写项目 runtime，直接输出报告 |
