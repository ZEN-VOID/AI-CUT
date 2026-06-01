# Review Contract: D-主板混合参照

本 review gate 只裁决 `D-主板混合参照` 的组级视频 prompt、混合参照、LibTV 计划、队列和项目持久化，不改写 `5-分组` 主真源。

## Review Checklist

1. 运行 Skill 2.0 结构校验。
2. 检查 `第N集-hybrid-group-index.json` 是否可回指 `5-分组/第N集.md` 的 `## group_id`。
3. 检查 prompt 是否为 source-first YAML：draft 以原 `## group_id` 起笔并保持未绑定 YAML；final 完整保留组正文，只在 fenced YAML 内注入故事板和主体 `reference_index / uploaded_url / image_token`。
4. 检查故事板参照是否来自 `7-图像/B-分镜故事板`，且只作为 `storyboard_total_reference`。
5. 检查主体参照是否只来自组底 YAML 与 `6-设计/*/3-生成` 的真实图片。
6. 检查每个已绑定主体是否在 final fenced YAML 对应 `角色 / 场景 / 道具` 列表项中出现 `name + reference_index + uploaded_url`，不得使用空 URL 或人工 `参照图N`。
7. 检查故事板和主体图片是否从当前本地生成目录 fresh resolve，并记录 `source_sha256 / source_size_bytes / source_mtime_ns`；历史上传缓存只有在 `path + 指纹` 完全匹配时才能复用。
8. 检查缺图主体、缺故事板或图片超限是否只写入 manifest、submit plan 和报告；远端 `libtv-submission.txt` 不得出现缺图/无缓存/未入预算/不创建空图片槽说明；真实进入 `mixedList` 的图片必须 <= 9，超限时必须先排除道具，再排除重复、不必要或可由源文本保留的次要主体。
9. 检查 `duration_hint` 是否等于 `clamp(duration_estimate_seconds, 4, 15)`，且远端 `duration` 与计划一致；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。
10. 检查 LibTV provider 路由：有任一参照图时远端提交必须锁定 `modeType=mixed2video` 和 `mixedList`，无图时锁定 `modeType=text2video`，不得退回 `image2video` 或拆成 B/C 分开提交。
10a. 检查 `asset_uploads` 与 `generation_slots` 是否分层：上传层只绑定故事板/主体身份和 OSS URL，最终 `reference_index` 必须等于 UI 图N或实际 `mixedList` 槽位顺序；不得把 OSS 上传顺序当作图N顺序真源。
11. 检查远端 `*-libtv-submission.txt` 是否只在 final `【分镜组源文本】` fenced YAML 内写入进入 `mixedList` 的故事板身份/主体名 + `reference_index / uploaded_url / image_token`，不预设 `参照图1/2/N` 人工编号。
12. 检查远端 `*-libtv-submission.txt` 的 `【直接生成请求】` 是否使用 final source-first YAML 形态的 `【分镜组源文本】` 作为生成 prompt 完整体；不得另起 `【混合参照说明】`，不得出现裸图片 token 丢失故事板身份或主体名绑定。
13. 检查远端 `*-libtv-submission.txt` 是否声明 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 和禁止优化/重排/摘要/改写/补镜头约束；除非 submit plan 记录用户 opt-in，否则 query 中不得出现远端自行生成的优化版提示词、镜头计划或摘要分镜。
14. 检查提交前是否有 `LIBTV_ACCESS_KEY credential check` 策略；执行生成时是否有 queue ledger 与 sessionId / blocked reason。
15. 检查提交文本是否声明 `enableSound=on`；若生成前无法验证 `create_generation_task.params.enableSound`，是否记录 `audio_preflight_unverified_non_blocking`；生成后或下载后是否通过音频证据 / `ffprobe`。
16. 检查输出路径是否全部位于 `projects/aigc/<项目名>/8-视频/D-主板混合参照/第N集/`。

## Review Gates

