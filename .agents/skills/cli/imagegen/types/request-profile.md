# Imagegen Request Profile Package

This type package expands `types/type-map.md` classification fields. It does not execute image generation and does not define output gates.

## Classification Checklist

| field | classify_by | return_to |
| --- | --- | --- |
| `intent` | whether the user asks for a new image, an edit, or generation with references | `N2-TYPE` |
| `asset_count` | single output, explicit variants, or multiple distinct assets | `N2-TYPE` |
| `batch_execution` | subagents parallel default, explicit main-thread serial, or not applicable | `N2-TYPE` |
| `background_need` | opaque, transparent chroma-key, or unsupported native transparency | `N2-TYPE` |
| `execution_mode` | built-in `image_gen` or unsupported non-built-in route | `N3-MODE` |
| `persistence` | preview-only, project-bound, or user-named destination | `N7-PERSIST` |
| `resolution_target` | 2K default, explicit user/upstream, or model-limited default | `N4-PROMPT` |
| `risk_profile` | text-heavy, identity-sensitive, mask-sensitive, style-sensitive, or low-risk | `N6-INSPECT` |

## Example Profiles

| signal | type_profile |
| --- | --- |
| "Make one hero image for this landing page" | `intent=generate`, `asset_count=single`, `execution_mode=built_in`, `persistence=project_bound`, `resolution_target=2k_default` |
| "Create four different item icons" | `intent=generate`, `asset_count=multiple_distinct`, `batch_execution=subagents_parallel_default`, `execution_mode=built_in` |
| "Replace the background in this uploaded portrait" | `intent=edit`, `asset_count=single`, `execution_mode=built_in`, `risk_profile=identity_sensitive` |
| "Give me a transparent PNG logo cutout" | `background_need=transparent_chroma_key` unless the user requires true/native transparency, which becomes `execution_mode=unsupported_non_builtin` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Did the type package return a profile instead of executing? | Any tool call, output write, or provider choice inside this package fails | `FAIL-IMG-TYPES` | `types/request-profile.md` and `SKILL.md#type-routing-matrix` | returned `type_profile` fields and no execution side effect |
