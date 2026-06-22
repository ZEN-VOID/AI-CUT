# Review Contract

This file owns final quality gates for imagegen tasks.

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | Image deliverable is ready and all required persistence/quality checks passed |
| `pass_with_todo` | Deliverable is usable, with explicitly reported non-blocking risks |
| `needs_rework` | Blocking mismatch, missing file, wrong route, or failed transparency/text/invariant gate |
| `blocked` | Missing user input, built-in tool unavailable, or request requires a non-built-in route |

## Required Checks

| dimension | checks |
| --- | --- |
| mode | Built-in `image_gen` was used; no local/API/CLI fallback was used under this skill |
| intent | Generated vs edited image matches the request |
| input_roles | Edit target, reference image, and supporting image roles are not confused |
| prompt | Prompt preserves user intent and avoids invented unrelated objects or copy |
| visual_quality | Subject, style, composition, lighting, and key constraints are plausible |
| batch_execution | Batch/multiple deliverables used subagents parallel fan-out with max concurrency 10 unless the user explicitly requested main-thread serial execution |
| resolution | Default 2K target was requested when no explicit target exists, or an explicit user/upstream/model-limited size was honored |
| text | Exact requested text is quoted in prompt and visually checked when present |
| invariants | Edit changes only requested elements and preserves locked regions |
| transparency | Alpha output has alpha channel, transparent corners, and no obvious key fringe |
| persistence | Project-bound finals are copied/moved into workspace and not only `$CODEX_HOME/*` |
| associated_project | Outputs tied to a project are transferred into the related project directory, not left only in subagent/default generated paths |
| naming | Existing files are not overwritten without explicit replacement intent |
| reporting | Final response includes mode, saved path(s), prompt or prompt set, and residual risk |

## Provider / Reviewer Fallback

The preferred review path is this local checklist. A separate `code-reviewer` or subagent reviewer can be used only when the active session policy and user request allow delegated review. If higher-priority policy blocks real reviewer dispatch, record the downgrade as:

- blocked layer: system/developer/tool/user;
- intended path: external or subagent reviewer;
- actual path: local checklist in this file;
- reviewer not launched.

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: mode | prompt | visual_quality | batch_execution | resolution | text | invariants | transparency | persistence | associated_project | naming
  symptom: ""
  direct_cause: ""
  rework_target: ""
```

## Completion Gate

Do not declare completion when:

- the selected image file cannot be located;
- a batch/multiple task was run serially without explicit user request or reported subagent unavailability;
- a batch/multiple task exceeds 10 concurrent subagent workers;
- project-bound output remains only under `$CODEX_HOME/generated_images/...`;
- associated-project output was not transferred into the related project directory;
- transparent output lacks alpha or has opaque corners;
- local/API/CLI fallback was used under `.agents/skills/cli/imagegen`;
- exact text or edit invariants visibly fail;
- final response omits saved path(s) for workspace-bound assets.
