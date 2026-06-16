# Review Contract: 漫画生成

## Review Scope

本 review gate 检查 3 号漫画生成是否完成结构、运行时和交付门禁。它不改写剧情、角色或分镜真源。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 结构、计划、built-in runtime 和交付文件满足本技能 Output Contract |
| `pass_with_todo` | plan 已完整，或 execute 有低风险视觉待复核，但交付证据齐全 |
| `needs_rework` | JSON、runtime、文件数、命名、项目持久化或跨阶段交接失败 |
| `blocked` | 缺少必要输入、built-in image_gen 不可用、或用户要求 non-built-in route 但未显式确认 |

## Checklist

| check_id | check | pass condition |
| --- | --- | --- |
| `REV-CG-01` | 输入真源 | `prompt_json` 通过 2 号 validator |
| `REV-CG-02` | runtime | report 中 `provider=built-in-imagegen`、`runtime.mode=built_in_image_gen` |
| `REV-CG-03` | prompt specs | `imagegen_prompt_set.json` 有 9 条，且每条一页 |
| `REV-CG-04` | 单页约束 | 每页 prompt 含 9:16、非拼图、非变体、多格漫画和右下角页码 |
| `REV-CG-05` | 输出目录 | 产物位于项目 3 号目录下的当前 group 子目录 |
| `REV-CG-06` | execute 文件 | execute 模式下存在 9 个 PNG，且不是只留在 `$CODEX_HOME` 或 subagent 路径 |
| `REV-CG-07` | 命名交接 | 默认命名为 `page01.png..page09.png` 或 group 前缀命名 |
| `REV-CG-08` | batch topology | 默认 subagents parallel fan-out，上限 10；主线程串行必须有用户显式请求 |
| `REV-CG-09` | legacy 边界 | 未经用户显式确认不得调用 CLI/API、Seedream、Dreamina、AnyFast |

## Provider Fallback Note

若上层策略阻断真实 reviewer/subagent，本技能降级为本地 checklist review。若 subagents 不可用而用户仍要求 execute，可在主线程串行执行，但必须在报告中记录降级原因；不得因此切换到 CLI/API/provider fallback。
