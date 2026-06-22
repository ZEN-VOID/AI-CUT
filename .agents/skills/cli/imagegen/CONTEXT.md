# Context: imagegen

This file is the runtime knowledge layer for `imagegen`. It stores reusable heuristics and failure repairs, not the authoritative execution contract.

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-field-notes-targeted
last_checked_at: 2026-04-24
```

## Type Map

| type_id | trigger symptom | root layer | immediate repair | prevention | validation point |
| --- | --- | --- | --- | --- | --- |
| `TM-IMG-01` | Ordinary image task tries to use CLI/API | mode routing | Stop and return to built-in `image_gen`; if impossible, report unsupported route | `SKILL.md` and `references/mode-routing.md` define imagegen as built-in only | No `OPENAI_API_KEY` is requested by this skill |
| `TM-IMG-02` | User says "batch" and execution jumps to CLI `generate-batch` or slow main-thread serial work | batch semantics | Treat as built-in `image_gen` subagent parallel fan-out, one task per distinct asset or explicit variant, max concurrency 10 | Keep batch wording separate from non-built-in tooling and make subagents the default batch topology in `SKILL.md` nodes | Distinct assets have distinct built-in prompts/calls; execution shape records subagents parallel or explicit user-requested serial |
| `TM-IMG-12` | Skill 2.0 validator rejects `steps/`, missing `test-prompts.json`, missing runtime-spine sections, or missing reference gate mappings | runtime-spine migration layer | Move node truth into `SKILL.md`, delete `steps/`, add evaluation prompts, and give each reference `Review Gate Mapping` or a no-independent-gate marker | Keep `SKILL.md` as the single executable spine and treat modules as authorized support only | `validate_skill_2_0.py --mode delivery` and `smoke_test_skill_2_0.py --mode delivery` pass |
| `TM-IMG-03` | Transparent request silently downgrades to `gpt-image-1.5` | provider drift | Use built-in chroma-key path or report limitation | No hidden CLI/API fallback under this skill | No `gpt-image-1.5` or API path used |
| `TM-IMG-04` | Project code references image still in `$CODEX_HOME/generated_images` or subagent-only output path | persistence | Copy/move selected final into the associated project directory | Run output persistence gate before closeout and parent-gather every subagent output | Reported path is under workspace/project directory |
| `TM-IMG-05` | Edit drifts identity, layout, or unchanged regions | edit invariants | Repeat invariants and make one targeted iteration | Label input roles and locked regions up front | Changed only requested elements |
| `TM-IMG-06` | In-image text is misspelled or extra words appear | text rendering | Re-prompt with exact quoted text and typography/placement | Treat text-heavy images as high-risk review items | Text matches verbatim request |
| `TM-IMG-07` | Chroma-key removal leaves colored halo or opaque corners | alpha post-process | Retry helper with tuned thresholds or edge contraction | Choose key color outside subject and forbid shadows | Alpha channel and transparent corners verified |
| `TM-IMG-08` | Prompt augmentation adds unrelated story elements | prompt specificity | Strip invented details back to user intent | Use allowed/disallowed augmentation table | Prompt only adds material clarifiers |
| `TM-IMG-09` | New image requests drift back to tool auto-size without 2K intent | resolution default | Add 2K target to built-in prompts | Keep review focused on prompt/delivery target | Prompt/report records 2K unless user or upstream set another size |
| `TM-IMG-10` | Upstream skill explicitly requests 4K but imagegen plan/prompt falls back to 2K | upstream resolution override lost | Restore the upstream `resolution_target` in prompt, report, and review notes | Treat `resolution_target: 4K` handoffs as explicit size requests | Prompt/report records 4K target |
| `TM-IMG-11` | Blurred aerial/action frame is blocked by built-in safety as self-harm or violence | safety false positive | Retry once with neutral wardrobe/identity-edit wording and no violence/action verbs | Describe pose, silhouette, costume, atmosphere, and camera only | No CLI/API fallback; output exists or blocker is reported |
| `TM-IMG-13` | Role replacement says a target character was used, but the result does not resemble the target face/costume | weak identity reference binding | Re-run with explicit image role mapping: edit target = composition/action only; target character reference = face, hair, clothing, identity. Prefer a cropped face reference plus costume/reference sheet and record `reference_input_status` | For identity-critical edits, never rely on a character name alone or a single mixed prompt; require per-task role mapping and visible reference evidence | Report includes edit target path/node, identity reference path/node, costume reference path/node, visible status, and identity review verdict |
| `TM-IMG-14` | Built-in edit of a cinematic martial/action frame returns an unrelated infographic or explanatory design | built-in route drift after safety/intent confusion | Do not persist the unrelated output. Retry once with neutral visual-edit wording and explicit `no infographic/no text` constraints; if it repeats, report the affected frame as residual risk or use a near-duplicate passed frame only when the source pose is materially equivalent and this reuse is documented | Keep action-frame prompts focused on visual composition, wardrobe, prop posture, lighting, and silhouette; avoid abstract labels that can be interpreted as diagram topics | Report identifies the rejected generated file behavior, retry result, and whether a persisted substitute or blocker was used |

## Repair Playbook

1. If mode choice is wrong, reload `references/mode-routing.md` before doing more work.
2. If output location is wrong, reload `references/output-persistence.md` and copy the selected final into the workspace.
3. If transparency fails, reload `references/transparent-background.md`, validate the alpha channel, and report built-in/chroma-key limitations instead of switching to CLI/API.
4. If prompt quality is weak, reload `references/prompting.md` and `types/type-map.md`, then rebuild the prompt from request type and constraints.
5. If multiple assets were requested, use `SKILL.md` `N4-PROMPT` and `N5-EXECUTE` to create one deliverable per requested asset or explicit variant, then default to subagents parallel fan-out capped at 10. Use main-thread serial execution only when the user explicitly requests it or subagent tooling is unavailable and reported.
6. If no user or upstream resolution was specified, make the 2K target explicit in the prompt or payload before execution.
7. If an upstream skill specifies `resolution_target`, preserve it. For example, storyboard-sheet `resolution_target: 4K` must not be downgraded to the generic 2K default.
8. If CLI/API was about to be used, stop: it is outside `.agents/skills/cli/imagegen` as now defined.
9. If built-in safety blocks a blurred martial/cinematic frame, retry with neutral wording such as "costume-and-character-design replacement", "airborne silhouette", "pose", "movement impression", and "wardrobe/identity edit"; avoid attack, weapon, injury, duel, or fight wording.
10. If a role replacement does not resemble the target character, treat it as an identity-binding failure first. Check whether the target reference image was visible, whether the prompt assigned it `character_identity_reference`, whether the source frame was accidentally allowed to preserve original face/clothing, and whether subject classification was ambiguous.
11. If built-in output turns a martial/action edit into an unrelated infographic or explanatory design, treat it as route drift: do not save it into the project, retry once with neutral visual-edit wording, and if it repeats, document the residual risk instead of fabricating completion.
12. Before final delivery, run `review/review-contract.md` and record the verdict in the response or report.
13. When maintaining package structure, do not recreate `steps/`; keep node tables, branch routes, gates, and Mermaid topology in `SKILL.md`, with long details in authorized references only.

## Reusable Heuristics

- Built-in `image_gen` is the only execution path for this skill because it avoids API-key, network, and model-parameter ambiguity.
- Default image work should target 2K unless the user or upstream skill specifies a different resolution; the built-in path expresses this in the prompt.
- Upstream skill handoffs can be resolution authorities. A parent workflow that passes `resolution_target: 4K` is equivalent to an explicit user size request for this skill.
- CLI/API/model-specific needs, masks, direct file-path controls, and true native transparency are outside this skill's single built-in route; report the boundary instead of falling back.
- Treat project persistence as part of image generation, not cleanup. An image used by repo code is not done until it lives in the workspace.
- Treat associated-project transfer as part of completion. A subagent or `$CODEX_HOME/generated_images/...` output is not final until the parent task has placed the selected image into the related project directory.
- For batch image work, subagents are the default scaling topology. Cap active workers at 10, give each worker a disjoint task/output name, and let the parent gather, persist, and review.
- Runtime-spine validation treats `steps/` as unsupported for this package. If old workflow detail is needed, migrate it into `SKILL.md` node rows or an authorized reference that does not own node truth.
- For edits, role labeling is the cheapest way to prevent reference images from becoming edit targets.
- For role replacement, the original frame should usually be composition/action/lighting only; the target character reference should be the only face, hair, costume, and identity source. If the target reference is a full character sheet with small face crops, add or crop a face close-up when likeness matters.
- Transparent backgrounds are a two-stage asset pipeline: keyed source first, alpha result second. The keyed source is evidence, not the final cutout.
- Prompt augmentation should clarify the user's intent. It should not quietly become art direction the user never asked for.
- Exact text in images is a review-risk item; quote it and inspect it before claiming success.
