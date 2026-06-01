# Light As Narrative Contract

## Purpose

`light-as-narrative-contract.md` defines how `4-摄影` treats light as a narrative agent rather than a static lighting setup. It is consumed by `N6.3-SCENE-VISUAL-CONSTRAINT`, `N6.4-FUNCTIONAL-PROJECTION`, `N6.5-SHOT-PLAN`, `N7-INJECT` and `N8-REVIEW`.

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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does each important light choice state what light does to a visible subject, object, text, shadow edge, body, face or space rather than only naming a source or mood? | `GATE-CINE-30` | `FAIL-CINE-05Y` | `steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` / `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` | `light_narrative_plan` samples with visible change, subject affected and shadow/highlight result |
| Is the light function one of character, timer, revelation, concealment, mood shift or power, and does it serve the current shot's information or relation task? | `GATE-CINE-30` / `GATE-CINE-28` | `FAIL-CINE-05Y` / `FAIL-CINE-05W` | `steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` / `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` | function-to-shot-purpose samples and delete-loss checks for decorative light |
| Does the plan avoid inventing a light source that contradicts `scene_visual_constraint`, or mark unknown source while prioritizing visible result? | `GATE-CINE-22` / `GATE-CINE-30` | `FAIL-CINE-05P` / `FAIL-CINE-05Y` | `steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` | scene light baseline, source-context notes and contradiction repairs |
| When a major story turn occurs inside the scene, is the light baseline rechecked for change of function, visibility, power relation or concealment? | `GATE-CINE-30` | `FAIL-CINE-05Y` | `steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | story-turn light recheck notes and updated `light_narrative_plan` samples |
| Does final `N7` prose write visible lighting results instead of internal enum labels or abstract words such as "cinematic light"? | `GATE-CINE-30` / `GATE-CINE-18` | `FAIL-CINE-05Y` / `FAIL-CINE-05G` | `steps/cinematography-workflow.md#N7-INJECT` | before/after prose samples replacing source/enum words with visible results |
| If light reveals information too early, does the repair coordinate with attention guidance and shot design to delay, conceal or stage the reveal? | `GATE-CINE-31` / `GATE-CINE-30` | `FAIL-CINE-05Z` / `FAIL-CINE-05Y` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | suspense-leak repair evidence and delayed-reveal plan |
