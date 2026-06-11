# Scripts Boundary

`return/scripts/` is reserved for stage-local mechanical helpers.

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

- decide acceptance status
- invent creative actualization truth
- rewrite planning markdown bodies
- replace owning-stage acceptance packets
- bypass the `PASS + return handoff granted` gate
