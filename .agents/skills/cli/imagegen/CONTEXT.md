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
| `TM-IMG-01` | Ordinary image task tries to use CLI/API by default | mode routing | Return to built-in `image_gen` route | Keep CLI fallback opt-in in `SKILL.md` and `references/mode-routing.md` | No `OPENAI_API_KEY` needed for normal tasks |
| `TM-IMG-02` | User says "batch" and execution jumps to CLI `generate-batch` | batch semantics | Treat as repeated built-in calls unless CLI was explicit | Keep batch wording separate from CLI opt-in | Distinct assets have distinct prompts/calls |
| `TM-IMG-03` | Transparent request silently downgrades to `gpt-image-1.5` | transparency fallback | Ask before true CLI transparency | Built-in chroma-key path remains default | User confirmed CLI/API/model path |
| `TM-IMG-04` | Project code references image still in `$CODEX_HOME/generated_images` | persistence | Copy/move selected final into workspace | Run output persistence gate before closeout | Reported path is under workspace |
| `TM-IMG-05` | Edit drifts identity, layout, or unchanged regions | edit invariants | Repeat invariants and make one targeted iteration | Label input roles and locked regions up front | Changed only requested elements |
| `TM-IMG-06` | In-image text is misspelled or extra words appear | text rendering | Re-prompt with exact quoted text and typography/placement | Treat text-heavy images as high-risk review items | Text matches verbatim request |
| `TM-IMG-07` | Chroma-key removal leaves colored halo or opaque corners | alpha post-process | Retry helper with tuned thresholds or edge contraction | Choose key color outside subject and forbid shadows | Alpha channel and transparent corners verified |
| `TM-IMG-08` | Prompt augmentation adds unrelated story elements | prompt specificity | Strip invented details back to user intent | Use allowed/disallowed augmentation table | Prompt only adds material clarifiers |
| `TM-IMG-09` | New image requests drift back to tool auto-size without 2K intent | resolution default | Add 2K target to built-in prompts or CLI payload | Keep `gpt-image-2` CLI default at `2048x1152` and review resolution target | Prompt/payload records 2K unless user or upstream set another size |
| `TM-IMG-10` | Upstream skill explicitly requests 4K but imagegen plan/prompt falls back to 2K | upstream resolution override lost | Restore the upstream `resolution_target` in prompt, payload, report, and review notes | Treat `resolution_target: 4K` handoffs as explicit size requests | Prompt/payload records 4K or a valid 4K size |

## Repair Playbook

1. If mode choice is wrong, reload `references/mode-routing.md` before doing more work.
2. If output location is wrong, reload `references/output-persistence.md` and copy the selected final into the workspace.
3. If transparency fails, reload `references/transparent-background.md`, validate the alpha channel, and ask before CLI true transparency.
4. If prompt quality is weak, reload `references/prompting.md` and `types/type-map.md`, then rebuild the prompt from request type and constraints.
5. If multiple assets were requested, ensure `steps/execution-workflow.md` has one deliverable per requested asset or explicit variant.
6. If no user or upstream resolution was specified, make the 2K target explicit in the prompt or payload before execution.
7. If an upstream skill specifies `resolution_target`, preserve it. For example, storyboard-sheet `resolution_target: 4K` must not be downgraded to the generic 2K default.
8. If CLI was used, confirm the user explicitly opted into CLI/API/model controls and record the command/result path.
9. Before final delivery, run `review/review-contract.md` and record the verdict in the response or report.

## Reusable Heuristics

- Built-in `image_gen` is the default path because it avoids API-key, network, and model-parameter drift for normal image work.
- Default image work should target 2K unless the user or upstream skill specifies a different resolution; the built-in path expresses this in the prompt, while CLI `gpt-image-2` uses `2048x1152`.
- Upstream skill handoffs can be resolution authorities. A parent workflow that passes `resolution_target: 4K` is equivalent to an explicit user size request for this skill.
- CLI fallback is a precision path, not a quality upgrade switch. Use it for explicit CLI/API/model needs, masks/file-path controls, or user-confirmed true transparency.
- Treat project persistence as part of image generation, not cleanup. An image used by repo code is not done until it lives in the workspace.
- For edits, role labeling is the cheapest way to prevent reference images from becoming edit targets.
- Transparent backgrounds are a two-stage asset pipeline: keyed source first, alpha result second. The keyed source is evidence, not the final cutout.
- Prompt augmentation should clarify the user's intent. It should not quietly become art direction the user never asked for.
- Exact text in images is a review-risk item; quote it and inspect it before claiming success.
