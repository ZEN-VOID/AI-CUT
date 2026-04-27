# Context: 4-润色

本文件是 `story-polishing` 的经验层知识库，不是过程日志。它用于沉淀从 `3-初稿` 到 `4-润色` 的二次改写、中文表达优化与题材质感校准经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-polishing-rules-expandable
last_checked_at: 2026-04-26
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-POLISH-01` | 润色稿像重新写章，初稿事实丢失 | source anchoring | 把 `3-初稿` 作为 prompt 主输入，并要求保留事件顺序、人物动机、信息揭示和章末牵引 | 父级 gate 固定 `G1-SOURCE-ANCHOR`，sidecar 记录源初稿路径 | 润色稿可逐段追溯初稿事实 |
| `TM-POLISH-02` | 语言通顺但仍有翻译腔、说明腔或 AI 腔 | Chinese prose texture | 加入中文语感门禁：句群呼吸、自然停顿、少解释多动作、对白保留潜台词 | 系统提示中把“中文表达风格”拆成可检查的句群、段落、对白与动作要求 | 连续段落读起来不像说明文、摘要或模型整理稿 |
| `TM-POLISH-03` | 润色后题材味变淡，文本变成通用顺滑 | genre texture | 回读 `north_star.yaml.genre_contract`，把题材压力转成场景、情绪、对白和心理节奏 | 父级 gate 固定 `G3-GENRE-TEXTURE`，禁止把题材锋芒磨平 | 题材质感能在正文手感中显现，而不是只在设定词中出现 |
| `TM-POLISH-04` | 输出成点评、修改建议或差异说明 | output shape | 强制完整 Markdown 章节输出，禁止说明过程和多个版本 | lane 模板固定 frontmatter + heading + prose | 文件可直接作为 `4-润色/第N卷/第N章.md` 落盘 |
| `TM-POLISH-05` | 润色稿只做同义词替换，读感变化很小 | shallow rewrite | 要求重做句群节奏、段落密度、动作/感官/对白/心理层面的二次加工 | 将“不是同义词替换”上升为父级 Base Polishing Rule | 抽查三段以上能看到叙述重心和节奏变化 |
| `TM-POLISH-06` | 润色稿为了高级感删掉爽点、压低情绪或抹平人物声音 | over-smoothing | 回到项目 `MEMORY.md` 和 `north_star`，恢复口味、人物声音、爽点/悬疑/情绪压力 | 系统提示禁止“清洗风格”为通用顺滑文本 | 润色后仍保留项目的锋芒、口味和人物辨识度 |
| `TM-POLISH-07` | local repair 扩大成整章重写 | repair scope creep | 根据 finding 标注段落、问题类型和最小修复范围 | `local_repair` 默认不扩大；除非 finding 指向全章失效 | 修复 diff 只影响问题区域及必要上下文 |
| `TM-POLISH-08` | 既有 `4-润色` 被覆盖但没有 backup 或显式确认 | writeback safety | 阻断正式写回，要求 `--force` 或等价确认并生成 backup sidecar | lane script 固定覆盖保护 | 覆盖前后均能追溯旧润色稿 |
| `TM-POLISH-09` | frontmatter 写入大量 planning/context 摘要 | metadata density | 只保留 `润色模型` 与 `初稿来源`，其它证据写入 sidecar | 输出模板和 validator 禁止上下文摘要进正文 YAML | YAML 头极简，正文 token 留给 prose |
| `TM-POLISH-10` | 用户要“更像中文”，但结果只是口语化、变浅 | Chinese style overcorrection | 区分自然中文与随意口语，保留文学密度、场景压力和语义层次 | 在 prompt 中同时要求自然语感与题材质感 | 文本更顺，但没有损失信息密度和气氛 |

## Repair Playbook

1. 先检查当前章 `3-初稿/第N卷/第N章.md` 是否存在；缺失时硬失败，不用 planning 补写。
2. 若用户只说“润色”，默认走 `B-Doubao流`；点名 GPT 或 DeepSeek 时进入对应 lane。
3. 若目标 `4-润色` 已存在，先回读既有润色稿；正式覆盖必须要求显式确认并保留 backup sidecar。
4. 若润色稿改动了核心剧情，回到初稿事实锚点，要求“只改表达，不改事件”。
5. 若润色稿只变顺但没质感，回读 `north_star.yaml.genre_contract` 与风格约束，把题材压力落实到段落节奏、场景密度和对白。
6. 若输出像点评或建议，回到 lane 模板，要求只输出完整 Markdown 文件本身。
7. 若 local repair 扩大为整章重写，重建 finding -> affected span -> minimal patch 的修复边界。
8. 若 provider/GPT 输出缺 `润色模型` 或 `初稿来源`，回到输出模板和 validator，而不是把上下文引用塞进正文 YAML。
9. 若需要扩容规则，优先把经验沉淀到本 `CONTEXT.md`；稳定后再晋升到 `SKILL.md` 的 Base Polishing Rules 或 Quality Gates。

## Reusable Heuristics

- 润色的第一真源是 `3-初稿` 正文，不是 planning；planning 只负责校准义务和防止偏航。
- “更像中文”通常不是堆成语，而是减少解释性连接词，增加动作、感官、停顿和对白中的潜台词。
- “更符合题材”不能只替换词汇；要让风险、欲望、恐惧、爽点或悬疑压力进入句群节奏。
- 好的二改会让读者感到人物更像活人在现场反应，而不是让文本变得更像规范答案。
- 悬疑/惊悚类润色要保留信息遮蔽、误导、延迟揭示和不安细节，不能把所有逻辑解释得过早。
- 武侠/动作类润色要保留招式节奏、身体受力、空间调度和江湖语气，不能只做华丽形容。
- 都市/现实类润色要保留生活纹理、利益压力、场景物件和口语分寸，不能写成抽象情绪散文。
- 爽文类润色要保护爽点的蓄力、释放和反馈，不要为了“文学化”削弱即时回报。
- 润色阶段最容易越权的是补剧情，最容易不足的是只换同义词；二者都不是合格二改。
- 父级 `4-润色` 只沉淀跨 lane 的稳定经验；provider 独有的失败模式应写入对应 lane 的 `CONTEXT.md`。
