# Output Persistence

This reference owns save-path and final asset persistence rules for built-in `image_gen` execution.

## Built-In Save-Path Policy

- Built-in `image_gen` saves generated images under `$CODEX_HOME/*` by default.
- Do not describe or rely on OS temp as the built-in default destination.
- Do not describe or rely on a destination-path argument on the built-in `image_gen` tool.
- If a specific location is needed, generate first and then move or copy the selected output from `$CODEX_HOME/generated_images/...`.

Save-path precedence in built-in mode:

1. If the user names a destination, move or copy the selected output there.
2. If the image is meant for the current project, move or copy the final selected image into the workspace before finishing.
3. If the image is only for preview or brainstorming, render it inline; the underlying file can remain at the default `$CODEX_HOME/*` path.

Never leave a project-referenced asset only at the default `$CODEX_HOME/*` path.

## Associated Project Directory Policy

- When the request is tied to `projects/aigc/<project>/`, `projects/story/<project>/`, `projects/comic/<project>/`, or another discoverable project root, the final image must be transferred into the related project directory or the user-named destination inside that project.
- For generated derivatives of existing project assets, prefer a sibling output directory or clearly named derivative directory under the same workflow area unless the user provided a more specific destination.
- In subagent batch mode, each worker may return the built-in generated source path, but the parent task is responsible for gathering every worker result and copying or moving selected finals into the associated project directory before closeout.
- A subagent-local path, default `$CODEX_HOME/generated_images/...` path, or thread-only preview is evidence of generation, not a project deliverable.

## Workspace Naming

- Do not overwrite an existing asset unless the user explicitly asked for replacement.
- Create descriptive sibling filenames when replacing is not explicit, such as `hero-v2.png`, `item-icon-edited.png`, or `cutout-alpha.png`.
- For batches, persist every requested final deliverable unless the user explicitly asked for preview-only outputs.
- For subagent batches, assign disjoint final filenames before dispatch when practical; otherwise the parent must normalize names during gather to avoid collisions.
- Discarded variants do not need to be kept unless requested.

## Final Report Requirements

Every completed imagegen task should report:

- execution mode: built-in `image_gen`, transparent chroma-key post-process, or blocked non-built-in route;
- batch execution shape when relevant: subagents parallel with max concurrency 10, or explicit user-requested main-thread serial;
- saved path(s) for any workspace-bound asset(s);
- final prompt or prompt set;
- whether transparent output was validated when requested;
- any residual risk, such as imperfect text rendering or built-in tool limitations.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Are project-bound or user-named outputs persisted outside default generated paths? | Workspace/project asset remains only under `$CODEX_HOME/*` or subagent-local path fails | `FAIL-IMG-PERSISTENCE` | `SKILL.md#thinking-action-node-map` / `N7-PERSIST` | saved path audit and associated project transfer note |
