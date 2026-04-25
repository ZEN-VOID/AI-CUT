# 4-Design / 2-设计 / 道具 Shared I/O Contract

本文件是 `aigc/4-Design/道具` 的输入输出、命名与 compat projection 单一辅助真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/道具清单.json` | 本阶段第一输入根 |
| 必需 | `projects/aigc/<项目名>/0-Init/north_star.yaml` | 项目世界观与创作基线 |
| 必需 | `projects/aigc/<项目名>/0-Init/init_handoff.yaml` | 初始化 handoff 与约束补充 |
| 必需 | `projects/aigc/<项目名>/2-Global/全局风格.md` | 项目全局风格锚点 |
| 必需 | `projects/aigc/<项目名>/2-Global/全集类型元素.md` | 类型与导演打法约束 |
| 可选 | `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/道具研究.json` | compat research 补证 |
| 可选 | `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/prop_design_bridge.json` | compat bridge 补证 |
| 可选 | `projects/aigc/<项目名>/3-Detail/第N集.json` | 镜头级事实回链 |
| 可选 | `projects/aigc/<项目名>/2-Global/导演意图.md` | 设计元素补充约束 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/<prop_id>-<canonical_name>.md` | 逐道具 Markdown 设计卡真源 |
| sidecar | `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/_manifest.json` | 审计侧车；基础壳固定为 `status / episode_id / input_file / output_dir / output_files / statistics / notes` |
| compat | `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/道具设计.json` | 旧下游兼容 projection，仅在显式模式下导出 |
| compat | `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/prop_design_prompt.json` | 旧下游 compat prompt sidecar，仅在显式模式下导出 |

## Naming Contract

- `<prop_id>-<canonical_name>.md`
- `_manifest.json`
- `道具设计.json`
- `prop_design_prompt.json`

## Markdown Card Contract

每个 `prop-*.md` 固定包含：

1. `# <canonical_name>`
2. `**物语**`
3. `**解构**`
4. `Reasoning Pivot: ...`
5. `## Photography ##`
6. `## Prop Design ##`
7. `**prompt整合**`

结构真源固定为 `templates/prop_masterprompt.structured.v2.md`。`3-面板` 与后续图像阶段默认从 `**prompt整合**` 区块提取 prompt；该区块必须包含英文 `Global style prefix` 与 `Integrated prompt`。`Integrated prompt` 必须是对同一模板上方全部内容的英文自然语言整合，尤其覆盖 `解构 / Photography / Prop Design` 中的结构、材质、纹理、功能、状态痕迹与负面约束；正文必须完全为英文 ASCII 文本，目标约 2000 UTF-8 bytes，硬门范围为 1800-2200 bytes；并且必须固定为 `isolated pure prop view`，显式禁止 hands 与 characters。

## Hard Rules

1. 第一输入根只能是 `道具清单.json`；compat research / bridge 只能补证。
2. 不得只写 compat JSON 而跳过 Markdown 主稿。
3. `道具设计.json` 与 `prop_design_prompt.json` 只能由 Markdown canonical truth 投影。
4. 若某个 prop 缺 `design_context.design_handoff`，必须阻塞并回退到 `1-清单/道具`。
