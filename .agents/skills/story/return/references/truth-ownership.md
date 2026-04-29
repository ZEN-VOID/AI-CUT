# Truth Ownership

This file expands the owner boundary summarized in `SKILL.md`.

## Owned By context-return

- `PASS + handoff granted` intake gate enforcement
- volume-level `context_return_delta` normalization
- Cards `current_state/history` validated actualization
- planning `.actualization.json` sidecars for book, volume, and chapters
- story_map slice actualization details
- root story_map actualization summary/index
- `STATE.json` projection refresh and runtime markers
- `projects/story/<项目名>/context-return/第V卷.context-return.json`
- route judgment for query/resume shaped 上下文回流 requests

## Not Owned By context-return

- changing `validation_status`
- changing `routing_decision` or `handoff_targets`
- producing official review reports
- editing `3-初稿` manuscript bodies
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
| What was written in this context return run? | `context-return/第V卷.context-return.json` |

## Source Repair Rule

If the target truth is wrong because an upstream source is wrong, do not patch over it in 上下文回流. Route to the owner stage:

- seed or project covenant: `0-初始化`
- object truth: `1-设定`
- plan truth: `2-卷章`
- manuscript truth: `3-初稿`
- validation judgment: `review`
- review persistence: `review/`
