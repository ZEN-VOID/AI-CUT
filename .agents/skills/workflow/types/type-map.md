# Type Package Map

`types/` 保存 `workflow` 的任务类型策略。任务需要分型时，先选择命中的类型包，再形成 `type_profile` 供 `SKILL.md` 的 `Thinking-Action Node Map` 消费。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `live-teaching-default` | `types/default/default.md` | livestream teaching footage, AIGC course recording, screen demo, learning-step guide, no supplied guide, source-derived steps, 1.1x source preprocessing, repeated livestream rounds, full-film source units, pure teaching video, optimized long film, maximized teaching slice quantity, teaching slice series, A/B1-B5/C combination slices, content-boundary slices, visible captions, corrected subtitles, semantic subtitle processing | fallback | `types/default/default.md` | none | none |

## Default Package Rule

- If the user provides raw live teaching material with a learning guide, use `live-teaching-default` and route to `teaching-cut`.
- If the user provides raw live teaching material without a learning guide or course brief, use `live-teaching-default` and route to `source-derived-guide`.
- If the user only asks for analysis or high-light discovery, still use `live-teaching-default` but route to `material-audit`.
- If existing output artifacts are present, form `type_profile` from the manifest first and then route to `render-only` or `repair-review`.
- If multiple unrelated tasks are present, do not guess; route to `ambiguous-batch`.

## Loading Flow

1. Collect user input, default path scan, material list, guide list, output root, and existing manifest.
2. Select the matching package from this index.
3. Load the package file listed in `context_files`.
4. Return to `SKILL.md` and let `Type Routing Matrix` choose nodes.
5. Load sibling skills only through `Peer Skill Routing Matrix`; type packages do not invoke tools directly.

## Anti-Patterns

- Do not let `types/` decide clip order, teaching claims, or completion status.
- Do not store transcripts, source evidence, or project manifests in `types/`.
- Do not maintain a second routing matrix outside `SKILL.md`.
