# Imported Reference Adaptation Map

本文件说明 `2-编剧` 如何消费从 `2-编导/references/` 全量复制来的指定合同。复制件保留原文完整内容；本文件只做 stage 适配和触发说明，不删减原合同。

## Source Preservation

| local_file | source_file | preservation_rule |
| --- | --- | --- |
| `scene-rhythm-contract.md` | `.agents/skills/aigc/2-编导/references/scene-rhythm-contract.md` | 原文完整复制；本技能消费场景节奏标注、信息密度和过渡方式 |
| `directorial-authorship-contract.md` | `.agents/skills/aigc/2-编导/references/directorial-authorship-contract.md` | 原文完整复制；本技能只消费“创作判断必须有可见/可听/可执行承托” |
| `climax-visual-treatment-contract.md` | `.agents/skills/aigc/2-编导/references/climax-visual-treatment-contract.md` | 原文完整复制；本技能消费高潮视觉、声音、情绪和行动落点 |
| `episode-final-image-contract.md` | `.agents/skills/aigc/2-编导/references/episode-final-image-contract.md` | 原文完整复制；本技能消费集末最终画面/声音/感受尾钩 |
| `narration-to-voice-adaptation-contract.md` | `.agents/skills/aigc/2-编导/references/narration-to-voice-adaptation-contract.md` | 原文完整复制；本技能消费陈述性信息转对白、独白、内心独白或喊出式台词 |
| `hollywood-quality-spec.md` | `.agents/skills/aigc/2-编导/references/hollywood-quality-spec.md` | 原文完整复制；本技能额外要求场景标题追加天气后缀 |
| `script-adaptation-contract.md` | `.agents/skills/aigc/2-编导/references/script-adaptation-contract.md` | 原文完整复制；其中输出路径在本技能运行时适配为 `projects/aigc/<项目名>/2-编剧/第N集.md` |
| `field-routing-and-audio-visual-contract.md` | `.agents/skills/aigc/2-编导/references/field-routing-and-audio-visual-contract.md` | 原文完整复制；本技能强制声音字段与对应画面字段就近配对，不新增 `声画同步锚点` 类正文标题；相邻画面字段必须通过同画面连续性检查，避免同一拍摄单位被重复拆写 |

## Stage Adaptation Rules

| source_phrase | local_runtime_interpretation |
| --- | --- |
| `2-编导 script layer` | `2-编剧 screenplay layer` |
| `2-编导/第N集.md` in script projection context | `2-编剧/第N集.md` |
| `director layer` / `performance layer` | 仅作为下游承接或剧本层承托提醒，不授权本技能输出导演稿或表演稿 |
| `4-摄影` consumption | 仅作为远端下游可读性目标；本技能不得写机位、景别、运镜或分镜 |
| `final image` | 剧本末尾最后可见/可听/可感受落点，不是生图 prompt |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否完整加载用户指定 8 个 copied references，且没有删除或削弱原文？ | `GATE-SCR-02` | `FAIL-SCR-LOAD` | `N1-SCR-INTAKE` | `reference_load_manifest` |
| 原 `2-编导` 字样是否被正确限权，没有让 `2-编剧` 越权输出导演/表演/摄影真源？ | `GATE-SCR-14` / `GATE-SCR-18` | `FAIL-SCR-DOWNSTREAM-OVERREACH` / `FAIL-MODULE-DRIFT` | `N6-SCR-CANDIDATE-DRAFT` / `Module Loading Matrix` | `downstream_overreach_check`、`module_authorization_audit` |

## Return Binding

本文件由 `SKILL.md` 的 `Imported Reference Adaptation Contract`、`Module Loading Matrix` 和 `Module Trigger Matrix` 消费。若新增 copied reference，必须同步三处表格和 `review/review-contract.md`。
