# Attention Guidance Contract

## Purpose

`attention-guidance-contract.md` defines how `5-摄影` actively controls what the audience notices first, second and last inside each shot. It is consumed by `N6.4-FUNCTIONAL-PROJECTION`, `N6.5-SHOT-PLAN`, `N7-INJECT` and `N8-REVIEW`.

## Guidance Techniques

| technique_id | technique | best use | common risk |
| --- | --- | --- | --- |
| `AG-01` | `brightness` | reveal a subject through light contrast | overexposed decorative spotlight |
| `AG-02` | `motion` | make the moving body/object lead the eye | random camera movement competing with actor action |
| `AG-03` | `focus` | rack focus or shallow depth draws discovery | focus shift without information change |
| `AG-04` | `size` | foreground/background scale creates priority | oversized prop steals action focus |
| `AG-05` | `contrast` | color, texture or silhouette separates target | contrast not tied to story |
| `AG-06` | `sound_image_sync` | sound cues tell the viewer where to look | sound explains what image already shows |
| `AG-07` | `pattern_break` | a small anomaly interrupts order | anomaly appears before suspense setup |
| `AG-08` | `eye_trace` | character gaze directs viewer attention | gaze relay used too often as default |

## Evidence Shape

```yaml
attention_guidance_plan:
  visual_unit_id: ""
  shot_id: ""
  source_anchor: ""
  first_attention_target: ""
  second_attention_target: ""
  final_attention_or_handoff: ""
  guidance_technique:
    - "AG-01 brightness"
  hidden_or_delayed_information: ""
  audience_question_at_cut: ""
  risk_check:
    all_information_visible_at_once: false
    prop_steals_focus: false
    gaze_default_overuse: false
    suspense_leak: false
```

## Rules

- Every non-trivial `shot_design_plan` must answer: what does the audience see first, what do they discover next, and what question remains at the cut or handoff.
- Dialogue scenes must not default to alternating speaker/listener coverage. The attention plan can move from mouth to hand, listener reaction, spatial distance, off-screen sound, prop ownership or power position when that better serves the scene.
- Hidden information must be explicitly named in the internal plan. If nothing is hidden or delayed, mark it as `none` and explain why direct presentation is correct.
- `N7-INJECT` writes the path of noticing as camera action or composition, not as explanatory text.

## Failure Patterns

| symptom | source layer | repair |
| --- | --- | --- |
| shot shows every important element at once | no attention hierarchy | return to `N6.4-FUNCTIONAL-PROJECTION` and set first/second/final attention targets |
| dialogue scene alternates speaker closeups mechanically | coverage template | add power, subtext, hand, prop, off-screen or listener attention strategy |
| focus pull happens but reveals nothing | decorative focus | connect focus shift to information, relationship, threat or concealment |
| audience sees the clue before the character pressure is ready | suspense leak | delay the clue through concealment, off-screen space, foreground block or later focus shift |

## Gate

`GATE-CINE-31` passes only when each important shot has a clear attention hierarchy, a reason for direct reveal or delay, and a handoff that preserves viewer orientation.
