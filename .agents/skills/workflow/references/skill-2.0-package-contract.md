# Package Contract

This reference records package ownership and compatibility notes for `workflow`. It is not a second execution contract; runtime behavior lives in `SKILL.md`.

## Scope

- Keep the package aligned with Skill 2.0: `SKILL.md` is the runtime spine; modules provide authorized detail only.
- Keep the business target narrow: livestream teaching material plus an optional learning-step guide becomes a source-preprocessed, source-backed instructional video package with long-film units, sequential slices, and combination slices.
- Keep sibling skills external: HyperFrames, video-editing-skill, WIS skills, and wangjianshuo-perspective are loaded through `Peer Skill Routing Matrix`.
- Treat git-history reference-rhythm, F1/F2, social-ad, asset-monitor, and video-to-manifest behavior as legacy background, not current runtime. The current user goal supersedes that old business target.

## Rules

- The source of truth for input paths, peer skill routing, node order, gates, and output path is `SKILL.md`.
- `templates/` may format reports and manifests, but must not generate teaching prose or decide clip order.
- `scripts/` may support validation and future mechanical helpers, but must not select pedagogical truth.
- If this reference changes route, gate, or output behavior, update `SKILL.md` in the same change.

## Legacy Migration Note

The previous tracked workflow package targeted HyperFrames-native reference-rhythm and public social-ad style videos. In the current working tree, those legacy files were already absent before this repair began. This update does not silently restore them. It intentionally lands the new user-requested business goal in `SKILL.md`: livestream teaching footage plus optional learning-step guide to pure teaching video, including 1.1x source preprocessing, repeated-round source units, and A/B1-B5/C combination slices.

Migrated principles:

- HyperFrames remains the primary composition and render route.
- LLM/Codex judgment owns video understanding, storyboard decisions, and content selection.
- Scripts remain mechanical validators or format helpers.
- Final delivery must include source evidence, QA, and a report.

Not migrated by default:

- Legacy F1/F2 runtime, social-ad layer taxonomy, asset usage monitor scripts, old visual/dialogue validators, `video-to-manifest`, and `text-to-speech` subpackages.
- Any future need for those legacy routes must be a separate explicit migration or source-layer repair.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does this reference remain subordinate to `SKILL.md`? | Any independent route, output path, fail code, or completion standard in this file fails | `FAIL-MODULE-DRIFT` | `SKILL.md Module Loading Matrix` | Reference diff and matching `SKILL.md` section |
| Are sibling skills routed only through `Peer Skill Routing Matrix`? | A sibling skill used as hidden default or source of output truth fails | `FAIL-PEER-ROUTING` | `SKILL.md Peer Skill Routing Matrix` | Peer skill load trace and node reason |

## SKILL.md Boundary

- Keep input and output decisions in `SKILL.md`.
- Keep `Multi-Subskill Continuous Workflow` in `SKILL.md` so whole-package calls have a stable default dispatch contract.
- Output decisions include required output, output format, output path, naming convention, and completion gate.
- Move process details, long examples, and edge-case handling into modules only when `SKILL.md` authorizes those modules in `Module Loading Matrix` and maps actual loading through `Module Trigger Matrix`.

## Source Ownership

`SKILL.md` owns workflow behavior. This reference is consumed by `FAIL-MODULE-DRIFT`, `FAIL-PEER-ROUTING`, and `FAIL-DIRECTORY-STRUCTURE-DRIFT` reviews.
