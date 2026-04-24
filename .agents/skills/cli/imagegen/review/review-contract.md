# Review Contract

This file owns final quality gates for imagegen tasks.

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | Image deliverable is ready and all required persistence/quality checks passed |
| `pass_with_todo` | Deliverable is usable, with explicitly reported non-blocking risks |
| `needs_rework` | Blocking mismatch, missing file, wrong route, or failed transparency/text/invariant gate |
| `blocked` | Missing user input, tool unavailable, or unconfirmed CLI/API fallback |

## Required Checks

| dimension | checks |
| --- | --- |
| mode | Built-in used by default; CLI fallback was explicitly requested or confirmed |
| intent | Generated vs edited image matches the request |
| input_roles | Edit target, reference image, and supporting image roles are not confused |
| prompt | Prompt preserves user intent and avoids invented unrelated objects or copy |
| visual_quality | Subject, style, composition, lighting, and key constraints are plausible |
| resolution | Default 2K target was requested or an explicit user/model-limited size was honored |
| text | Exact requested text is quoted in prompt and visually checked when present |
| invariants | Edit changes only requested elements and preserves locked regions |
| transparency | Alpha output has alpha channel, transparent corners, and no obvious key fringe |
| persistence | Project-bound finals are copied/moved into workspace and not only `$CODEX_HOME/*` |
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
  dimension: mode | prompt | visual_quality | resolution | text | invariants | transparency | persistence | naming
  symptom: ""
  direct_cause: ""
  rework_target: ""
```

## Completion Gate

Do not declare completion when:

- the selected image file cannot be located;
- project-bound output remains only under `$CODEX_HOME/generated_images/...`;
- transparent output lacks alpha or has opaque corners;
- CLI fallback was used without explicit opt-in;
- exact text or edit invariants visibly fail;
- final response omits saved path(s) for workspace-bound assets.
