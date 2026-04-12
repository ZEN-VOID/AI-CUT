# 2-Global Shared I/O Contract

本文件是 `aigc/2-Global` 的输入输出、命名与 handoff 单一真源。

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
| handoff | `agents_plan + patch / note / report` | subagents 返回给父 skill 的思考计划与局部增量 |

## Naming Contract

- `mission_brief`
- `subagent_brief_全局风格设计师`
- `subagent_brief_类型化指导`
- `subagent_brief_导演`
- `context_packet_全局风格设计师`
- `context_packet_类型化指导`
- `context_packet_导演`
- `agents_plan_全局风格设计师`
- `agents_plan_类型化指导`
- `agents_plan_导演`
- `plan_patch_全局风格设计师`
- `plan_patch_类型化指导`
- `artifact_patch_导演`
- `synthesis_report`

## Hard Rules

1. subagents 只能返回 `agents_plan + patch / note / report`，不能直接落盘 canonical Markdown。
2. `全局风格.md` 和 `类型指导.md` 的项目级总则必须保持稳定，不得被 episode 细节污染。
3. `导演意图.md` 必须按 `## 第N集 -> ### 【x-x-x】` 组织，父 skill 只更新命中章节。
4. `2-Global` 不得创建 `projects/<项目名>/3-Detail/第N集.json`。
