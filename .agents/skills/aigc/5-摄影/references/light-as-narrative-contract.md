# Light As Narrative Contract

## Purpose

`light-as-narrative-contract.md` defines how `5-摄影` treats light as a narrative agent rather than a static lighting setup. It is consumed by `N6.3-SCENE-VISUAL-CONSTRAINT`, `N6.4-FUNCTIONAL-PROJECTION`, `N6.5-SHOT-PLAN`, `N7-INJECT` and `N8-REVIEW`.

## Narrative Light Functions

| function_id | function | use when | required visible result |
| --- | --- | --- | --- |
| `LF-01` | `character` | light reveals a character's current inner state or social position | which part of the body/face is lit or withheld |
| `LF-02` | `timer` | light marks countdown, waiting, dusk/dawn shift, power outage or closing window | how light changes across the beat |
| `LF-03` | `revelation` | light exposes evidence, text, danger, rule or emotional truth | what becomes readable and at which moment |
| `LF-04` | `concealment` | darkness, shadow or glare strategically hides information | what is hidden and why the viewer should not see it yet |
| `LF-05` | `mood_shift` | the scene changes emotional register | visible color temperature, contrast or shadow change |
| `LF-06` | `power` | light separates, traps, dominates or isolates a person | who controls the bright area, doorway, window, spotlight or shadow boundary |

## Evidence Shape

```yaml
light_narrative_plan:
  scene_id: ""
  visual_unit_id: ""
  source_anchor: ""
  light_function: "LF-01 character | LF-02 timer | LF-03 revelation | LF-04 concealment | LF-05 mood_shift | LF-06 power"
  light_source_context: "window | doorway | screen | lamp | fire | corridor | practical | ambient | unknown"
  visible_change: ""
  subject_affected: ""
  shadow_or_highlight_result: ""
  narrative_reason: ""
  downstream_payload_note: ""
```

## Rules

- Light source words are not enough. Each plan must say what the light does to a visible subject: cuts a face, isolates a hand, hides an object, reveals text, traps a body or changes the emotional temperature.
- Light must not invent a new source that contradicts the established `scene_visual_constraint`. If the source is not established, describe visible result first and mark `light_source_context: unknown`.
- A scene can keep one light baseline, but major story turns inside the scene must re-check whether the light function changes.
- `N7-INJECT` should write the visible result, not the internal enum. For example: "doorway light cuts his shoulder from the dark hall" is valid; "`LF-06 power`" in the final draft is not.

## Failure Patterns

| symptom | source layer | repair |
| --- | --- | --- |
| only says "side light", "top light" or "cinematic light" | source/result confusion | add lit subject, shadow edge and narrative reason |
| light changes randomly between adjacent shots | continuity drift | return to `N6.3-SCENE-VISUAL-CONSTRAINT` and rebuild scene light baseline |
| light is beautiful but story-neutral | decorative lighting | choose one narrative function or remove the lighting emphasis |
| light reveals information too early | suspense leak | return to `attention_guidance_plan` and `shot_design_plan` to delay or conceal |

## Gate

`GATE-CINE-30` passes only when important light choices have a visible narrative function, remain compatible with scene continuity, and can be consumed by downstream image/video generation.
