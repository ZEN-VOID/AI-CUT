# Review Contract

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-ROUTE` | 视频任务只路由到一个子技能 | `FAIL-VIDEO-ROUTE` | `types/type-map.md` |
| `G2-RUNTIME` | 输出根位于 `projects/aigc/<项目名>/7-视频/` | `FAIL-VIDEO-RUNTIME` | `references/video-stage-runtime.md` |
| `G3-CHILD` | 子技能 review verdict 通过或有非阻断 TODO | `FAIL-VIDEO-HANDOFF` | owning child review |
| `G4-LEGACY` | legacy `6-Video` 只作为兼容回读 | `FAIL-VIDEO-RUNTIME` | registry / route policy |
