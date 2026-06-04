# 2-编剧 Output Template

## Output Contract Alignment

- Required output: `projects/aigc/<项目名>/2-编剧/第N集.md` and `projects/aigc/<项目名>/2-编剧/执行报告.md`.
- Output format: Markdown screenplay plus Markdown execution report.
- Output path: canonical `2-编剧/` project runtime only.
- Naming convention: `第N集.md`; report is `执行报告.md`.
- Completion gate: `GATE-SCR-01..18` blocking failures are zero.
- Module trigger evidence: cite `reference_load_manifest` and the matching `Module Trigger Matrix` row.
- Business analysis evidence: include `business_profile` and `genre_narrative_profile`.
- Quant criteria evidence: include source count, beat count, rhythm maps, climax/hook maps, A/V pair count, and same-frame continuity checks.
- Attention evidence: include drift signals and re-center actions if any.
- Checkpoint evidence: include `CHK-SCOPE`, `CHK-SEMANTIC`, `CHK-VALIDATION`, `CHK-DARWIN` status.
- Prompt eval evidence: include `test-prompts.json` ids and `eval_mode` when evaluation is requested.

## Episode Screenplay Skeleton

```markdown
---
stage: 2-编剧
episode_id: 第N集
source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
output_path: projects/aigc/<项目名>/2-编剧/第N集.md
genre_profile:
  primary_genre:
  secondary_genre:
rhythm_strategy:
  primary:
  secondary:
screenplay_field_policy: align_with_2_编剧_screenplay_layer
audio_visual_pairing: required
same_frame_continuity: required
review_verdict:
---

# 第N集

## 题材与叙事情节画像

## 2-编剧交接摘要

【剧本正文】

### 场景1：内景/外景 地点 - 日/夜 - 天气

环境描写：<地点、空间结构、光照、天气、静置物件、环境声底色；不写剧情解释。>

角色动作：<角色可见动作、姿态、视线、手部、呼吸、空间移动和与道具/他人的接触。>

对白（角色名，语态/状态短语）：“<对白内容>”
对白画面：<该句对白附近的可见承托；不复述对白；若与上一条动作/表情属于同一画面，合并为同一拍摄单位。>

独白（角色）：“<仅当非引号客观叙事通过派生语音 gate 时使用。>”
独白画面：<独白发生时的身体、声线、空间、道具或环境声承托。>

内心独白（角色）：“<用户口语中的内心OS按本字段处理；优先第一人称或明确自指。>”
内心独白画面：<压住未说出口信息时的可见反应、停顿、呼吸、手部或对手未察觉细节。>

旁白（主体）：“<只有没有合法场内角色可拥有、但必须声音交代的信息才使用。>”
旁白画面：<旁白对应的信息载体或当下可见后果。>

音效（来源）：“<声音本体>”
音效画面：<声音源头、人物反应、空间承托或不可见来源处理；避免与道具特写/群像画面重复描述同一声源画面。>

道具特写：<关键物件、线索痕迹、归属压力或状态变化。>

心理反应：<把内心信息外化为可感知反应，不写抽象心理结论。>

场面调度：<人物站坐高低、远近、出入口、遮挡、道具归属、视线方向和权力关系变化。>

转场：<硬切、声音桥、动作中断、对比转场、物件串联、环境渐变、重复节奏或跳切压缩之一。>
```

## Execution Report Skeleton

```markdown
# 2-编剧 执行报告

## Source Manifest

## Reference Load Manifest

## Execution Decision Trace

| node_id | decision | source_anchor | reference_or_gate | reason | output_landing |
| --- | --- | --- | --- | --- | --- |

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |

## Rule Evidence Map

| rule_or_gate | source_anchor | script_landing | report_evidence | verdict |
| --- | --- | --- | --- | --- |

## Genre Narrative Profile

## Source To Script Map

## Narration To Voice Adaptation Map

## Audio Visual Pairing Map

## Same Frame Continuity Map

| visual_cluster | time_space_relation | merge_or_keep_decision | kept_field | downstream_split_risk |
| --- | --- | --- | --- | --- |

## AIGC Handoff Manifest

## N/A Justification

| rule_or_reference | why_not_triggered | safe_to_skip_reason |
| --- | --- | --- |

## Rhythm Strategy Map

## Climax Treatment Map

## Episode Final Image Map

## Continuity Detail Map

## Review Verdict

## Repair Actions

## Repair Log

| fail_code | rework_target | repair_action | result |
| --- | --- | --- | --- |

## Handoff
```
