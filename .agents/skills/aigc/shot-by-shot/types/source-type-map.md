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
| `3-美学整体` | 用户要对齐 3-美学、全套美学、风格解析或六子技能 side context | `references/aesthetic-style-analysis-contract.md`，加载 `.agents/skills/aigc/3-美学/SKILL.md + CONTEXT.md` 及六子技能合同 |
| `画面基调` | 用户要临摹或补强全片画面基调、媒介技术栈、美学范式、节奏锚点 | `references/aesthetic-style-analysis-contract.md`、`.agents/skills/aigc/3-美学/画面基调/SKILL.md + CONTEXT.md` |
| `角色风格` | 用户要临摹角色层视觉风格、轮廓、妆发、服装结构或体态质感 | `references/aesthetic-style-analysis-contract.md`、`.agents/skills/aigc/3-美学/角色风格/SKILL.md + CONTEXT.md` |
| `场景风格` | 用户要临摹空间风格、空镜秩序、材质光影或世界地理视觉信号 | `references/aesthetic-style-analysis-contract.md`、`.agents/skills/aigc/3-美学/场景风格/SKILL.md + CONTEXT.md` |
| `道具风格` | 用户要临摹道具功能层级、材质体系、符号边界或细节密度 | `references/aesthetic-style-analysis-contract.md`、`.agents/skills/aigc/3-美学/道具风格/SKILL.md + CONTEXT.md` |
| `摄影风格` | 用户要临摹摄影风格层面的构图秩序、景别、机位、运动、连续性 | `references/aesthetic-style-analysis-contract.md`、`.agents/skills/aigc/3-美学/摄影风格/SKILL.md + CONTEXT.md` |
| `分镜风格` | 用户要临摹分镜组织、节奏密度、镜头组合、转场和信息流 | `references/aesthetic-style-analysis-contract.md`、`.agents/skills/aigc/3-美学/分镜风格/SKILL.md + CONTEXT.md` |
| `编剧` | 用户要临摹戏剧问题、人物压力、对白策略、声画承托或场面任务 | `.agents/skills/aigc/2-编剧/SKILL.md + CONTEXT.md`、`references/screenwriter-style-analysis-contract.md` |
| `导演` | 用户要临摹导演意图、场面调度、声画配对、画面化选择或批注意图 | `.agents/skills/aigc/4-导演/SKILL.md + CONTEXT.md`、`references/adaptation-output-contract.md` |
| `表演` | 用户要临摹微表情、动作停顿、潜台词行为、台词语气或演员表演任务 | `.agents/skills/aigc/5-表演/SKILL.md + CONTEXT.md`、`references/adaptation-output-contract.md` |
| `分镜` | 用户要临摹角色/道具移动、相对位置变化、动作路径、参考系、跨画面连续性或分镜节奏 | `.agents/skills/aigc/7-分镜/SKILL.md + CONTEXT.md`、`references/adaptation-output-contract.md` |
| `摄影` | 用户要临摹可转入摄影阶段的镜头语言、运镜、构图、视点、焦点或节奏 | `.agents/skills/aigc/8-摄影/SKILL.md + CONTEXT.md`、`references/cinematography-style-analysis-contract.md` |
| `光影` | 用户要临摹光源叙事、光色母题、空气介质、明暗关系或材质反射 | `.agents/skills/aigc/9-光影/SKILL.md + CONTEXT.md`、`references/cinematography-style-analysis-contract.md` |
| `11-主体` | 用户要给角色、场景、道具正式设计阶段提供参考原则 | 按目标加载 `11-主体/角色/2-设计`、`11-主体/场景/2-设计`、`11-主体/道具/2-设计` 与 `references/design-style-analysis-contract.md` |
| `分镜脚本` | 用户要标准表格式分镜脚本或需要对齐 Numbers 示例 | `references/storyboard-script-contract.md`、`templates/output-template.md` |
| `全量输出` | 用户要融合 3-美学风格解析、编剧、导演、表演、分镜、摄影、光影、主体和分镜脚本可套用结果 | 同时加载 3-美学六子技能、`2-编剧`、`4-导演`、`5-表演`、`7-分镜`、`8-摄影`、`9-光影`、对应 `11-主体` 子技能和分镜脚本合同 |
| `research_only` | 用户只要分析，不绑定项目阶段 | 不写项目 runtime，直接输出报告 |
