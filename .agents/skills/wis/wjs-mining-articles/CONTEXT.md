# Context: wjs-mining-articles

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2260
current_lines: 47
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-mining-articles` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 用户只有视频/音频，没有 SRT，却直接开始挖文章 | input routing | 先转 `wjs-transcribing-audio` 生成 SRT | 本技能入口固定为 SRT -> topics -> articles -> drafts | 本轮存在可读 SRT 路径与解析输出 |
| 对谈里默认“说得最多的人就是王建硕” | speaker attribution | 暂停选题，贴开头对话让用户确认谁是王建硕 | 对谈路径必须先确认 speaker 身份 | 用户确认前不进入 Step 2 选题清单 |
| 把对方观点写成王建硕第一人称主张 | attribution boundary | 移除或改成引子/背景，存疑句交给用户判 | `source.srt.md` 记录对谈来源、对方身份和引用边界 | article 主体只承载王建硕展开过的观点 |
| 多个独立观点被硬塞成一篇长文 | topic mining | 重新拆成“一篇一个核心”的候选清单 | Step 1 先识别 N 个独立话题，再让用户勾选 | 每篇都有独立标题、主张、时间段 |
| article.md 仍像逐字稿，保留大量口头碎屑 | writing transformation | 书面化重写，删除“呃/然后/就是说”等口语噪声 | 字幕只作原料，正文按公众号成稿标准创作 | 正文 800-1000 字，逻辑成段且保留作者语气 |
| 缺 `meta.json` 或 `source.srt.md`，后续题图/草稿无法复用 | handoff artifact | 补齐每篇文件夹三件套 | 输出合同固定为 `article.md + meta.json + source.srt.md` | publishing 脚本能读取 title / summary / slug |
| 忘记盘古之白或红色加粗 | publishing constraint reuse | 跑 pangu，并补 2-4 处点睛句加粗 | 复用 `wjs-publishing-wechat` 的成稿约束，不另立标准 | 正文含 2-4 处 `**...**`，中英文空格已处理 |
| 自动群发微信公众号 | publishing boundary | 只建微信草稿，群发留给用户后台手动决定 | 本技能停止在“后台已有草稿”状态 | 没有执行群发动作，只交付草稿状态 |

## Repair Playbook

1. 先确认输入是 SRT；没有 SRT 时路由到转写技能，不用本技能硬猜内容。
2. 解析 SRT 后先判断独白还是对谈；跳过寒暄、调设备、休息等非正片口水段。
3. 对谈必须先让用户确认谁是王建硕；ASR 人名和身份存疑时不要替用户认领。
4. 输出候选选题并等待用户勾选；≤4 篇用多选，>4 篇用表格编号并接受“全要”。
5. 只为选中的话题成文；写前载入 `wangjianshuo-perspective`，并沿用 `wjs-publishing-wechat` 的字数、加粗、无 AI 味约束。
6. 每篇落到独立文件夹，补齐 `article.md`、`meta.json`、`source.srt.md`，再跑 pangu。
7. 建草稿时调用 publishing 现成脚本；图片/草稿生成失败应按篇记录，不影响其他已完成文章。
8. 用户要同步发 X 时，转交 `wjs-tweeting-from-articles`，本技能不自建排期规则。

## Reusable Heuristics

- 时间段是文章溯源锚点，不是机械切片边界；话题跨多块时取第一块起到最后一块止。
- 长对谈可以一次挖 10+ 篇，但派并行 agent 前必须先统一 speaker 归属、ASR 更正和候选边界。
- 对方的话可以作为“有人问我...”式引子，但不能成为正文核心论点。
- `source.srt.md` 是可追溯 sidecar，不是把完整 SRT 无筛选灌入业务真源。
- “全要”只在用户看到候选清单之后有效；不能先默认全写。
- 选题排序优先看观点强度和“像王建硕招牌观点”的程度，而不是按时间线平均分配。

## Promotion Backlog

- 增加 article folder validator：检查三件套、meta 字段、字数区间、加粗数量和 source 时间段。
- 为长对谈批量建草稿增加幂等 runner，图已存在时跳过，逐篇记录成功/失败。
- 增加对谈 speaker attribution checklist，派并行 agent 前作为必填输入。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
