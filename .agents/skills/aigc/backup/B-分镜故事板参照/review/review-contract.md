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

## Review Gates

| gate_id | gate | fail_code | owner / rework target | required evidence |
| --- | --- | --- | --- | --- |
| `GATE-SBVID-01` | 项目、集号、目标分镜组与 `4-分组/第N集.md` 真源已锁定，辅助上下文不得覆盖组正文 | `FAIL-SBVID-INPUT` | `N1-INTAKE` / `N2-CONTEXT` | input manifest、source file path、target group scope |
| `GATE-SBVID-02` | 每个普通 `## x-y-z` 分镜组唯一可回指，连接件 `## x-y-z~x-y-z` 未进入 group job | `FAIL-SBVID-GROUP` | `N3-GROUP-INDEX` | group index、heading、line range 或 `source_body_hash` |
| `GATE-SBVID-03` | `group_content` 完整保留现有组正文，prompt 主体未摘要、未改写、未重排 | `FAIL-SBVID-PROMPT` | `N3-GROUP-INDEX` / `N5-YAML` | prompt package、source hash、diff 或 excerpt evidence |
| `GATE-SBVID-04` | `duration_estimate_seconds` 可回指组底 YAML、分镜秒数求和或明确 fallback，`duration_hint` 使用 4-15 秒 clamp | `FAIL-SBVID-DURATION` | `N3-GROUP-INDEX` / `N5-YAML` | duration source、estimate、hint、remote duration |
| `GATE-SBVID-05` | 故事板参照只按 `group_id` 从 `6-图像/B-分镜故事板` 真实图片绑定；无图为空引用；多候选阻断 | `FAIL-SBVID-REF` | `N4-REF-BIND` | reference manifest、candidate list、file existence proof |
| `GATE-SBVID-06` | B 路线有图时只提交 1 张故事板总参照到 `imageList[0]` 且不超过 9 张；无图走 `text2video` | `FAIL-SBVID-LIBTV` | `N5-YAML` / `N7-DISPATCH` | batch YAML、submit text、remote params |
| `GATE-SBVID-07` | `storyboard_uploads` 与 `generation_slots` 分层，最终 `reference_index=1` 来自 UI 图1或实际 `imageList[0]` | `FAIL-SBVID-SLOT` | `N7-DISPATCH` | upload ledger、slot ledger、final YAML、remote `imageList[0]` |
| `GATE-SBVID-08` | source-first YAML 两阶段正确：draft 不写空槽位；final 只在 fenced YAML `故事板参照` 写真实绑定 | `FAIL-SBVID-PROMPT` | `N5-YAML` / `N7-DISPATCH` | draft prompt、final prompt、fenced YAML |
| `GATE-SBVID-09` | 远端 `*-libtv-submission.txt` 第一段锁定 `provider=seedance2.0 / taskType=video / modeType`，不得包含本地图片路径、占位 URL 或人工 `参照图N` | `FAIL-SBVID-LIBTV` | `N5-YAML` / `N7-DISPATCH` | submission text、uploaded URL、projectUuid |
| `GATE-SBVID-10` | `【直接生成请求】` 基于完整 `【分镜组源文本】`，保留故事板总参照身份与图片 token/URL 绑定，不退化为裸图片 token | `FAIL-SBVID-PROMPT` | `N5-YAML` / `N7-DISPATCH` | submission text、query prompt echo |
| `GATE-SBVID-11` | 默认 `strict_original + transport_only`，未 opt-in 时禁止远端优化、摘要、重排、改写或补镜头 | `FAIL-SBVID-FIDELITY` | `N5-YAML` / `N6-REVIEW` / `N7-DISPATCH` | submit plan、query transcript、opt-in record |
| `GATE-SBVID-12` | LibTV 官方技能与脚本顺序被遵守，`projectUuid/projectUrl/sessionId` 可追踪，access key 未写入文件 | `FAIL-SBVID-LIBTV` | `N7-DISPATCH` / `N8-QUEUE` | command log、queue ledger、canvas link、sanitized report |
| `GATE-SBVID-13` | `enableSound=on` 已进入提交文本；生成前无法强验证时记录非阻断，生成后必须有音频证据 | `FAIL-SBVID-AUDIO` | `N7-DISPATCH` / `N9-QUERY-DOWNLOAD` | submission text、task_result.audios、ffprobe output |
| `GATE-SBVID-14` | 并发只在 group job 层发生，queue/result/report 由单线程汇流，失败组保留可返工入口 | `FAIL-SBVID-QUEUE` | `N7-DISPATCH` / `N8-QUEUE` / `N11-CLOSE` | tmp result、queue ledger、final report |
| `GATE-SBVID-15` | 输出路径、下载文件名、状态报告均落在本技能项目目录，不能把远端 URL 或短轮询当作已交付视频 | `FAIL-SBVID-REPORT` | `N9-QUERY-DOWNLOAD` / `N10-WRITE` / `N11-CLOSE` | local video path、results JSON、执行报告 |

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
