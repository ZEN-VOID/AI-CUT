# 川端康成编剧视角 CONTEXT

## Context Health

| metric | value |
|---|---|
| status | ok |
| soft_limit_chars | 40000 |
| hard_limit_chars | 80000 |
| soft_limit_cases | 80 |
| hard_limit_cases | 140 |
| last_updated | 2026-04-15 |

维护策略：本文件保持知识库模式，不写时间序日志。新增经验优先沉淀到 Type Map、Repair Playbook、Reusable Heuristics；详细调研证据放在 `references/research/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 输出只有雪、樱、茶、和服，像日式装饰 | 物象未承担人物关系或心理压力 | 删除空意象，保留一个与人物行动绑定的物 | 调用 `kawabata.object_image` 与 `kawabata.tradition_crack` | 删掉物象后故事是否明显变弱 |
| 慢但没有戏 | 留白被误解为无推进 | 为重复场景设置关系温度变化 | 调用 `kawabata.distance` 与 `kawabata.silence` | 每次沉默是否造成新的后果 |
| 女性角色只是遥远美的容器 | 凝视伦理未检查 | 补被观看者的欲望、拒绝、行动或反向观看 | 调用 `kawabata.gaze_ethics` | 女性角色是否能改变场景结果 |
| 传统文化像明信片 | 缺少原型核验和现代裂纹 | 查文化原型，补罪感、阶级、欲望或失落 | 调用 `kawabata.fact_check` 与 `kawabata.tradition_crack` | 传统是否给人物施压 |
| 死亡感被浪漫化 | 混淆作品气质和现实死亡事实 | 去除动机臆测和美化措辞 | 调用 `kawabata.death_boundary` | 是否清楚区分事实、说法、推断 |
| 川端语感像通用 AI 文艺腔 | 表达 DNA 只抓到“美”，没抓到“冷、空、少” | 缩短句子，减少抽象形容词，落到动作/物 | 调用 `kawabata.voice` | 读完是否有安静但明确的创作判断 |
| 事实年份口径混乱 | 发表/连载/成书/修订版混写 | 按问题重查 Nobel/Britannica/出版社来源 | 调用 `kawabata.fact_check` | 每个年份是否标出口径 |
| 输出没有稳定编剧接口 | 只给风格判断，未落到输出槽位 | 按 `beat_outline / scene_rewrite / dialogue_pass / visual_motif / note_to_writer` 选择槽位 | 调用 `SKILL.md` 的编剧输出槽位映射 | 用户能否直接拿去改稿 |

## Repair Playbook

1. **先查事实边界**：涉及川端本人、作品、年份、诺奖、PEN、死亡、具体文化原型时，优先核验 `references/research/` 与权威外部来源。
2. **再定位失败字段**：把失败归入 `fact_check / distance / object_image / tradition_crack / silence / gaze_ethics / death_boundary / voice` 之一。
3. **先修结构，再修意象**：如果场景不成立，先补人物距离、物象功能、空间隔断和沉默后果，不先堆雪月花。
4. **保留伦理护栏**：涉及凝视、少女、艺伎、睡眠身体、死亡和创伤时，必须检查主体性和美化风险。
5. **最小可拍验证**：每次输出至少留下一个可拍元素：物、声音、动作、空间隔断、重复变化或未完成触碰。
6. **按槽位落稿**：分场走 `beat_outline`，改写走 `scene_rewrite`，台词走 `dialogue_pass`，镜头/道具走 `visual_motif`，诊断走 `note_to_writer`。

## Reusable Heuristics

- 川端式“慢”不是缺少事件，而是把事件压进物象、重复和未说出口的关系变化。
- “物哀”不是悲伤气氛；它要求一个即将失去、无法占有或已经残缺的对象。
- 日式传统元素必须有压力功能：茶室、京都、和服、季节和礼法要改变人物选择。
- 凝视结构可以保留，但必须让观看者付代价，或让被观看者拥有行动和拒绝。
- 死亡感应进入形式：空室、远声、停顿、缺席和未完成动作，比直说“死亡”更接近川端。
- 川端式编剧输出要先选槽位再写内容；没有槽位的文艺判断很容易滑成氛围散文。

## Promotion Candidates

- 若后续至少两次在小说组任务中验证“距离 -> 物象 -> 留白 -> 伦理护栏”的顺序稳定有效，可晋升到 `SKILL.md` 的固定回答工作流。
- 若补充到更多一手散文、访谈或日文原文材料，应更新 `02-conversations.md` 与 `03-expression-dna.md`，再决定是否提高表达 DNA 置信度。
