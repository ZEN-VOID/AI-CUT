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
| 监制包未按项目 `team.yaml` 已指定监制组请教，只给泛泛创作建议 | project team consultation gap | 读取 `roles.production.members`，为每位相关大师提出具体问题并汇流可执行指导 | 监制包固定 `project_team_ref / consultations / executable_guidance` 字段 | DeepSeek messages 含可追溯的请教式监制包 |
| 只加载最近上一章，导致同卷早前事实、伏笔、线索、道具流向、卷目标完成度、任务连续性或悬疑节奏把控性断裂 | same-volume continuity underload | 加载当前卷内所有已存在且早于目标章的正文，并把最近前章末尾摘录单独置入 provider prompt | 将“上一章正文”升级为“同卷前文连续性桥”，并在 dry-run summary 暴露 `previous_chapter_refs` | messages pack 中能看到同卷前文逐章摘录；正文开章能读出同卷前文之后的下一步 |
| DeepSeek provider 返回 markdown 但缺 YAML 头 | provider output validation | 阻断写回，调整 prompt 或增大 `max_tokens` 后重试 | 写回前固定校验 `写作模型: Deepseek` 与 `字数: XXX字` | 非法输出不落到 `第N章.md` |
| DeepSeek 返回结构字段齐全但正文仍是占位、过短或 planning 复述 | prose completeness validation | 阻断写回，要求 provider 重出完整小说 prose | validator 只要求极简 YAML 头，同时检查正文长度、占位符和 planning 术语 | `[请填充完整章节正文]`、缺 closing frontmatter、`本章冲突` 等样本均被拒绝 |
| provider 证据链缺失 | evidence routing | 重新跑脚本并核对 stdout 摘要、provider 命中与 canonical writeback | 默认不落盘 provider artifacts；需要调试时才显式传 `--output-dir` | 未传 `--output-dir` 时只写 `3-初稿/第N卷/第N章.md` |
| auto 模式在现有章上静默重写 | writeback safety gate | 现有章正式写回必须显式 mode + `--force` | `auto` 只允许新章直写；现稿 dry-run/no-writeback 可装配上下文但不覆盖 | 已存在 `第N章.md` 时普通 auto 调用会阻断 |
| 角色对白同质化，所有人物都用同一种冷静说明腔 | character voice under-specified | 从角色卡抽取 `voice_and_presence` 形成“角色对白声纹表”，并要求每句对白承担角色意图 | prompt 固定导入声纹表；对白必须按身份、关系、情绪和利益差异化 | messages pack 中存在声纹表；抽查同场对话能不看话标区分说话人 |
| `不是……是……` 句式高频重复，解释感生硬 | sentence-pattern loop | 在 system prompt 中把该句式降为偶发关键反转用法，并在 validator 中设置上限 | 生成前给替代表达路径：动作、感官、比喻、反问、停顿、误读修正或角色化口语 | validator 统计该句式不超过上限；正文不连续使用同一解释框架 |
| 卷级 review 失败后 GPT 直接改正文，导致 C lane provider ownership 失真 | review loop ownership drift | GPT/subagents 只产出 repair brief，仍由 DeepSeek 执行 `local_repair` 或 `chapter_rewrite` | review aggregate 必须带 `original_drafting_lane=C-Deepseek流` 与 repair mode | 返工 sidecar 有 DeepSeek messages/provider report |
| 用户授权 subagents 5路修复后，误把 worker 并行当成正文主创模型切换 | subagent repair overreach | worker 负责分章/分问题 brief，DeepSeek 按每个 brief 执行修复并落 provider sidecar | C lane 硬写“修复优化不是 GPT 直写许可”；最终报告列出 repair creative engine | 每个受影响章节有 DeepSeek repair messages/report，正文 `写作模型: Deepseek` 与证据一致 |

## Repair Playbook

1. 先确认失败在 provider、上下文加载、frontmatter、风格吸收还是写回路径。
2. 若 provider 报认证或模型错误，优先修 `.agents/skills/api/deepseek` 与 `.env`，不改正文。
3. 若正文风格不对，先检查 `messages_path` 中是否导入风格卡、MEMORY 与相关 CONTEXT。
4. 若正文像提纲，回到 `templates/deepseek-system-prompt.md` 与 `references/chapter-drafting-contract.md`，强化 prose conversion。
5. 若上下章像各写各的，优先检查 messages pack 是否覆盖当前卷内全部已存在前序章；最近前章末尾负责开章入场，其他前序章负责事实、伏笔、线索、关系、道具、卷目标完成度、任务连续性和悬疑节奏边界。
6. 若 YAML 头缺字段，只检查并补正 `写作模型: Deepseek` 与 `字数: XXX字`；上下文缺口回到 context pack / sidecar，而不是补进正文头。
7. 若正文过短、仍含模板占位符或 planning 标题句法，先修 provider prompt / context pack，再重试，不允许写回 canonical path。
8. 若路径不对，先修 `chapter_paths` / output contract，再重试 provider。
9. 若人工校阅指出对白同质化，先查 messages pack 是否含角色对白声纹表；若缺失，修脚本抽取角色卡，再用 `local_repair` 或 `chapter_rewrite` 让 DeepSeek 按声纹重写相关章节。
10. 若人工校阅指出句式循环，先查 system prompt 与 validator；修复后用同一 finding 回跑 provider，禁止用简单替换脚本机械改正文。
11. 若正式写作没有监制包，先查 subagent 是否被上层阻断；未阻断则补真实 subagents，已阻断则补降级报告。若监制包缺 `team.yaml` roster 来源、请教问题或可执行指导，重新按项目监制组执行请教汇流。
12. 若 review 触发修复，先生成 repair brief，再调用 DeepSeek 执行正文修复；若环境暂时无法调用 DeepSeek，必须报告阻断，不能为了推进而用 GPT 直接改写 DeepSeek lane 正文。

## Reusable Heuristics

- DeepSeek 流的价值在于强推理先综合上下文，再输出统一章节；不要把上下文裁得只剩当前章 planning。
- 对风格一致性最有用的输入通常是风格卡 + 同卷前文 + 项目 MEMORY；三者缺一时要在 report 中能看出来。
- 若同卷前文存在，最可靠的承接组合是“最近前章末尾 3-6k 字 + 同卷全部前序章逐章摘录”；最近前章负责因果入场，早前章节负责事实、伏笔、线索、关系、道具、卷目标完成度、任务连续性和悬疑节奏边界。
- `thinking enabled + reasoning_effort high` 会消耗更多 token，章节创作默认应给足 `--max-tokens`。
- provider sidecar 是排查“到底有没有走 DeepSeek”的第一证据，不要只看最终正文文件。
- 现有章是高风险写回目标；正式覆盖必须同时满足显式 mode 与 `--force`，普通 `auto` 只能在缺章时起稿。
- C lane 的高级化关键是“GPT 监制不抢笔”：监制包越锋利，越要交给 DeepSeek 高推理执行，而不是让 GPT 临场改稿。
- C lane 的监制包应像“向项目已选大师逐一请教后的写作备忘”，不是 GPT 对 DeepSeek prompt 的泛泛润色；最终只保留能直接影响正文的指导。
- 修复优化也是主创环节：只要写入 `3-初稿/第N卷/第N章.md` 的正文内容发生创作性改写，就必须遵守本 lane 的 DeepSeek 执行层边界。
- 人工反馈里出现“对白都像同一个人”“句式反复”时，优先视为 prompt/context pack 源层问题，而不是单章偶发瑕疵；先修声纹导入和句式门禁，再返工正文。
