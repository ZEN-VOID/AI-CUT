---
name: story-review-prose-style
description: "Use when reviewing Chinese novel prose quality, reader feel, scene texture, and anti-AI prose artifacts."
governance_tier: lite
---

# review / 文体读感

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `review/SKILL.md`、`../_shared/validation-root-contract.md`、`../_shared/validation-child-output-contract.md`。
- 正式审查前，必须读取锁定后的 `validation_fact_pack` 与当前正文快照。

## Invocation Modes

- `drafting_inline`
  - 被 `3-初稿` 在 registry 指定 step 写回后调用，判断当前文本是否已经具备小说现场感与中文读感。
- `final_acceptance`
  - 被 `review` 父层在终验中并发调用，参与最终 `validation_status` 聚合。

## Parent Positioning

本 child 负责：

- 检查正文是否像成熟中文小说 prose，而不是 planning 复述、影像分镜、评论腔或模型整理稿。
- 检查场景可感性、物件锚、身体反应、声音/气味/触感、空间阻隔和环境反作用是否足以支撑读者沉浸。
- 检查句群节奏、段落呼吸、对白潜台词、心理暗流、叙述视角和题材质感是否成立。
- 检查 AI 腔、总结腔、模板化脸色反应、机械反转句式和“漂亮但无现场”的顺滑段落。

它不负责：

- 判断 planning 义务是否完整兑现；那属于 `结构兑现`。
- 判断人物动机是否 OOC；那属于 `人物一致性`。
- 判断因果、设定规则或时间锚是否冲突；那分别属于 `逻辑自洽校验` 与 `时间线`。

## Total Input Contract

- 必需输入：
  - 当前正文快照
  - `validation_fact_pack.promise_slice`
  - `validation_fact_pack.style_gate` 或等价风格/项目口味约束
  - 当前章 planning 与连续性桥
- 硬规则：
  - 先判文本是否仍是“小说现场”，再判它是否顺。
  - 顺滑、工整、信息完整不自动等于 PASS；若文本没有物理细节、人物反应、句群变化和潜台词，应判为弱读感。

## Output Contract

- `role_id`:
  - `prose-style-validator`
- `dimension_packet`:
  - 至少包含 `scene_density_gaps`、`ai_formula_hits`、`meta_residue_hits`、`emotion_telling_hits`、`sentence_rhythm_flattening`、`sensory_anchor_hits`
- `dimension_report_ref`:
  - `review/第V卷/文体读感.md`
- 默认返工节点：
  - `3-场景和氛围渲染`
  - `5-对白优化`
  - `6-心理活动描写`
  - `8-润色`

## Thinking-Action Network

| node_id | field_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-PROSE-ISOLATE` | `FIELD-PS-01` | 把正文从 frontmatter、标题和流程材料中剥离 | 只读取小说正文段落 | `prose_sample` | -> `N2` | prose scope 清楚 |
| `N2-SCENE-TEXTURE` | `FIELD-PS-02` | 判断场景是否有可感知细节和现场发现 | 检查物件、声音、气味、身体、空间、环境反作用 | `scene_texture_note` | -> `N3` | 场景不是空口解释 |
| `N3-VOICE-RHYTHM` | `FIELD-PS-03` | 判断句群、对白和心理是否有角色化气口 | 检查平均句长、解释对白、潜台词、节奏单一 | `voice_rhythm_note` | -> `N4` | 不机械整齐 |
| `N4-ARTIFACT-GATE` | `FIELD-PS-04` | 清查 AI 腔、meta 腔、分镜腔和模板反应 | 标注总结腔、流程术语、脸色捷径、套话 | `artifact_note` | -> `N5` | 没有明显破沉浸痕迹 |
| `N5-PACKET-WRITE` | `FIELD-PS-05` | 输出文体读感维度结论 | 生成 `dimension_packet + report_ref` | `packet_note` | done | 只写本维度 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-PS-01` | prose scope | 审查对象锁定为小说正文 | `FAIL-PS-01` | `N1` |
| `FIELD-PS-02` | scene texture verdict | 至少有能改变人物反应或信息推进的现场发现 | `FAIL-PS-02` | `3-场景和氛围渲染` |
| `FIELD-PS-03` | rhythm and voice verdict | 句群有起伏，对白/心理不只是说明书 | `FAIL-PS-03` | `5-对白优化` / `6-心理活动描写` |
| `FIELD-PS-04` | artifact verdict | 无明显 AI 腔、meta 腔、模板脸色和分镜残留 | `FAIL-PS-04` | `8-润色` |
| `FIELD-PS-05` | dimension packet | 报告完整、可聚合 | `FAIL-PS-05` | `N5` |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 维度审查入口与父层边界 | `../SKILL.md`、`../_shared/validation-root-contract.md` |
| 文体读感步骤网络 | `steps/validation-flow.md` |
| 质量门禁 | `review/review-gate.md` |
| 类型化读感策略 | `types/type-map.md` |
| 输出样式 | `templates/output-template.md` |
| 可复用经验 | `knowledge-base/heuristics.md` 与 `CONTEXT.md` |
| 产品侧入口 | `agents/openai.yaml` |

## Root-Cause Execution Contract

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

若正文没有现场感，优先打回 `3-场景和氛围渲染`；若对白解释腔重，打回 `5-对白优化`；若心理只报情绪标签，打回 `6-心理活动描写`；若主要问题是 AI 腔、meta 腔、句群过分工整或模板反应，打回 `8-润色`。

## Skill 2.0 Output Contract

- Required output: 文体读感 `dimension_packet` 与 `dimension_report_ref`。
- Output format: Markdown 维度报告 + 父层可聚合结构化 packet。
- Output path: `projects/story/<项目名>/review/第V卷/文体读感.md`。
- Naming convention: report filename 以父层 registry 的 `report_filename` 为准。
- Completion gate: 场景现场、句群读感、AI 腔与返工入口均可追溯。
