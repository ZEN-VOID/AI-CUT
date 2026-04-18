# 林青霞表演视角 · CONTEXT

## Context Health

- status: ok
- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- last_checked: 2026-04-15
- maintenance_policy: 知识库模式；优先更新 Type Map、Repair Playbook、Reusable Heuristics。详细过程和低频材料外置到 `CHANGELOG.md` 或 `reports/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 输出像普通“冷艳美人”建议 | `SKILL.md` 模型未触发 | 强制使用 `mirror_duality / reverse_gaze / old_dream_fire` 中至少两个字段 | 回答工作流保留“镜前身份 + 镜后伤口 + 看回去动作” | 答案含视线主动权和时间压力 |
| 过度女神化 | 表达 DNA 偏移 | 删除“绝代美人”式空赞美，补角色伤口、凝视压力和退场余温 | 反模式中保留“美貌是压力，不是答案” | 角色不只被夸漂亮 |
| 性别流动猎奇化 | `gender_power` 漏用 | 改成权力、欲望、孤独和身体轮廓分析 | 字段映射固定 `gender_power` 作为反串/雌雄同体入口 | 不出现“像男/像女”作为核心判断 |
| 类型片建议只讲造型 | `myth_outline` 与情感根断开 | 增加旧梦、烈性、镜后破绽或时代压力 | 高风格角色必须同时写视觉轮廓与情感破口 | 答案既有视觉方案也有角色动机 |
| 退场戏拖沓说教 | `exit_afterglow` 漏填 | 删除解释性台词，保留最后动作、物件或目光 | 退场类问题固定输出“余温动作” | 结尾有可拍摄的动作，不是总结发言 |
| 事实错误或伪引用 | source_check 缺失 | 回到 `references/research/` 或联网核对 | 作品、奖项、访谈和近年动态必须标注来源等级 | 无来源时降级为推断 |
| 目录真源漂移 | research/scripts 与 `SKILL.md` 分落到不同目录 | 删除半成品重复目录，保留含 `SKILL.md + CONTEXT.md + references/research + scripts` 的唯一 skill 根 | 新建或迁移本 skill 时先跑 `find <skill-root> -maxdepth 3 -type f`，确认自包含结构完整 | 目标 skill 根下同时存在合同、经验层、研究文件和脚本 |

## Repair Playbook

1. 先判断失败类型：泛化、女神化、事实错、性别猎奇、只有造型、退场拖沓。
2. 回读 `SKILL.md` 的字段中心映射，定位对应 `field_id`。
3. 回读 `references/research/0X-*.md`，补证据或降级不确定表述。
4. 修正输出时先落到轮廓、视线、身体和镜头，再补情绪解释。
5. 维护目录时确认只有一个 canonical skill root；若出现只有 `references/` 或 `scripts/` 的半成品同名目录，先清理再验证。
6. 若修复属于稳定规则，更新 `SKILL.md`；若属于运行经验，更新本 `CONTEXT.md`；不要把过程流水写进这里。

## Reusable Heuristics

- 林青霞式表演建议必须同时处理“被看见”和“看回去”。只有美貌描写会失真。
- 处理《东方不败》式气质时，先分析权力结构，再谈性别外形。
- 冷艳不是没情绪，而是角色暂时不把情绪交出来；表演方案应设计给、收、转身的节拍。
- 旧梦人物不能只柔美，必须有烈性、刺或时代伤口。
- 高风格角色先定轮廓，但最后必须回到角色为什么非这样站在镜头里不可。
- 退场类表演不宜解释完；留下一个物件、一眼回身或一步离开，通常比长台词更接近这个视角。

## Source Notes

- 机构来源优先：HKU、UCLA、CUHK、Criterion。
- 近年访谈可用于写作身份和公共状态：Tatler Asia、Taipei Times。
- 百科、粉丝剪辑、论坛和无法核验转述默认低权重；仅可用于发现线索，不进入高权重证据。

## Promotion Candidates

- 若演员组继续增加女演员视角，可把“凝视权力/造型文本/退场余温”抽象为演员组共享模板。
- 若性别流动角色在多个演员 Skill 中复用，应提升为演员组共享硬门槛：先问权力与欲望，再问妆发和外形。

## Evidence Links

- 主要调研见 `references/research/01-writings.md` 至 `06-timeline.md`。
