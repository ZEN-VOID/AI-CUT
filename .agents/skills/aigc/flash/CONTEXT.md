# CONTEXT.md

## Purpose & Loading Contract

本文件是 `.agents/skills/aigc/flash` 的经验层知识库，不是第二份执行合同。调用 `$aigc-flash` 或 `flash` 时，它必须与同目录 `SKILL.md` 一起加载，用于避免短视频 prompt 漂成正式项目阶段、空泛视觉词、参考污染或多模态误读。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-chat-only-prompt-heuristics

## Type Map

| type_id | symptom | likely root layer | immediate fix | verification |
| --- | --- | --- | --- | --- |
| `FLASH-TM-01` | 用户只要 prompt，但输出开始写项目路径或执行报告 | 输出边界漂移 | 回 `Output Contract`，只输出聊天窗口 prompt pack | final answer 没有落盘路径 |
| `FLASH-TM-02` | 纯文本故事源被扩成长篇剧本 | 4-编剧压缩失败 | 回 `F3-SCREENPLAY-COMPRESS`，只保留短冲突、动作链和尾钩 | prompt 可在 11.5 秒内拍完 |
| `FLASH-TM-03` | 图生视频 prompt 改掉首帧主体、构图或主光 | 多模态锁定不足 | 回 `F2`，列 `confirmed` 保持项和允许变化项 | prompt 有保持主体/构图/光影约束 |
| `FLASH-TM-04` | 首尾帧生视频中间运动无法从 A 到 B | 连续性设计不足 | 建 `first_last_state_map`，只设计可见状态差之间的运动路径 | 首帧、尾帧、中间过渡三者一致 |
| `FLASH-TM-05` | 参考视频 prompt 照搬具体镜头或美术 | 参考污染 | 写 `do_not_copy`，只迁移节奏、运动原则、光影策略 | prompt 不含参考片独特表达 |
| `FLASH-TM-06` | 输出堆砌“电影感、高级感、氛围感” | 美学具体性不足 | 回 `F4/F8`，改成色温、材质、主光、空间、机位和空气介质 | 空泛词可删不影响 prompt |
| `FLASH-TM-07` | 默认 11.5 秒但镜头段时长不相加 | 量化门缺失 | 回 `F6` 重算镜头段 | 总时长等于目标时长 |
| `FLASH-TM-08` | 来源含台词/对白/旁白，但最终 prompt 遗漏、意译、改成字幕或新增未授权台词 | 台词输入没有进入字段真源 | 回 `F1/F3/F6/F9` 建 `dialogue_manifest`、`dialogue_policy`、`dialogue_timing_map`，逐字保留 `hard_frozen` 台词 | 输出有台词策略，冻结台词原文一致且有时码/交付方式 |

## Repair Playbook

1. 先确认是否仍是 `chat_only`。一旦用户要求保存文件、阶段推进或调用 provider，转路由，不在 `flash` 内伪执行。
2. 文本源任务优先建立 `mini_screenplay_profile`：人物、目标、阻力、动作链、声画承托、尾钩。
3. 图生视频任务先写 `image_evidence_table`：主体、空间、构图、光影、材质、色调、可动元素、不可改元素。
4. 首尾帧任务先锁首帧状态和尾帧状态，再补中间运动；不要凭空加入第三个关键状态。
5. 参考视频任务先写可迁移原则和禁止照搬清单，再生成新 prompt。
6. 台词任务先抽取 speaker、line、source anchor、freeze level 和 delivery type；用户明确给出的引号、角色冒号发言或“必须说/原样保留”默认 `hard_frozen`，不得静默改写。
7. 台词过长时，不要擅自删句；优先标注 timing risk，并在 prompt 中建议放宽时长、转旁白/画外音或等待用户确认压缩边界。
8. Prompt 最终应更像 production note，而不是诗性散文；每个形容词最好能落到画面、动作、镜头、光影或模型约束。
9. 若用户指定模型，保留模型术语；若模型未知，输出通用 prompt，不编造 provider 参数。

## Reusable Heuristics

- `flash` 的价值是把当前 2-8 活跃链压成一个短片段 prompt，并在聊天内锁定 mini subject map，而不是把短片段恢复成完整项目流水线；archived `5-表演 / 6-氛围 / 9-光影` 只作显式 legacy 辅助，不进默认链。
- 默认 11.5 秒适合 2-3 个镜头段：开场锁定、动作推进、尾钩/状态变化。复杂动作最多 4 段。
- 图生视频 prompt 的第一优先级是“保持参照图稳定”，第二优先级才是运动丰富。
- 首尾帧生视频最容易失败在中间过渡太大；优先设计连续小动作、视线、手势、光影变化和镜头缓慢移动。
- 参考视频只学“原则”：节奏、调度、焦点策略、运动曲线、光影关系。不要学“具体表达”：镜头顺序、构图复刻、人物造型、台词、Logo、独特道具。
- 负面约束不应无限堆叠；优先写会破坏短视频的关键风险：身份漂移、肢体变形、画面跳切、镜头抖动、光影闪烁、文本水印、过度变焦。
- 台词不是普通氛围词。只要用户提供了明确台词，就先当作输入真源处理；视频模型不支持音频时，也要把台词保留为导演/旁白意图，并明确不生成字幕或屏幕文字。
