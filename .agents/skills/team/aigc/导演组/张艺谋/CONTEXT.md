# 张艺谋 · CONTEXT

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
| 输出只像通用导演建议 | `image_motif` 未触发 | 强制补“画面母题 + 人物入口 + 观众记忆点” | 回答工作流保留视觉母题和人物承压 | 答案有可执行视觉系统 |
| 只写大红大绿 | `color_structure` 装饰化 | 给每种颜色分配权力、欲望、证词或命运归属 | 色彩必须承担叙事结构 | 色彩变化能解释人物关系 |
| 群众场面空心 | `mass_ritual` 漏填 | 先定现场观众/转播镜头，再收回一张脸或一个符号 | 群众场面固定做观看路径检查 | 观众能记住人或核心符号 |
| 主流题材变口号 | `small_person_big_era / genre_shell` 漏填 | 增加普通人愿望、类型外壳和具体危险 | 现实议题必须通过人物和类型进入 | 删除口号后故事仍能成立 |
| 传统符号像陈列 | `tradition_translation` 未启动 | 把传统转为镜头规则、声音节奏或空间运动 | 国风/历史方案固定问“怎么动起来” | 符号参与叙事而非只摆设 |
| 技术方案炫技 | `tech_to_memory` 漏填 | 给技术绑定一个情感记忆瞬间 | AI/VFX/LED 必须服务电影初心 | 去掉技术后情绪是否消失 |
| 女性角色景观化 | 人物行动与制度压力不足 | 补欲望、主动选择、代价和反抗/妥协路径 | 女性角色固定检查“她想要什么” | 她不是只被观看 |
| 事实错误或伪引用 | `source_check` 缺失 | 回到 `references/research/` 或联网核对 | 作品、奖项、票房、新片、政策题材强制来源核查 | 无来源时改写为“推断/待核对” |
| 调研摘要脚本识别来源为 0 | research 文件只回指 source-index，缺少直接 URL | 在每份 `references/research/0X-*.md` 末尾补直接 URL | 保留 `source-index.md` 作集中索引，同时让每份 research 自带可机读 URL | `merge_research.py` 能统计到来源数 |
| 女娲质量脚本误判 | section 标题与脚本锚点不一致 | 保留 `## 表达DNA`、`## 诚实边界` 等锚点，并用显式“内在张力表”承载多组张力 | 新建人物 skill 时优先满足模板关键锚点 | `quality_check.py` 通过 |

## Repair Playbook

1. 先判断失败类型：泛化、色彩装饰化、群众空心、主题口号化、传统陈列化、技术炫技、女性景观化，或事实错误。
2. 回读 `SKILL.md` 字段中心映射，定位对应 `field_id`。
3. 回读 `references/research/0X-*.md`，补来源证据或降低不确定说法。
4. 修正输出时先补“画面母题”和“人物入口”，再补色彩、群众调度、类型外壳和传播。
5. 如果输出过度宏大，优先删掉不改变人物愿望、不改变观众记忆点的阵列或符号。
6. 若修复属于稳定规则，更新 `SKILL.md`；若属于运行经验，更新本 `CONTEXT.md`；不要把过程流水写入这里。

## Reusable Heuristics

- 张艺谋式导演建议必须同时有“画面母题”和“人物承压”。只有色彩没有人物，会变成美术稿；只有主题没有画面，会变成报告。
- 处理色彩时，永远问“这是谁的颜色”。颜色要归属于权力、欲望、记忆、证词、阶层或命运。
- 群众场面先设计观看路径：现场、转播、手机切片分别记住什么。人数不是答案，记忆点才是答案。
- 现实议题要用类型外壳进入大众市场：悬疑、喜剧、谍战、战争、法庭或家庭戏。直接讲道理最容易失败。
- 传统符号必须运动起来。水墨要变成天气和人性灰度，灯笼要变成制度，雪花要变成共同体符号。
- 技术越新，越要回到电影初心：观众最后是否记住一个情感瞬间，而不是只记住技术规格。
- 张艺谋式“宏大”不是只加规模，而是把规模收束到一个符号、一张脸、一个动作。
- 女娲 research 文件可以集中维护 `source-index.md`，但每份 `0X-*.md` 仍要直接出现 URL，避免 `merge_research.py` 把来源数误判为 0。
- 维护人物导演 skill 时，`SKILL.md` 必须显式保留 `Context Loading Contract` 和“必须同时加载同目录 `CONTEXT.md`”规则；缺失会阻塞 `skill_context_audit.py --strict`。

## Source Notes

- 高权重机构来源：Britannica、Senses of Cinema、BU Today、CGTN、China Daily/Xinhua、CCTV、People's Daily、China.org.cn、AP。
- 早期方法论证据优先来自作品结构和学术影评；晚近动态必须用新闻和官方物料交叉核对。
- 票房、上映日期、项目状态变化快，回答时应二次检索。
- 百科、论坛、粉丝整理、二手搬运默认低权重；除非用于发现线索，否则不进入高权重证据。

## Promotion Candidates

- 若导演组继续沉淀多位中国导演视角，可把“画面母题/人物承压/视觉结构/群众调度/类型外壳/传播风险”抽象为导演组共享诊断模板。
- 若 AIGC 影像链路反复出现“漂亮画面不服务人物”的问题，应提升为导演组主合同或分镜生成技能的硬门槛。
- 若文旅/开幕式类任务增多，应把“现场观众/转播镜头/手机切片/场地伦理”提升为大型演出子模板。
