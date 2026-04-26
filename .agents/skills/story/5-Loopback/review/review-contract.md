# Loopback Review Contract

This review gate verifies that `5-Loopback` remains a Skill 2.0 package and that a loopback run respects validated actualization boundaries.

## Default Provider

- Default provider: `code-reviewer`
- In this repository, a user request to enable subagents or a skill contract that explicitly defaults to reviewer dispatch authorizes real subagent review unless blocked by higher-priority policy.
- If provider or subagent dispatch is blocked, report the blocking layer, planned path, actual fallback, and skipped reviewers.

## Review Dimensions

| dimension | checks |
| --- | --- |
| `gate` | `PASS + handoff granted` is enforced, not replaced by PASS-only |
| `truth_ownership` | Cards, planning sidecars, story_map, STATE, and artifact boundaries are respected |
| `delta` | deltas use whitelist and validated evidence only |
| `commit` | writeback is staged first and committed serially |
| `satellite` | query/resume/source repair requests are not disguised as loopback artifacts |
| `template` | `templates/loopback.json` and `templates/output-template.md` align with `SKILL.md` Output Contract |
| `structure` | canonical Skill 2.0 dirs and root files exist |
| `scripts` | scripts perform mechanical writeback and validation, not creative or validation judgment |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | package or run is deliverable |
| `pass_with_followups` | deliverable with non-blocking follow-ups |
| `needs_rework` | blocking issue must be fixed before delivery |
| `blocked` | missing input, missing permission, or upstream source unavailable |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: gate | truth_ownership | delta | commit | satellite | template | structure | scripts
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Completion Checklist

- validation aggregate gate is legal
- normalized delta contains at least one valid actualization or projection refresh
- revision guards pass
- pending marker is created before truth writeback
- writeback order is `Cards -> Planning sidecars -> MAP -> STATE -> artifact`
- pending marker is removed or converted into a committed manifest
- artifact can point to validation and governance evidence
- no query/resume output impersonates loopback artifact
