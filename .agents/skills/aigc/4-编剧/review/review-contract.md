# 4-编剧 Review Contract

本 review gate 验证逐集剧本是否把小说 source 转成保真、可拍、可听、可演、短剧节奏明确且 AIGC 下游可解析的 canonical 剧本。

## Default Provider

- Default auxiliary provider: `code-reviewer` stance for structure and gate review.
- 创作质量判断仍由 LLM 主审；脚本只做格式、路径、字段和引用存在性辅助检查。

## Review Dimensions

| dimension | checks |
| --- | --- |
| source_lock | source、集号、输出路径、改写权限明确 |
| imported_references | 8 个指定 copied references 均在 load manifest 中，且适配边界清楚 |
| upstream_context_direction | `1-分集`、`2-美学/类型风格.md`、`3-主体/主体注册表.md`、项目记忆/上下文如何引导本集创作方向、正文落点和边界检查清楚 |
| type_style_context | `类型风格.md` 的题材类型、标志性元素和题材专属表现技巧被投影到节奏、高潮、尾钩和声画策略 |
| subject_registry_context | `主体注册表.md` 的角色、场景、道具 canonical name 被用于剧本和 handoff，没有静默新增、改名或拆分同一主体 |
| genre_narrative | 题材类型、叙事 beats、人物欲望/阻碍、信息差、观众契约完整 |
| faithfulness | 剧情事实、事件顺序、人物关系和已有对白不漂移 |
| hollywood_format | 场景标题与 `4-编剧` 保持一致并追加天气后缀，字段顺序和剧本可读性 |
| voice_adaptation | 陈述性信息转对白/独白/喊出式台词有 source anchor 和 voice owner |
| audio_visual_sync | 对白、独白、内心独白、旁白、音效等声音字段与对应画面字段就近成对出现，不使用 `【声画同步锚点】` 正文标题；相邻画面字段通过同画面连续性检查，不把同一拍摄单位重复拆写 |
| rhythm_support | 节奏机制匹配题材/情节，且有场内承托 |
| climax_hook | 高潮有视觉/声音/情绪/行动落点，尾钩有最后可感落点 |
| aigc_handoff | 下游理解和声画配对证据在 frontmatter 或执行报告中清晰，不写入正文第二套标题字段，不写镜头、分镜、prompt 或视频参数 |
| execution_report_evidence | 报告包含可审计决策链、references 执行矩阵、上游上下文应用、上游创作方向矩阵、类型风格应用、主体注册表应用、规则证据、N/A 说明和返工记录 |
| llm_first | 核心创作由 LLM 完成，脚本未替代主创 |
| convergence | 阻断项修复并复审通过后才写回 canonical |

## Gate Table

