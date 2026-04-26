# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| DeepSeek 流生成正文时模型漂移到非 `deepseek-v4-pro` | provider model contract | 回到 `.agents/skills/api/deepseek`，拒绝非固定模型 | 在 C 流脚本中不传 `--model`，由 provider skill 固定模型 | dry-run payload 始终为 `deepseek-v4-pro` |
| DeepSeek 调用没有默认高推理 | provider reasoning contract | 显式传 `--thinking enabled --reasoning-effort high` 或依赖 provider 默认 | 在 C 流合同中固定默认高推理路径 | provider messages/report 能显示 high reasoning 请求 |
| 正文看起来像 planning 摘要而不是小说 | prose conversion | 回到 system prompt 强调只输出 mature prose，并禁止 planning 标题句法 | `templates/deepseek-system-prompt.md` 固化风格转译规则 | 正文没有“本章任务/规避/职责映射”等字样 |
| 项目风格没有被吸收 | style context loading | 检查风格卡、项目 MEMORY、项目 CONTEXT 是否进入 messages pack | 脚本固定读取并摘要导入 style cards / MEMORY / CONTEXT | messages JSON 中有风格卡与项目记忆摘录 |
| DeepSeek provider 返回 markdown 但缺 YAML 头 | provider output validation | 阻断写回，调整 prompt 或增大 `max_tokens` 后重试 | 写回前固定校验 REQUIRED_OUTPUT_MARKERS | 非法输出不落到 `第N章.md` |
| DeepSeek 返回结构字段齐全但正文仍是占位、过短或 planning 复述 | prose completeness validation | 阻断写回，要求 provider 重出完整小说 prose | validator 同时解析 YAML、检查嵌套字段、正文长度、占位符和 planning 术语 | `[请填充完整章节正文]`、缺 closing frontmatter、`本章冲突` 等样本均被拒绝 |
| provider 证据链缺失 | evidence routing | 重新跑脚本，保留 messages pack、raw generated preview 和 provider sidecar | artifacts 固定落到 `reports/3-Drafting/deepseek/...` | 目录中可追溯 messages / raw / report |
| auto 模式在现有章上静默重写 | writeback safety gate | 现有章正式写回必须显式 mode + `--force` | `auto` 只允许新章直写；现稿 dry-run/no-writeback 可装配上下文但不覆盖 | 已存在 `第N章.md` 时普通 auto 调用会阻断 |

## Repair Playbook

1. 先确认失败在 provider、上下文加载、frontmatter、风格吸收还是写回路径。
2. 若 provider 报认证或模型错误，优先修 `.agents/skills/api/deepseek` 与 `.env`，不改正文。
3. 若正文风格不对，先检查 `messages_path` 中是否导入风格卡、MEMORY 与相关 CONTEXT。
4. 若正文像提纲，回到 `templates/deepseek-system-prompt.md` 与 `references/chapter-drafting-contract.md`，强化 prose conversion。
5. 若 YAML 头缺字段，不允许人工补字段冒充成功；先修 provider prompt 或重跑。
6. 若正文过短、仍含模板占位符或 planning 标题句法，先修 provider prompt / context pack，再重试，不允许写回 canonical path。
7. 若路径不对，先修 `chapter_paths` / output contract，再重试 provider。

## Reusable Heuristics

- DeepSeek 流的价值在于强推理先综合上下文，再输出统一章节；不要把上下文裁得只剩当前章 planning。
- 对风格一致性最有用的输入通常是风格卡 + 上一章正文 + 项目 MEMORY；三者缺一时要在 report 中能看出来。
- `thinking enabled + reasoning_effort high` 会消耗更多 token，章节创作默认应给足 `--max-tokens`。
- provider sidecar 是排查“到底有没有走 DeepSeek”的第一证据，不要只看最终正文文件。
- 现有章是高风险写回目标；正式覆盖必须同时满足显式 mode 与 `--force`，普通 `auto` 只能在缺章时起稿。
