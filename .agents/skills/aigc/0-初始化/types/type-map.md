# Type Map Index

This file is the Skill 2.0 type package index for `$aigc-init`. It does not replace the concrete subtype package in `init-type-map.md`.

## Package Index

| package | purpose | load when |
| --- | --- | --- |
| `init-type-map.md` | initialization task classification, lineup route, source readiness profile, reset profile, governance profile, and execution profile | every `$aigc-init` call |

## Default Package Rule

Load `init-type-map.md` by default for every invocation of this skill. If future subtype packages are added, select only packages whose routing variables are needed by the current task, then let `steps/init-workflow.md` consume the resulting type profile.

## Loading Flow

1. Load `SKILL.md + CONTEXT.md`.
2. Load this `types/type-map.md` as the package index.
3. Load `types/init-type-map.md` as the default type package.
4. Use the resolved `task_type`, `lineup_type`, `source_profile`, `reset_profile`, `governance_profile`, and `execution_profile` to choose references, steps, and review gates.
