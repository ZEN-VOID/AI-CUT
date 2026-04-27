# Review Contract: 漫画生成

## Review Scope

本 review gate 检查 3 号漫画生成是否完成结构、运行时和交付门禁。它不改写剧情、角色或分镜真源。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 结构、计划、runtime 和交付文件满足本技能 Output Contract |
| `pass_with_todo` | dry-run 已完整，或 execute 有低风险视觉待复核，但交付证据齐全 |
| `needs_rework` | JSON、runtime、文件数、命名或跨阶段交接失败 |
| `blocked` | 缺少必要输入、API key、网络或用户确认 |

## Checklist

| check_id | check | pass condition |
| --- | --- | --- |
| `REV-CG-01` | 输入真源 | `prompt_json` 通过 2 号 validator |
| `REV-CG-02` | runtime | report 中 `provider=cli-imagegen`、`model=gpt-image-2` |
| `REV-CG-03` | prompt jobs | `imagegen_jobs.jsonl` 有 9 行，且每行一页 |
| `REV-CG-04` | 单页约束 | 每页 prompt 含 9:16、非拼图、非变体、多格漫画和右下角页码 |
| `REV-CG-05` | 输出目录 | 产物位于项目 3 号目录下的当前 group 子目录 |
| `REV-CG-06` | execute 文件 | execute 模式下存在 9 个 PNG |
| `REV-CG-07` | 命名交接 | 默认命名为 `page01.png..page09.png` 或 group 前缀命名 |
| `REV-CG-08` | legacy 边界 | 未经用户显式确认不得默认调用 Seedream/Dreamina/AnyFast/built-in |

## Provider Fallback Note

若上层策略阻断真实 reviewer/subagent，本技能降级为本地 checklist review。当前系统级工具策略未允许仓库规则自动启动 subagents，因此 review 默认由主 agent 本地执行，并在最终报告中说明验证命令。
