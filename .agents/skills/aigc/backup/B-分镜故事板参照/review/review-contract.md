# Review Contract

本 review gate 只裁决 `B-分镜故事板参照` 的结构、三步 handoff、LibTV 队列与输出路径，不改写业务主真源。

## Review Dimensions

| dimension | pass condition | fail route |
| --- | --- | --- |
| structure_compliance | Skill 2.0 必需目录、根文件、`agents/openai.yaml` 与 output template 齐备 | 修结构 |
| group_source | 每个目标组可从 `4-分组/第N集.md` 唯一回指，组正文完整 | `references/group-source-contract.md` |
| prompt_authorship | prompt 主体直接使用现有分镜组内容，LLM 只做保真指令化组织 | `SKILL.md#LLM-First Creative Authorship Contract` |
| reference_binding | 参照图路径真实、位于 `6-图像/B-分镜故事板`；无图为空引用；多候选阻断 | `references/storyboard-image-binding-contract.md` |
| libtv_handoff | YAML 可投影为合法提交；远端 handoff 有故事板图时锁 `modeType=singleImage2video` 和单张 `imageList[0]`，无图时锁 `text2video`；提交文本不预设 `参照图N`，生成 prompt 保留 final fenced YAML `故事板参照.reference_index / uploaded_url / image_token` 与真实图片 token/编号/URL 绑定 | `references/libtv-handoff-contract.md` |
| reference_slot_order | `storyboard_uploads` 只记录 `group_id/storyboard_sheet -> uploaded_url` 身份映射；`generation_slots` 记录 `图1/imageList[0] -> uploaded_url -> 故事板总参照`；YAML `reference_index` 必须来自最终 `generation_slots`，不得来自 OSS 上传动作；若 UI 缩略图可观测，以 UI 图1 / `Image 1` 为准 | `references/libtv-handoff-contract.md` |
| reference_prompt_integrity | draft prompt 允许保持未绑定 YAML，但不得伪造空 `reference_index / uploaded_url`；final 与远端 `libtv-submission.txt` 使用 source-first YAML，只在 `【分镜组源文本】` fenced YAML 内列进入 `imageList[0]` 的故事板总参照 + `reference_index / uploaded_url / image_token`；不得另起 `【故事板参照说明】`；缺故事板、多候选未裁决、被排除或空槽说明不得进入远端提交 | `references/libtv-handoff-contract.md` |
| audio_preflight | 远端提交文本必须声明 `enableSound=on`；若 CLI 路径无法在生成前验证 `create_generation_task.params.enableSound`，记录 `audio_preflight_unverified_non_blocking`，不得仅因此阻断官方 `$libTV` 提交 | `references/libtv-handoff-contract.md` |
| audio_acceptance | 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含 audio stream | `references/libtv-handoff-contract.md` |
| duration_handoff | `duration_estimate_seconds` 可回指 `4-分组` 当前组，`duration_hint=clamp(duration_estimate_seconds, 4, 15)`，远端提交中的 `duration` 与 plan 一致 | `references/group-source-contract.md` / `references/libtv-handoff-contract.md` |
| prompt_fidelity | 默认 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false`；未 opt-in 时远端不得优化、摘要、重新编排或补镜头 | `references/libtv-handoff-contract.md` |
| queue_tracking | 多任务均有 queue row、sessionId 或明确失败原因、next_action | `.agents/skills/cli/libTV/SKILL.md` |
| concurrency | 并发只写临时结果，最终 report / results 单线程汇流 | `steps/storyboard-video-workflow.md` |
| route_clarity | 当前 mode、skipped stages、rework entry 与 next entry 清楚 | `types/type-map.md` |

## Verdict Model

- `pass`：结构与语义 gate 均通过。
- `pass_with_todo`：存在非阻断 TODO，例如部分任务仍在 LibTV 远端排队。
- `blocked`：缺少必需文件、LLM 主创被脚本替代、引用或 LibTV handoff 存在硬失败。

## Local Review Checklist

1. 运行 `validate_skill_2_0.py`。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁与输出合同。
3. 检查 step1 是否以 `4-分组` 为主信息来源，并直接保留组正文。
4. 检查 step2 是否只按 `group_id` 绑定真实故事板图；无图是否为空引用。
5. 检查 step3 是否在有故事板图时锁 `modeType=singleImage2video` 和单张 `imageList[0]`，且 `imageList` <= 9；无图时锁 `text2video`。
5a. 检查 `storyboard_uploads` 与 `generation_slots` 是否分层：上传层只绑定故事板和 OSS URL，最终 `reference_index=1` 必须对应 UI 图1或实际 `imageList[0]`。
6. 检查 `duration_hint` 是否等于 `clamp(duration_estimate_seconds, 4, 15)`，且远端 `duration` 与计划一致；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。
7. 检查远端 `*-libtv-submission.txt` 是否只在 final `【分镜组源文本】` fenced YAML 的 `故事板参照` 写入故事板总参照 + `reference_index / uploaded_url / image_token`，不预设 `参照图1/2/N` 人工编号。
8. 检查远端 `*-libtv-submission.txt` 的 `【直接生成请求】` 是否使用 final source-first YAML 形态的 `【分镜组源文本】` 作为生成 prompt 完整体；不得另起 `【故事板参照说明】`，不得出现裸图片 token 丢失故事板总参照身份。
9. 检查远端 `*-libtv-submission.txt` 是否未包含缺故事板、多候选未裁决、被排除或空槽说明；只在 YAML 中列进入 `imageList[0]` 的故事板总参照 + uploaded URL。
10. 检查远端 `*-libtv-submission.txt` 是否声明 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 和禁止优化/重排/摘要/改写/补镜头约束；除非 submit plan 记录用户 opt-in，否则 query 中不得出现远端自行生成的优化版提示词、镜头计划或摘要分镜。
11. 检查生成前是否要求 `LIBTV_ACCESS_KEY credential check`。
12. 检查提交文本是否声明 `enableSound=on`；若生成前无法验证 `create_generation_task.params.enableSound`，是否记录 `audio_preflight_unverified_non_blocking`；生成后或下载后是否通过音频证据 / `ffprobe`。
13. 检查批量并发是否有 queue ledger、sessionId、next_action 和单线程汇流。
14. 检查输出路径是否全部位于 `projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/`。
