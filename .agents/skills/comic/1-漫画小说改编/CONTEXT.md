# Context: 漫画小说改编

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~5200
current_lines: ~95
current_cases: 1
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-13T18:30:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件用于沉淀 `漫画小说改编` 的来源适配经验、钩子经验、失败类型与可晋升 heuristic，不记录过程流水。

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-COMIC-01` | 改编稿像摘要，不像小说 | 正文执行层 | 回到章节骨架，把摘要句改写成场景、动作、对白 | 在 `comic-novel-writing-spec` 固化“场景先于解释” | 任一章节都能拆出至少一个明确场景 |
| `TM-COMIC-02` | 图片/视频改编很美，但没有剧情发动机 | 来源归一层 | 重做 `source_digest`，补齐前因后果、关系与未解点 | 在来源路由表中固定“视觉奇点必须转事件链” | 成稿能回答“谁想要什么、被谁阻拦” |
| `TM-COMIC-03` | 新闻/热搜改编后事实与虚构混淆 | 事实边界层 | 增加 `boundary_note`，把真实信息与虚构承载角色拆开 | 在 `hotsearch-news-adaptation` 固化三种边界模式 | 读者能区分事实锚点与剧情扩写 |
| `TM-COMIC-04` | 章末没有追更欲 | 钩子层 | 回到 `hook_pack`，重写为未闭合缺口 | 在主合同强制每章命中一种钩子类型 | 任一章末都能提出“下一章必须看的理由” |
| `TM-COMIC-05` | 文稿可读但不利于后续漫画生成 | 下游桥接层 | 补角色外观、动作节点、场景奇点与关键道具 | 在桥接包强制要求视觉锚点表 | 下游可以直接提取角色/场景/动作清单 |
| `TM-COMIC-06` | 多源素材互相打架，稿子没有主线 | 汇流层 | 先裁定主锚点，再删去从属重复信息 | 在来源归一细则中固定“多源先裁主后融合” | 成稿能用一句话说清主冲突 |
| `TM-COMIC-07` | 氛围写得浓，但漫画页冲击力不足 | 正文前置设计层 | 在写正文前补锁 `impact_beats / impact_map`，先定大格候选与翻页点 | 在主合同和写作规格中强制“冲击画面预演” | 读完后能明确指出至少 2-3 处适合做大格/跨页 |
| `TM-COMIC-08` | 文字有画面，但作为解说旁白念出来发绕发满 | 声音栈设计层 | 回到 `voice_brief`，删解释重句，重做句长与停顿 | 在主合同中增加 `delivery_flavor=explainer_comic_compatible` 与朗读门禁 | 抽读关键段时能一口气念顺，且不损失画面感 |

## Repair Playbook

1. 先判定失败点在来源归一、事实边界、剧情发动机、章末钩子还是视觉桥接。
2. 若稿子发虚，先回 `source_digest` 与 `adaptation_brief`，不要只补辞藻。
3. 若新闻/热搜类稿子失真，优先修 `truth_boundary`，不要直接重写剧情。
4. 若“有情节没追更欲”，优先重写章末钩子，而不是扩写整章。
5. 若“能读不能画”，优先补视觉桥接层，而不是继续堆解释性内心戏。

## Reusable Heuristics

- 对漫画小说而言，真正稀缺的不是文采，而是“每一章都能拆成几页漫画”的可视化密度。
- 来源是图片或视频时，最稳的做法不是描述画面，而是推断“这幅画面之前刚发生了什么、之后最可能发生什么”。
- 热搜/新闻最适合改成“事实锚点 + 虚构人物承载线”，既保住讨论度，也避免伪纪实滑坡。
- 钩子不等于硬拐弯；它更像是在冲突最贵的位置故意停笔。
- 同一篇稿子里，钩子类型最好轮换使用：危险逼近、真相留白、身份反转、代价升级交替出现会更稳。
- 如果正文中几乎没有动作节点、目光变化、场景切换和能入镜的细节，后续漫画生成一定会吃力。
- 氛围感最稳的写法不是加更多形容词，而是提前锁定“哪一格要让读者停住”，然后反推声场、光线、物件和动作停顿。
- 对恐怖/悬疑单章，最值钱的往往不是解释真相，而是让异常先以“半显形”进入画面：先听见、再看见一点、最后才揭开全貌。
- 解说漫兼容的关键，不是先写小说再硬切旁白，而是在正文生成时就让句子同时承担“带观众看”与“替镜头压气”的双重职责。
- 最好的旁白句往往也是最好的漫画说明句：短、准、带一个可见物和一个正在发生的变化。

## Case Log

## [20260413-001] 2026-04-13 11:30 PDT - 初始化“漫画小说改编”技能真源

### 元信息

- milestone_type: new_success_class
- 范围/目标: 为 `.agents/skills/comic/漫画小说改编` 建立可执行的单技能真源，覆盖文本、图片、视频、新闻热搜到漫画小说底稿的改编链。
- 触发（用户原话或摘要）: “完善 `.agents/skills/comic/漫画小说改编`，将任意资料改编为精彩的漫画小说，默认概念包含多类章末钩子、类型化示例以及网络热搜参照。”
- 涉及技能:
  - `.agents/skills/comic/漫画小说改编`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-知行合一`
