# Init Type Map

Current `$aigc-init` supports only scaffold-oriented types.

| type | trigger | required input | output |
| --- | --- | --- | --- |
| `new_scaffold` | new AIGC film/video project init | project name and optional memory requirements | current 0-14 directories plus `MEMORY.md` |
| `repair_scaffold` | existing project missing scaffold directories | existing project root | missing current 0-14 directories plus preserved `MEMORY.md` |
| `memory_update` | user provides long-term preference, constraint, exclusion, or special element | project root and memory content | merged `MEMORY.md` |
| `unsafe_reset` | delete, purge, overwrite, or path escape implied | explicit separate destructive scope | blocked by this skill |

Former types such as source-light/source-grounded bootstrap, auto/custom lineup, advisor execution, north-star synthesis, and story-source reconciliation are inactive for scaffold initialization.

## Routing Notes

- Missing project name blocks before writeback.
- Non-AIGC media reroutes to the owning story/comic workflow.
- Stage output generation reroutes to the owning stage skill.
- Empty scaffold directories do not count as completed stage outputs.