| gate_id | pass_standard | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `GATE-SCR-01` | 输出只写 `projects/aigc/<项目名>/4-编剧/第N集.md` 和 `执行报告.md`，不改上游 | `FAIL-SCR-PATH` | `N8-SCR-WRITEBACK-CLOSE` | `output_path_check` |
| `GATE-SCR-02` | `SKILL.md + CONTEXT.md`、项目上下文和 8 个 imported references 已加载 | `FAIL-SCR-LOAD` | `N1-SCR-INTAKE` | `reference_load_manifest` |
| `GATE-SCR-03` | `genre_narrative_profile` 能解释节奏选择 | `FAIL-SCR-GENRE-NARRATIVE` | `N2-SCR-GENRE-NARRATIVE` | `genre_narrative_profile` |
| `GATE-SCR-04` | 上游事实、顺序、人物关系、已有对白保真 | `FAIL-SCR-FAITHFULNESS` | `N3-SCR-FAITHFUL-PROJECTION` | `source_to_script_map` |
| `GATE-SCR-05` | 场景标题符合 `### 场景N：内景/外景 地点 - 日/夜 - 天气` | `FAIL-SCR-SCENE-HEADING` | `N3-SCR-FAITHFUL-PROJECTION` | `scene_heading_check` |
| `GATE-SCR-06` | 派生语音有 source anchor、voice owner、知识依据、预算和现场承托 | `FAIL-SCR-VOICE` | `N3/N6` | `narration_to_voice_adaptation_map` |
| `GATE-SCR-07` | 声音字段就近配对对应画面字段：对白画面、独白画面、内心独白画面、旁白画面、音效画面；正文不得使用 `【声画同步锚点】`；同一时刻/同一主体/同一动作链的相邻画面字段不得重复拆成多个拍摄单位 | `FAIL-SCR-AUDIO-VISUAL` | `N6-SCR-CANDIDATE-DRAFT` | `audio_visual_pairing_map`、`same_frame_continuity_map` |
| `GATE-SCR-08` | 节奏机制有匹配理由、source anchor 和承托字段 | `FAIL-SCR-RHYTHM` | `N4-SCR-RHYTHM-ENGINE` | `rhythm_strategy_map` |
| `GATE-SCR-09` | 高潮含视觉、声音、情绪、行动落点，不新增结果 | `FAIL-SCR-CLIMAX` | `N5-SCR-CLIMAX-HOOK` | `climax_treatment_map` |
| `GATE-SCR-10` | 尾钩是最后可见/可听/可感受落点，并指向下一集未闭合问题 | `FAIL-SCR-HOOK` | `N5-SCR-CLIMAX-HOOK` | `episode_final_image_map` |
| `GATE-SCR-11` | 必要细节补充服务连贯或下游理解，有来源或连续性理由 | `FAIL-SCR-DETAILS` | `N6-SCR-CANDIDATE-DRAFT` | `continuity_detail_map` |
| `GATE-SCR-12` | 改写尺度符合授权，未擅自改变因果、动机或结局 | `FAIL-SCR-REWRITE-SCOPE` | `N3/N6` | `rewrite_scope_check` |
| `GATE-SCR-13` | AIGC 下游 handoff 完整，且只在 frontmatter 或执行报告中承载，不污染剧本正文正式字段 | `FAIL-SCR-AIGC-FIELDS` | `N6/N8` | `aigc_handoff_manifest` |
| `GATE-SCR-14` | 无机位、景别、运镜、分镜编号、图像 prompt、视频参数越权 | `FAIL-SCR-DOWNSTREAM-OVERREACH` | `N6-SCR-CANDIDATE-DRAFT` | `downstream_overreach_check` |
| `GATE-SCR-15` | 剧本可拍、可听、可演、可读，字段纯度足够 | `FAIL-SCR-SCREENPLAY-QUALITY` | `N6-SCR-CANDIDATE-DRAFT` | `field_quality_check` |
| `GATE-SCR-16` | 执行报告含 `Execution Decision Trace`、`Reference Execution Matrix`、`Upstream Context Application Map`、`Upstream Creative Direction Matrix`、`Type Style Application Map`、`Subject Registry Application Map`、`Rule Evidence Map`、`N/A Justification`、`Repair Log`、required evidence maps、review verdict、repair actions、handoff | `FAIL-SCR-REPORT` | `N8-SCR-WRITEBACK-CLOSE` | `execution_report`、`execution_decision_trace`、`reference_execution_matrix`、`upstream_context_application_map`、`upstream_creative_direction_matrix`、`type_style_application_map`、`subject_registry_application_map`、`rule_evidence_map`、`na_justification`、`repair_log` |
| `GATE-SCR-17` | 核心创作由 LLM 完成，脚本只做机械辅助 | `FAIL-SCR-LLM-FIRST` | `LLM-First Creative Authorship Contract` | `authorship_check` |
| `GATE-SCR-18` | 模块没有成为第二规则源或第二输出真源 | `FAIL-MODULE-DRIFT` | `Module Loading Matrix` | `module_authorization_audit` |
| `GATE-SCR-19` | 剧本正文、节奏方案、对白、高潮、尾钩和 handoff 无脚本化生成、批量插入、正则套句、映射投影、模板句式复用、关键词锚点替换、句式轮换或同义改写批量生成痕迹 | `FAIL-SCR-SCRIPTED-DRAFT` | `N6-SCR-CANDIDATE-DRAFT` / `R1-SCR-REWORK` | `anti_scripted_draft_audit` |
| `GATE-SCR-20` | `1-分集` 或指定 source 被明确投影为剧本层决策，并记录 source anchor、local decision 和 preservation check，而非只写“已读取/已参考” | `FAIL-SCR-UPSTREAM-CONTEXT` | `N1-SCR-INTAKE` / `N3-SCR-FAITHFUL-PROJECTION` / `N8-SCR-WRITEBACK-CLOSE` | `upstream_context_application_map` |
| `GATE-SCR-21` | `2-美学/类型风格.md` 被明确投影为本集题材、节奏、高潮、尾钩和声画策略，而不是只作为标签复述 | `FAIL-SCR-TYPE-STYLE-CONTEXT` | `N1-SCR-INTAKE` / `N2-SCR-GENRE-NARRATIVE` / `N8-SCR-WRITEBACK-CLOSE` | `type_style_application_map` |
| `GATE-SCR-22` | `3-主体/主体注册表.md` 被明确投影为本集角色、场景、道具命名真源，且剧本中未静默新增或改名主体 | `FAIL-SCR-SUBJECT-REGISTRY-CONTEXT` | `N1-SCR-INTAKE` / `N2-SCR-GENRE-NARRATIVE` / `N8-SCR-WRITEBACK-CLOSE` | `subject_registry_application_map` |
| `GATE-SCR-23` | `1-分集`、`2-美学/类型风格.md`、`3-主体/主体注册表.md`、项目 `MEMORY.md/CONTEXT/` 分别如何引导本集编剧创作方向、正文落点和禁止越权检查清楚 | `FAIL-SCR-UPSTREAM-DIRECTION-MATRIX` | `N1-SCR-INTAKE` / `N2-SCR-GENRE-NARRATIVE` / `N8-SCR-WRITEBACK-CLOSE` | `upstream_creative_direction_matrix` |

