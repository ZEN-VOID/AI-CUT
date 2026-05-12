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
| `G4-SLOTS` | 只绑定同画布 active uploaded URL 或可上传的本地真实图片；需要新上传时多视图优先，缺图不留空路径；多候选必须有视觉消歧证据或进入 ambiguous | `FAIL-VIDSUBJ-REF` | `references/reference-slot-binding.md` |
| `G5-LOCAL-ASSET-EVIDENCE` | 每个已绑定主体都在 manifest / submit plan 中保留复用或上传来源；同画布复用可只记录 active uploaded URL 和 registry key，本地路径/指纹作为可选审计证据；prompt 不再用 `@<图片路径>` 展开主体说明，远端提交不得泄漏本地路径 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G6-REFERENCE-BUDGET` | 进入 LibTV 的 `images[]` / `mixedList` 单组不超过 9 张；超限时已优先排除道具，其次排除重复、不必要或可由源文本保留的次要主体，并记录取舍；无法合理压缩到 9 张以内时不得提交 | `FAIL-VIDSUBJ-REF-BUDGET` | `references/reference-slot-binding.md` |
| `G7-PROVIDER-ROUTE` | 有图或视觉消歧已唯一解决时远端 handoff 锁 `modeType=mixed2video` 和 `mixedList`，无图锁 `modeType=text2video`，未解决 ambiguous 不提交且不传空图片槽 | `FAIL-VIDSUBJ-LIBTV` | `references/libtv-handoff.md` |
| `G8-DURATION` | `duration_estimate_seconds` 可回指 `4-分组` 当前组，`duration_hint=clamp(duration_estimate_seconds, 4, 15)`，远端提交中的 `duration` 与 plan 一致；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒 | `FAIL-VIDSUBJ-DURATION` | `references/group-source-extraction.md` / `references/libtv-handoff.md` |
| `G9-REMOTE-NUMBERING` | 远端提交只写主体名 + uploaded URL，不预设 `参照图1/2/N` 人工编号；若系统生成真实图片 token/编号，主体名必须邻近真实 token/编号 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G10-SELF-CHECK` | 生成前有 `LIBTV_ACCESS_KEY credential check` 自检策略或结果 | `FAIL-VIDSUBJ-LIBTV` | `.agents/skills/cli/libTV/SKILL.md` |
| `G11-QUEUE` | 每个 submitted / pending 任务都有 group package 内的 `queue.md`、sessionId 或 blocked reason；多轮查询摘要写入 `libtv-results.json.attempts[]`；集级 queue 只作汇总 | `FAIL-VIDSUBJ-LIBTV` | `references/libtv-handoff.md` |
| `G12-PERSIST` | compact 默认下，group 根目录只保留 `reference-manifest.json / prompt.md / libtv-submission.txt / libtv-submit-plan.json / queue.md / libtv-results.json / 执行报告.md / 视频`；`group-index / source-body / upload-ledger / query / gate / reference-order` 折叠到 manifest 或 results attempts；full-trace 才写入 `debug/attempts/`；集级文件只作派生 summary | `FAIL-VIDSUBJ-LIBTV` | `templates/output-template.md` |
| `G13-REPORT` | 执行报告列出 submitted / queued / downloaded / skipped / failed 与返工入口 | `FAIL-VIDSUBJ-REPORT` | `templates/output-template.md` |
| `G14-POST-SUBMIT` | create_session 后已 query 一次并执行 post-submit gate；`ask_user` / 等待下一条消息 / 请稍候不得被标为 `pending_remote_generation`；`task_type`、字符串型 `params` 等远端 envelope 变体只记录为观测项，不作为投递文本失败依据 | `FAIL-VIDSUBJ-LIBTV-STALL` | `references/libtv-handoff.md` |
| `G15-SAME-CANVAS-REUSE` | 任何复用 uploaded URL 必须来自当前 `projectUuid/projectID` 的 active 资产登记，URL `/claw/<projectUuid>/` 与 submit plan 一致；图片调整、更换或用户显式要求替换时必须重传并更新 active URL；同名多 URL 无 active/latest 裁决时不得猜测 | `FAIL-VIDSUBJ-REFERENCE-PROJECT-SCOPE` / `FAIL-VIDSUBJ-ASSET-REGISTRY-AMBIGUOUS` | `references/reference-slot-binding.md` |
| `G16-REF-PROMPT-INTEGRITY` | draft 相位允许 `prompt.md` 保留未绑定 YAML，但不得伪造空 `reference_index / uploaded_url` 且不得创建最终远端提交；final 相位要求 manifest、prompt、remote submission、submit plan 四者引用一致：已绑定主体不在缺图/预算排除清单；`reference-manifest.json.generation_slots` 必须注册 `reference_index -> yaml_name -> uploaded_url -> mixedList[n-1]`；`images[]`、`mixedList`、YAML 按 `reference_index` 排序后的主体名和 `uploaded_url` 同槽一致；未声明共享关系时无重复 URL；uploaded URL 的 `/claw/<projectUuid>/` 与 submit plan `projectUuid` 一致；远端提交不含缺图/无可复用 URL/未入预算主体列表，连续性句只出现一次并并入直接请求，不单独列标题 | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` / `FAIL-VIDSUBJ-REFERENCE-PROJECT-SCOPE` / `FAIL-VIDSUBJ-REFERENCE-SLOT-REGISTRY` | `references/video-prompt-assembly-contract.md` / `references/libtv-handoff.md` |
| `G17-AUDIO-PREFLIGHT` | 远端提交文本请求 `enableSound:on`，并在 submit plan / queue / report 中记录生成前音频控制是否可验证；不可验证时标记 `audio_preflight_unverified_non_blocking`，不阻断提交 | `WARN-VIDSUBJ-AUDIO-PREFLIGHT-UNVERIFIED` | `references/libtv-handoff.md` |
| `G18-AUDIO-ACCEPTANCE` | 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含音频 stream；否则结果不得 pass | `FAIL-VIDSUBJ-AUDIO-MISSING` | `references/libtv-handoff.md` |
| `G19-REMOTE-REFERENCE-ORDER` | 提交后若 query 已观测到 `create_generation_task`，远端 `params.modeType` 必须为 `mixed2video`，且 `params.mixedList` / `imageList` URL 顺序必须逐项等于本地最终 `generation_slots` 顺序；若有用户截图或 UI 缩略图确认，则 UI 图N / `Portrait N` 顺序是最终 `generation_slots` 真源，高于工具层旧回显。远端 prompt 中每个已上传主体必须保留主体名、`reference_index` 与 URL 或 `mixedList[n]` / `Portrait N` / `Image N` / `图片N` 邻近绑定；本地必须存在或可生成 `reference-manifest.json.asset_uploads / generation_slots`，分别负责 `yaml_name -> uploaded_url` 与 `图N -> uploaded_url -> yaml_name`。若实际远端顺序或主体名与最终槽位不同，必须按实际槽位 URL 反查 name 并回刷 YAML 后重提 | `FAIL-VIDSUBJ-REMOTE-REFERENCE-ORDER` / `FAIL-VIDSUBJ-PROMPT-REFERENCE-BINDING` / `FAIL-VIDSUBJ-UPLOAD-LEDGER` / `FAIL-VIDSUBJ-REFERENCE-SLOT-REGISTRY` | `references/libtv-handoff.md` / `scripts/build-upload-ledger.py` / `scripts/validate-post-submit-reference-order.py` |

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
    - G5-LOCAL-ASSET-EVIDENCE
    - G6-REFERENCE-BUDGET
    - G7-PROVIDER-ROUTE
    - G8-DURATION
    - G9-REMOTE-NUMBERING
    - G10-SELF-CHECK
    - G11-QUEUE
    - G12-PERSIST
    - G13-REPORT
    - G14-POST-SUBMIT
    - G15-SAME-CANVAS-REUSE
    - G16-REF-PROMPT-INTEGRITY
    - G17-AUDIO-PREFLIGHT
    - G18-AUDIO-ACCEPTANCE
    - G19-REMOTE-REFERENCE-ORDER
  todos: []
```
