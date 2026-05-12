# Review Contract

本 review gate 只裁决 `A-分镜画面参照` 的结构、三步 handoff、LibTV 队列与输出路径，不改写业务主真源。

## Review Dimensions

| dimension | pass condition | fail route |
| --- | --- | --- |
| structure_compliance | Skill 2.0 必需目录、根文件、`agents/openai.yaml` 与 output template 齐备 | 修结构 |
| group_source | 每个目标组可从 `4-分组/第N集.md` 唯一回指，组正文完整 | `references/group-shot-source-contract.md` |
| shot_id_mapping | 每个四段式 `分镜ID` 可回指源组和组内 `分镜N` 或已有 ID | `references/group-shot-source-contract.md` |
| prompt_authorship | prompt 主体直接使用现有分镜组内容，LLM 只做保真指令化组织 | `SKILL.md#LLM-First Creative Authorship Contract` |
| reference_binding | 参照图路径真实、位于 `6-图像/A-分镜画面`；无图移除空槽位；多候选阻断 | `references/frame-image-binding-contract.md` |
| libtv_handoff | YAML 可投影为合法提交；远端 handoff 有图默认 `modeType=image2video` 且 `imageList` <= 9，显式首尾帧才允许 `frames2video`，无图 `text2video`；提交文本不预设 `参照图N`，生成 prompt 保留 final fenced YAML `分镜画面参照[].reference_index / uploaded_url / image_token` 与真实图片 token/编号/URL 绑定 | `references/libtv-handoff-contract.md` |
| reference_slot_order | `frame_uploads` 只记录 `shot_id/source_label -> uploaded_url` 身份映射；`generation_slots` 记录 `图N/imageList[n-1] -> uploaded_url -> shot_id/source_label`；YAML `reference_index` 必须来自最终 `generation_slots`，不得来自 OSS 上传顺序；若 UI 缩略图可观测，以 UI 图N / `Image N` 为准 | `references/libtv-handoff-contract.md` |
| reference_prompt_integrity | draft prompt 允许保持未绑定 YAML，但不得伪造空 `reference_index / uploaded_url`；final 与远端 `libtv-submission.txt` 使用 source-first YAML，只在 `【分镜组源文本】` fenced YAML 内列进入 `imageList` 的分镜ID/镜头标签 + `reference_index / uploaded_url / image_token`；不得另起 `【分镜画面参照说明】`；缺图、未入预算、被排除或空槽说明不得进入远端提交 | `references/libtv-handoff-contract.md` |
| audio_preflight | 远端提交文本必须声明 `enableSound=on`；若 CLI 路径无法在生成前验证 `create_generation_task.params.enableSound`，记录 `audio_preflight_unverified_non_blocking`，不得仅因此阻断官方 `$libTV` 提交 | `references/libtv-handoff-contract.md` |
| audio_acceptance | 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含 audio stream | `references/libtv-handoff-contract.md` |
| duration_handoff | `duration_estimate_seconds` 可回指 `4-分组` 当前组，`duration_hint=clamp(duration_estimate_seconds, 4, 15)`，远端提交中的 `duration` 与 plan 一致 | `references/group-shot-source-contract.md` / `references/libtv-handoff-contract.md` |
| prompt_fidelity | 默认 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false`；未 opt-in 时远端不得优化、摘要、重新编排或补镜头 | `references/libtv-handoff-contract.md` |
| queue_tracking | 多任务均有 queue row、sessionId 或明确失败原因、next_action | `.agents/skills/cli/libTV/SKILL.md` |
| concurrency | 并发只写临时结果，最终 report / results 单线程汇流 | `steps/frame-reference-video-workflow.md` |
| route_clarity | 当前 mode、skipped stages、rework entry 与 next entry 清楚 | `types/type-map.md` |

## Verdict Model

- `pass`：结构与语义 gate 均通过。
- `pass_with_todo`：存在非阻断 TODO，例如部分任务仍在 LibTV 远端排队，或部分镜头缺图但组级生成仍可执行。
- `blocked`：缺少必需文件、LLM 主创被脚本替代、引用或 LibTV handoff 存在硬失败。

## Local Review Checklist

1. 运行 `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/7-视频/A-分镜画面参照`。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁与输出合同。
3. 检查 step1 是否以 `4-分组` 为主信息来源，并直接保留组正文。
4. 检查 step1 是否把组内分镜稳定映射到四段式 `分镜ID`。
5. 检查 step2 是否只按 `shot_id` 绑定真实分镜画面图；无图是否移除空槽位。
6. 检查 prompt / YAML 是否在 final fenced YAML `分镜画面参照` 中体现对应 `分镜ID / 镜头标签 / reference_index / uploaded_url / image_token`，并正确投影到 LibTV `imageList`。
7. 检查 step3 是否在有图时默认锁 `modeType=image2video` 和 `imageList`，且 `imageList` 单组不超过 9；超限时是否记录 `excluded_due_to_budget` 或阻断；显式首尾帧才允许 `frames2video`，无图时锁 `text2video`。
7a. 检查 `frame_uploads` 与 `generation_slots` 是否分层：上传层只绑定分镜ID和 OSS URL，最终 `reference_index` 必须等于 UI 图N或实际 `imageList` 槽位顺序。
8. 检查 `duration_hint` 是否等于 `clamp(duration_estimate_seconds, 4, 15)`，且远端 `duration` 与计划一致；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。
9. 检查远端 `*-libtv-submission.txt` 是否只在 final `【分镜组源文本】` fenced YAML 的 `分镜画面参照[]` 写入分镜ID/镜头标签 + `reference_index / uploaded_url / image_token`，不预设 `参照图1/2/N` 人工编号。
10. 检查远端 `*-libtv-submission.txt` 的 `【直接生成请求】` 是否使用 final source-first YAML 形态的 `【分镜组源文本】` 作为生成 prompt 完整体；不得另起 `【分镜画面参照说明】`，不得出现裸图片 token 丢失分镜ID/镜头标签绑定。
11. 检查远端 `*-libtv-submission.txt` 是否未包含缺图、未入预算、被排除或空槽说明；只在 YAML 中列进入 `imageList` 的分镜ID/镜头标签 + uploaded URL。
12. 检查远端 `*-libtv-submission.txt` 是否声明 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 和禁止优化/重排/摘要/改写/补镜头约束；除非 submit plan 记录用户 opt-in，否则 query 中不得出现远端自行生成的优化版提示词、镜头计划或摘要分镜。
13. 检查生成前是否要求 `LIBTV_ACCESS_KEY credential check`。
14. 检查提交文本是否声明 `enableSound=on`；若生成前无法验证 `create_generation_task.params.enableSound`，是否记录 `audio_preflight_unverified_non_blocking`；生成后或下载后是否通过音频证据 / `ffprobe`。
15. 检查批量并发是否有 queue ledger、sessionId、next_action 和单线程汇流。
16. 检查输出路径是否全部位于 `projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/`。
