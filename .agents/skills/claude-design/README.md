# Claude Design Codex Adapter

Codex-adapted wrapper for `jiji262/claude-design-skill`.

## Source

- Upstream: `https://github.com/jiji262/claude-design-skill`
- Installed commit: `f1ac87c3decb175d99a269f23ca84860786a598b`
- Upstream copy: `references/upstream/`

## Directory Tree

```text
claude-design/
├── agents/
│   └── openai.yaml
├── references/
│   └── upstream/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Usage

Use `$html-claude-design` when an HTML artifact needs stronger visual direction, high-fidelity composition, variants, brand-aware execution, final file writeback, and browser verification.

Every run should maximize the relevant upstream capability set through the local runtime spine: design workflow, design principles, format-specific guidance, variation support, brand/fact verification when needed, artifact writeback, and browser verification. The run starts by loading `SKILL.md + CONTEXT.md`, turning loaded context into `loaded_context_manifest`, choosing only triggered upstream modules, and declaring a concrete `visual_system` before implementation.

For PPT, HTML, deck, and courseware artifact builds, the skill may call `.agents/skills/cli/imagegen` to create missing bitmap image elements, adapt them to the artifact visual system, persist them beside the artifact, and reference them from the final surface. Imagegen owns image generation mode and persistence; `html-claude-design` owns asset need detection, `style_adaptation_profile`, and final composition.

Functional-but-generic output is not a pass. Artifact creation or modification is not complete until the handoff includes `artifact_paths` plus `writeback_status`, or an explicit blocker explains why no file could be written. When generated images are triggered, completion also requires `asset_generation_status`, `style_adaptation_profile`, workspace-bound `generated_asset_paths`, and verification that the artifact renders those assets in the intended style. Scripts and templates may support mechanics, but they must not generate creative decisions, layout systems, copy decisions, generated-asset prompt constraints, or quality verdicts.

The local `SKILL.md` is the authoritative Codex runtime contract. Upstream files are reference modules loaded only when triggered.

## Runtime Spine Coverage

- `Core Task Contract`, `Input Contract`, `Type Routing Matrix`, `Thinking-Action Node Map`, `Visual Maps`, `Convergence Contract`, `Review Gate Binding`, `Output Contract`, and `Learning / Context Writeback` live in `SKILL.md`.
- `Context Processing Contract` distinguishes context loading from context application and writeback.
- `Module Loading Matrix` and `Module Trigger Matrix` authorize individual upstream reference files and the sibling imagegen bridge.
- `test-prompts.json` covers redesign, direction selection, brand-aware prototype, generated assets, style adaptation, and lesson handoff regression scenarios.

## Upgrade Migration Summary

| legacy source | Skill 2.0 landing |
| --- | --- |
| Upstream `references/upstream/SKILL.md` workflow and guardrails | Local `SKILL.md` runtime spine plus explicit upstream module rows |
| Upstream design principles, formats, styles, brand/fact, React/Babel, verification references | Authorized reference modules loaded only through `Module Trigger Matrix` |
| Local adapter notes and repeated failure patterns | `CONTEXT.md` Type Map, Repair Playbook, and Reusable Heuristics |
| Artifact writeback, image bridge, source boundary, and verification rules | Local `SKILL.md` contracts, node map, convergence gates, and review gates |
| Typical regression scenarios | `test-prompts.json` |

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/claude-design --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/claude-design --mode delivery
```
