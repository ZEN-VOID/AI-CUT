# Context: aigc 7-视频 / A-分镜画面参照

本文件是 `A-分镜画面参照` 的经验层知识库，不是执行流水账。调用同目录 `SKILL.md` 时必须同时加载本文件。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-target-scoped-updates
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `TM-FVID-SHOT-ID` | `4-分组` 镜级映射层 | 回到 `## x-y-z` 与组内 `分镜N`，重建四段式 `x-y-z-N`；若已有 `分镜ID`，以已有 ID 为准 | 在 shot index 中同时保存 source group、source label 和 canonical shot_id | `第N集-group-shot-index.json` 可双向回指 |
| `TM-FVID-PROMPT-REWRITE` | prompt 作者层 | 恢复完整分镜组正文，只保留最小 LibTV 指令前缀和参照映射说明 | 把“现有组内容作为主体”固定为 review gate | prompt 中能找到完整组正文主体 |
| `TM-FVID-EMPTY-SLOT` | 参照绑定层 | 删除缺图镜头的 `reference_images` 空槽位，只在 manifest 记 `missing_optional` | YAML schema 禁止空 path、空 marker 和伪路径 | LibTV submit plan没有空 `upload_file.py` |
| `TM-FVID-IMAGE-AMBIGUOUS` | 文件匹配层 | 阻断当前组或镜，输出候选列表等待人工裁决 | 按 `images/<shot_id>.*` 优先级和同级唯一性匹配 | 同一 `shot_id` 不存在多个同优先级候选 |
| `TM-FVID-MULTIMODAL-LIMIT` | provider 能力层 | 对超过 LibTV 可承受参照数量的多图任务标记 `reference_over_limit`，按用户策略阻断、分段或降级 | 提交前读取 `.agents/skills/cli/libTV` 当前可承受参照数量 | batch YAML 记录 selected / omitted / blocked |
| `TM-FVID-MODETYPE` | provider 路由层 | 默认锁定 `modeType=image2video`；只有用户显式首尾帧/起止帧过渡且图数 1-2 时才用 `frames2video`；无图用 `text2video` | `libtv-handoff-contract.md` 固定 A 专属 modeType 判定 | 远端提交首段出现正确 `modeType` |
| `TM-FVID-QUEUE-DRIFT` | 异步队列层 | 用 `query_session` /  校正 queue ledger 的状态和 next_action | 每次提交后立即写 queue row，汇流阶段统一写 results | 每个 submitted job 有 sessionId 或失败原因 |
| `TM-FVID-REMOTE-STORYBOARD-DRIFT` | LibTV 远端 handoff 口径层 | 回刷 `*-libtv-submission.txt`，首段加入 A 专属 `【LibTV 调用锁定】` 和 `modeType=image2video` | `references/libtv-handoff-contract.md` 固定 Remote Handoff Contract | 远端提交首段出现正确 `modeType`，且本地路径关键词扫描无命中 |

## Repair Playbook

1. 先确认 mode：`prompt_only`、单组、整集、多组、多镜、查询、修复还是审查。
2. 若 ID 对不上，先只修 `group-shot-index`，不要顺手改写 `4-分组` 正文。
3. 若 prompt 被摘要或扩写，恢复完整组正文，再重建 LibTV 前缀和 `@图N` 映射。
4. 若图片不存在，移除该镜的图片槽位，不写空 path；缺图默认不阻断组级 text-only 或剩余多图任务。
5. 若一个 `shot_id` 命中多个同优先级图片，阻断该组并报告候选，不随机选择。
6. 若多图超过 $libTV skill scripts 当前限制，不静默丢弃图片；必须在 manifest 和 report 中记录处理策略。
7. 提交前固定执行 `LIBTV_ACCESS_KEY credential check`；失败时停止提交并转 LibTV 登录/环境修复。
8. 并发 worker 只写临时结果，最终 queue、results 和 report 由主流程单线程汇流。
9. 若远端代理把 A 任务改成 `singleImage2video`、默认 `frames2video`、新生成分镜图或合成流程，先修 `*-libtv-submission.txt` 的 `modeType` 调用锁，再重新提交，不要改写 `4-分组` 或补跑 `6-图像`。

## Reusable Heuristics

- `A-分镜画面参照` 的核心对象是“组级视频 job + 镜级图片引用”，不是单镜视频 job。
- 四段式 `分镜ID` 是参照绑定锚点；三段式 `group_id` 是视频输出命名和队列锚点。
- `分镜ID@路径` 是本技能的中间人类可读映射；$libTV skill scripts 实际提交仍应投影为 uploaded reference URLs 和 prompt 内的 `@图N -> shot_id@path`。
- 缺图不等于失败；错绑、猜图和空槽位才是失败。
- 多张分镜画面更适合 `libtv_session_with_uploaded_references`；没有任何图片时再走 `libtv_session_text_only`。
- `frames2video` 是首尾帧/起止帧过渡路线，不应默认替代本技能的多图分镜画面参照；A 默认用 `image2video` 承载按 shot 顺序排列的多张分镜画面图。
- LibTV 远端只需要 uploaded URL 和直接视频任务指令；本地 `projects/...` 路径留在 manifest / 审核 prompt，不能进入 `*-libtv-submission.txt`。