## Reference Gate Coverage

| reference_file | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `references/imported-reference-adaptation-map.md` | `GATE-SCR-02`, `GATE-SCR-14`, `GATE-SCR-18` | `FAIL-SCR-LOAD`, `FAIL-SCR-DOWNSTREAM-OVERREACH`, `FAIL-MODULE-DRIFT` | `N1`, `N6`, `Module Loading Matrix` | `reference_load_manifest`, `downstream_overreach_check` |
| `references/screenwriting-masters-and-shortdrama-rhythm-contract.md` | `GATE-SCR-03`, `GATE-SCR-08`, `GATE-SCR-09`, `GATE-SCR-10` | `FAIL-SCR-GENRE-NARRATIVE`, `FAIL-SCR-RHYTHM`, `FAIL-SCR-CLIMAX`, `FAIL-SCR-HOOK` | `N2`, `N4`, `N5` | `genre_narrative_profile`, `rhythm_strategy_map`, `climax_treatment_map`, `episode_final_image_map` |
| copied `scene-rhythm-contract.md` | `GATE-SCR-08` | `FAIL-SCR-RHYTHM` | `N4-SCR-RHYTHM-ENGINE` | `rhythm_support_evidence` |
| copied `directorial-authorship-contract.md` | `GATE-SCR-08`, `GATE-SCR-09`, `GATE-SCR-10` | `FAIL-SCR-RHYTHM`, `FAIL-SCR-CLIMAX`, `FAIL-SCR-HOOK` | `N4/N5` | `support_evidence` |
| copied `climax-visual-treatment-contract.md` | `GATE-SCR-09` | `FAIL-SCR-CLIMAX` | `N5-SCR-CLIMAX-HOOK` | `climax_treatment_map` |
| copied `episode-final-image-contract.md` | `GATE-SCR-10` | `FAIL-SCR-HOOK` | `N5-SCR-CLIMAX-HOOK` | `episode_final_image_map` |
| copied `narration-to-voice-adaptation-contract.md` | `GATE-SCR-06` | `FAIL-SCR-VOICE` | `N3/N6` | `narration_to_voice_adaptation_map` |
| copied `hollywood-quality-spec.md` | `GATE-SCR-05`, `GATE-SCR-15` | `FAIL-SCR-SCENE-HEADING`, `FAIL-SCR-SCREENPLAY-QUALITY` | `N3/N6` | `scene_heading_check`, `field_quality_check` |
| copied `script-adaptation-contract.md` | `GATE-SCR-04`, `GATE-SCR-05` | `FAIL-SCR-FAITHFULNESS`, `FAIL-SCR-SCENE-HEADING` | `N3` | `source_to_script_map`, `scene_heading_check` |
| copied `field-routing-and-audio-visual-contract.md` | `GATE-SCR-07`, `GATE-SCR-13` | `FAIL-SCR-AUDIO-VISUAL`, `FAIL-SCR-AIGC-FIELDS` | `N6` | `audio_visual_pairing_map`, `same_frame_continuity_map`, `aigc_handoff_manifest` |
| `../_shared/upstream-context-application-contract.md` | `GATE-SCR-20`, `GATE-SCR-23` | `FAIL-SCR-UPSTREAM-CONTEXT`, `FAIL-SCR-UPSTREAM-DIRECTION-MATRIX` | `N1/N2/N3/N8` | `upstream_context_application_map`, `upstream_creative_direction_matrix` |
| `templates/output-template.md` | `GATE-SCR-16`, `GATE-SCR-21`, `GATE-SCR-22`, `GATE-SCR-23` | `FAIL-SCR-REPORT`, `FAIL-SCR-TYPE-STYLE-CONTEXT`, `FAIL-SCR-SUBJECT-REGISTRY-CONTEXT`, `FAIL-SCR-UPSTREAM-DIRECTION-MATRIX` | `N8` | `execution_report`, `type_style_application_map`, `subject_registry_application_map`, `upstream_creative_direction_matrix` |

## Verdict

`pass | pass_with_followups | needs_rework | blocked`

- `pass`: 阻断项为 0，followup 为 0。
- `pass_with_followups`: 阻断项为 0，非阻断 followup 不超过 3 项，且不影响保真、路径、声画、节奏、高潮、尾钩、上游创作方向矩阵或主体命名对齐。
- `needs_rework`: 任一阻断 gate 失败，且可在 3 轮内修复。
- `blocked`: source 缺失、权限不明、用户授权冲突或同一 fail code 3 轮后仍失败。
