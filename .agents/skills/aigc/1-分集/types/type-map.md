# Type Map Index

This file is the Skill 2.0 type package index for `$aigc-episode-split`. It does not replace the concrete source classification package in `source-type-map.md`.

## Package Index

| package | purpose | load when |
| --- | --- | --- |
| `source-type-map.md` | source material classification: explicit episode source, chaptered novel, plain novel, mixed source, or blocked source | every `$aigc-episode-split` call |

## Default Package Rule

Load `source-type-map.md` by default for every invocation of this skill. If future subtype packages are added, select only the packages needed by the current source material and let `steps/episode-split-workflow.md` consume the resulting source type.

## Loading Flow

1. Load `SKILL.md + CONTEXT.md`.
2. Load this `types/type-map.md` as the package index.
3. Load `types/source-type-map.md` as the default type package.
4. Use the resolved source type to choose `explicit_episode_split`, `length_based_split`, `repair`, or blocked output.
