# 渡边淳一编剧视角 CONTEXT

## Context Health

| metric | value |
|---|---|
| status | ok |
| soft_limit_chars | 40000 |
| hard_limit_chars | 80000 |
| soft_limit_cases | 80 |
| hard_limit_cases | 140 |
| last_updated | 2026-04-16 |

维护策略：本文件保持知识库模式，不写时间序日志。新增经验优先沉淀到 Type Map、Repair Playbook、Reusable Heuristics；详细调研证据放在 `references/research/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 情欲戏只有刺激，没有人物推进 | 身体描写未绑定羞耻、代价和后效 | 补身体事实、关系后果和下一场余震 | 调用 `watanabe.body_truth` + `watanabe.desire_cost` | 删除亲密描写后关系是否仍无变化 |
| 婚外恋被写成简单道德审判 | 禁忌成本没有具体化 | 列家庭、职业、名誉、健康、时间账单 | 调用 `watanabe.social_ethics` | 是否能看见每个相关人的代价 |
| 医生角色像术语机器 | 医学视线只剩专业词汇 | 补观察动作、职业职责、制度边界和失败记忆 | 调用 `watanabe.medical_fact` + `watanabe.clinical_gaze` | 医生的选择是否受职业伦理限制 |
| 中老年爱情像年轻人换皮 | 熟年时间与身体压力缺失 | 补孩子、配偶、病历、职位、衰老和可支配时间 | 调用 `watanabe.mature_love` | 角色年龄一换是否戏仍成立，若成立则失败 |
| 钝感力被当成逃避责任 | 迟钝未区分生存策略与麻木伤害 | 标注谁受益、谁受伤、谁被忽略 | 调用 `watanabe.donkanryoku` | 钝感是否听不见他人痛苦 |
| 殉情/死亡结尾被浪漫化 | 死亡被用作结构偷懒 | 改成事实后果、生者余震或非死亡承担方式 | 调用 `watanabe.death_boundary` | 结尾是否承认家庭和社会后果 |
| 女性角色成为男性欲望容器 | 男性医学/情欲视线未加护栏 | 补女性主体、选择、拒绝、欲望和后续行动 | 调用 `watanabe.social_ethics` | 女性是否能改变关系结果 |
| 渡边语感像通用 AI | 只抓到“婚外恋”，没抓到医学观察和社会账单 | 改为临床判断、身体事实、禁忌成本、成熟冷静语气 | 调用 `watanabe.voice` | 开头是否像诊断而非鸡汤 |
| 质量检查脚本误报章节缺失 | Markdown section 正则在 DOTALL 下用 `.*` 跨行吞段 | 将标题行匹配限定为 `[^\n]*` | 脚本中所有标题行匹配禁止跨行贪婪；新增脚本后必须实际跑一次 | `quality_check.py` 对本 skill 输出 9/9 PASS |

## Repair Playbook

1. **先核验事实边界**：涉及作品、年份、奖项、医学事件、疾病、手术、死亡、文学奖动态时，先查 `references/research/` 与权威外部来源。
2. **再定位失败字段**：把失败归入 `medical_fact / clinical_gaze / body_truth / desire_cost / social_ethics / mature_love / donkanryoku / death_boundary / voice` 之一。
3. **先写账单，再写欲望**：禁忌关系必须先有可见代价，情欲场景才不会空心化。
4. **医学只做真实锚点**：医学事实用于约束角色和伦理，不用于制造猎奇、权威感或万能解释。
5. **熟年人物必须带时间压力**：职业末期、孩子、配偶、病痛、药物、衰老、孤独至少选两项进入场景。
6. **死亡结尾必须二次审查**：任何殉情、自毁、病死、衰老美学都先走 `risk_note`，再决定是否保留。
7. **按槽位落稿**：关系诊断走 `relationship_diagnosis`，分场走 `beat_outline`，改写走 `scene_rewrite`，医疗题材走 `medical_scene_note`，台词走 `dialogue_pass`，风险走 `risk_note`。
8. **脚本先跑后交付**：新增 skill-local 验证脚本时，必须用当前 skill 真实文件跑一次；若正则解析 markdown section，标题行匹配只能使用 `[^\n]*` 这类单行约束，避免 DOTALL 跨段误报。

## Reusable Heuristics

- 渡边式情欲不是“更露骨”，而是把身体、羞耻、社会身份和后效放在同一场戏里。
- 婚外恋题材不要先判善恶，先列账单；账单越具体，人物越难逃。
- 医生角色的真实感来自观察习惯和责任边界，不来自术语密度。
- 熟年爱情的核心不是重返青春，而是时间变少后，欲望突然变得昂贵。
- 钝感力只在抵抗无效羞辱时有效；面对亲密伤害、医疗权力和伦理责任时，钝感常是危险麻醉。
- 《失乐园》式结尾不能当模板套用；如果死亡不能带来更真实的余震，就不要用死亡完成结构。
- 验证脚本本身也是源层合同的一部分；脚本误报时先修脚本和 CONTEXT，再把验证结果用于交付判断。

## Promotion Candidates

- 若后续至少两次验证“身体事实 -> 禁忌账单 -> 熟年时间 -> 伦理余震”的顺序稳定有效，可晋升到 `SKILL.md` 的固定回答工作流。
- 若补充到日文原作摘录、正式访谈或中文译者访谈，应更新 `02-conversations.md` 与 `03-expression-dna.md`，再提升表达 DNA 置信度。
