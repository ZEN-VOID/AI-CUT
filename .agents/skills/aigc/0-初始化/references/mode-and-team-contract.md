# Mode And Team Legacy Note

This reference is inactive for current `$aigc-init` execution.

Current initialization has no `smart_advisor`, `auto/custom`, team lineup, planning direct-answer packet, or `team.yaml` writeback. It creates the project scaffold directories, project `MEMORY.md`, and project `CONTEXT/README.md`. If the user specifies team configuration, collaborators, reviewers, creative viewpoints, or team exclusions during initialization, those details are absorbed into project `MEMORY.md` under the centralized memory contract.

If a future workflow needs executable team selection or advisor synthesis, that workflow must declare its own active module loading, review gate, and output contract. It must still treat project `MEMORY.md` as the first source for user-specified team preferences and must not infer team runtime behavior from this historical note.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does initialization avoid team mode locks and `team.yaml` generation while preserving user-specified team context in `MEMORY.md`? | `FIELD-INIT-05` / `FIELD-INIT-09` | `FAIL-INIT-05` / `FAIL-INIT-09` | `SKILL.md` `Output Contract`; `steps/init-workflow.md`; `templates/project-memory.template.md` | Final readback confirms no `team.yaml` was created and memory captured or explicitly marked team context as N/A. |
