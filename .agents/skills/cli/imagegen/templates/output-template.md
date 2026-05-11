# Imagegen Output Template

Use this template when a task needs a structured delivery note, report, sidecar summary, or handoff record.

## Output Contract Alignment

| Output Contract field | This template field |
| --- | --- |
| Required output | `deliverables` |
| Output format | `format` and `mode` |
| Output path | `saved_paths` |
| Naming convention | `naming_notes` |
| Completion gate | `review_verdict` and `validation` |

## Template

```yaml
imagegen_result:
  mode: built_in_image_gen | transparent_chroma_key | cli_fallback
  deliverables:
    - label: ""
      format: png | jpeg | webp | gif
      saved_path: ""
      source_path: ""
  prompt:
    use_case: ""
    final_prompt: ""
    input_roles: []
    resolution_target: 2k_default | explicit_user_or_upstream | model_limited_default
    resolution_value: 2K | 4K | WIDTHxHEIGHT | auto
  naming_notes: ""
  validation:
    visual_quality: pass | pass_with_todo | needs_rework | blocked
    resolution: pass | pass_with_todo | needs_rework
    transparency: not_applicable | pass | pass_with_todo | needs_rework
    text_accuracy: not_applicable | pass | pass_with_todo | needs_rework
    persistence: pass | needs_rework
  review_verdict: pass | pass_with_todo | needs_rework | blocked
  residual_risks: []
```
