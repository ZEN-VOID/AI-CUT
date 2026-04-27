# 剧集海报 Review Contract

本文件定义 `comic-episode-poster` 的结构、语义与生图交接门禁。它不改写业务主真源，审查结论必须回流到同目录 `SKILL.md` 与 `steps/poster-design-workflow.md` 指定的 owner。

## Review Inputs

- 已生成或待修复的 `comic_episode_poster_design.v1` JSON。
- 本集分组剧本与九刀流 JSON 的实际读取证据。
- 可选的 3 号漫画生成图、报告或用户提供标题。
- 若用户要求生图，还必须检查 `.agents/skills/cli/imagegen` handoff 字段。

## Gate Table

| gate_id | check | pass condition | failure route |
| --- | --- | --- | --- |
| `G1-SCHEMA` | JSON 结构和 schema version | validator 通过，必填字段齐全 | `N8-ASSEMBLY` |
| `G2-UPSTREAM` | 上游加载 | `loaded_artifacts` 至少包含 `grouped_script` 与 `nine_blade_json` | `N3-UPSTREAM-LOAD` |
| `G3-STYLE` | 风格继承 | 角色阶段、场景连续、风格锚点来自上游 | `N4-EPISODE-FACTS` |
| `G4-HIGHLIGHT` | 剧情高光发现 | 先列 3-5 个候选，再说明最终选择 | `N5-HIGHLIGHT-DISCOVERY` |
| `G5-SUBJECT` | 主体边界 | 所有 `primary_subjects` 都有本集 presence evidence | `N6-POSTER-LOCK` |
| `G6-HOOK` | 标题与钩子 | 标题可传播、可回指本集事实；用户标题优先 | `N6-POSTER-LOCK` |
| `G7-COMPOSITION` | 画面层次 | foreground / subjects / background 全齐且服务同一场面 | `N7-VISUAL-TEXT` |
| `G8-TEXT` | 居中文字系统 | episode label 与 hook title 均显式水平+垂直居中 | `N7-VISUAL-TEXT` |
| `G9-PROMPT` | 可生图性 | `positive_prompt` 能直接指导海报图，非名词清单 | `N8-ASSEMBLY` |
| `G10-IMAGEGEN` | 生图交接 | `imagegen_handoff.tool_skill_path == ".agents/skills/cli/imagegen"` | `N8-ASSEMBLY` |

## Verdict Model

| verdict | meaning | allowed next action |
| --- | --- | --- |
| `pass` | 结构和语义均通过 | 写入 canonical JSON；若用户要求生图，交给 imagegen |
| `pass_with_todo` | JSON 可用，但存在非阻塞改进项 | 交付并记录 todo |
| `needs_rework` | 有硬门禁失败 | 按 failure route 回退修复 |
| `blocked` | 缺少项目上游真源或用户未授权覆盖 | 停止并报告缺口 |

## Imagegen Handoff Review

当用户要求生成海报图时，必须额外检查：

- 生图工具固定为 `.agents/skills/cli/imagegen`，不是旧 API skill、旧 Seedream route 或散装脚本。
- 本技能不临时另写一份独立海报 prompt；只能从已校验 JSON 的 `prompt_package.positive_prompt` 和 `imagegen_handoff` 派生。
- imagegen 执行前必须加载其 `SKILL.md + CONTEXT.md`，并遵守其 built-in 默认、CLI fallback opt-in、项目持久化规则。
- 项目绑定图片不得只留在 `$CODEX_HOME/generated_images`，必须落到 `projects/comic/<项目名>/4-剧集海报/` 下的稳定路径或用户指定项目路径。
