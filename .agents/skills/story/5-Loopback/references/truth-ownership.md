# Truth Ownership

This file expands the owner boundary summarized in `SKILL.md`.

## Owned By 5-Loopback

- `PASS + handoff granted` intake gate enforcement
- volume-level `loopback_delta` normalization
- Cards `current_state/history` validated actualization
- planning `.actualization.json` sidecars for book, volume, and chapters
- story_map slice actualization details
- root story_map actualization summary/index
- `STATE.json` projection refresh and runtime markers
- `projects/story/<项目名>/5-Loopback/第V卷.loopback.json`
- route judgment for query/resume shaped loopback requests

## Not Owned By 5-Loopback

- changing `validation_status`
- changing `routing_decision` or `handoff_targets`
- producing official review reports
- editing `3-Drafting` manuscript bodies
- overwriting `Cards.core`
- overwriting planning `planned_*`
- changing project genre/type cards
- treating runtime projections as validation evidence

## Truth Split

| question | canonical layer |
| --- | --- |
| What is an object like now? | `Cards.current_state/history` |
| Which planned promise has been actually fulfilled? | planning `.actualization.json` sidecars and story_map actualization |
| What can the next runtime step consume quickly? | `STATE.json` projections |
| What was written in this loopback run? | `5-Loopback/第V卷.loopback.json` |

## Source Repair Rule

If the target truth is wrong because an upstream source is wrong, do not patch over it in loopback. Route to the owner stage:

- seed or project covenant: `0-Init`
- object truth: `1-Cards`
- plan truth: `2-Planning`
- manuscript truth: `3-Drafting`
- validation judgment: `4-Review`
- review persistence: `review/`
