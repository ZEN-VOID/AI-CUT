# Output Template

## Output Contract Alignment

- Required output: `projects/story/<项目名>/2-卷章/第N卷/第N章.md`，或对该文件的局部 section patch / review verdict。
- Output format: Markdown 章级规划；完整正文结构由 `templates/chapter-planning.template.md` 承载。
- Output path: canonical 业务真源固定为 `projects/story/<项目名>/2-卷章/第N卷/第N章.md`。
- Naming convention: 卷目录使用 `第N卷`，章文件使用 `第N章.md`；任务 ID 和引用 ID 保持 ASCII 安全字符。
- Completion gate: 上游已回读，必填标题齐全，本章时间推进继承卷级时间线且含 `chapter_start_state / visible_time_span / event_order / parallel_hidden_events / chapter_end_state / handoff_to_next_chapter`，爽点设计齐全且能回指读者期待、卷级 promise、类型画像、角色个性与可验证兑现动作，本章悬念开关继承卷级悬念且能约束读者可知、角色可知、悬念线程动作、隐藏、误导、揭秘、只埋不揭、悬念负载和正文禁区，所有高潮点具备 `payoff_variation_axis`，高超对决额外具备 `duel_variation_axis`，夸张设计有角色动机、处境压力或成长节点支撑，节奏 handoff 齐全且含 Mermaid，`payoff_type / micro_payoff / rhythm_intensity / previous_next_contrast` 可复核并与爽点设计和悬念压力一致，任务线可汇聚，线索/伏笔分离且服从悬念开关，无正文越界，review verdict 至少为 `pass_with_followups`。

## Final Output

完整章级规划请使用：

- `templates/chapter-planning.template.md`

局部修订输出应包含：

| section | patch_summary | replacement_or_delta | validation_note |
| --- | --- | --- | --- |
| `[目标标题]` | `[本次改动摘要]` | `[可直接写回的局部内容]` | `[对应 review gate]` |

## Evidence

- 上游 `整体规划.md` 已读取：
- 目标卷 `卷规划.md` 已读取：
- 命中的 Cards 真源：
- review verdict：
