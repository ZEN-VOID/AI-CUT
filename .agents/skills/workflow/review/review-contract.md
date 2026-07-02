# Workflow Review Contract

本文件展开 workflow 的审查问题，不替代 `SKILL.md` 的 `Review Gate Binding`。执行时必须回接 `SKILL.md` 中的 fail code 和返工节点。

## Review Checklist

| area | question | blocking_when | return_to |
| --- | --- | --- | --- |
| HyperFrames-only | 是否存在 F1 script、F1 validator、MoviePy/ffmpeg 主链依赖，或把 `video-to-manifest` 当作必需真源/runtime？ | 任一出现即阻断；共享 manifest 仅作可选证据输入不阻断 | `N2-HYPERFRAMES-LOAD` |
| Input | full build 是否有内容真源、主时钟方案、素材池或生成授权？ | 缺最小输入且未降级 route | `N1-INTAKE` |
| Reference | 参考视频是否只用于 rhythm/style？ | 参考画面或素材进入成片候选 | `N3-MEDIA-EVIDENCE` |
| Evidence | 每个进入成片的素材是否有视觉证据和用途？ | 无 source anchor 或用途不清 | `N3-MEDIA-EVIDENCE` |
| Dialogue | 台词字幕 cue 是否能追踪到音频/脚本，按脚本顺序和音频 anchor 顺序单调推进，HTML 字幕是否用 `data-cue-id` 回指同一 cue，并满足同步容差或有逐 cue 人工校时证据，且 `validate_dialogue_sync.py --strict-final` 通过？当前 `projects/内容/文案/` 与 `projects/内容/音频/` 批量输入是否按同名 stem 配对并显式记录路径？ | 全片比例分配、语义错配、字幕顺序错乱、HTML cue-id/time/text 错配、跨 stem 错配音频、把 `BGM.*` 当旁白主时钟、缺 `selected_script_audio_pair` / `source_script` / `source_audio` / `script_audio_stem`、缺 `caption_type`/`audio_anchor`/脚本锚点/script order、仅按总时长手工分配却声称严格同步、validator fail | `N1/N4-DIALOGUE-CLOCK` |
| Plan | storyboard 是否覆盖 hook/content/CTA 三段、背景 throughline、字幕、主视觉、PiP、大字报、转场和 BGM？ | 计划缺段落、缺四层、背景拉通证据不足、背景使用蒙版/opacity/半透明遮罩，或缺素材/字幕 cue 证据 | `N5-STORYBOARD-PLAN` |
| Composition | DOM timing、media 引用、assets、captions 是否可定位？ | HyperFrames core 合同断裂 | `N6-HYPERFRAMES-AUTHOR` |
| Visual Contract | `validate_visual_contract.py` 是否通过，且报告覆盖观众可见文本、主字幕、大字报、PiP、三段四层 assembly 和批量 ledger/audit？ | 内部提示可见、缺 hook/content/CTA、缺背景/PiP/字幕/大字报层、背景 throughline 非连续/加蒙版/降低 opacity/半透明遮罩、字幕缺失/叠显/省略号/换行、大字报整句重复字幕、PiP 太少/无 cue 依据/0 分 manifest 回指、批量 audit 不一致 | `N4/N5/N6/N7` |
| Preview | snapshot 是否非空、叠层不挡字幕和核心 UI？ | 空画面、遮挡、validate 失败或 visual contract fail | `N7-PREVIEW-VALIDATE` |
| Render | final 是否非空、可播放、有音轨、时长合理，且已下载/归集为本地 MP4？ | final 缺失、只停在网页预览/浏览器端、不可验收 | `N8-RENDER-VERIFY` |
| Material Monitor | final 验证通过后，是否已更新 `projects/素材使用监控.csv`，且字段为 `素材名/文件路径/使用次数/使用程度`？ | CSV 缺失、表头不一致、使用次数不是整数、使用程度不是 `全片` 或 `部分切片`，或实际素材使用没有落到全局监控 | `N3/N9` |
| Output Topology | 是否把 `projects/素材/` 和 `projects/示例/` 保持为只读通用素材池，过程文件写入 `projects/output/<日期>/过程/`，单条 final 写入 `projects/output/<日期>/`，批量 final 归集到 `projects/output/<日期>/成片/`？ | 输出写入通用素材池，过程文件散落在日期根，单条 final 留在 `过程/` 或网页端作为唯一交付，或批量 final 未归集到 `成片/` 且无显式豁免 | `N1/N9` |
| Directory Routing | `Directory Structure & Detail Routing Contract`、README 目录树、Module Loading Matrix 和真实文件结构是否一致？ | 真实目录存在但未授权、README 漂移、卫星技能边界不清、`CONTEXT/` 未出现在目录路由中 | `Directory Structure & Detail Routing Contract` / `C10` |
| Context Semantics | `CONTEXT/` 是否包含五个固定文件，且旧 `CONTEXT.md` 已移除？ | 缺五文件、旧 `CONTEXT.md` 仍存在、好/坏示例和正/负经验混写、没有写回分流 | `CONTEXT/ File Semantics Contract` / `Learning / Context Writeback` |
| Report | 是否包含路径、验证、残余风险和 Source Sync Check？ | 缺证据矩阵或多 final 口径 | `N9-CLOSE` |

