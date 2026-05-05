# Type Package Map

`types/` stores fixed context packages for LibTV request classes. Load one package by default, and stack more only when the user explicitly combines operations.

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `generation` | `types/generation/` | new LibTV image/video, storyboard, MV, ad, short drama, product video, text-to-media | exclusive | `types/generation/generation.md` | `editing`, `session-ops` | none |
| `editing` | `types/editing/` | local image/video reference plus modify, replace, remove, animate, extend, restyle, turn into video | exclusive | `types/editing/editing.md` | `generation`, `session-ops` | none |
| `session-ops` | `types/session-ops/` | `sessionId`, explicit progress query, append message, explicit download results, switch project | exclusive | `types/session-ops/session-ops.md` | `generation`, `editing` | none |

## Default Package Rule

1. If the user names LibTV and gives only creative intent, choose `generation`.
2. If the user supplies a local media path and asks for a change or reference-based creation, choose `editing`.
3. If the user supplies a `sessionId` or explicitly asks for progress/download/project changes, choose `session-ops`.
4. If the request lacks required data for the selected package, ask the smallest possible clarification.

## Loading Flow

1. Read the user request and identify LibTV intent, local files, and session metadata.
2. Select one package from the `Package Index`.
3. Load the package's `context_files`.
4. Execute `steps/execution-workflow.md` using that type context.
5. Apply `review/review-contract.md` before final delivery.