- layered_trace:
  - symptom/failure: 目标目录存在但没有实际技能合同，无法稳定处理多来源改编与章末钩子控制。
  - direct technical cause: 缺少 `SKILL.md`、`CONTEXT.md`、入口元数据与来源/钩子/热搜细则真源。
  - rule source: `.agents/skills/comic/漫画小说改编/SKILL.md` 及 `references/*`
  - meta rule source: 仓库 `AGENTS.md` 的 Rollout Standard、Root-Cause First、Canonical Source Governance，以及 `skill-知行合一` 的 skeleton-first 合同
- 产出物/变更路径:
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/comic/漫画小说改编/CONTEXT.md`
  - `.agents/skills/comic/漫画小说改编/agents/openai.yaml`
  - `.agents/skills/comic/漫画小说改编/references/source-intake-and-mode-selection.md`
  - `.agents/skills/comic/漫画小说改编/references/comic-novel-writing-spec.md`
  - `.agents/skills/comic/漫画小说改编/references/hook-ending-playbook.md`
  - `.agents/skills/comic/漫画小说改编/references/hotsearch-news-adaptation.md`
- evidence paths:
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/comic/漫画小说改编/references/hook-ending-playbook.md`
- 用户反馈: 希望技能能处理任意来源，默认强调漫画生成友好的小说化改编与高强度章末钩子。

### Feature / Positive（可复用经验）

- F1:
  - 证据: 将“来源归一 -> 事实边界 -> 剧情发动机 -> 章节正文 -> 钩子 -> 视觉桥接”写成单一思行网络后，文本/图像/视频/热搜输入终于能走同一条可复用执行链。
  - 复用方式: 以后凡是“任意来源 -> 小说/脚本底稿”的技能，都应先做来源归一与边界裁决，再进入文学化与结构化写作。
  - 适用边界: 适用于需要面向后续视觉生成、分镜或长链内容消费的改编型技能。

## [20260413-002] 2026-04-13 12:20 PDT - 将“画面冲击预演”前置为漫画小说真源合同

### 元信息

- milestone_type: source_contract_change
- 范围/目标: 解决“正文有氛围但漫画冲击点后置、只能事后补桥接”的执行缺口。
- 触发（用户原话或摘要）: “氛围感再加强一点……在创作时预先考虑到相应漫画表现时画面冲击力的方便？”
- 涉及技能:
  - `.agents/skills/comic/漫画小说改编`
  - `.agents/skills/aigc2026/1-编剧/6-氛围感`
