# CONTEXT.md

本文件是 `story2026 / 4-润色` 的经验层知识库。它用于沉淀从 `3-初稿` 到 `4-润色` 的最小局部修补、中文表达局部优化、题材质感校准、AI 腔坏点定位和单根技能包运行经验，不再维护旧分支经验。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-single-root-polishing-context
last_checked_at: 2026-06-10
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-POLISH-01` | 润色稿像重新写章，初稿事实丢失 | source anchoring | 回到 `3-初稿` 源章逐段锚定，只改表达坏点 | `P1-SOURCE-LOCK` 和 `P3-REPAIR-PLAN` 固定源章锚定 | 润色稿核心事实可追溯源初稿 |
| `TM-POLISH-02` | 用户只说润色，却被分流到旧子目录 | topology drift | 直接进入 `.agents/skills/story/4-润色/SKILL.md` | 根技能声明单一阶段入口 | `rg` 不再出现旧分支子路径主路由 |
| `TM-POLISH-03` | frontmatter 继续写 `润色模型` 并按该字段返工 | metadata drift | 新产物改用 `修订阶段: 润色`、`初稿来源`、`字数`；旧字段只作 legacy 读取 | Output Contract 固定阶段字段，不把旧 metadata 作为路由真源 | 新模板不含 `润色模型` |
| `TM-POLISH-04` | 语言变顺但题材味被磨平 | genre texture loss | 回读 `north_star.yaml.genre_contract`，只在必要处加场景压力、对白锋利度和心理节奏 | Base Polishing Rules 固定题材质感保护 | 文本更顺但不通用顺滑 |
| `TM-POLISH-05` | AI 腔只被泛化处理，结果更像规整优化稿 | anti-ai underspecification | 拆成连接词、段落均匀、主谓完整、情绪标签、解释插入语、总结句或角色混声 | `P3-REPAIR-PLAN` 要求具体坏点清单 | repair plan 有可定位坏点 |
| `TM-POLISH-06` | local repair 扩大成整章重写 | repair scope creep | 标注 affected span，只修问题区域和必要上下文 | 默认最小局部修补，整章重润需用户授权 | diff 范围可解释 |
| `TM-POLISH-07` | 场景密度被当成冗余删掉 | density compression | 恢复承载空间、物件、身体反应、关系压力或悬念延迟的颗粒 | Base Polishing Rules 固定密度节奏保护 | 场景仍可感知 |
| `TM-POLISH-08` | 旧润色稿被静默覆盖 | writeback safety | 回读既有稿并要求显式覆盖授权 | `P1-SOURCE-LOCK` 固定覆盖门 | 覆盖证据可追溯 |
| `TM-POLISH-09` | 多维验收或审计只有意见没有优化正文 | acceptance-repair gap | 先按本技能内置验收维度拆审，再把 findings 回灌到 `acceptance_repair` / `local_repair` | `P2A-ACCEPTANCE-BRIEF` 不允许只审不改后宣称完成 | 最终润色稿体现 findings 修复，验收包同步更新 |

## Repair Playbook

1. 先检查当前章 `3-初稿/第N卷/第N章.md` 是否存在；缺失时硬失败，不用 planning 补写。
2. 若用户给出执行环境偏好或当前会话润色，不新增分支入口；只在执行报告中记录。
3. 若目标 `4-润色` 已存在，先回读既有润色稿；正式覆盖必须有显式确认。
4. 若润色稿改动核心剧情，回到源初稿事实锚点，要求“只改表达，不改事件”。
5. 若用户只说“AI 味重”，先定位具体文本特征，不直接触发整章重写。
6. 若润色后场景变空，优先恢复源初稿中承载压力的物件、身体反应、空间距离和信息延迟。
7. 若多维验收或审计只完成意见汇总而没有改稿，回到 `P2A -> P3 -> P4 -> P5`，让 findings 进入正文修补并重新生成验收包。
8. 若脚本或模板产出润色正文，把该产物废弃，回到 LLM-first 润色节点。

## Reusable Heuristics

- 润色的第一真源是 `3-初稿` 正文，不是 planning。
- “更像中文”不是堆成语，也不是口语化变浅，而是减少解释性连接词，让动作、感官、停顿和对白潜台词承担信息。
- 好的二改会让人物更像在现场反应，而不是让文本更像规范答案。
- AI 检测友好的润色通常不是更顺，而是少动：保留初稿句群骨架、长短不齐、局部粗粝和人工式不均匀，只修坏处。
