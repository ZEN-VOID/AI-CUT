# Scripts Boundary

`context-return/scripts/` is reserved for stage-local mechanical helpers.

Current mechanical execution is shared at the story root:

- `../scripts/context_return_manager.py`
- `../scripts/workflow_manager.py`

These scripts may:

- load JSON files
- validate required fields and revisions
- compute and apply staged patches
- write manifests and artifacts
- report status

They must not:

- decide validation status
- invent creative actualization truth
- rewrite planning markdown bodies
- replace `review/` reports
- bypass the `PASS + handoff granted` gate
