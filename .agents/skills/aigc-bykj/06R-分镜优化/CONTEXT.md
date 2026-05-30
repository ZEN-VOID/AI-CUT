# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/06R-分镜优化` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 14000
- hard_limit_chars: 28000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 06R 被当成重新分镜 | 阶段边界层 | 回到 `06` 源稿锁定，只做 patch 或优化版 JSON | `Source Continuity Contract` 固定 06R 只承接 06 输出 | manifest 回指 `06-智能分镜` |
| 用户自然语言被直接写成 prompt | 意图解析层 | 先补 `storyboard_intent_map`，再改字段 | `N2A-INTENT-PARSE` 固定为前置节点 | 每条反馈有 target object、field、risk |
| group 规则被简化 | 原 6-分组同步层 | 补回场景标题、定场、构图、六分区、画面属性、三项风格、正文、统计和计数边界 | `PASS-06R-07` 阻断规则降级 | `group_rule_sync_check` pass |
| bridge 字段被压缩 | 原连接件同步层 | 补完整连接件字段、禁止字段和计数边界 | `PASS-06R-08` 阻断连接件简化 | `bridge_rule_sync_check` pass |
| frame 镜头像复述剧情 | 摄影决策层 | 补 `shot_function`、camera、lighting、attention、handoff 与非复述检查 | `PASS-06R-06` 固定 frame 摄影门 | 删除源句事实后仍能读出摄影选择 |
| group 时长越修越乱 | 分组边界层 | 回到 frame duration 和 atomic unit，不按字数/情绪切 | 原 `6-分组` 12-18 秒与 18 秒硬上限 | `duration_seconds <= 18` |
| bridge 新增剧情或端点复述 | 连接件边界层 | 只写尾帧到首帧中间过程，删除新剧情/新人物/端点字段 | 原 `bridge-shot-contract` 固定边界 | bridge 无禁用字段 |
| payload 漂移到无证据画面 | AI 稳定层 | 回到 frame 摄影决策和资产/风格证据，删无证据词 | payload 从 `shot_design` 推导 | `generation_payload` 可回指 frame |
| 资产/风格引用漂移 | 上游对齐层 | 回到 `04R/04` 与 `05R/05` 输出，只修引用或 projection | 不在 06R 新造资产/风格 | `asset_style_alignment` pass |
| schema 合法但下游不可消费 | 汇流层 | 重新检查 frame->group->bridge->storyboard 索引关系 | `PASS-06R-10` 固定写回门 | optimized index 全可解析 |

## Repair Playbook

1. 先判断问题属于源稿锁定、自然语言意图、范围授权、frame 摄影、group 规则、bridge 连接、payload、资产风格、schema ID 还是写回。
2. 若源稿缺失，先修 `N1-SOURCE-LOCK`；不要用 `03` 剧本直接生成 `06R`。
3. 若用户只说“优化一下”“更电影感”“更稳”，先做 `storyboard_intent_map` 和澄清门；不要直接大改所有 frames。
4. 若 frame 太平，先补镜头叙事功能、观看位置、注意力路径和光线结果；不要只加“电影感/高级感”。
5. 若 group 出问题，优先对齐原 `6-分组` 规则：场景标题、定场、构图六分区、画面属性、三项风格、正文、统计、计数边界。
6. 若 bridge 出问题，先确认相邻 group 的尾帧/首帧，再写过程；不要复述端点。
7. 若组时长超限，移动完整 atomic unit 或修 frame 时值；不要删字段绕过统计。
8. 若 prompt 不稳，先修 camera-first、方向参照、光线结果和可见微动态，再调英文词。
9. 若资产或风格不一致，回上游 JSON 对齐引用，不在 06R 发明新主体。
10. 输出要给下游直接使用时，优先同时提供 patch 和 full optimized JSON；只审查任务只输出报告。

## Reusable Heuristics

- `06R` 的价值不是重新生成更漂亮的分镜，而是把用户反馈变成可审查的 storyboard patch。
- frame 修复看“镜头是否新增观看价值”；group 修复看“是否完整同步 6-分组规则”；bridge 修复看“是否从尾帧连续抵达首帧”。
- 用户说“同步 6-分组”时，修的是规则，不是旧输出路径。
- JSON-first 不是简化规则；原 `6-分组` 的 Markdown 字段必须有 JSON 等价承载。
- group 优化最容易误删组头和统计字段；任何“简洁化”都可能破坏下游生产。
- bridge 最容易写成新剧情；连接件只服务首尾帧参照图生视频，不承担剧情推进。
- prompt 修复必须由 `shot_design` 推导；没有摄影证据的英文词越多，越容易让下游漂移。
- Patch-first 能保留可追溯性；full optimized JSON 只在需要直接交付下游时投影生成。
