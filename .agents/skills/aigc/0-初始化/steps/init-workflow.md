# Init Workflow

This file owns the thinking-action node network for `$aigc-init`.

## Topology Fit

The main topology is serial with one controlled branch:

`N0 -> N1 -> N2 -> N3 -> N4(auto|custom) -> N5 -> N6 -> N7`

Only `N4` branches. All branches converge before synthesis and audit.

## Node Schema

Each node must define:

| slot | meaning |
| --- | --- |
| `node_id` | stable node identifier |
| `objective` | judgment and action objective |
| `inputs` | context, files, upstream decisions |
| `actions` | actual work |
| `evidence` | artifact, note, command, or conclusion left behind |
| `route_out` | success, failure, branch, and reentry route |
| `gate` | whether final writeback may proceed |
| `decision_lock` | decisions fixed by this node |
| `dispatch_contract` | subagent ownership and downgrade policy |
| `write_scope` | patches or files allowed |
| `blocker_rule` | when to stop |
| `reentry_rule` | where to return when upstream information changes |

## Node Semantics

| node_id | decision_lock | dispatch_contract | write_scope | blocker_rule | reentry_rule |
| --- | --- | --- | --- | --- | --- |
| `N0-intake` | `project_scope`, `rebootstrap_requested` | no subagents | `project_scope_note`, `reset_intent_note`, `task_entry_decision` | stop if the task cannot be classified as init, rebootstrap, resume, or query | user clarification returns to `N0` |
| `N1-mode-gate` | `init_mode == smart_advisor`, `team_lineup_mode`, `decision_owner` | no subagents | `mode_lock_note`, option card, `lineup_mode_decision` | stop until `auto/custom` is locked | lineup change returns to `N1` |
| `N2-runtime-bootstrap` | `project_root`, canonical runtime layout | no subagents | directory skeleton, project `MEMORY.md`, project `CONTEXT/`, project `CHANGELOG.md`, `runtime_bootstrap_note` | stop if project path conflicts with shared layout | project name/layout change returns to `N2` |
| `N3-internal-router` | `selector_scope_root`, `team_context_budget`, `story_source_status` | no subagents | `route_plan_patch`, `context_packet_plan`, `team_context_packet` | stop if candidate advisors leave `.agents/skills/team/` or source state is unknown | new candidates/source data return to `N3` |
| `N4-mode-engine` | `team.yaml` draft, `roles.planning.members` roster | real subagents required for `planning_direct_answer_engine`; no local imitation | `team_manifest_patch`, `selection_rationale`, `direct_answer_report`, `north_star_patch`, `init_handoff_patch` | stop if subagents unavailable, roster empty, or roster outside `.agents/skills/team/` | lineup/source/prompt changes return to `N3` or `N4` |
| `N5-synthesis` | `source-light/source-grounded`, artifact ownership split | no new planning subagents | draft core five-piece set | stop if patch provenance is incomplete or team is not locked | patch/source changes return to `N4` or `N5` |
| `N6-lazy-governance` | `governance_trigger_set`, optional `reset_bridge` | no init advisor subagents | optional governance carriers only | do not create carriers for structural completeness alone | governance trigger changes return to `N6` |
| `N7-internal-audit` | `sufficiency_status`, `next_entry_truth` | no subagents | `audit_report`, `reentry_decision`, final writeback approval | stop if source, team, subagent provenance, or next-entry truth is incomplete | fail routes to `N1/N3/N4/N5/N6` by gap |

## Topology Contract

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N0-intake` | classify first init, rebootstrap, or resume/query | user request, project path, existing artifacts | identify task nature and reset intent | `project_scope_note`, `reset_intent_note` | `N1`, or route to `resume/` | no |
| `N1-mode-gate` | lock `smart_advisor` and `auto/custom` | user intent, lineup signal, option card | record mode metadata or show option card | `mode_lock_note`, `lineup_mode_decision` | `N2`; conflict returns to `N1` | no |
| `N2-runtime-bootstrap` | create runtime skeleton | project name, shared runtime layout | create roots, active skeleton, `MEMORY.md`, `CONTEXT/`, `CHANGELOG.md` | `runtime_bootstrap_note`, path check | `N3` | no |
| `N3-internal-router` | reduce context to needed route/team/source packet | locked mode, current gaps, budget | build route and team context packets | `route_plan_patch`, scope check, source note | `N4`; missing mode returns to `N1` | no |
| `N4-mode-engine` | lock team and run planning direct-answer packet | router packet, templates, team candidates | run one lineup path, then planning direct-answer subagents | team patch, roster, direct-answer report | `N5`; blocked returns to `N1/N3` | no |
| `N5-synthesis` | synthesize five-piece set | team patch, direct-answer patch, templates, shared contracts | draft team/source/north-star/handoff/state | `artifact_patch_set`, provenance note | `N6` | conditional |
| `N6-lazy-governance` | add optional governance only when triggered | core five-piece, governance triggers | draft sidecars and reset bridge if needed | governance patch set, trigger note | `N7` | conditional |
| `N7-internal-audit` | verify sufficiency and next-entry alignment | all drafts, review rules, source layers | audit and decide writeback or reentry | `audit_report`, `reentry_decision` | writeback or reenter failed node | yes |

## Ordered And Unordered Rules

- `N1 -> N2 -> N3 -> N4 -> N5 -> N6 -> N7` is fixed.
- `N4` may choose exactly one subpath: auto lineup or custom lineup.
- After `team.yaml` is locked, `roles.planning.members` run the first direct-answer packet.
- `监制` and `评审` do not replace the initialization planning owner.
- Parent skill performs final synthesis; advisor packets are local deltas, not parallel main drafts.
- Nodes that change route, ownership, or required fields must update `SKILL.md`, `review/init-review-gate.md`, and any relevant template in the same task.

## Reentry Rules

| finding | reentry |
| --- | --- |
| ambiguous `auto/custom` | `N1` |
| advisor outside `.agents/skills/team/` | `N3` |
| planning roster empty or subagents blocked | `N4` |
| provenance missing from artifact patches | `N5` |
| source-light story overclaim | `N5` plus `references/artifacts-and-sources.md` |
| reset trace missing | `N6` |
| multiple next entries | `N7` then `N5` |
