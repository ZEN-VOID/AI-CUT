# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/shot-by-shot` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- recommended_action: keep-reference-analysis-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 拉片变成剧情摘要 | 证据建模层 | 回到镜头边界、时间码、画面事件和镜头功能 | 在主流程固定 `shot boundary map` 先于主题归纳 | 表格中每条分析都能回指具体镜头 |
| 输出像影评，没有下游可消费字段 | 阶段桥接层 | 把观察拆成 `0-初始化 visual style bridge`、`2-编导 bridge`、`3-摄影 bridge` 与 `5-设计 bridge` | 模板固定四份项目 `CONTEXT/` 解析字段 | 下游可直接作为上下文喂给 owning stage |
| 临摹变成照搬 | 权利边界层 | 把具体表达移入 `forbidden-copy ledger`，只保留 craft principle | review gate 固定“原则可学、表达不可复制” | 阶段解析不含参考片具体台词、构图复制、风格复制、设计复制或镜头顺序复制 |
| `画面风格解析.md` 写成 north star 直接覆盖稿 | north-star 边界层 | 改成 side context：字段对齐、补强短语、可回刷建议和 Do Not Import | `adaptation-output-contract.md` 固定 0-初始化 bridge 禁止直接改写 canonical north star | 输出只服务 `全局风格 / 细分风格.画面风格 / 类型元素`，不包含完整 north star |
| 给 `编导解析.md` 写了摄影方案 | 阶段边界层 | 删除机位、景别、运镜、分镜编号，改成表演任务、场面调度和可拍承托 | `adaptation-output-contract.md` 固定 0/2/3/5 字段边界 | `编导解析.md` 不出现 `分镜N`、景别、焦段、机位 |
| 给 `3-摄影` 的包只有参数堆叠 | 摄影消费层 | 转成 `visual_unit -> beat_map -> camera_grammar_plan -> functional_projection_payload` | 模板固定 shot design seed，而不是参数清单 | 可改写为自然中文 `分镜明细：` |
| 视频证据不足却给强结论 | 证据可信度层 | 降级为观察假设，标注需补证时间码/截图 | 类型表固定 evidence_grade | 报告区分 confirmed / inferred / insufficient |
| 输出仍沿用旧文件名 | 输出合同漂移层 | 改为 `全局风格解析.md`、`编剧风格解析.md`、`摄影风格解析.md`、`设计风格解析.md`、`分镜脚本.md` | 旧 `画面风格解析.md`、`编导解析.md`、`摄影解析.md`、`设计解析.md` 只作为 legacy mirror | 主报告阶段对接列出 canonical 新文件 |
| 分镜脚本字段与示例 Numbers 不一致 | 表格投影层 | 按 `input/苍穹裂缝·战神降维.numbers` 恢复 19 列和固定顺序 | `storyboard-script-contract.md` 与 validator 同步检查表头 | `分镜脚本.md` 表头完整包含 `镜号` 到 `视频运动提示词` |

## Repair Playbook

1. 先锁定参考素材证据：文件、截图、时间码或用户描述的来源。
2. 再切镜头边界；若无法准确切镜，先用观察段落临时编号，并标注 `evidence_grade: inferred`。
3. 每镜至少回答：观众看见什么、镜头怎样进入、注意力如何转移、镜头为何结束。
4. 将观察拆成导演/表演/摄影/剪辑/声音/美术/AIGC 可行性，不把所有判断塞进“氛围”。
5. 输出临摹建议前，先写禁止照搬项；不能明确禁止项时，临摹建议通常过于贴近原片。
6. 对 `0-初始化` 只给 north star 风格块的补强语法；对 `2-编导` 只给戏剧、表演、调度和可拍承托；对 `3-摄影` 再给景别、运镜、构图、光色和下游 payload；对 `5-设计` 只给角色/场景/道具可迁移视觉原则和画面合同边界。
7. 输出 `分镜脚本.md` 时先固定 Numbers 示例 19 列，再填镜头内容；不要为了适配项目四段式分镜 ID 改列名。
8. 结尾必须说明“怎么套用到当前 AIGC 项目”，否则拉片只是研究报告，不是生产参照包。

## Reusable Heuristics

- 好的拉片不是复述“这一镜很好”，而是说清它用什么可观察手段完成了什么观看任务。
- 临摹的单位应是 craft principle，不是 frame、pose、dialogue 或 shot order。
- `0-初始化` 需要的是“全片共同画面基调如何稳定继承”；`2-编导` 需要的是“角色在空间中如何被迫行动”；`3-摄影` 需要的是“摄影机如何把行动变成观看路径”；`5-设计` 需要的是“资产如何承载身份、空间和物证压力”。
- 新输出命名里，`全局风格解析.md` 承接 global-style 字段逻辑，`编剧风格解析.md` 承接戏剧/表演/调度，`摄影风格解析.md` 承接镜头语法，`设计风格解析.md` 承接角色/场景/道具资产，`分镜脚本.md` 承接 Numbers 表格。
- 如果一个参考镜头只能通过复制构图才能成立，它不适合作为项目临摹原则。
- AIGC 可执行性要提前判断：复杂长镜头、群像大调度和连续物理特效可以学习节奏与焦点转移，但落地时常需要拆成更清晰的可生成镜头。
