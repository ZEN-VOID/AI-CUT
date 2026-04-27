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
| GPT 监制意见只停在口头，没有进入 DeepSeek prompt | supervision packet drop | 把 subagents 汇流为 `supervision_packet`，通过 `--supervision-packet` 注入 messages pack | C lane 固定 GPT 为监制层、DeepSeek 为执行层；脚本记录 `supervision_packet_ref` | messages JSON 中含监制包；最终正文仍有 DeepSeek provider 证据 |
| 上一章虽然被读取，但新章仍像重新开局 | continuity bridge under-specified | 把上一章末尾摘录单独置入 provider prompt，并显式要求承接既成事实、位置、情绪余波、未完成动作和悬念压力 | 将“上一章正文”升级为 `continuity bridge`，并在 dry-run summary 暴露 `previous_chapter_ref` | messages pack 中能看到连续性桥；正文开章能读出上一章之后的下一步 |
| DeepSeek provider 返回 markdown 但缺 YAML 头 | provider output validation | 阻断写回，调整 prompt 或增大 `max_tokens` 后重试 | 写回前固定校验 `润色模型: Deepseek` | 非法输出不落到 `第N章.md` |
| DeepSeek 返回结构字段齐全但正文仍是占位、过短或 planning 复述 | prose completeness validation | 阻断写回，要求 provider 重出完整小说 prose | validator 只要求极简 YAML 头，同时检查正文长度、占位符和 planning 术语 | `[请填充完整润色章节润色稿]`、缺 closing frontmatter、`本章冲突` 等样本均被拒绝 |
| provider 证据链缺失 | evidence routing | 重新跑脚本并核对 stdout 摘要、provider 命中与 canonical writeback | 默认不落盘 provider artifacts；需要调试时才显式传 `--output-dir` | 未传 `--output-dir` 时只写 `4-润色/第N卷/第N章.md` |
| auto 模式在现有章上静默重写 | writeback safety gate | 现有章正式写回必须显式 mode + `--force` | `auto` 只允许新章直写；现稿 dry-run/no-writeback 可装配上下文但不覆盖 | 已存在 `第N章.md` 时普通 auto 调用会阻断 |
| 卷级 review 失败后 GPT 直接改正文，导致 C lane provider ownership 失真 | review loop ownership drift | GPT/subagents 只产出 repair brief，仍由 DeepSeek 执行 `local_repair` 或 `polish_rewrite` | review aggregate 必须带 `original_polishing_lane=C-Deepseek流` 与 repair mode | 返工 sidecar 有 DeepSeek messages/provider report |

## Repair Playbook

1. 先确认失败在 provider、上下文加载、frontmatter、风格吸收还是写回路径。
2. 若 provider 报认证或模型错误，优先修 `.agents/skills/api/deepseek` 与 `.env`，不改正文。
3. 若正文风格不对，先检查 `messages_path` 中是否导入风格卡、MEMORY 与相关 CONTEXT。
4. 若正文像提纲，回到 `templates/deepseek-system-prompt.md` 与 `references/chapter-polishing-contract.md`，强化 prose conversion。
5. 若上下章像各写各的，优先检查 messages pack 是否只截取了上一章开头；承接判断应优先看上一章末尾，而不是章节开篇。
6. 若 YAML 头缺字段，只检查并补正 `润色模型: Deepseek`；上下文缺口回到 context pack / sidecar，而不是补进正文头。
7. 若正文过短、仍含模板占位符或 planning 标题句法，先修 provider prompt / context pack，再重试，不允许写回 canonical path。
8. 若路径不对，先修 `chapter_paths` / output contract，再重试 provider。
9. 若正式写作没有监制包，先查 subagent 是否被上层阻断；未阻断则补真实 subagents，已阻断则补降级报告。

## Reusable Heuristics

- DeepSeek 流的价值在于强推理先综合上下文，再输出统一章节；不要把上下文裁得只剩当前章 planning。
- 对风格一致性最有用的输入通常是风格卡 + 上一章正文 + 项目 MEMORY；三者缺一时要在 report 中能看出来。
- 若上一章存在，最可靠的承接材料通常是上一章末尾 3-6k 字，而不是上一章开头；章节开头负责调性，章节末尾负责因果入场。
- `thinking enabled + reasoning_effort high` 会消耗更多 token，章节创作默认应给足 `--max-tokens`。
- provider sidecar 是排查“到底有没有走 DeepSeek”的第一证据，不要只看最终正文文件。
- 现有章是高风险写回目标；正式覆盖必须同时满足显式 mode 与 `--force`，普通 `auto` 只能在缺章时起稿。
- C lane 的高级化关键是“GPT 监制不抢笔”：监制包越锋利，越要交给 DeepSeek 高推理执行，而不是让 GPT 临场改稿。
