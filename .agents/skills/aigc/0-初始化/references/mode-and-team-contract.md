# Mode And Team Legacy Note

This reference is inactive for current `$aigc-init` execution.

Current initialization has no `smart_advisor`, `auto/custom`, team lineup, planning direct-answer packet, or `team.yaml` writeback. It creates only the project scaffold directories, project `MEMORY.md`, and project `CONTEXT/README.md`.

If a future workflow needs team selection or advisor synthesis, that workflow must declare its own active module loading, review gate, and output contract. Do not infer team runtime behavior from this historical note.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does scaffold initialization avoid team mode locks and `team.yaml` generation? | `FIELD-INIT-05` | `FAIL-INIT-05` | `SKILL.md` `Output Contract`; `steps/init-workflow.md` | Final readback confirms no `team.yaml` was created by initialization. |
