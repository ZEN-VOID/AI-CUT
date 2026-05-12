# Review Contract: D-主板混合参照

本 review gate 只裁决 `D-主板混合参照` 的组级视频 prompt、混合参照、LibTV 计划、队列和项目持久化，不改写 `4-分组` 主真源。

## Review Checklist

1. 运行 Skill 2.0 结构校验。
2. 检查 `第N集-hybrid-group-index.json` 是否可回指 `4-分组/第N集.md` 的 `## group_id`。
3. 检查 prompt 是否为 source-first YAML：draft 以原 `## group_id` 起笔并保持未绑定 YAML；final 完整保留组正文，只在 fenced YAML 内注入故事板和主体 `reference_index / uploaded_url / image_token`。
4. 检查故事板参照是否来自 `6-图像/B-分镜故事板`，且只作为 `storyboard_total_reference`。
5. 检查主体参照是否只来自组底 YAML 与 `5-设计/*/3-生成` 的真实图片。
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
16. 检查输出路径是否全部位于 `projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/`。

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
