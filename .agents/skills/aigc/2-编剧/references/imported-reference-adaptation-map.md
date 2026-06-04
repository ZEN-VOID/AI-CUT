# Imported Reference Adaptation Map

本文件说明 `2-编剧` 如何消费从 legacy `2-编导/references/` 迁入并本地适配的指定合同。本文件只做 stage 适配和触发说明，不授权旧路径或旧 owner 重新成为当前 runtime truth。

## Source Preservation

| local_file | source_file | preservation_rule |
| --- | --- | --- |
| `scene-rhythm-contract.md` | local adapted copy from legacy 2-编导 reference source: scene-rhythm-contract | 本技能消费场景节奏标注、信息密度和过渡方式 |
| `directorial-authorship-contract.md` | local adapted copy from legacy 2-编导 reference source: directorial-authorship-contract | 本技能只消费“创作判断必须有可见/可听/可执行承托” |
| `climax-visual-treatment-contract.md` | local adapted copy from legacy 2-编导 reference source: climax-visual-treatment-contract | 本技能消费高潮视觉、声音、情绪和行动落点 |
| `episode-final-image-contract.md` | local adapted copy from legacy 2-编导 reference source: episode-final-image-contract | 本技能消费集末最终画面/声音/感受尾钩 |
| `narration-to-voice-adaptation-contract.md` | local adapted copy from legacy 2-编导 reference source: narration-to-voice-adaptation-contract | 本技能消费陈述性信息转对白、独白、内心独白或喊出式台词 |
| `hollywood-quality-spec.md` | local adapted copy from legacy 2-编导 reference source: hollywood-quality-spec | 本技能额外要求场景标题追加天气后缀 |
| `script-adaptation-contract.md` | local adapted copy from legacy 2-编导 reference source: script-adaptation-contract | 输出路径固定为 `projects/aigc/<项目名>/2-编剧/第N集.md` |
| `field-routing-and-audio-visual-contract.md` | local adapted copy from legacy 2-编导 reference source: field-routing-and-audio-visual-contract | 本技能强制声音字段与对应画面字段就近配对，不新增 `声画同步锚点` 类正文标题；相邻画面字段必须通过同画面连续性检查，避免同一拍摄单位被重复拆写 |

## Stage Adaptation Rules

| source_phrase | local_runtime_interpretation |
| --- | --- |
| legacy `2-编导 script layer` | `2-编剧 screenplay layer` |
| legacy `2-编导/第N集.md` in script projection context | `2-编剧/第N集.md` |
| legacy `director layer` / `performance layer` | `4-导演` / `5-表演` 下游承接提醒，不授权本技能输出导演稿或表演稿 |
| legacy `4-摄影` consumption | `8-摄影` / `9-光影` 下游可读性目标；本技能不得写机位、景别、运镜、光影注入或分镜 |
| `final image` | 剧本末尾最后可见/可听/可感受落点，不是生图 prompt |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否完整加载用户指定 8 个 copied references，且没有删除或削弱原文？ | `GATE-SCR-02` | `FAIL-SCR-LOAD` | `N1-SCR-INTAKE` | `reference_load_manifest` |
| legacy `2-编导` 字样是否只作为迁移证据出现，没有让 `2-编剧` 越权输出导演/表演/摄影真源？ | `GATE-SCR-14` / `GATE-SCR-18` | `FAIL-SCR-DOWNSTREAM-OVERREACH` / `FAIL-MODULE-DRIFT` | `N6-SCR-CANDIDATE-DRAFT` / `Module Loading Matrix` | `downstream_overreach_check`、`module_authorization_audit` |

## Return Binding

本文件由 `SKILL.md` 的 `Imported Reference Adaptation Contract`、`Module Loading Matrix` 和 `Module Trigger Matrix` 消费。若新增 copied reference，必须同步三处表格和 `review/review-contract.md`。
