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
- Long dialogue scenes must form `long_dialogue_visual_plan` when upstream provides `long_dialogue_beat_map` or `long_dialogue_delivery_map`. The attention path should vary by beat: speaker control, listener absorption, hand/object pressure, spatial distance, group hierarchy, off-screen sound, silence or environment pressure. A single frontal talking-head shot is only allowed when the internal frame changes enough to carry the whole dramatic action.
- Hidden information must be explicitly named in the internal plan. If nothing is hidden or delayed, mark it as `none` and explain why direct presentation is correct.
- `N7-INJECT` writes the path of noticing as camera action or composition, not as explanatory text.

## Long Dialogue Attention Flow

`long_dialogue_visual_plan` extends `dialogue_scene_variation_plan` for long dialogue. It does not require many shots by default; it requires that each shot has a different viewing task.

Required internal fields:

```yaml
long_dialogue_visual_plan:
  source_dialogue_ref: ""
  beat_refs: []
  visual_beats:
    - beat_id: ""
      carried_text_or_reaction: ""
      focus_target: "speaker | listener | hand | prop | spatial_gap | group | offscreen_source | silence"
      attention_reason: ""
      continuity_handoff: ""
      duration_link: ""
  risk_check:
    talking_head_single_shot: false
    same_focus_repeated: false
    missing_listener_or_pressure_cutaway: false
    beat_text_mismatch: false
```

Rules:

- Use speaker face only when the face carries new information: loss of control, mask crack, deliberate pressure, withheld emotion or a meaningful change in voice/body.
- Listener reaction is not filler. It must show absorption, resistance, misunderstanding, fear, calculation, emotional rupture or power shift.
- Hands, props and space are valid focus targets only when they carry pressure already present in the scene; do not insert decorative objects.
- Every visual beat must preserve axis, eye-line and body orientation continuity with surrounding dialogue shots.

## Failure Patterns

| symptom | source layer | repair |
| --- | --- | --- |
| shot shows every important element at once | no attention hierarchy | return to `N6.4-FUNCTIONAL-PROJECTION` and set first/second/final attention targets |
| dialogue scene alternates speaker closeups mechanically | coverage template | add power, subtext, hand, prop, off-screen or listener attention strategy |
| long dialogue stays on one speaker with no internal visual change | talking-head treatment | build `long_dialogue_visual_plan` from beat refs and vary focus by speaker/listener/hand/space/silence |
| focus pull happens but reveals nothing | decorative focus | connect focus shift to information, relationship, threat or concealment |
| audience sees the clue before the character pressure is ready | suspense leak | delay the clue through concealment, off-screen space, foreground block or later focus shift |

## Gate

`GATE-CINE-31` passes only when each important shot has a clear attention hierarchy, a reason for direct reveal or delay, and a handoff that preserves viewer orientation.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does every non-trivial `shot_design_plan` define what the audience notices first, discovers next, and carries out at the cut or handoff? | `GATE-CINE-31` | `FAIL-CINE-05Z` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `attention_guidance_plan` with `first_attention_target` / `second_attention_target` / `final_attention_or_handoff` samples |
| Does the shot avoid showing all important information at once unless direct presentation is explicitly justified? | `GATE-CINE-31` | `FAIL-CINE-05Z` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` | `hidden_or_delayed_information` value or `none` justification, plus full-information exceptions |
| In dialogue scenes, is the focus chosen from power, subtext, hand, prop, off-screen sound, listener reaction, spatial distance or group hierarchy instead of mechanical speaker/listener alternation? | `GATE-CINE-32` | `FAIL-DIALOGUE-CINEMATOGRAPHY-TEMPLATE` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `dialogue_scene_variation_plan` and repaired dialogue shot samples |
| In long dialogue scenes, does `long_dialogue_visual_plan` map each source beat to a changing attention task and avoid a single talking-head or repeated speaker-only focus? | `GATE-CINE-33` | `FAIL-LONG-DIALOGUE-CINEMATOGRAPHY` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `long_dialogue_visual_plan` samples with beat refs, focus targets, duration links and continuity handoffs |
| Does every focus pull, gaze relay, sound cue, pattern break or brightness cue reveal new information, relation, threat or concealment rather than decorative movement? | `GATE-CINE-31` | `FAIL-CINE-05Z` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` | technique-to-viewing-result sample for `AG-*` decisions |
| Is the attention path written into `分镜N` as camera action, composition, focus or blocking rather than explanatory text about what the audience should feel? | `GATE-CINE-10` / `GATE-CINE-18` | `FAIL-CINE-05A` / `FAIL-CINE-05G` | `steps/cinematography-workflow.md#N7-INJECT` | before/after lines showing explanatory attention text rewritten as visible camera behavior |
| Do failure patterns such as all-information display, decorative focus, gaze overuse or suspense leak route back to an executable plan node instead of remaining a note? | `GATE-CINE-17A` | `FAIL-CINE-05REF` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N8-REVIEW` | reference gate coverage row and any `FAIL-CINE-05Z` or dialogue-template repair evidence |
