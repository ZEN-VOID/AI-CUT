# Type Package: render-ready-handoff

## Purpose

当用户要求生成海报图时，本包把海报 JSON 变成可交给 `.agents/skills/cli/imagegen` 的稳定 handoff。

## Fixed Context

- 生图工具固定为 `.agents/skills/cli/imagegen`。
- 本技能先产出并校验 JSON，再调用 imagegen；不得先绕过 JSON 直接写图像 prompt。
- `imagegen_handoff.tool_skill_path` 必须等于 `.agents/skills/cli/imagegen`。
- `imagegen_handoff.render_prompt_source` 默认是 `prompt_package.positive_prompt`。
- 项目绑定图片应落到 `projects/comic/<项目名>/4-剧集海报/imagegen/` 或用户指定项目目录。
- imagegen 的 built-in / CLI fallback / 透明背景 / 持久化规则由 `.agents/skills/cli/imagegen` 自己裁决。

## Review Focus

- positive prompt 是否足以直接生成海报图？
- handoff 是否记录了工具路径、prompt 来源、输出目录和持久化规则？
- 是否避免了旧 Seedream/API route 或临时脚本成为新的默认生图真源？
