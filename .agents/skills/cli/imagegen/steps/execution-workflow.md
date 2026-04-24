# Execution Workflow

This file owns the thinking-action node network for imagegen execution.

## Business Requirement Analysis

| slot | question |
| --- | --- |
| `business_goal` | Create or edit bitmap assets that satisfy the user's visual intent and delivery constraints |
| `business_object` | Generated images, edited images, prompts, local source files, project asset paths, optional CLI payloads |
| `constraint_profile` | Tool capability, user opt-in, image visibility, transparency, text fidelity, path persistence |
| `success_criteria` | Final image(s) match request, are saved where needed, and pass review gates |
| `non_goals` | SVG/vector/code-native creation, unconfirmed API fallback, modifying bundled CLI internals |
| `complexity_source` | Intent classification, reference roles, transparency, batch convergence, text/image fidelity |
| `topology_fit` | Hybrid: classify first, branch by mode, converge through review and persistence |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | Lock request, assets, constraints, and destination | User request, images, file paths, project context | Identify required asset(s), edit target, references, exact text, avoid list, output destination | `request_summary` | `N2-TYPE` | Enough input to classify |
| `N2-TYPE` | Build `type_profile` | `types/type-map.md`, `request_summary` | Classify intent, asset count, persistence, background need, execution mode, risk | `type_profile` | `N3-MODE` | Mode is valid and user opt-in is honored |
| `N3-MODE` | Select execution route | `type_profile`, `references/mode-routing.md` | Choose built-in generate/edit, chroma-key transparency, or confirmed CLI fallback | `mode_decision` | `N4-PROMPT` | CLI fallback only when confirmed |
| `N4-PROMPT` | Prepare prompt or CLI payload | `references/prompting.md`, `references/sample-prompts.md` | Normalize prompt, label image roles, apply default 2K target, preserve invariants, prepare batch prompts | `prompt_spec` | `N5-EXECUTE` | Prompt preserves user intent and resolution target |
| `N5-EXECUTE` | Generate or edit | Built-in tool or `scripts/image_gen.py` | Run one call per asset/variant, or confirmed CLI command | output image(s), CLI stdout/path | `N6-INSPECT` | Output exists or failure is explained |
| `N6-INSPECT` | Check visual result | Request constraints, output image(s) | Inspect subject, style, composition, text, invariants, alpha if needed | `inspection_notes` | `N7-PERSIST` or `N4-PROMPT` | At most targeted iteration unless user asked for more |
| `N7-PERSIST` | Save final deliverables | `references/output-persistence.md`, selected outputs | Copy/move project-bound finals, avoid overwrite, keep stable names | final saved path(s) | `N8-REVIEW` | Workspace-bound assets are not only in `$CODEX_HOME/*` |
| `N8-REVIEW` | Validate and close | `review/review-contract.md`, saved paths, prompts | Run final gate, produce verdict and delivery note | verdict, final report | done | `pass` or `pass_with_todo` |

## Branch Rules

- `built_in_generate`: no CLI docs are needed unless user asks for fallback controls.
- `built_in_edit`: local edit targets must be inspected into context before the built-in edit flow.
- `transparent_chroma_key`: execute normal built-in generation first, then local alpha removal and validation.
- `cli_fallback`: load `references/cli.md`, `references/image-api.md`, and `references/codex-network.md`; verify API-key/network requirements before live calls.
- `cli_fallback` with default `gpt-image-2`: omitted `--size` resolves to `2048x1152`; if another model is selected, use a supported model default or explicit user size.
- `batch_or_variants`: distinct assets require distinct prompts; variants of one prompt may share a base prompt with controlled differences.

## Convergence Rules

- Every branch converges through `N6-INSPECT`, `N7-PERSIST`, and `N8-REVIEW`.
- A request-ready sidecar or CLI dry-run is not the same as a generated image unless the user asked for a plan only.
- A project-bound asset is incomplete until the final selected image exists in the workspace.
- A transparent asset is incomplete until alpha validation passes or the residual risk is reported.
