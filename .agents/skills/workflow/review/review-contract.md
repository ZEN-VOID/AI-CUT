# Workflow Review Contract

本文件展开 workflow 的审查问题，不替代 `SKILL.md` 的 `Review Gate Binding`。执行时必须回接 `SKILL.md` 中的 fail code 和返工节点。

## Review Checklist

| area | question | blocking_when | return_to |
| --- | --- | --- | --- |
| HyperFrames-only | 是否存在 F1 script、F1 validator、MoviePy/ffmpeg 主链依赖，或把 `video-to-manifest` 当作必需真源/runtime？ | 任一出现即阻断；共享 manifest 仅作可选证据输入不阻断 | `N2-HYPERFRAMES-LOAD` |
| Input | full build 是否有内容真源、主时钟方案、素材池或生成授权？ | 缺最小输入且未降级 route | `N1-INTAKE` |
| Reference | 参考视频是否只用于 rhythm/style？ | 参考画面或素材进入成片候选 | `N3-MEDIA-EVIDENCE` |
| Evidence | 每个进入成片的素材是否有视觉证据和用途？ | 无 source anchor 或用途不清 | `N3-MEDIA-EVIDENCE` |
| Dialogue | 台词字幕 cue 是否能追踪到音频/脚本，并满足同步容差或有逐 cue 人工校时证据，且 `validate_dialogue_sync.py --strict-final` 通过？ | 全片比例分配、语义错配、缺 `caption_type`/`audio_anchor`/脚本锚点、仅按总时长手工分配却声称严格同步、validator fail | `N4-DIALOGUE-CLOCK` |
| Plan | storyboard 是否覆盖字幕、主视觉、PiP、大字报、转场和 BGM？ | 计划缺段落或缺证据 | `N5-STORYBOARD-PLAN` |
| Composition | DOM timing、media 引用、assets、captions 是否可定位？ | HyperFrames core 合同断裂 | `N6-HYPERFRAMES-AUTHOR` |
| Visual Contract | `validate_visual_contract.py` 是否通过，且报告覆盖观众可见文本、主字幕、大字报、PiP 和批量 ledger/audit？ | 内部提示可见、字幕缺失/叠显/省略号/换行、大字报整句重复字幕、PiP 太少/无 cue 依据/0 分 manifest 回指、批量 audit 不一致 | `N4/N5/N6/N7` |
| Preview | snapshot 是否非空、叠层不挡字幕和核心 UI？ | 空画面、遮挡、validate 失败或 visual contract fail | `N7-PREVIEW-VALIDATE` |
| Render | final 是否非空、可播放、有音轨、时长合理？ | final 缺失或不可验收 | `N8-RENDER-VERIFY` |
| Output Topology | 是否把 `projects/素材/` 和 `projects/示例/` 保持为只读通用素材池，过程文件写入 `projects/output/<日期>/过程/`，单条 final 写入 `projects/output/<日期>/`，批量 final 归集到 `projects/output/<日期>/成片/`？ | 输出写入通用素材池，过程文件散落在日期根，单条 final 留在 `过程/` 作为唯一交付，或批量 final 未归集到 `成片/` 且无显式豁免 | `N1/N9` |
| Report | 是否包含路径、验证、残余风险和 Source Sync Check？ | 缺证据矩阵或多 final 口径 | `N9-CLOSE` |

## Report Evidence Requirements

- `loaded_modules`: 实际加载的 HyperFrames 子技能和本地模块。
- `artifact_paths`: work root、process root、composition root、snapshot、render、report。
- `output_topology`: shared asset roots、output date root、process root、single final root、batch final collection root、canonical final path。
- `dialogue_sync_validation`: final route must include validator command, JSON report path, verdict and fail/warn count.
- `visual_contract_validation`: social-ad, batch, visual repair and final routes must include validator command, JSON report path, verdict and fail/warn count.
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
| Does output topology match the workflow contract? | Outputs under shared asset roots, process files outside `projects/output/<日期>/过程/`, single final trapped in process root, or missing batch final collection fail | `FAIL-BATCH-FINAL-COLLECTION` / `FAIL-OUTPUT-CONTRACT` | `N1/N9` | path map, process root listing, final collection listing, ledger final_path |
