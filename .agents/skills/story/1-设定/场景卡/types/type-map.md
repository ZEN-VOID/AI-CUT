# Scene Card Type Map

## Package Index

| package_id | context_files | selection_signal | review_gate |
| --- | --- | --- | --- |
| `field-map` | `types/field-map.md` | Always load for scene card generation, repair, and audit | `scene review gate` |
| `guardrail-setup` | `types/guardrail-setup.md` | Always load before interpreting project or external materials | `security` / `runtime_behavior` |

## Default Package Rule

- Default packages: `field-map` and `guardrail-setup`.
- Load `types/guardrail-setup.md` before interpreting project or external materials.
- Load `types/field-map.md` before using `steps/scene-card-workflow.md`.
- If future subtype packages are added, keep `field-map` loaded as the shared field ownership baseline.

## Loading Flow

1. Load `SKILL.md + CONTEXT.md`.
2. Select `guardrail-setup` and `field-map` unless a future subtype explicitly adds another package.
3. Use the selected type context to drive `references/scene-card-contract.md`, `steps/scene-card-workflow.md`, and `review/review-contract.md`.