| gate_id | review gate | fail code | rework target | evidence |
| --- | --- | --- | --- | --- |
| `GATE-VIDHYB-GROUP-01` | 目标 `group_id` 必须唯一回指 `5-分组/第N集.md` 的普通 `## x-y-z` 标题，连接件 `## x-y-z~x-y-z` 不得作为可生成组 | `FAIL-VIDHYB-GROUP` | `N2-GROUP-EXTRACT` / `references/group-source-extraction.md` | `第N集-hybrid-group-index.json` 中的 source heading、line range、connector exclusion |
| `GATE-VIDHYB-GROUP-02` | 组正文提取必须保留原分镜顺序、动作、音效、场景、YAML 和 body hash，不得摘要、扩写或改写剧情事实 | `FAIL-VIDHYB-GROUP` | `N2-GROUP-EXTRACT` / `references/group-source-extraction.md` | group body snapshot、body hash、source line range |
| `GATE-VIDHYB-GROUP-03` | 组底 fenced YAML 是主体基准；YAML 缺失时不得从正文猜 `角色 / 场景 / 道具`，必须阻断或按用户要求降级 | `FAIL-VIDHYB-GROUP` | `N2-GROUP-EXTRACT` / `N4-SUBJECT-BIND` | YAML parse status、missing_subject_yaml finding、降级或 blocked reason |
| `GATE-VIDHYB-DURATION-01` | 必须从组底 `时长估算` 或分镜明细求和形成 `duration_estimate_seconds`，并在 handoff 层按 `clamp(4,15)` 生成 `duration_hint` | `FAIL-VIDHYB-DURATION` | `N2-GROUP-EXTRACT` / `N6-PLAN-BUILD` | duration_source、duration_estimate_seconds、submit plan duration_hint |
| `GATE-VIDHYB-GROUP-04` | 连接件块不得进入 prompt、故事板/主体 manifest、LibTV job、视频文件命名或分镜组时长估算 | `FAIL-VIDHYB-GROUP` | `N2-GROUP-EXTRACT` / `N6-PLAN-BUILD` | connector skip list、job list、duration calculation notes |
| `GATE-VIDHYB-REF-01` | 故事板总参照必须从当前 `7-图像/B-分镜故事板/第N集` 按 `group_id` 唯一解析；无命中只记录 optional missing，多命中阻断，不得挂到主体后 | `FAIL-VIDHYB-REF` | `N3-STORYBOARD-BIND` / `references/hybrid-reference-binding.md` | storyboard search roots、candidate list、unique/missing/multiple verdict、manifest storyboard slot |
| `GATE-VIDHYB-REF-02` | 主体参照只能来自组底 YAML 的 `角色 / 场景 / 道具` 与当前 `6-设计/*/3-生成` 真实图片；不得从正文泛词扩展、跨类型替图或把 JSON/Markdown 当图 | `FAIL-VIDHYB-REF` | `N4-SUBJECT-BIND` / `references/hybrid-reference-binding.md` | YAML subject list、design image candidates、selected_variant、missing subject notes |
| `GATE-VIDHYB-REF-03` | 每个进入 LibTV 的故事板或主体图片必须 fresh resolve 并记录 `path + source_sha256 + source_size_bytes + source_mtime_ns`；上传缓存只有指纹完全匹配时可复用 | `FAIL-VIDHYB-STALE-REFERENCE-ASSET` | `N3-STORYBOARD-BIND` / `N4-SUBJECT-BIND` / `references/hybrid-reference-binding.md` | fresh resolution record、fingerprint fields、cache match/mismatch verdict |
| `GATE-VIDHYB-BUDGET-01` | 故事板总参照与主体参照共同计入单组 `mixedList` 9 图预算；超限必须按故事板、角色/场景、道具、次要主体顺序裁决并记录排除，无法压缩时不得提交 | `FAIL-VIDHYB-LIBTV` | `N4-SUBJECT-BIND` / `N6-PLAN-BUILD` / `references/hybrid-reference-binding.md` | reference_image_budget、excluded_due_to_budget、needs_rework reason、mixedList count |
| `GATE-VIDHYB-PROMPT-01` | 本地 `prompt.md` 必须是 source-first 两阶段：draft 直接保留原组正文和原 YAML，不提前写 `reference_index / uploaded_url`，也不在原文前另起混合参照说明 | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `references/hybrid-prompt-assembly-contract.md` | draft prompt、prebinding scan、prefix scan |
| `GATE-VIDHYB-PROMPT-02` | final 只能在 fenced YAML 内注入故事板 `故事板参照` 与已绑定主体的 `name + reference_index + uploaded_url + image_token`；缺图或未入预算主体不得写空 URL、`null` 或缺图说明 | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N4-SUBJECT-BIND` | final YAML diff、manifest bound/missing subjects、empty slot scan |
| `GATE-VIDHYB-SLOT-01` | `asset_uploads` 只记录身份到 OSS URL；最终 `reference_index` 必须来自 UI 图N或实际 `mixedList` 形成的 `generation_slots`，不得用上传顺序当图N真源 | `FAIL-VIDHYB-UPLOAD-SLOT-CONFLATION` | `N6-PLAN-BUILD` / `references/hybrid-prompt-assembly-contract.md` | asset_uploads ledger、generation_slots ledger、final YAML slot projection |
| `GATE-VIDHYB-REMOTE-01` | `*-libtv-submission.txt` 必须以 D 专属 `【LibTV 调用锁定】` 开头；有图时锁定 `mixed2video + mixedList`，无图时锁定 `text2video` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `references/hybrid-prompt-assembly-contract.md` / `references/libtv-handoff.md` | submission header、modeType、mixedList or text2video evidence |
| `GATE-VIDHYB-REMOTE-02` | 远端提交不得包含本地路径、人工 `参照图N`、缺图/无缓存/未入预算说明或裸图片 token；必须通过 final `【分镜组源文本】` 保留故事板/主体名和槽位绑定 | `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `N5-PROMPT-ASSEMBLE` / `N6-PLAN-BUILD` | submission text scan、final source-first YAML、token-name adjacency evidence |
| `GATE-VIDHYB-FIDELITY-01` | 默认必须 `strict_original + transport_only + allow_libtv_prompt_optimization=false`；未记录用户 opt-in 时禁止优化、摘要、重排、改写或补镜头 | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N7-REVIEW-GATE` | submit plan fidelity fields、submission constraints、query prompt comparison |
| `GATE-VIDHYB-LIBTV-01` | 视频生成必须加载并调用 `.agents/skills/cli/libTV` 官方技能包，完成 `LIBTV_ACCESS_KEY` 自检和 `projectUuid/projectUrl` 锁定；不得绕过官方脚本或伪造 sessionId | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `N8-SUBMIT-OR-SKIP` / `references/libtv-handoff.md` | libTV SKILL load note、credential check、project lock、blocked reason or sessionId |
| `GATE-VIDHYB-LIBTV-02` | 有参照图时官方脚本顺序必须为 project lock -> upload -> create_session -> query -> download，且每个 uploaded URL 的 project scope 与锁定 `projectUuid` 一致 | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `N8-SUBMIT-OR-SKIP` / `references/libtv-handoff.md` | command log、upload URL `/claw/<projectUuid>/` scope、submit plan projectUuid、queue projectUuid |
| `GATE-VIDHYB-LIBTV-03` | queue、canvas、query、download 和输出持久化必须可续查：同一 `projectUrl` 有生成节点/结果，下载到本技能集目录并精确命名 `<group_id>.mp4` | `FAIL-VIDHYB-LIBTV` | `N8-SUBMIT-OR-SKIP` / `N9-QUERY-DOWNLOAD` / `N10-CLOSEOUT` / `references/libtv-handoff.md` | queue ledger、canvas result evidence、download command、output path |
| `GATE-VIDHYB-AUDIO-01` | 远端提交必须声明 `enableSound=on`；生成前无法验证 `create_generation_task.params.enableSound` 时只可记录 `audio_preflight_unverified_non_blocking`，不得伪造强证据 | `FAIL-VIDHYB-AUDIO-PREFLIGHT` | `N6-PLAN-BUILD` / `N7-REVIEW-GATE` / `references/libtv-handoff.md` | submission enableSound field、preflight verification or non-blocking note |
| `GATE-VIDHYB-AUDIO-02` | 生成后必须通过 `task_result.audios`、音频 URL 或下载后 `ffprobe` 证明存在音频；缺音频不得交付 | `FAIL-VIDHYB-AUDIO-MISSING` | `N9-QUERY-DOWNLOAD` / `N10-CLOSEOUT` / `references/libtv-handoff.md` | query audio evidence、audio URL、ffprobe audio stream output |
| `GATE-VIDHYB-REPORT-01` | report 必须记录 verdict、处理范围、缺图/排除/失败/跳过、sessionId 或 blocked reason，以及可执行返工入口 | `FAIL-VIDHYB-REPORT` | `N10-CLOSEOUT` / `templates/output-template.md` | 执行报告、queue ledger、review findings |

## Verdict

| verdict | meaning |
| --- | --- |
| `pass` | 全部必需 gate 通过 |
| `pass_with_todo` | 非阻断缺图或待查询事项已记录 |
| `fail` | prompt、参照、命令、路径或队列任一硬门失败 |

## Failure Routing

| fail code | rework |
| --- | --- |
| `FAIL-VIDHYB-INPUT` | `types/type-map.md` |
| `FAIL-VIDHYB-GROUP` | `references/group-source-extraction.md` |
| `FAIL-VIDHYB-PROMPT` | `references/hybrid-prompt-assembly-contract.md` |
| `FAIL-VIDHYB-REF` | `references/hybrid-reference-binding.md` |
| `FAIL-VIDHYB-DURATION` | `references/group-source-extraction.md` / `references/libtv-handoff.md` |
| `FAIL-VIDHYB-LIBTV` | `references/libtv-handoff.md` |
| `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `references/hybrid-prompt-assembly-contract.md` / `references/libtv-handoff.md` |
| `FAIL-VIDHYB-UPLOAD-SLOT-CONFLATION` | `references/hybrid-prompt-assembly-contract.md` / `references/libtv-handoff.md` |
| `FAIL-VIDHYB-STALE-REFERENCE-ASSET` | `references/hybrid-reference-binding.md` |
| `FAIL-VIDHYB-AUDIO-PREFLIGHT` | `references/libtv-handoff.md` |
| `FAIL-VIDHYB-AUDIO-MISSING` | `references/libtv-handoff.md` |
| `FAIL-VIDHYB-REPORT` | `templates/output-template.md` |
