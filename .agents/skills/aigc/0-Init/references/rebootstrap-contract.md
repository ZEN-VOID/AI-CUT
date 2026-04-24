# Rebootstrap Contract

This file owns reset-style reinitialization for `$aigc-init`.

## Trigger

Use rebootstrap when an existing project has initialization or downstream artifacts, and the user clearly wants to:

- return to initialization state
- rebuild the north star
- discard the current direction
- keep the project shell but restart creative direction

Do not use rebootstrap for continuing the current direction, repairing governance, or reconstructing a checkpoint. Those route to `resume/`.

## Ownership Boundary

`0-Init` owns:

- recomputing `north_star`
- rewriting `init_handoff`
- lowering the active project entry back to `0-Init`
- judging preserve/archive/purge scope
- re-locking `smart_advisor` and `auto/custom`

`resume/` owns:

- safe continuation from current truth
- governance-gap repair
- last-stable-entry reconstruction

## Reset Modes

| mode | default | purpose | default preserve | default forbidden |
| --- | --- | --- | --- | --- |
| `refresh_reset` | no | rewrite initialization core and mark old downstream artifacts stale without moving files | `Story/`, source, original assets, references, existing downstream files | treating old downstream outputs as active truth |
| `archive_reset` | yes | archive old downstream derived outputs and old governance artifacts under `0-Init/rebootstrap-archive/<timestamp>/`, then rewrite init core | `Story/`, source, original assets, necessary references | silent clearing, overwriting irreplaceable materials |
| `purge_reset` | explicit only | purge specified derived artifacts after preserve/archive confirmation | `Story/`, source, original assets unless explicitly discarded | unauthorized deletion or using Git reset as business reset |

## Preservation Rules

1. Keep `Story/` and registered source by default.
2. Keep original materials, reference images, external research, and irreplaceable assets.
3. Keep and update `story-source-manifest.yaml` rather than discarding source readiness.
4. Archive derived outputs from `1-Planning` through `7-Cut` and old governance carriers by default.
5. Keep `team.yaml` unless the team or advisor duties are part of the reset.

## Writeback Rules

Every rebootstrap rewrites at least:

- `0-Init/north_star.yaml`
- `0-Init/init_handoff.yaml`
- `STATE.json`

If the team changed, rewrite `team.yaml`.

`STATE.json` must set the active entry back to `0-Init` until the new sufficiency gate passes.

If `governance-state.yaml` exists or is triggered, write `reset_bridge`:

- `last_reset_at`
- `reset_mode`
- `reset_reason`
- `preserved_paths`
- `archived_paths`
- `stale_paths`

Old `preflight-verdict.yaml`, `validation-report.md`, and `learning-record.md` may not continue as current gates after reset.

## Hard Rules

1. Explicit "back to initialization" requests route to `0-Init`, not `resume/`.
2. Default `reset_mode` is `archive_reset`.
3. Rebootstrap is not Git rollback.
4. The new cycle still returns to `N1-mode-gate`; do not silently reuse a previous lineup.
5. Old downstream seeds do not feed the next `1-Planning` cycle unless they are explicitly revalidated.
