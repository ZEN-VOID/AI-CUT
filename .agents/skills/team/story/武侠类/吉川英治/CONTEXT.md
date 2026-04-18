# 吉川英治小说视角 CONTEXT

## Context Health

| metric | value |
| --- | --- |
| status | ok |
| soft_limit_chars | 40000 |
| hard_limit_chars | 80000 |
| soft_limit_cases | 80 |
| hard_limit_cases | 140 |
| last_updated | 2026-04-18 |

维护策略：本文件保持知识库模式，不写时间序日志。新增经验优先沉淀到 Type Map、Repair Playbook、Reusable Heuristics；详细调研证据放在 `references/research/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 主角像开挂模板，没有成长弧 | `quest-growth` 模型未启用 | 回到“败 - 学 - 转 - 定”的四段成长线 | 先输出 `hero_arc` 再写场面 | 主角至少有一次失败和一次转心 |
| 历史材料很多，但小说读不动 | `public-epic` 缺失 | 把史料压回人物目标、阻碍和章回钩子 | 每章先定读者入口，再加史料 | 普通读者能说出这一回谁要做什么 |
| 打斗热闹却没精神 | `sword-to-discipline` 缺失 | 重写胜负代价，让决斗改变人物 | 每场武戏都绑定人格变化 | 删掉打斗后人物弧是否受损 |
| 只写英雄，不写时代和百姓 | `tide-and-crowd` 缺失 | 补一个时代代价承受者和一个主角镜像 | 默认输出 `ensemble_map` | 群像里至少有一名普通人承担时代成本 |
| 把史实空白写成确定事实 | `history-gap` 边界失守 | 标出史实、演义、推断三层 | 事实问题先核 `references/research/` | 回答里能区分已证与推断 |
| 语言只剩古风腔和大词 | 表达 DNA 误读 | 减少空洞大词，改为路径、地点、动作、人情 | 先写场面骨架，再加气口 | 删去“江湖/乱世/苍生”等词后文本是否仍成立 |
| 长篇章节没有回合感 | `serial-engine` 未开启 | 改成章回节点，补“下一程”钩子 | 先用 `chapter_outline` 起盘 | 每回结尾都留下一件未完成之事 |
| 把吉川写成纯爽文作者 | 外部定位误读 | 补“国民文学 + 人格修行 + 史料边界”三件套 | 先看 `01-writings.md` 与 `04-external-views.md` | 输出既可读也保有人物与历史重量 |

## Repair Playbook

1. 先判断问题属于 `事实边界`、`主角成长`、`群像组织`、`场面失效`、`章节节奏` 还是 `语言气口`。
2. 事实问题先回看 `references/research/01-06.md`；不够再联网补核。
3. 创作问题先定输出槽位：成长看 `hero_arc`，长篇看 `chapter_outline`，单场看 `scene_engine`，群像看 `ensemble_map`。
4. 若是武侠/历史题材，先写地理与时代压力，再写招式与酷感。
5. 若文本失去大众可读性，删概念解释，改成人物目标、阻碍和回合推进。
6. 若文本只剩爽感，补一处失败、一位镜像人物和一个人情场面。

## Reusable Heuristics

- 吉川式英雄必须从未完成处起步，不能一上来像成神后的海报。
- 历史小说最好写法不是“我查到了很多”，而是“我只把最能改变人物命运的史实留在台上”。
- 武戏的真正价值不在招式酷，而在人物通过胜负学会了什么。
- 国民文学不是讨好所有人，而是让普通读者也能进入高密度历史叙事。
- 长篇回合的基本单元可以记成：上路、遇人、受阻、决断、留钩。
- 吉川式群像不是抢戏，而是让主角在他人映照下慢慢长出轮廓。

## Promotion Candidates

- 若后续至少两次验证“败 - 学 - 转 - 定”四段主角线对武侠长篇稳定有效，可晋升到 `SKILL.md` 的默认起盘合同。
- 若后续继续补到更多吉川随笔、演讲或相关书信，可增强表达 DNA 的口语层证据。
