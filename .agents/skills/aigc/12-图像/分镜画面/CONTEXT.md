# Context: aigc 12-图像 / 分镜画面

本文件是 `分镜画面` 的经验层知识库，不是执行日志。调用同目录 `SKILL.md` 时必须同时加载本文件。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 24000
hard_limit_chars: 48000
status: ok
last_checked_at: 2026-06-04
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 只用了单镜片段，没有完整组稿 | group source layer | 回到 `10-分组` 目标 `## x-y-z`，把完整组块作为 `group_full_content` | `G1-GROUP-SOURCE` 阻断摘要替代完整源 | prompt/report 能定位完整组稿来源 |
| 把连接件生成了图片 | connector boundary layer | 从 group index 和 plan 中删除 `## x-y-z~x-y-z` 任务 | 连接件只进 `skipped_connectors[]` | plan 中连接件任务数为 0 |
| `shot_id` 数量和组内 `分镜N` 不一致 | shot point mapping layer | 重新统计普通 `分镜N` 并生成 `x-y-z-N` | `shot_count == prompt sections == plan.n == returned_count` | report 中四项计数一致 |
| 多图任务被拆成逐镜任务 | handoff topology layer | 合并为每组一个 `multi_image_task` | plan schema 固定 `task_id=<group_id>.multi_image` | 同一 group 只有一个 task |
| 未指定比例却生成竖图或方图 | aspect ratio layer | 恢复 `aspect_ratio=16:9` 并同步 prompt、plan 和 report | `aspect_ratio_override` 只能来自用户显式要求 | plan 中未指定时 selected ratio 为 16:9 |
| 生成成故事板拼图或多 panel | prompt prefix layer | 重写 Task Execution Prefix，强调 separate images 和 not collage/grid/panel | review 固化 `G5-PROMPT` 和 `G8-RESULT-MAP` | 返回为多张独立图片 |
| 角色或场景跨多图不一致 | group consistency layer | 补 `Group Consistency Contract`，共享主体参照、服装、场景、光影和空间锚点 | 同组共享 YAML 对应主体图和场景视觉锁 | 多图中的角色/场景身份一致 |
| 主体参照图错绑 | YAML reference binding layer | 回到组底 YAML 和 `11-主体/*/3-生成` 精确匹配；多视图优先 | 禁止泛词、子串和 JSON 伪图绑定 | manifest bound paths 存在且 selected_variant 正确 |
| 本地参照图只写路径未可见化 | visual context layer | 生成前逐张 `view_image` | `reference_input_status` 不得在生成模式停留 `pending_view_image` | plan/result/report 记录 visible status |
| provider 单次多图超上限 | provider cap layer | 报告 blocked 或请求用户授权拆组/重组 | 默认 cap 10，覆盖值必须写入 plan/report | `shot_count <= provider_cap` 或 blocked |
| 返回图片数少于/多于分镜数 | result mapping layer | 不猜测补齐或丢弃；进入 repair | `G8-RESULT-MAP` 阻断 | `expected_count == returned_count` |
| 输出顺序错位 | result persistence layer | 用返回 image_index 按 `shot_id_order` 重建映射 | results 固定 `image_index_to_shot_id` | 每个 `<shot_id>.png` 对应正确 source_shot_label |
| prompt 形式字段齐全但只是锚点替换、批量插入、正则套句或映射投影 | scripted authorship layer | 标记 `FAIL-FRAME-SCRIPTED-PROJECTION`，回到 `N6-PROMPT-PACKAGE` 由 LLM 基于完整组稿和分镜点重写 | review gate 固化 `G5B-AUTHORSHIP` | Image sections 能说明各自 source shot anchor 和本组独有画面状态 |

## Repair Playbook

1. 先判断本轮是 `prompt_only`、`single_group_generate`、`episode_group_generate`、`group_batch_generate`、`repair` 还是 `review_only`。
2. 任何 prompt 问题先检查 `group_full_content` 是否完整进入 prompt 或可审计引用。
3. 任何数量问题先检查 `group-index.json.shot_count`，再对照 prompt Image section 数、plan.n、results returned_count。
4. 四段式 ID 最后一段现在按组内普通 `分镜N` 源顺序映射；不得恢复旧 frame landing 自由拆分逻辑。
5. 三段式 `group_id` 是生成任务单位；四段式 `shot_id` 是返回图片映射单位。
6. 未指定比例时默认 16:9；只有用户明确要求 9:16、1:1 或其他比例时才写 `aspect_ratio_override`。
7. 生成模式下本地参照图必须先 `view_image`；`prompt_only` 可记录 `pending_view_image`。
8. 对同一组多图，优先通过共享角色/场景/道具参照和 `Group Consistency Contract` 保持一致，而不是靠逐镜串行回看上一张图。
9. 若生成结果是一张拼图，即使视觉上包含所有分镜，也必须判定失败并重写非拼图前缀。
10. 若组内分镜数超过 provider cap，不要自动拆成多个任务；先报告阻断或取得用户明确授权。
11. 执行报告必须记录 Reference Execution Matrix、Rule Evidence Map、N/A Justification 和 Repair Log；报告缺证据不能判 `pass`。
12. prompt 字数、Image section 数、主体名和 `shot_id` 齐全不等于主创合格；若每节只是固定句式替换角色/场景/道具锚点或批量同义改写，直接返工。

## Reusable Heuristics

- 这条技能的注意力锚点是“一个分镜组一次多图”，不是“一个分镜一任务”。
- 完整组稿比单个分镜点更重要，因为组内对白、音效、画面风格、YAML 和前后分镜共同约束多图一致性。
- 任务执行词前缀要足够硬：`separate images`、`exactly N`、`not storyboard sheet`、`not collage`、`not grid`、`not multi-panel`、`not variants` 都应出现。
- `n` 是审计字段，不是建议字段。它必须等于组内普通 `分镜N` 的数量。
- 默认画面比例为 16:9；用户显式要求时才切换到 9:16 或其他比例。
- 同组多图保持一致的关键不是复用上一张生成图，而是让所有图片在同一 GPT-IMAGE-2 调用中共享参照图、组级空间模型和风格锁。
- YAML 主体图绑定要比文字主体名更保守；缺图时记录 missing 通常比错绑更安全。
- 场景参照图在本技能中同时承担 `scene_reference` 和 `scene_visual_style_reference`，用于锁定空间、材质、光影、色调和氛围。
- 输出检查必须同时看“数量”和“形态”：数量对但生成拼图仍失败；形态对但数量不对也失败。
- 对用户只给四段式 `shot_id` 的请求，默认回到该 `shot_id` 所在 `group_id`，因为 GPT-IMAGE-2 多图一致性任务单位是组。
- 脚本适合数分镜、整理已定 plan 字段、检查文件和映射结果。
- 脚本不适合生成多图 prompt 正文、一致性策略、批量插入、正则套句或映射投影。看到模板味很重的 prompt 时，优先怀疑主创边界被脚本越权。
