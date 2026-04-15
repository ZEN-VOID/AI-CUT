# 梁家辉表演视角 CONTEXT

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
| 输出变成"千面影帝"空泛赞美 | `SKILL.md` 模型未触发 | 强制使用 `type_gravity`、`life_origin`、`work_unit` 中至少两个字段 | 回答工作流保留"生活来源 + 类型重心 + 具体动作" | 答案含角色日常、身体重心或工种条件 |
| 黑帮角色只写凶狠 | `power_source` 缺失 | 拆权力来源：制度、仪式、关系、暴躁、沉默、失控 | 黑帮/警匪问题固定先问权力从哪里来 | 不用"气场"替代动作和关系 |
| 喜剧建议只剩夸张 | `serious_comedy` 漏用 | 让角色认真相信自己的逻辑，再调节节拍 | 喜剧场景固定检查误会、身份落差、停顿和反应拍 | 答案包含节拍或反应，而非只叫演员放开 |
| 历史/制服角色外观化 | `costume_language` 漏填 | 把服装转成站姿、手、步速、称谓和口音压力 | 造型建议必须配身体动作 | 每条造型建议有可演动作 |
| 事实错或奖项过时 | source_check 缺失 | 回查 `references/research/00-source-index.md` 与 HKFAA 官方页 | 奖项、提名、近况使用绝对日期 | 2026-04-19 前只写第 44 届提名 |
| 把《情人》简化为性感 | `watched_body` 缺失 | 加入殖民/异国凝视、阶层、沉默和权力差 | 国际项目分析必须写"谁在看他" | 不把身体展示当唯一表演论据 |
| 答案像导演课不服务演员 | execution_slot 缺失 | 每段建议落到眼神、手、步速、口音、停顿、距离 | Step 3 固定输出身体方案 | 用户能直接排练一段动作 |

## Repair Playbook

1. 先判断问题类型：角色诊断、类型切换、权力人物、喜剧、事实核查、剧组生产条件。
2. 回读 `SKILL.md` 的字段中心映射，选择对应 `field_id`。
3. 若涉及作品、奖项、近况，先读 `references/research/00-source-index.md` 并联网核对最新事实。
4. 输出修复时先写生活来源，再写类型重心，最后写演员动作。
5. 稳定规则进入 `SKILL.md`；运行经验进入本 `CONTEXT.md`；详细调研过程留在 `references/research/`。

## Reusable Heuristics

- 梁家辉式表演建议的核心不是"演什么都像"，而是每换一个类型就重建一次身体、口音、权力来源和生活底盘。
- 处理权力角色时，不先写"霸气"。先判断权力来自职位、钱、江湖仪式、信息差、父权、暴力还是关系债。
- 喜剧角色要认真演自己的目标；笑点来自世界错位，不来自演员主动卖丑。
- 服装不是造型描述。警服、龙袍、西装、家居服都要改变手的位置、站姿、步速和说话方式。
- 对活跃演员 skill，近况要用绝对日期，尤其是提名与颁奖日期，避免把未来结果写成事实。

## Source Notes

- 机构来源优先：香港电影资料馆、香港电影金像奖官方名单、金马奖资料、Asian Film Awards Academy。
- 中文访谈优先使用权威媒体或原始视频字幕；知乎、微信公众号、百度百科不进入证据层。
- 影评和媒体报道只用于外部评价，不用于伪造本人观点。

## Promotion Candidates

- 演员组共享模板可抽象"类型重心 / 权力来源 / 生活底盘 / 身体执行 / 工种边界"五字段。
- 若后续多个演员视角都处理"奖项与近况易过时"，可提升为演员组统一 source_check gate。
