# 张曼玉表演视角 CONTEXT

## Context Health

- last_checked: 2026-04-15
- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- maintenance_policy: 知识库模式；优先更新 Type Map、Repair Playbook、Reusable Heuristics。详细过程、来源长摘录和低频材料外置到 `references/research/` 或 `reports/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 输出像普通“优雅女神”赞美 | `SKILL.md` 的留白与身段字段未触发 | 强制回到 `gesture_subtraction / qipao_as_prison / ordinary_emotion` 至少两个字段 | 回答工作流要求每次给身体动作和镜头留白 | 答案包含具体手、肩、步伐、眼神或停顿 |
| 把张曼玉写成单一《花样年华》符号 | 资料维度过窄 | 加入 `Police Story`、`Center Stage`、`Irma Vep`、`Comrades`、`Clean` 的转型链 | 研究维度固定覆盖早期工业训练、王家卫、关锦鹏、陈可辛、Assayas | 答案能处理喜剧、动作、传记、爱情、欧洲作者片 |
| 表演建议过度沉默、不可执行 | 留白模型被误用成“少演就好” | 给出“减什么、留什么、在哪一拍破口” | Playbook 固定要求“减法之后补一个可见动作” | 答案不只说克制，而写明破口动作 |
| 事实错误或奖项错置 | `references/research/` 未核对 | 优先核对 Cannes、BFI、香港电影资料馆、Berlinale/奖项资料 | 对奖项、时间线、复出动态标注来源等级 | 无来源时改为“待核对/低置信” |
| 转型建议太励志 | 忽略其职业选择里的拒绝和退出 | 用 `refusal_as_craft` 字段重写 | 启发式保留“拒绝重复是表演的一部分” | 建议包含“不接/不演/退后”的判断 |
| 跨文化角色分析空泛 | 未使用语言与语境压力 | 加入 `language_displacement` 研究维度 | 表格中保留跨语境表演字段 | 答案说明语言、口音、异乡身份如何进入角色 |
| 造型分析只讲美 | `qipao_as_prison` 漏用 | 写出造型如何限制身体和制造社会目光 | 任何服装/造型问题必须回答“它让角色不能做什么” | 答案不只描述服装颜色或漂亮 |
| 女娲合并脚本误报来源数为 0 | `01-06` 调研文件未内嵌 URL，只在 `00-source-index.md` 集中列源 | 把关键 URL 回填到每个维度文件 | 新建人物 skill 时既保留 source index，也在 `01-06` 文件写入本维度来源 URL | `merge_research.py` 总来源数不低于 10 |

## Repair Playbook

1. 先判断失败类型：泛化、女神化、事实错、动作不可执行、只会《花样年华》、或跨语境分析不足。
2. 回读 `SKILL.md` 的轻量字段映射，锁定对应 `field_id`。
3. 回读 `references/research/0X-*.md`，补证据或降级不确定说法。
4. 修正输出时先落到身体，再落到镜头，最后补一句角色命题。
5. 运行 `merge_research.py` 时若来源数异常，优先检查 `01-06` 调研文件是否含本维度 URL；`00-source-index.md` 不会被该脚本计数。
6. 若修复属于稳定规则，更新 `SKILL.md`；若属于运行经验，更新本 `CONTEXT.md`；不要把过程流水写入这里。

## Reusable Heuristics

- 张曼玉式表演不是“永远少演”，而是先删掉外露解释，再保留一个会泄露角色处境的小动作。
- 处理旗袍、发型、妆面、空间时，先问它们如何限制身体；美感必须带来压力，否则只是造型评论。
- 处理转型问题时，不把“多栖”写成勤奋神话；重点是她如何从高产类型片训练中，选择更难、更慢、更不重复的角色。
- 处理跨文化角色时，语言不只是台词媒介，也会改变人物的防御、尴尬、距离和自我翻译。
- 对低调近况和社交平台动态，只记录可核验的公开出现，不把粉丝期待写成本人复出意图。
- 女娲模板的结构锚点要优先满足工具识别，例如 `表达DNA` 不拆成 `表达 DNA`；可读性微调不能破坏质量脚本。

## Source Notes

- 高权重来源：Festival de Cannes、BFI、香港电影资料馆、Berlinale/官方奖项、Criterion、导演或演员访谈。
- 中权重来源：The Guardian、The Independent、GQ、The Straits Times、AnOther 等可追溯媒体长文。
- 低权重来源：百科、粉丝整理、短社媒转述。只用于发现线索，不作为核心证据。

## Promotion Candidates

- 若演员组继续沉淀女性演员视角，可把“造型限制身体”“留白与破口”“拒绝重复”抽象为演员组共享表演模板。
- 若跨文化/跨语言表演在多个 actor skill 中复用，应提升为演员组主合同的研究维度，而不是保留在单人 skill。
