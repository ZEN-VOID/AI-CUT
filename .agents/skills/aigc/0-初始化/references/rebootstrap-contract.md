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

`0-初始化` owns:

- recomputing `north_star`
- rewriting `init_handoff`
- lowering the active project entry back to `0-初始化`
- judging preserve/archive/purge scope
- re-locking `smart_advisor` and `auto/custom`

`resume/` owns:

- safe continuation from current truth
- governance-gap repair
- last-stable-entry reconstruction

## Reset Modes

| mode | default | purpose | default preserve | default forbidden |
| --- | --- | --- | --- | --- |
| `refresh_reset` | no | rewrite initialization core and mark old downstream artifacts stale without moving files | `源/`, legacy `Original/`, source, original assets, references, existing downstream files | treating old downstream outputs as active truth |
| `archive_reset` | yes | archive old downstream derived outputs and old governance artifacts under `0-初始化/rebootstrap-archive/<timestamp>/`, then rewrite init core | `源/`, legacy `Original/`, source, original assets, necessary references | silent clearing, overwriting irreplaceable materials |
| `purge_reset` | explicit only | purge specified derived artifacts after preserve/archive confirmation | `源/`, legacy `Original/`, source, original assets unless explicitly discarded | unauthorized deletion or using Git reset as business reset |

## Preservation Rules

1. Keep `源/`, legacy `Original/`, and registered source by default.
2. Keep original materials, reference images, external research, and irreplaceable assets.
3. Keep and update `story-source-manifest.yaml` rather than discarding source readiness.
4. Archive derived outputs from downstream stages and old governance carriers by default.
5. Keep `team.yaml` unless the team or advisor duties are part of the reset.

## Writeback Rules

Every rebootstrap rewrites at least:

- `0-初始化/north_star.yaml`
- `0-初始化/init_handoff.yaml`
- `STATE.json`

If the team changed, rewrite `team.yaml`.

`STATE.json` must set the active entry back to `0-初始化` until the new sufficiency gate passes.

If `governance-state.yaml` exists or is triggered, write `reset_bridge`:

- `last_reset_at`
- `reset_mode`
- `reset_reason`
- `preserved_paths`
- `archived_paths`
- `stale_paths`

Old `preflight-verdict.yaml`, `validation-report.md`, and `learning-record.md` may not continue as current gates after reset.

## Hard Rules

1. Explicit "back to initialization" requests route to `0-初始化`, not `resume/`.
2. Default `reset_mode` is `archive_reset`.
3. Rebootstrap is not Git rollback.
4. The new cycle still returns to `N1-mode-gate`; do not silently reuse a previous lineup.
5. Old downstream seeds do not feed the next `1-分集` cycle unless they are explicitly revalidated.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does an explicit "return to initialization / rebuild north star / discard current direction" request route to `0-初始化`, while continuation, governance repair, or checkpoint reconstruction routes to `resume/` instead? | `FIELD-INIT-08` | `FAIL-INIT-08` | `steps/init-workflow.md` `N0-intake`; `SKILL.md` `When Not to Use`; this file's `Trigger` and `Ownership Boundary` sections | Review report cites the user reset wording, existing project state, chosen route, and any ambiguity that required clarification. |
| Is the reset mode resolved as `archive_reset` by default, with `refresh_reset` or `purge_reset` used only when their scope is explicit and safe? | `FIELD-INIT-08` | `FAIL-INIT-08` | `steps/init-workflow.md` `N0-intake` and `N6-lazy-governance`; this file's `Reset Modes` section | Review report records `reset_mode`, reset reason, explicit purge or refresh authorization if any, and the archive or stale-marking plan. |
| Are `源/`, legacy `Original/`, registered source, original assets, reference images, research, and irreplaceable materials preserved by default, with destructive purge blocked without explicit authorization? | `FIELD-INIT-08` | `FAIL-INIT-08` | `steps/init-workflow.md` `N6-lazy-governance` and `N7-internal-audit`; this file's `Preservation Rules` section | Review report lists preserved paths, archived paths, stale paths, requested purge paths, and any blocked unsafe deletion. |
| Does every rebootstrap rewrite `north_star.yaml`, `init_handoff.yaml`, and `STATE.json`, update `team.yaml` only when the team changed, and set active entry back to `0-初始化` until sufficiency passes? | `FIELD-INIT-08` | `FAIL-INIT-08` | `steps/init-workflow.md` `N5-synthesis`, `N6-lazy-governance`, and `N7-internal-audit`; this file's `Writeback Rules` section | Review report cites the rewritten artifact paths, `STATE.json` active entry, team-change decision, and sufficiency status after reset. |
| If `governance-state.yaml` exists or is triggered, does it write `reset_bridge` and prevent old `preflight-verdict.yaml`, `validation-report.md`, or `learning-record.md` from continuing as current gates? | `FIELD-INIT-08` | `FAIL-INIT-08` | `steps/init-workflow.md` `N6-lazy-governance`; this file's `Writeback Rules` section | Review report records `reset_bridge.last_reset_at`, reset mode, preserved/archived/stale paths, and any old gate files demoted from active status. |
| Does the new cycle return to `N1-mode-gate` without silently reusing the previous lineup, and are old downstream seeds excluded from the next `1-分集` cycle unless revalidated? | `FIELD-INIT-08` | `FAIL-INIT-08` | `steps/init-workflow.md` `N1-mode-gate`, `N5-synthesis`, and `N7-internal-audit`; this file's `Hard Rules` section | Review report records the new lineup decision state, revalidated seed list if any, and any stale downstream seed blocked from active flow. |
| Does this reference itself keep every mandatory rebootstrap rule bound to a review gate, fail code, rework target, and report evidence row? | `FIELD-INIT-10` | `FAIL-INIT-10` | This `Review Gate Mapping` section; `review/init-review-gate.md`; `steps/init-workflow.md` | Maintenance report enumerates this file in the reference gate coverage list and confirms trigger, reset mode, preservation, writeback, and hard-rule coverage. |
