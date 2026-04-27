# Context: 九刀流漫画提示词

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 16097
current_lines: 178
current_cases: 21
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T07:20:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件沉淀“分组漫剧剧本 `第N组.md` / 兼容 raw source -> 九页漫画生成提示词 JSON”的经验。默认知识库模式，不记录流水账。

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-NB-01` | 下游生成九宫格拼图 | 顶层生成合同 | 在 `hard_constraints` 与 master prompt 写明 9 separate images/pages, not collage | schema 和脚本检查禁拼图约束 | 3 号技能 dry-run prompt 含 hard constraints |
| `TM-NB-02` | 九张图像同一画面的变体 | 故事切页层 | 重做 `story_beat_map[9]`，每页必须有不同动作目标和情绪转折 | 每页 `page_role / narrative_function` 必填 | 9 页标题连读能形成剧情链 |
| `TM-NB-03` | 角色在各页漂移 | 连续性层 | 补 `character_locks`，把脸型、服装、道具、色彩写成复用短语 | 每页 prompt 必须引用角色锁 | 主角描述不靠临场自由发挥 |
| `TM-NB-13` | 已经写了 `character_locks`，但主角脸/毛色/服装仍跨页漂移 | 主角锚定真源缺失层 | 新增唯一 `main_character_lock`，用 `Character locked across all panels: [name], ...` 高密度锚定句锁主角，再把该句逐页注入 `positive_prompt` | `SKILL.md`、reference、template、schema、validator 同步要求 `main_character_lock` 为必填，并校验每页 prompt 含主角锚定语句 | 页面 prompt 中既能看到主角姓名，也能看到稳定脸/服装/轮廓语义 |
| `TM-NB-14` | 多角色同页时，主角稳定但配角脸/服装/身高关系漂移 | 群像协同真源缺失层 | 把 recurring characters 升级为具名 `character_locks`，并在每页显式写 `active_character_ids`；多人页 prompt 必须点名出场角色并要求 `visually consistent and clearly distinguishable` | schema、template、validator、master prompt 同步要求多人页声明 active ids 且 prompt 提到这些角色 | 多人页 prompt 能读到所有出场 recurring character 的名字或稳定身份 |
| `TM-NB-15` | 同一地点跨页建筑/地标/光线漂移，像换了场景 | 场景锚定真源缺失层 | 新增 `scene_continuity_bible.scene_locks[]`，每页通过 `scene_id` 绑定场景锁，并把场景锚定句写进 page prompt | `SKILL.md`、reference、template、schema、validator、3 号编译器同步要求场景锁与 page scene_id | page prompt 中能读到场景名和稳定建筑/地标/光线语义 |
| `TM-NB-16` | 最终漫画页没有页码，或页码不是右下角纯数字 | 页码覆盖层缺失 | 在顶层 hard constraints 和每页 `page_number_overlay` 中同时声明 `bottom-right` + `digits only` + 当前页数字 | 2 号 schema/template/validator 与 3 号编译器同时固化页码合同 | dry-run master prompt 与页级 prompt 都明确写出右下角数字页码 |
| `TM-NB-12` | 角色锁存在但生成时仍出现人物或场景漂移 | 页级提示词显式约束层 | 在每页 `positive_prompt` 的版式之后固定写入 `keep character and scene consistency across all pages` 或等价语义 | `SKILL.md`、reference、模板和 validator 同步要求 hard constraints 与每页 prompt 都包含角色/场景一致性语义 | validator 对缺少一致性语义的 hard constraints 或 page prompt 报错 |
| `TM-NB-04` | 页面像电影分镜，不像漫画页 | 漫画语法层 | 增加 panel borders、gutter、caption、SFX、speed lines、inset panel 等漫画技法 | 版式库在 reference 中固定 | 每页至少一个漫画技法标签 |
| `TM-NB-05` | 文本气泡不可读或挤压画面 | 文字系统层 | 对白压短，旁白进 caption，独白与对白分离 | `comic_text_system` 固定四类文本槽 | 每个 text slot 类型明确 |
| `TM-NB-06` | JSON 能读但不能被 3 号技能执行 | 结构合同层 | 按 schema 补齐 `generation_contract/pages/global_negative_prompt` | 验证脚本作为交接门 | validator 零错误 |
| `TM-NB-07` | 流程通畅但画面漫画感不够犀利 | 全局风格层 | 在 `style_bible` 加 `manga_style_keywords / layout_directive`，用 ink、screentone、black gutters、oversized SFX 等词先锁漫画页语法 | reference 固化全局漫画风格锐化词库，validator 检查 style_bible 不只写泛影视词 | master prompt 前半段出现明确漫画页风格词 |
| `TM-NB-08` | 9 页都从上到下平整排列 | 版式多样性层 | 重排 `layout_id / panel_ratios`，加入 splash、inset、diagonal、split、border-breaking、zigzag 等经典布局 | validator 检查至少 5 个 layout_id 且动态版式不少于 3 类 | 9 页缩略图能看出节奏变化 |
| `TM-NB-09` | 单页有漫画词但冲击力弱 | 画面力度层 | 每页补 1 个主视觉冲击词组：extreme perspective、impact burst、heavy ink shadow、focus lines、border-breaking pose 等 | `style_bible` 分成线条、明暗、运动、文字、印刷质感五类，而不是只给一串泛词 | 高冲击页的 prompt 首段能读出“视觉冲击机制” |
| `TM-NB-10` | 版式名存在但 panel 关系不清 | 版式执行层 | 在 `layout.panel_ratios` 和 `positive_prompt` 写清 dominant panel、inset、gutter、reading path、final reveal 的相对位置 | 版式提示词必须同时包含“格数/比例/阅读动线/冲击点”四项 | 不看剧情也能画出页面骨架 |
| `TM-NB-11` | 气泡/SFX 破坏画面或阅读顺序 | lettering 层 | 把 speech bubble 贴近说话角色，SFX 绑定动作源，避免贴边漂浮和压住关键表情 | 文本槽提示词写入 near speaker / inside panel / no tangent / readable Chinese | 页面缩略图中视线不需要左右大幅摆动 |
| `TM-NB-17` | `comic_text_system` 存在，但 JSON 仍退化成只有旁白或缺少独白/SFX | 结构合同层 | 把四类文字系统从裸 object 升级为显式对象合同，并要求九页整体至少覆盖 `dialogue / narration / inner_monologue / sfx` 各一次 | schema + validator 同步要求四类系统齐备、页面整体覆盖四类槽位 | validator 对“只有 narration”的 JSON 报错 |
| `TM-NB-18` | 槽位类型正确，但对白/独白/旁白在画面中的位置和归属混乱 | 结构语义层 | 为 `text_slots` 补 `speaker_id / placement / bubble_style / inside_panel`；对白与独白必须绑定当前页角色 | schema 与 validator 同步检查 `speaker_id` 回指 `active_character_ids`，并校验 bubble/placement 语义 | validator 对无说话者或错误 placement 的槽位报错 |
| `TM-NB-19` | 文档写了长度上限和可读性，但超长对白与不可读中文仍通过 | 校验门禁层 | 把长度上限和 `clear legible Chinese text` 约束同时落到 schema、validator 和 page prompt 注入模板 | validator 按类型检查 `max_chars` 和 prompt 文本可读性语义 | 超长对白、缺文字可读性提示的 page prompt 无法通过 |
| `TM-NB-20` | 在 Coze/扣子这类 Agent 平台上，9 页成品的漫画风格断层漂移：有页像黑白港漫，有页像儿童彩图，有页像影视概念图 | 全局风格锁缺失层 | 在 `style_bible` 和每页 `positive_prompt` 前段同时注入同一条 `global style anchor`，锁死渲染媒介、线条体系、明暗方法、上色策略、lettering 质感与角色年龄比例，并显式写 `forbidden style shifts` | 在 `SKILL.md`、reference 与导出的 Agent system prompt 同步提升“全局风格锁”优先级；把页间风格稳定看作高于单页炫技 | 页 1-9 允许构图变化，但不再出现儿童绘本 / Q 版 / 写实概念图的断层混切 |
| `TM-NB-21` | 把整段上游剧本直接压成一个 9 页包后，节奏忽快忽慢：有时 9 页塞太多事件，有时又被拉得过空 | 分组真源缺失层 | 优先要求 1 号阶段产出 `第N组.md`，并按约 1000 字规则逐组跑九刀 | `SKILL.md`、reference、template、父子技能 handoff 同步提升 `第N组.md` 为 canonical 上游规则 | 每个 group 的 9 页都能成立完整小节奏，且项目不再只有一个过载或过空 JSON |
| `TM-NB-22` | 分组后单组节奏合理，但组与组之间人物、风格、场景像换了作品 | 组间 continuity 合同缺失层 | 在每个组级 JSON 中显式加入 `page_group / continuity_context`，并要求继承同一套 `main_character_lock / style_bible / character_locks / scene_continuity_bible` | schema/template/validator 与下游技能同步识别组级 metadata，防止多组输出退化成多个独立短篇 | page-group-01 与 page-group-02 的视觉 DNA、角色锚点和场景锚点可连续对读 |
| `TM-NB-23` | 4 号剧集海报阶段能读到页级 prompt，但抽不出稳定的剧情高光候选，结果像通用角色海报 | 海报交接层 | 在 `pages[].panels[]` 中补齐 `shot / action / comic_techniques / text_slots`，并让 `positive_prompt` 先写版式、再写 panel 级动作 | 4 号技能默认按 `one page / key panel -> one highlight candidate` 提炼海报候选；2 号模板与人工验收同步把 panel 结构当作海报高光输入 | 4 号 dry-run 能从 JSON 中抽出 3-5 个剧情高光候选，而不是只剩一个大句子 |
| `TM-NB-24` | 上游已经锁了类型包，但组级 JSON 没透传，结果 3/4/5 段又回到默认题材语法 | type-pack handoff 层 | 把 `type_stack_ref / type_pack_context` 设为组级 JSON 的强制字段，并按 `stage_projection.nine_blade_prompting` 写入布局/对白/风格偏置 | schema、template、validator 和 child handoff 同步要求 pack 字段存在 | 任一 group JSON 都能回指 active packs 和九刀阶段投影 |

## Repair Playbook

1. 先看失败是 `9 图合同`、`故事切页`、`角色锁`、`漫画语法`、`文字系统` 还是 `JSON 结构`。
2. 若下游像九宫格，优先修顶层 hard constraints，而不是改单页文案。
3. 若下游像九个变体，优先重切 `story_beat_map`。
4. 若单页漫画感弱，优先补 panel 结构、gutter、caption、SFX、速度线、跨格构图。
5. 若文字失败，减少文字数量；不要指望模型稳定生成长段中文。
6. 若用户反馈“漫画感不够”但流程本身通畅，优先修全局风格词与版式多样性，而不是重切故事。
7. 若用户要求“更有冲击力”，先判定冲击点类型：构图冲击、动作冲击、明暗冲击、情绪冲击、文字/SFX 冲击；每页只主打一到两类，避免词堆叠互相稀释。
8. 若用户要求“布局更像漫画”，不要只新增 layout 名称；必须补 `panel_ratios`、dominant panel 位置、inset 位置、gutter 颜色/宽度、阅读路径和页末停顿点。
9. 若用户反馈“风格不稳定”，先不要急着加更多风格词；先检查是否缺少“同一套视觉 DNA 必须逐页重复”的硬门禁。单靠顶层 `style_bible`，很多 Agent 平台会把 9 页当 9 次独立创作。
10. 若用户反馈“这一组突然不像前一组那个题材了”，先检查 `type_pack_context` 是否丢失，而不是先重写 page prompt。

## Reusable Heuristics

- 当前默认生图执行层为 `.agents/skills/cli/imagegen`；提示词 JSON 的职责是让 9 个单页 job “各有剧情功能”，不是把九页压成九宫格。
- 本技能升级到 Skill 2.0 后，入口 `SKILL.md` 只保留输入、路由、动态引用、Output Contract 与 Root-Cause 链路；来源前奏和九刀节点看 `steps/`，类型分支看 `types/`，审计门禁看 `review/`，风格/版式/提示词经验看 `knowledge-base/`。后续新增规则先判断 owner，不要把长细则重新堆回 `SKILL.md`。
- 漫画题材知识包已经从父级 `comic/type-packs/漫画/` 迁入本技能 `types/漫画/`；后续题材新增、题材细化、`meta.yaml` 控制面维护都应落在本技能 `types/漫画/<题材>/`，父级 `comic/type-packs/runtime.yaml` 只保留跨阶段默认栈配置。
- 若 `projects/comic/<项目名>/` 下只有 `metadata.json` 没有目标章节正文，不要先跑整书下载；优先读取 `metadata.data.lists[*].item_id`，用单章级正文抓取补齐当前集源文本，再进入九刀前奏。
- 当 `1-漫画剧本改编/第N组.md` 已存在时，优先把它视为唯一文本真源；不要回退到整篇 Markdown 主稿重新猜 `ordered_story_units[]`。
- 当用户要求同项目的第 2 集/第 3 集“保持角色和风格一致”时，优先把上一集的 `page-group-*.json` 或 `第N集-page-group-*.json` 视为 continuity truth：继承 `main_character_lock`、`style_bible`、既有 `character_locks`，只对新增人物和新增场景做增量扩展。
- 当一个项目篇幅明显超过单组承载能力时，最稳的做法不是压缩剧情，而是先产出 `第N组.md`：以约 1000 字原文为目标切组，优先 obey scene / impact beat / hook 的自然边界。
- `page-group` 是节奏单元，不是风格单元。允许每组的剧情功能不同，但 `main_character_lock`、`style_bible`、`scene_continuity_bible` 和 recurring `character_locks` 必须跨组继承。
- 如果下游不仅要生图，还要做图生视频，那么 2 号技能的页级产物必须同时满足“可生成漫画页”和“可还原为多分镜动画 storyboard”两套要求；最稳做法是保留清晰的 `panels[]` 粒度，而不是把所有动作压扁成一条大 prompt。
- 每页内部可以是三格、二格、四格或 splash + inset；九页之间不要都用同一版式。
- 页级 prompt 最稳的结构是：页面版式 -> 角色锁 -> panels -> 文本槽 -> overall -> negative。
- 对连续 9 页漫画，`character_locks` 只能描述角色表，不能替代主角锚。最稳结构是：页面版式 -> `main_character_lock.anchor_prompt` -> 角色/场景一致性语义 -> panels -> 文本槽 -> overall -> negative。
- 多人页要稳定，不能只靠 `character_locks` 存在于 JSON 顶层。必须把当页 `active_character_ids` 对应的角色名或身份锚点直接打进 `positive_prompt`，否则模型会把配角当成可自由漂移的背景路人。
- 对连续多页漫画，`character_locks/location_locks` 是结构锁，但模型生成时仍需要在每页 `positive_prompt` 显式看到角色与场景一致性短语；该短语应放在版式说明之后、具体动作之前，避免被单页动作描述稀释。
- 当用户已经给出高密度人物锁定句时，不要把它拆散到多个字段后期待模型自己拼回去；应保留为 `main_character_lock.anchor_prompt`，逐页原样或近原样注入。
- 场景连续性最稳的方式不是抽象写 `same location`，而是给出具名场景锁：场景名 + 建筑/地标 + 光线/时段 + 空间朝向，再由每页 `scene_id` 显式回指。
- 页码要进最终图，必须让它既存在于结构字段，也存在于页级 prompt 和 master prompt；只在 JSON 里存一个 `page_number` 数字并不会自动出现在图上。
- 多集漫画项目若继续沿用根级 `nine_blade_comic_prompts.json`，会覆盖上一集；在没有更强 episode 子目录合同前，默认应改用 `第N集-page-group-XX-...` 前缀文件名，并让中间真源与摘要同前缀联动。
- 当阶段目录里已经存在单集旧产物而用户继续点名“第2集 / 第3集”时，最稳做法不是直接覆盖旧文件，而是先把旧产物迁成 `第1集-page-group-XX-...` 或对应集号前缀，再把当前集写成新的 `第N集-page-group-XX-...`；否则下游会出现“上一集真源消失、当前集冒充唯一 canonical”的假单集状态。
- 中文气泡要短，旁白比对白更适合承载解释，SFX 只承载动作声音。
- 文字系统如果只存在于顶层说明文而不进入 `text_slots` 结构字段，生成时就会退化为“模型自由发挥的气泡”。要把 `speaker_id / placement / bubble_style / inside_panel` 当成执行合同，而不是备注。
- 9 页漫画足够覆盖对白、旁白、独白、SFX 四类文字形态；若最终 JSON 缺其中一类，通常不是“题材不需要”，而是文字系统在切页或模板阶段被压扁了。
- 正向验证：`滴滴滴` 项目完整链路顺畅，说明三段链、阶段落点和 JSON validator 可作为默认执行路径复用；下一层质量杠杆应转向 `style_bible` 的漫画风格锐化词和 `pages[].layout` 的经典漫画版式轮换，并继续保证这些字段足够支撑 4 号剧集海报的高光提炼。
- 对 CLI imagegen 逐页漫画，`cinematic realism` 只能保证画面质感，不能保证漫画语法；必须显式写入 `dynamic manga paneling / screentone shadows / high contrast black gutters / oversized SFX / irregular gutters` 这类词。
- 对 Coze/扣子这类 Agent 平台，只在顶层定义画风通常不够。最稳的做法是：`style_bible` 有全局风格锁，且每页 `positive_prompt` 再重复同一条 `global style anchor + forbidden style shifts`，让模型没有机会把 9 页当成 9 次试风格。
- 当质量优化点已经明确为“漫画感”和“布局感”时，思行网络不能继续维持单线 `Comic Grammar` 节点；应拆成 `STYLE-SHARPEN / LAYOUT-DIVERSIFY / TEXT-SYSTEM` 三支路，并在汇流门阻断缺风格词、缺动态版式或文字槽失控的 JSON。
- 如果最终图像出现“第一页像港漫、第二页像儿童绘本、第三页像影视概念图”，根因通常不是故事切页，而是 `global style anchor` 缺失或没有逐页重复注入。
- 冲击力不是“更多形容词”，而是“明确的视觉机制”：低机位仰拍制造压迫，极近特写制造情绪，斜切 panel 制造速度，黑 gutter 制造悬念，破框 SFX 制造爆发。
- 版式提示词应像给分镜师的页面设计单：先写页面骨架，再写每格功能；如果 prompt 只剩镜头描述，模型容易回到电影分镜而不是漫画页。
- 高冲击页可用 `one dominant splash panel + 2 small reaction insets + oversized SFX crossing the gutter`；解释页可用 `evidence strip + reaction close-up + caption anchor`，不必都做大爆炸。
- 气泡位置是阅读动线的一部分。对白气泡离角色太远，模型即便画出气泡，也会让读者视线在页面两端摇摆；提示词应写 `speech bubble close to the speaking character, inside the panel, not at the far edge`。

## Online Research Synthesis

2026-04-15 联网检索后，将外部资料只抽象为可复用经验，不把网页内容当作本 skill 的第二真源。

参考来源：

- [Lee Sullivan Art - A Guide to Writing & Drawing for Comic Books](https://leesullivanart.co.uk/LEE/guidelines.htm)：强调漫画优先服务 storytelling，画面要包含 drama、dynamics，并通过远景/中景/特写变化建立地点、人物、表情与动作。
- [Making Comics - Page Layouts](https://makingcomics.com/2014/05/07/panel-layout-golden-ratio/)：页面版式会通过 panel 大小、关系和阅读路径影响节奏与重点；适合抽象为 `dominant panel / reading path / final reveal` 类提示词。
- [Clip Studio Tips - Manga Effects Every Artist Should Know](https://tips.clip-studio.com/en-us/articles/10107)：可将 action lines、focus/flash lines、hatching、screentone、sparkle 等漫画效果拆成风格词库。
- [Clip Studio Tips - Webtoon Storyboard Notes](https://tips.clip-studio.com/en-us/articles/9394)：气泡位置和 panel 间距共同决定阅读流，漫画画面应尽量做到去掉文字也能看懂大致动作。
- [Blambot - Comic Book Grammar & Tradition](https://blambot.com/en-gb/pages/comic-book-grammar-tradition)：lettering、caption、balloon、SFX 与 tangents 是漫画页语法的一部分，不应作为后置装饰。

经验转译：

- `style_bible` 里应同时覆盖“线条/明暗/动态/印刷/lettering”五类漫画语法，不能只写题材风格。
- `pages[].layout` 应承担视觉叙事功能：开场建立、危机压迫、动作爆发、静默反应、证据揭示、页末钩子。
- `panels[].comic_techniques` 是冲击力的最小落点。每格应选择 1-3 个技术词，而不是把全局词重复粘贴到所有 panel。

## Impact Style Prompt Bank

这些词库用于 `style_bible.manga_style_keywords`、`pages[].positive_prompt` 或 `panels[].comic_techniques`。原则：每页选 4-8 个，全局选 8-14 个；不要全量堆叠。

| style_family | 可用提示词 | 最适合页面 | 使用注意 |
| --- | --- | --- | --- |
| 线条压迫 | `heavy black ink linework`, `bold contour lines`, `razor-sharp ink strokes`, `scratchy cross-hatching`, `thick silhouette edges` | 反派压迫、恐怖、命运宣告 | 和 `clean glossy anime` 同时出现会互相抵消 |
| 明暗冲击 | `deep chiaroscuro shadows`, `black gutter suspense`, `hard rim light`, `single bright highlight`, `crushed blacks and stark whites` | 揭示、审讯、绝境、恐怖 | 暗部过多时要指定 readable faces |
| 动作爆发 | `speed lines`, `focus lines`, `impact burst`, `motion trails across panels`, `kinetic diagonal composition`, `foreshortened action pose` | 战斗、坠落、追逐、觉醒 | 每页只让一个动作成为主爆点 |
| 画面变形 | `extreme low-angle perspective`, `wide-angle distortion`, `claustrophobic close-up crop`, `tilted Dutch angle panel`, `overlapping foreground silhouette` | 权力压迫、眩晕、失控 | 变形要服务情绪，不要让角色识别物漂移 |
| 印刷质感 | `screentone shadows`, `halftone texture`, `printed comic page grain`, `ben-day dot texture`, `rough paper ink texture` | 所有漫画页全局底色 | 作为统一风格锁，别写成单页主戏 |
| 文字冲击 | `oversized hand-lettered SFX`, `SFX breaking the panel border`, `jagged scream balloon`, `rectangular caption anchor`, `caption embedded in black gutter` | 爆炸、尖叫、钩子、旁白页 | SFX 绑定动作源；caption 绑定叙事压缩 |
| 情绪装饰 | `shoujo sparkle screentone`, `floating reaction inset`, `silent beat panel`, `negative space around the face`, `tiny sweat-drop emphasis` | 恋爱、尴尬、震惊、沉默 | 情绪装饰适合小格，不宜抢主画面 |
| 悬疑证据 | `evidence close-up strip`, `cold noir gutter`, `documentary evidence insert`, `fingerprint detail panel`, `red-circled clue accent` | 推理、罪案、真相揭示 | 证据页也要有角色反应小格 |
| 奇观尺度 | `full-bleed epic splash`, `tiny figure against colossal background`, `mythic scale contrast`, `vertical aura trails`, `ornate ink detail density` | 玄幻、灾难、神迹、城市毁灭 | 巨物页要保留人物尺度参照 |

## Layout Prompt Matrix

版式提示词应同时包含：`panel_count`、`panel_ratios`、dominant panel、reading path、gutter / inset / SFX 关系。

| layout_id | 页功能 | 可直接改写的 layout prompt | 常见反模式 |
| --- | --- | --- | --- |
| `opening-hook-splash` | 第 1 页异常初现 | `vertical 9:16 comic page, one full-bleed opening splash occupying 70% of the page, two small bottom reaction insets, black gutters, final caption in the lower gutter` | 只写大场景但没有读者视线落点 |
| `threat-low-angle-stack` | 压迫登场 | `three stacked panels: top extreme low-angle villain silhouette, middle narrow terrified eye close-up strip, bottom wide room panel with heavy black gutters` | 反派和主角同权重，压迫感消失 |
| `diagonal-impact-run` | 追逐/攻击 | `four irregular panels cut by one strong diagonal reading path, speed lines crossing gutters, final panel is a foreshortened impact pose with oversized SFX` | 斜切很多但动作方向不清 |
| `splash-with-reaction-insets` | 爆点/觉醒 | `one dominant splash panel with the hero action, 2-3 overlapping reaction insets near the edge, SFX partly breaking the splash border` | inset 遮住主角脸或关键动作 |
| `silent-beat-triptych` | 情绪停顿 | `three quiet narrow panels with minimal dialogue: hand detail, eye close-up, empty space, one small caption box anchoring the pause` | 停顿页塞满解释对白 |
| `evidence-ladder` | 推理/线索 | `zigzag evidence ladder: close-up clue panel, witness reaction inset, document strip, final dark room reveal, captions placed in gutters` | 证据图像没有和剧情动作绑定 |
| `vertical-fall-cascade` | 坠落/失控 | `tall vertical cascading panels, body motion trail moving downward through panel borders, narrow black gutters, bottom impact burst` | 每格都是同一姿势的重复 |
| `border-breaking-cliffhanger` | 页末钩子 | `bottom cliffhanger close-up breaks out of the panel border into the black gutter, one short final caption, large negative space above` | 钩子藏在普通小格里 |
| `split-focus-reveal` | 双线揭示 | `split-focus page: foreground extreme close-up face on the left, background action panel on the right, thin inset clue between them, controlled reading path` | 两个焦点没有主次 |
| `lettering-impact-page` | 声音/爆炸主导 | `dominant action panel, oversized hand-lettered SFX integrated with the explosion shape, smaller aftermath panel below, no floating disconnected letters` | SFX 像贴纸，不像画面元素 |

## Prompt Assembly Patterns

页级 `positive_prompt` 可按以下句式拼装，保证画风和版式同时进入模型上下文：

```text
Vertical 9:16 comic page, [layout_id as natural language], [dominant panel + inset relationship], [reading path], [gutter/SFX/caption placement].
Art style: [2 line/ink terms], [1 shading term], [1 print texture term], [1 motion/emotion effect].
Panel 1: [shot + action + comic technique].
Panel 2: [shot + reaction/transition + comic technique].
Panel 3: [shot + reveal/hook + text slot placement].
Readable Chinese lettering: [speech/caption/SFX rule].
Avoid collage, contact sheet, duplicate composition, nine variations of the same scene.
```

全局 `style_bible` 可分栏写：

```json
{
  "line_and_ink": ["heavy black ink linework", "bold contour lines"],
  "contrast_and_texture": ["screentone shadows", "printed comic page grain"],
  "motion_and_impact": ["speed lines", "impact burst", "border-breaking SFX"],
  "layout_language": ["dominant splash panel", "reaction insets", "irregular black gutters"],
  "lettering_language": ["clear Chinese speech bubbles near speakers", "caption boxes in gutters"]
}
```

## Anti-Pattern Checklist

- 只写 `cinematic masterpiece`，没有 `panel / gutter / balloon / SFX / screentone`。
- 只写 layout 名称，不写 panel 比例、dominant panel 和阅读路径。
- 每页都使用同一种三格上中下条带，导致九页缩略图节奏相同。
- 高冲击页没有大画面、没有 inset 反应、没有 SFX 或 focus lines。
- 解释页只有人物说话，没有证据 close-up、caption anchor 或静默反应格。
- 气泡漂到页面边缘，远离说话角色；SFX 没有绑定动作源。
- 所有 panel 都塞满效果词，反而没有主次；每格应有一个主视觉功能。
