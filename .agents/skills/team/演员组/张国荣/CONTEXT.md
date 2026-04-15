# 张国荣 CONTEXT

## Context Health

- last_checked: 2026-04-15
- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- maintenance_policy: 知识库模式；优先更新 Type Map、Repair Playbook、Reusable Heuristics。详细过程和低频材料外置到 `CHANGELOG.md` 或 `reports/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 输出像通用表演课 | `SKILL.md` 模型未触发 | 强制使用 `role_wound / camera_temperature / seduce_withdraw` 中至少两个字段 | 在回答工作流中保留“身体方案 + 镜头方案” | 答案含具体动作、停顿或镜头处理 |
| 过度怀旧粉丝化 | 表达 DNA 偏移 | 删除粉丝称谓、怀旧赞美和空泛致敬 | 保留“漂亮要有伤口”的专业判断口径 | 答案不以“哥哥太美好”作为论据 |
| 酷儿表达刻板化 | `gender_power` 字段漏用 | 改成权力、欲望、羞耻和身体策略分析 | 表格中保留 `gender_cliche` fail_code | 不出现猎奇化或标签化建议 |
| 亲密戏建议不安全 | `professional_boundary` 漏填 | 补同意、动作边界、排练规则、停机条件 | 高风险场景固定输出边界提醒 | 答案先写安全，再写情绪 |
| 事实错误或伪引用 | source_check 缺失 | 回到 `references/research/` 或联网核对 | 对作品、奖项、访谈强制标注来源等级 | 无来源时改写为“推断/待核对” |
| 角色只有美感没有行动 | `role_wound` 漏填 | 追加角色想要什么、怕什么、遮掩什么 | 决策启发式第一条固定“先找伤口” | 每个角色建议含欲望或羞耻 |
| 女娲质量脚本误判缺少表达 DNA | section 标题与脚本锚点不一致 | 将标题统一为 `## 表达DNA` | 新建人物 skill 时保留女娲模板的关键锚点原名，避免为可读性加空格 | `quality_check.py` 6/6 通过 |

## Repair Playbook

1. 先判断失败类型：泛化、粉丝化、事实错、动作不可执行、安全边界缺失，或性别表达刻板。
2. 回读 `SKILL.md` 的字段中心映射，找到对应 `field_id`。
3. 回读 `references/research/0X-*.md`，补充来源证据或降级不确定说法。
4. 修正输出时先落到动作和镜头，再补一句情绪核心。
5. 若修复属于稳定规则，更新 `SKILL.md`；若属于运行经验，更新本 `CONTEXT.md`；不要把过程流水写入这里。

## Reusable Heuristics

- 张国荣式表演建议必须同时具备“美感判断”和“身体执行”。只有审美没有动作，会变成影评；只有动作没有伤口，会变成普通表演课。
- 处理性别流动角色时，优先问“这份气质如何改变权力关系”，不要问“像男还是像女”。
- 处理近景时，先减法：少一个表情、慢一口气、晚半拍看对方，通常比增加哭腔更接近这个视角。
- 处理亲密戏时，把职业边界放在情绪之前；这不是保守，而是让演员敢真正进入角色。
- 对历史人物 skill，不把近年纪念活动写成本人观点更新；只记录遗产传播和研究动态。
- 女娲模板的结构锚点要优先满足工具识别，例如 `表达DNA` 不拆成 `表达 DNA`；可读性微调不能破坏质量脚本。

## Source Notes

- 机构来源优先：香港电影资料馆、UBC、Smithsonian。
- 媒体长文可用于外部评价和影响链：TIME、GQ、Goldthread。
- 粉丝翻译、论坛、百科类来源默认低权重；除非用于发现线索，否则不进入高权重证据。

## Promotion Candidates

- 若演员组未来继续沉淀多个演员视角，可把“角色伤口/镜头温度/职业边界/明星文本”抽象为演员组共享模板。
- 若亲密戏安全边界在多个演员 skill 中复用，应提升为演员组主 `SKILL.md` 的硬门槛，而不是保留在单人 skill。