## Report Evidence Requirements

- `loaded_modules`: 实际加载的 HyperFrames 子技能和本地模块。
- `artifact_paths`: work root、process root、composition root、snapshot、render、report。
- `output_topology`: shared asset roots、output date root、process root、single final root、batch final collection root、canonical final path。
- `dialogue_sync_validation`: final route must include validator command, JSON report path, verdict, fail/warn count, script-order evidence, audio-anchor order evidence and HTML cue-id mapping; current `projects/内容/文案/` + `projects/内容/音频/` routes must include `--require-script-audio-pair`.
- `visual_contract_validation`: social-ad, batch, visual repair and final routes must include validator command, JSON report path, verdict and fail/warn count, including no background mask/opacity findings.
- `material_usage_monitor`: final routes that use shared assets must include `projects/素材使用监控.csv`, `update_asset_usage_monitor.py` command/output, and confirmation that `使用程度` values are `全片` or `部分切片`.
- `layered_assembly`: `workflow_composition_plan.json` must include `background_throughline` and `timeline_segments` evidence for hook/content/CTA and the four visual layers.
- `directory_routing_audit`: true file listing, README tree, Module Loading Matrix and registry context carriers must agree.
- `context_semantics_audit`: `CONTEXT/` five-file list, migrated content landing and absence of legacy `CONTEXT.md`.
- `reference_execution_matrix`: 每个被加载 reference 的触发、适用、证据和 N/A。
- `rule_evidence_map`: 将 review gate 映射到具体 artifact 或截图/CLI 证据。
- `repair_log`: 返工原因、失败码、修复目标、重新验证结果。

## Verdict

| verdict | meaning | allowed_next_step |
| --- | --- | --- |
| `pass` | workflow route、证据、composition、preview/render 和报告门禁均满足对应完成层级。 | close |
| `conditional_pass` | project 或 plan 可交付，但 render、CLI、素材或授权存在明确阻断。 | report residual risk |
| `fail` | 存在阻断性 gate 失败，必须回到对应 workflow node 返工。 | rework |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| Is the workflow review tied back to SKILL.md gates? | Review finding without fail code and node target fails | `FAIL-REVIEW-BINDING` | `Review Gate Binding` | finding table |
| Are all blocking findings routed to a node? | Any blocking issue without `return_to` fails | `FAIL-REVIEW-RETURN` | `Thinking-Action Node Map` | checklist row |
| Does the report include direct evidence? | Only generic statements without artifact paths or CLI/snapshot evidence fail | `FAIL-REVIEW-EVIDENCE` | `N9-CLOSE` | report evidence section |
| Did visual contract validation run when required? | Missing or failing `visual_contract_validation.json` fails social-ad/batch/visual final routes | `FAIL-QUANT-VISUAL-CONTRACT` | `N5/N6/N7` | validator JSON |
| Did material usage update the global monitor? | Verified final usage without a valid `projects/素材使用监控.csv` update fails | `FAIL-ASSET-USAGE-MONITOR` | `N3/N9` | monitor CSV and update script output |
| Does the composition plan implement layered rhythm assembly? | Missing hook/content/CTA, missing background/PiP/caption/editorial overlay layers, non-continuous/masked/transparent background throughline, or missing content subtypes fails social-ad/batch visual routes | `FAIL-LAYERED-ASSEMBLY` | `N3/N5/N6/N7` | `workflow_composition_plan.json`, validator JSON |
| Does output topology match the workflow contract? | Outputs under shared asset roots, process files outside `projects/output/<日期>/过程/`, single final trapped in process root or browser page only, or missing batch final collection fail | `FAIL-BATCH-FINAL-COLLECTION` / `FAIL-OUTPUT-CONTRACT` | `N1/N9` | path map, process root listing, final collection listing, ledger final_path |
| Does directory routing match the real package? | Directory tree, README, Module Matrix, registry or satellite boundary drift fails | `FAIL-DIRECTORY-ROUTING` | `Directory Structure & Detail Routing Contract` | file listing, README tree, registry row |
| Does `CONTEXT/` satisfy Skill 2.0 semantics? | Missing five files, legacy `CONTEXT.md`, or unclear writeback routing fails | `FAIL-CONTEXT-SEMANTICS` | `CONTEXT/ File Semantics Contract` | context file list and writeback map |
