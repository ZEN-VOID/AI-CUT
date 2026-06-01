# Review Contract

本 review gate 只裁决 `A-分镜画面参照` 的结构、三步 handoff、LibTV 队列与输出路径，不改写业务主真源。

## Review Dimensions

| dimension | pass condition | fail route |
| --- | --- | --- |
| structure_compliance | Skill 2.0 必需目录、根文件、`agents/openai.yaml` 与 output template 齐备 | 修结构 |
| group_source | 每个目标组可从 `5-分组/第N集.md` 唯一回指，组正文完整 | `references/group-shot-source-contract.md` |
| shot_id_mapping | 每个四段式 `分镜ID` 可回指源组和组内 `分镜N` 或已有 ID | `references/group-shot-source-contract.md` |
| prompt_authorship | prompt 主体直接使用现有分镜组内容，LLM 只做保真指令化组织 | `SKILL.md#LLM-First Creative Authorship Contract` |
| reference_binding | 参照图路径真实、位于 `7-图像/A-分镜画面`；无图移除空槽位；多候选阻断 | `references/frame-image-binding-contract.md` |
| libtv_handoff | YAML 可投影为合法提交；远端 handoff 有图默认 `modeType=image2video` 且 `imageList` <= 9，显式首尾帧才允许 `frames2video`，无图 `text2video`；提交文本不预设 `参照图N`，生成 prompt 保留 final fenced YAML `分镜画面参照[].reference_index / uploaded_url / image_token` 与真实图片 token/编号/URL 绑定 | `references/libtv-handoff-contract.md` |
| reference_slot_order | `frame_uploads` 只记录 `shot_id/source_label -> uploaded_url` 身份映射；`generation_slots` 记录 `图N/imageList[n-1] -> uploaded_url -> shot_id/source_label`；YAML `reference_index` 必须来自最终 `generation_slots`，不得来自 OSS 上传顺序；若 UI 缩略图可观测，以 UI 图N / `Image N` 为准 | `references/libtv-handoff-contract.md` |
| reference_prompt_integrity | draft prompt 允许保持未绑定 YAML，但不得伪造空 `reference_index / uploaded_url`；final 与远端 `libtv-submission.txt` 使用 source-first YAML，只在 `【分镜组源文本】` fenced YAML 内列进入 `imageList` 的分镜ID/镜头标签 + `reference_index / uploaded_url / image_token`；不得另起 `【分镜画面参照说明】`；缺图、未入预算、被排除或空槽说明不得进入远端提交 | `references/libtv-handoff-contract.md` |
| audio_preflight | 远端提交文本必须声明 `enableSound=on`；若 CLI 路径无法在生成前验证 `create_generation_task.params.enableSound`，记录 `audio_preflight_unverified_non_blocking`，不得仅因此阻断官方 `$libTV` 提交 | `references/libtv-handoff-contract.md` |
| audio_acceptance | 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含 audio stream | `references/libtv-handoff-contract.md` |
| duration_handoff | `duration_estimate_seconds` 可回指 `5-分组` 当前组，`duration_hint=clamp(duration_estimate_seconds, 4, 15)`，远端提交中的 `duration` 与 plan 一致 | `references/group-shot-source-contract.md` / `references/libtv-handoff-contract.md` |
| prompt_fidelity | 默认 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false`；未 opt-in 时远端不得优化、摘要、重新编排或补镜头 | `references/libtv-handoff-contract.md` |
| queue_tracking | 多任务均有 queue row、sessionId 或明确失败原因、next_action | `.agents/skills/cli/libTV/SKILL.md` |
| concurrency | 并发只写临时结果，最终 report / results 单线程汇流 | `steps/frame-reference-video-workflow.md` |
| route_clarity | 当前 mode、skipped stages、rework entry 与 next entry 清楚 | `types/type-map.md` |

## Review Gates

| gate_id | owner dimension | pass condition | fail code | rework target | report evidence |
| --- | --- | --- | --- | --- | --- |
| `GATE-FVID-GROUP-01` | `group_source` | 目标 `source_file` 固定来自 `projects/aigc/<项目名>/5-分组/第N集.md`，项目 `MEMORY.md` 与 `CONTEXT/` 只作辅助上下文，不覆盖组正文 | `FAIL-FVID-INPUT` | `N3-GROUP-INDEX` | input manifest 中的 `source_file`、episode、target groups、context usage note |
| `GATE-FVID-GROUP-02` | `group_source` | 普通组只识别 `## x-y-z`；连接件 `## x-y-z~x-y-z` 不进入 `group_content`、prompt、manifest、batch 或命名 | `FAIL-FVID-GROUP-BOUNDARY` | `N3-GROUP-INDEX` | group index 的 heading、line range/hash、ignored connector list |
| `GATE-FVID-GROUP-03` | `group_source` | `group_content` 完整保留现有组正文，不能用底部 YAML、摘要或压缩版替代 | `FAIL-FVID-PROMPT` | `N3-GROUP-INDEX` | prompt package 中的原始 `## group_id` 正文、`source_body_hash` |
| `GATE-FVID-SHOT-01` | `shot_id_mapping` | 组内 `分镜N` / 已有四段式 `分镜ID` 可稳定映射为唯一 `shot_id`，四段式输入可回推所属 `group_id` | `FAIL-FVID-SHOT-ID` | `N4-SHOT-ID` | `group-shot-index.json` 中的 `shot_id`、`source_label`、`group_id` |
| `GATE-FVID-DURATION-01` | `duration_handoff` | `duration_estimate_seconds` 按组底 `时长估算`、组内秒数求和、明确 fallback 的优先级生成，连接件时长不参与 | `FAIL-FVID-DURATION` | `N3-GROUP-INDEX` | `duration_source`、原文时长证据、`duration_estimate_seconds` |
| `GATE-FVID-PROMPT-01` | `prompt_authorship` | prompt 主体不得改写剧情事实、对白事实、镜头顺序、角色关系、场景结果或组边界；默认不压缩 | `FAIL-FVID-PROMPT` | `N6-YAML` | prompt package 的 source-first 正文、compression opt-in 记录 |
| `GATE-FVID-PROMPT-02` | `reference_prompt_integrity` | 有图镜头只在 final fenced YAML 的 `分镜画面参照[]` 写入真实槽位绑定；draft 不伪造 URL，远端不使用 `shot_id@path`、`@图N` 或另起参照说明段 | `FAIL-FVID-PROMPT` | `N6-YAML` | draft/final YAML diff、`*-libtv-submission.txt` 截要、slot ledger |
| `GATE-FVID-REF-01` | `reference_binding` | 图片候选根只来自当前项目 `7-图像/A-分镜画面/第N集/` 与其 `images/` 子目录，路径真实且位于项目根内 | `FAIL-FVID-REF` | `N5-REF-BIND` | reference manifest 的 search roots、resolved paths、existence check |
| `GATE-FVID-REF-02` | `reference_binding` | 默认只用四段式 `shot_id` 匹配图片，优先 `images/<shot_id>.<ext>`，其次同集目录 `<shot_id>.<ext>`；不按角色、场景或语义猜图 | `FAIL-FVID-REF` | `N5-REF-BIND` | candidate list、match priority、selected candidate reason |
| `GATE-FVID-REF-03` | `reference_binding` | 唯一命中时写入 manifest 与 `reference_images`；缺图只写 `missing_optional` 并移除空槽位；同优先级多候选阻断 | `FAIL-FVID-REF` | `N5-REF-BIND` | reference manifest 的 `found / missing_optional / ambiguous` 状态 |
| `GATE-FVID-REF-04` | `reference_slot_order` | 本地 `marker` 只服务 review；最终 `reference_index` 必须来自进入 `imageList` 的 1-based 槽位顺序，不得把本地 marker 当远端人工 `参照图N` | `FAIL-FVID-SLOT-ORDER` | `N8-DISPATCH` | `generation_slots`、`imageList`、final YAML `reference_index` 对照 |
| `GATE-FVID-REF-05` | `libtv_handoff` | 单组真实 `imageList` 不超过 9 张；超限时有预算裁决、`excluded_due_to_budget` 或阻断，不静默丢图或超量提交 | `FAIL-FVID-REFERENCE-BUDGET` | `N5-REF-BIND` | selected / excluded shot list、budget rationale、blocked reason |
| `GATE-FVID-REF-06` | `prompt_authorship` | 分镜画面参照只作为视觉参照，不反向改写 `5-分组` 的剧情、镜头事实或组正文 | `FAIL-FVID-PROMPT` | `N6-YAML` | prompt package 与 group source hash 对照、reference usage note |
| `GATE-FVID-LIBTV-01` | `libtv_handoff` | 当前组至少一张图时走 uploaded references；无图时走 text-only；两种路线都不得保留空图片槽位 | `FAIL-FVID-LIBTV` | `N6-YAML` | batch YAML 的 command type、reference count、empty slot scan |
| `GATE-FVID-LIBTV-02` | `libtv_handoff` | 生成前加载 `.agents/skills/cli/libTV/SKILL.md`，调用官方 `$libTV` 技能和脚本，不绕过为私有 OpenAPI 或手写提交器 | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | submit plan 中的 `$libTV` skill load note、script command list、private API scan |
| `GATE-FVID-LIBTV-03` | `libtv_handoff` | 执行前完成 `LIBTV_ACCESS_KEY` credential check，且 key 不写入 prompt、batch、queue、模板或报告 | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | credential check status、redacted env note、secret scan summary |
| `GATE-FVID-LIBTV-04` | `libtv_handoff` | 新任务先锁定 `projectUuid/projectUrl` 或使用用户显式 existing 画布；submit plan、queue、report 与 `create_session.py` 返回值一致 | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | `projectUuid/projectUrl` lock record、create_session response、queue/report projection |
| `GATE-FVID-LIBTV-05` | `reference_slot_order` | 每个 uploaded URL 的 `/claw/<projectUuid>/` 与锁定画布一致；上传结果只进 `frame_uploads` 身份映射，不直接当 `reference_index` 顺序 | `FAIL-FVID-SLOT-ORDER` | `N8-DISPATCH` | upload ledger、project scope check、`frame_uploads` / `generation_slots` 对照 |
| `GATE-FVID-LIBTV-06` | `libtv_handoff` | 官方脚本顺序为 `change_project.py -> upload_file.py -> create_session.py -> query_session.py -> download_results.py`；无参照图只跳过 upload，不跳过画布锁、查询和下载规则 | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | command projection、per-job execution trace、text-only branch note |
| `GATE-FVID-LIBTV-07` | `queue_tracking` | 画布中缺生成节点或结果 URL 时，本地状态不得标为 `generated` / `downloaded`；queue/result/report 保留 `sessionId/projectUuid/projectUrl` | `FAIL-FVID-QUEUE` | `N9-QUEUE` | queue ledger、query response excerpt、remote node/result URL status |
| `GATE-FVID-PROMPT-03` | `prompt_fidelity` | 默认远端 handoff 为 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false`；未 opt-in 时 query 不得出现远端优化、摘要、重排、补镜头或镜头计划 | `FAIL-FVID-PROMPT` | `N6-YAML` | submit plan opt-in field、submission text fidelity block、query prompt audit |
| `GATE-FVID-DURATION-02` | `duration_handoff` | batch 与远端提交中的 `duration` 必须等于当前组 `duration_hint=clamp(duration_estimate_seconds, 4, 15)`，不得全组固定 15 秒 | `FAIL-FVID-DURATION` | `N6-YAML` | group duration evidence、batch `duration_hint`、remote submission duration |
| `GATE-FVID-AUDIO-01` | `audio_preflight` | 远端提交声明 `enableSound=on`；若生成前无法验证工具参数，记录 `audio_preflight_unverified_non_blocking`，不得只因预检不可见阻断官方提交流程 | `FAIL-FVID-AUDIO` | `N8-DISPATCH` | submission audio line、preflight verification status、non-blocking note |
| `GATE-FVID-AUDIO-02` | `audio_acceptance` | 生成后必须有 `task_result.audios`、音频 URL 或下载后 `ffprobe` audio stream 证据；无音轨不得交付 | `FAIL-FVID-AUDIO` | `N10-QUERY-DOWNLOAD` | query audio evidence、ffprobe JSON、`audio_missing / no_audio_stream` status if failed |
| `GATE-FVID-DOWNLOAD-01` | `queue_tracking` | 完成后按 `$libTV` 查询并自动下载到 `8-视频/A-分镜画面参照/第N集/`，文件名精确为 `<group_id>.mp4`，不得把远端成功或半截文件误判为本地交付 | `FAIL-FVID-DOWNLOAD` | `N10-QUERY-DOWNLOAD` | download command、expected video path、file existence/size and retry note |
| `GATE-FVID-REPORT-01` | `route_clarity` | group index、reference manifest、batch/plan 与执行报告都能说明处理范围、跳过/缺图/阻断原因和返工入口 | `FAIL-FVID-REPORT` | `N12-CLOSE` | close report 的 coverage、status summary、rework targets |

## Verdict Model

- `pass`：结构与语义 gate 均通过。
- `pass_with_todo`：存在非阻断 TODO，例如部分任务仍在 LibTV 远端排队，或部分镜头缺图但组级生成仍可执行。
- `blocked`：缺少必需文件、LLM 主创被脚本替代、引用或 LibTV handoff 存在硬失败。

## Local Review Checklist

1. 运行 `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/8-视频-backup/A-分镜画面参照`。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁与输出合同。
3. 检查 step1 是否以 `5-分组` 为主信息来源，并直接保留组正文。
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
16. 检查输出路径是否全部位于 `projects/aigc/<项目名>/8-视频/A-分镜画面参照/第N集/`。
