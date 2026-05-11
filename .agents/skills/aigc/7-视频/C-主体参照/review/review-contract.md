# Review Contract

本 review gate 只裁决 `C-主体参照` 的组级视频 prompt、主体参照、LibTV 计划、队列和项目持久化，不改写 `4-分组` 主真源。

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 LibTV |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、排队、下载或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照、提交命令或结果追踪的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `group_id` 可回指 `4-分组` 源标题、组正文和 YAML | `FAIL-VIDSUBJ-GROUP` | `references/group-source-extraction.md` |
| `G2-CONTENT` | prompt 主体直接使用现有组正文，分镜顺序完整 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G3-SUBJECTS` | Characters / Scene / Props 只来自组底 YAML | `FAIL-VIDSUBJ-REF` | `references/reference-slot-binding.md` |
| `G4-SLOTS` | 只绑定存在图片，多视图优先，缺图不留空路径；多候选必须有视觉消歧证据或进入 ambiguous | `FAIL-VIDSUBJ-REF` | `references/reference-slot-binding.md` |
| `G5-PATH-SUFFIX` | 每个已绑定主体的信息后都有 `@<图片路径>`，且与 `images[]` 顺序一致；不得使用抽象 `@图N` 替代真实路径 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G6-REFERENCE-BUDGET` | 进入 LibTV 的 `images[]` / `mixedList` 单组不超过 9 张；超限时已优先排除道具，其次排除重复、不必要或可由源文本保留的次要主体，并记录取舍；无法合理压缩到 9 张以内时不得提交 | `FAIL-VIDSUBJ-REF-BUDGET` | `references/reference-slot-binding.md` |
| `G7-PROVIDER-ROUTE` | 有图或视觉消歧已唯一解决时远端 handoff 锁 `modeType=mixed2video` 和 `mixedList`，无图锁 `modeType=text2video`，未解决 ambiguous 不提交且不传空图片槽 | `FAIL-VIDSUBJ-LIBTV` | `references/libtv-handoff.md` |
| `G8-DURATION` | `duration_estimate_seconds` 可回指 `4-分组` 当前组，`duration_hint=clamp(duration_estimate_seconds, 4, 15)`，远端提交中的 `duration` 与 plan 一致；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒 | `FAIL-VIDSUBJ-DURATION` | `references/group-source-extraction.md` / `references/libtv-handoff.md` |
| `G9-REMOTE-NUMBERING` | 远端提交只写主体名 + uploaded URL，不预设 `参照图1/2/N` 人工编号；若系统生成真实图片 token/编号，主体名必须邻近真实 token/编号 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G10-SELF-CHECK` | 生成前有 `LIBTV_ACCESS_KEY credential check` 自检策略或结果 | `FAIL-VIDSUBJ-LIBTV` | `.agents/skills/cli/libTV/SKILL.md` |
| `G11-QUEUE` | 每个 submitted / pending 任务都有 group package 内的 `queue.md`、sessionId 或 blocked reason；集级 queue 只作汇总 | `FAIL-VIDSUBJ-LIBTV` | `references/libtv-handoff.md` |
| `G12-PERSIST` | prompt、manifest、plan、queue、results、report 和视频下载路径位于 `groups/<分镜组ID>/`；集级文件只作派生 summary | `FAIL-VIDSUBJ-LIBTV` | `templates/output-template.md` |
| `G13-REPORT` | 执行报告列出 submitted / queued / downloaded / skipped / failed 与返工入口 | `FAIL-VIDSUBJ-REPORT` | `templates/output-template.md` |
| `G14-POST-SUBMIT` | create_session 后已 query 一次并执行 post-submit gate；`ask_user` / 等待下一条消息 / 请稍候不得被标为 `pending_remote_generation`；`task_type`、字符串型 `params` 等远端 envelope 变体只记录为观测项，不作为投递文本失败依据 | `FAIL-VIDSUBJ-LIBTV-STALL` | `references/libtv-handoff.md` |
| `G15-CACHE-FRESHNESS` | 任何 uploaded URL 若来自缓存，必须有当前本地源图存在性与 `source_sha256 / source_size_bytes / source_mtime_ns` 指纹匹配证据；源图缺失或无指纹缓存不得进入远端提交 | `FAIL-VIDSUBJ-STALE-REFERENCE-ASSET` | `references/reference-slot-binding.md` |
| `G16-REF-PROMPT-INTEGRITY` | manifest、prompt、remote submission、submit plan 四者引用一致：已绑定主体不在缺图/预算排除清单；`images[]`、`mixedList`、YAML `uploaded_url` 集合一致；未声明共享关系时无重复 URL；uploaded URL 的 `/claw/<projectUuid>/` 与 submit plan `projectUuid` 一致；远端提交不含缺图/无缓存/未入预算主体列表，连续性句只出现一次并并入直接请求，不单独列标题 | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` / `FAIL-VIDSUBJ-REFERENCE-PROJECT-SCOPE` | `references/video-prompt-assembly-contract.md` / `references/libtv-handoff.md` |
| `G17-AUDIO-PREFLIGHT` | 远端提交文本请求 `enableSound:on`，并在 submit plan / queue / report 中记录生成前音频控制是否可验证；不可验证时标记 `audio_preflight_unverified_non_blocking`，不阻断提交 | `WARN-VIDSUBJ-AUDIO-PREFLIGHT-UNVERIFIED` | `references/libtv-handoff.md` |
| `G18-AUDIO-ACCEPTANCE` | 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含音频 stream；否则结果不得 pass | `FAIL-VIDSUBJ-AUDIO-MISSING` | `references/libtv-handoff.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-CONTENT
    - G3-SUBJECTS
    - G4-SLOTS
    - G5-PATH-SUFFIX
    - G6-REFERENCE-BUDGET
    - G7-PROVIDER-ROUTE
    - G8-DURATION
    - G9-REMOTE-NUMBERING
    - G10-SELF-CHECK
    - G11-QUEUE
    - G12-PERSIST
    - G13-REPORT
    - G14-POST-SUBMIT
    - G15-CACHE-FRESHNESS
    - G16-REF-PROMPT-INTEGRITY
    - G17-AUDIO-PREFLIGHT
    - G18-AUDIO-ACCEPTANCE
  todos: []
```