- layered_trace:
  - symptom/failure: 当前合同强调视觉锚点和桥接包，但没有把“高冲击画面候选”前置到正文设计阶段。
  - direct technical cause: `SKILL.md` 与 `comic-novel-writing-spec.md` 缺少强制性的 `impact_beats / impact_map / 翻页点` 预演要求。
  - rule source: `.agents/skills/comic/漫画小说改编/SKILL.md`、`.agents/skills/comic/漫画小说改编/references/comic-novel-writing-spec.md`
  - meta rule source: 仓库 `AGENTS.md` 的 Root-Cause First、Canonical Source Governance 与 `atmosphere-elevation` 的“氛围必须可拍摄、可分镜、可回收”约束
- 产出物/变更路径:
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/comic/漫画小说改编/references/comic-novel-writing-spec.md`
  - `.agents/skills/comic/漫画小说改编/CONTEXT.md`
- evidence paths:
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/comic/漫画小说改编/references/comic-novel-writing-spec.md`
- 用户反馈: 希望氛围感更强，同时在创作时就考虑漫画表现的画面冲击力。

### Root Cause / Fix / Prevention

- 根因位置: `漫画小说改编` 的真源更偏“写完后桥接”，缺少“写前先锁炸点画面”的门禁。
- 立即修复: 在主合同加入 `manga_impact_profile`、`impact_beats`、`impact_map`、大格/翻页点要求，并将氛围定义为可分镜的情绪压力场。
- 系统预防修复: 在写作规格中固定“冲击画面预演”，并在经验层沉淀“氛围不足不等于多写形容词，而是要前置冲击页设计”的 heuristic。

## [20260413-003] 2026-04-13 12:45 PDT - 为漫画小说改编加入“解说漫兼容”双栈合同

### 元信息

- milestone_type: source_contract_change
- 范围/目标: 让 `漫画小说改编` 在保持漫画画面感的同时，能直接产出适合解说漫朗读的沉浸式描述。
- 触发（用户原话或摘要）: “能否设计为兼容解说漫的创作逻辑……既要有漫画画面感，还要有解说的声音沉浸感……不啰嗦，不冗余，沉浸式。”
- 涉及技能:
  - `.agents/skills/comic/漫画小说改编`
  - `.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧`
- layered_trace:
  - symptom/failure: 当前技能能产出强画面稿，但缺少“作为旁白直接读出来也成立”的声音栈约束。
  - direct technical cause: `SKILL.md` 与写作规格未定义 `delivery_flavor / narration_density / voice_brief`，也未继承解说剧的同命题声画约束。
  - rule source: `.agents/skills/comic/漫画小说改编/SKILL.md`、`.agents/skills/comic/漫画小说改编/references/comic-novel-writing-spec.md`
  - meta rule source: 仓库 `AGENTS.md` 的 Root-Cause First、Canonical Source Governance，以及 `解说剧` 技能的“旁白主导 + 同命题配对”约束
- 产出物/变更路径:
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/comic/漫画小说改编/references/comic-novel-writing-spec.md`
  - `.agents/skills/comic/漫画小说改编/CONTEXT.md`
- evidence paths:
  - `.agents/skills/comic/漫画小说改编/SKILL.md`
  - `.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md`
- 用户反馈: 要求同时兼容漫画画面感与解说旁白沉浸感，且语言不啰嗦、不冗余。

### Root Cause / Fix / Prevention

- 根因位置: 旧合同只有视觉栈，没有声音栈，导致“能画不能念”的隐性质量缺口。
- 立即修复: 加入 `delivery_flavor=explainer_comic_compatible`、`narration_density`、`voice_brief`、`narration_ready_passages` 与朗读门禁。
- 系统预防修复: 显式引用 `解说剧` 技能作为旁白约束来源，并在写作规格里固化“句长控制、停顿设计、去冗余解释”的声画双栈规则。
