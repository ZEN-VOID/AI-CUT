# 2-Global Shared I/O Contract

本文件是 `aigc/2-Global` 的输入输出、命名与汇流写回单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/<项目名>/1-Planning/3-分组/第N集.md` | 当前集导演前置工作的主输入；正文内部带三段式 `分镜组ID` 标题 `【x-x-x】` |
| 可选 | `projects/<项目名>/1-Planning/3-分组/执行报告.md` | 当前集分组决议、组序与 handoff 摘要 |
| 必需 | `projects/<项目名>/0-Init/north_star.yaml` | 项目级目标与风格方向 |
| 必需 | `projects/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段高层 handoff |
| 可选 | `projects/<项目名>/0-Init/story-source-manifest.yaml` | 预设、锁轴、保真模式证据 |
| 可选 | `projects/<项目名>/1-Planning/2-剧本/第N集.md` | 当前集逐集剧本主稿 |
| 可选 | `projects/<项目名>/2-Global/*.md` | 已有全局文档，供增量 patch 使用 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/<项目名>/2-Global/全局风格.md` | 项目级风格底座 |
| canonical | `projects/<项目名>/2-Global/类型指导.md` | 项目级类型化导演协议 |
| canonical | `projects/<项目名>/2-Global/导演意图.md` | 按集、按组组织的导演构思主稿 |
| internal | `global_style_plan / type_guidance_plan / director_intent_plan` | 三条内部能力链的思行计划 |
| internal | `style_note / type_note / director_note / convergence_report` | 取舍、阻塞与汇流审计侧车 |
| internal | `writeback_patch_set` | 父 skill 最终写回前的统一 patch 集 |

## Naming Contract

- `input_lock_note`
- `invariant_brief`
- `branch_scope_plan`
- `global_style_plan`
- `global_style_patch`
- `style_note`
- `style_report`
- `type_guidance_plan`
- `type_guidance_patch`
- `type_note`
- `type_report`
- `director_intent_plan`
- `director_intent_patch`
- `director_note`
- `director_report`
- `constraint_bridge_note`
- `convergence_report`
- `writeback_patch_set`
- `handoff_note`

## Hard Rules

1. 本阶段只存在父 skill 一个 canonical writeback owner。
2. `全局风格.md` 和 `类型指导.md` 的项目级总则必须保持稳定，不得被 episode 细节污染。
3. `导演意图.md` 必须按 `## 第N集 -> ### 【x-x-x】` 组织，父 skill 只更新命中章节。
4. `2-Global` 不得创建 `projects/<项目名>/3-Detail/第N集.json`。
5. 不再允许 `subagent_brief_*`、`context_packet_*`、`agents_plan_*` 这类外置导演组命名语义继续作为本阶段真源。
