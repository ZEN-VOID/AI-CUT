# CONTEXT.md

本文件是 `story2026 / 3-初稿` 的经验层知识库。它记录章节初稿的上下文加载、正文真源、防漂移、最小写回和单根技能包运行经验，不再维护旧分支经验。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-single-root-drafting-context
last_checked_at: 2026-06-10
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 普通写章请求仍被分流到旧子目录 | topology drift | 直接进入 `.agents/skills/story/3-初稿/SKILL.md` | 根技能声明单一阶段入口 | `rg` 不再出现旧分支子路径主路由 |
| 初稿正文头部继续写 `写作模型` 并按该字段返工 | metadata drift | 新产物改用 `创作阶段: 初稿` 与 `字数`；旧字段只作 legacy 读取 | Output Contract 固定阶段字段，不把旧 metadata 作为路由真源 | 新模板不含 `写作模型` |
| 正文看起来像 planning 摘要而不是小说 | prose conversion gap | 回到 `N5-CREATIVE-DRAFT`，逐条把任务义务转成现场动作、物件、对白和章末牵引 | `references/chapter-drafting-contract.md` 固定 prose conversion 与现场发现门 | 正文无 planning 标题句法 |
| 新章只接最近上一章，漏掉同卷早前伏笔和线索 | continuity underload | 加载当前卷全部已存在前序章，最近前章只负责开章姿态 | Context Loading Contract 与 `N3-CONTINUITY` 固定全部前序章清单 | `continuity_bridge.previous_chapter_refs` 覆盖同卷前文 |
| 监制意见泛泛，没有进入正文创作约束 | supervision packet gap | 回读 `_shared/supervised-drafting-review-loop-contract.md`，按项目 `team.yaml` 请教具体问题 | `N4-SUPERVISION` 要求 packet 或降级说明 | 报告可追溯 roster、问题、摘要和可执行指导 |
| 执行环境提示被误当成技能分流 | execution environment confusion | 仍进入本技能，只记录执行备注 | 根合同禁止创建分支入口 | 输出路径仍是 `3-初稿/第N卷/第N章.md` |
| 情绪表达反复落在脸色颜色变化 | emotion shorthand loop | 改用动作、呼吸、手部、视线、物件误触、话语断裂或空间退让 | Core Gates 和 review gate 固定脸色捷径门禁 | 抽查关键情绪段不靠脸色颜色词承载 |
| 章节编号、sidecar 等执行层标签进入正文 | narrative perspective leak | 改写为角色可感知的事件、地点、物件或伤亡称呼 | Core Gates 固定叙事内视角完整性 | 正文无 `上一章/本章/frontmatter` 等词 |

## Repair Playbook

1. 若写章入口仍指向旧分支子目录，先修 registry、story 根路由和阶段 `SKILL.md`，再处理正文。
2. 若用户给出执行环境偏好或当前会话写作，不新增分支入口；只在执行报告中记录。
3. 若正文像提纲，回到源层检查 context pack 是否直接泄漏 planning 标题，再让 LLM 重新做小说化转译。
4. 若同卷连续性断裂，先看是否加载了当前卷所有前序章；不要只补一句“承接上一章”。
5. 若目标章已存在，必须先回读并确认是续写、重写还是局部修复；默认不静默覆盖。
6. 若 review 返工涉及创作性改写，回到本根技能的 `local_repair / chapter_rewrite`，不再追溯旧分支。
7. 若脚本或模板产出正文内容，把该产物废弃，回到 LLM-first 主创节点。

## Reusable Heuristics

- `3-初稿` 的核心是把 planning 义务变成有现场、有动作、有声口、有牵引的章节 prose。
- 初稿 frontmatter 越极简越稳；上下文证据放报告或 sidecar，不要挤进正文头。
- 同卷前文是写作连续性的底盘；最近上一章解决入场姿态，早前章节解决事实、伏笔、道具和卷目标进度。
- 章节正文里的读者感受来自场景中发生的发现、误触、沉默和反作用，而不是从 planning 字段翻译出的说明。
