# director_episode_output.schema.json Notes

## Purpose

`director_episode_output.schema.json` is the shared structural contract for:

- `2-Global` seeding the episode root
- `3-Detail` filling canonical group and shot fields
- downstream `4-Design`, `5-Image`, and `6-Video` consumers reading the same root

The schema is intended to validate structure, not to be the primary long-form governance doc.

## Slimming Policy

The JSON schema was intentionally slimmed down to keep validation-focused content in the schema file itself:

- keep structural keys, required fields, enums, refs, and compatibility shapes
- remove bulky `title`, `description`, and `examples` blocks from the JSON schema
- keep legacy compatibility keys until runtime consumers stop reading them

This means the schema remains large in field surface, but is substantially lighter in non-executable prose.

## What Still Must Stay For Now

These areas are still intentionally present because runtime consumers or validators still read them:

- canonical group and shot fields such as `正文切分参考`, `正文回指`, `角色表现`, `运动表现`, `氛围表现`, `视觉强化`, `分镜构图`, `摄影美学`, `运镜手法`, `转场特效`
- legacy alias and fallback fields such as `人物表演锚点`, `动作路径`, `空间氛围`, `视觉抓手`, `构图骨架`, `分镜表现`, `角色背景面`, `角色站位走位`, `镜头类型兼容`
- compatibility sidecar defs such as `detail_patch_sidecar`, `detail_group_patch`, `detail_beat_patch`, and `detail_shot_patch`

## Safe Next Step

If we continue simplifying, the next safe phase is:

1. move legacy sidecar defs into a dedicated compat schema
2. update validators and prompt bridges to read canonical-only fields first without requiring legacy companions
3. remove alias and fallback keys from the main schema only after sibling runtime parity is verified
