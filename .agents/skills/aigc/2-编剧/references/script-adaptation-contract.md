# Script Adaptation Contract

> **契约地位**：本文件是 `2-编剧` script layer 的核心契约，定义不可违背的保真规则和基础投影规范。其他 reference 文档中的保真规则必须与本文件保持一致；如有冲突，以本文件为准。

## Canonical Purpose

`2-编剧` script layer 将 `projects/aigc/<项目名>/1-分集/第N集.md` 投影为 `projects/aigc/<项目名>/2-编剧/第N集.md`。

输出是上游正文的**影视剧本化结构投影**，不是改写版小说、概要、梗概或自由发挥剧本。

---

## Fidelity Rules（保真规则）

> 以下规则为本技能的**不可违背底线**，任何执行路径都不得违反。

### FR-1：事实保真

- **FR-1.1** 不得压缩、摘要、删减剧情事实
- **FR-1.2** 不得自由改写剧情因果
- **FR-1.3** 不得重排上游事件顺序

### FR-2：信息量保真

除以下明确允许的扩展外，必须完整承接上游原文信息量：

| 允许扩展类型 | 具体形式 | 限制 |
|--------------|----------|------|
| 新增 frontmatter | 项目元数据 | 不得作为剧情摘要替代正文 |
| 新增场景标题 | slugline 格式 | 不得写成剧情摘要或 beat 解释 |
| 新增字段标签 | 27种正式字段 | 不得新增其他解析体系或摄影方案字段 |
| 画面化改写 | 目标/阻碍/策略/停顿/视线/呼吸/手部动作/身体距离/道具关系 | 不得删除事实、改变事件顺序或把动作改成解释性旁白 |
| 角色主观经验投影 | `独白（角色）`、`内心独白（角色）`、可感知 `心理反应`、可执行 `表演提示` | `心理反应` 必须落实为身体、表情、呼吸、停顿、声线、道具或空间反应，不能成为抽象内心解释 |
| 客观叙事派生语音 | 非引号内客观叙事可按 `narration-to-voice-adaptation-contract.md` 转为有锚点的对白、独白、内心独白或旁白 | 不得改写上游已有对白，不得新增事实、事件、因果、规则、线索、人物动机或信息差泄露，必须在报告中留 `narration_to_voice_adaptation_map` |

### FR-3：对话冻结

| 规则 | 说明 |
|------|------|
| **逐字保真** | 上游已有对白必须逐字保留，不润色、不删改、不同义替换、不调整语序 |
| **长对白节拍** | 上游单段长对白可以拆成多个连续原文片段，但所有片段按顺序拼回必须逐字等于上游对白；断句只改变结构落点，不改变文本 |
| **格式规范** | 对白字段标题固定为 `对白（角色名，语态/状态短语）`；角色名必须取自上游真实说话者，`原文角色`、`角色名`、`某人` 等模板占位不得进入终稿 |
| **语态限制** | 第二项只展示上游已有或上下文可确认的说话方式与角色状态，可以是短语（例如 `压着笑意`、`声音发颤`），不强制一词或以"地"结尾；不得借该项改变对白含义或新增人物心理 |
| **引号纯度** | 引号内不得混入动作描写；动作、表情、停顿、空间反应全部下沉到对应 `*画面`、`角色动作`、`表情特写` 或 `表演提示` |

派生语音边界：从非引号内客观叙事转出的 `derived_voice_line` 不属于 `source_dialogue`，但必须满足 `narration-to-voice-adaptation-contract.md` 的触发、说话者资格、预算和证据要求；它不得替代、修饰或续写上游已有对白。

### FR-4：场景标题规范

场景标题统一使用阿拉伯数字编号 + 好莱坞标准 slugline：

```md
### 场景1：内景 永夜私立中学二年级A班教室 - 日
### 场景2：外景 学校操场 - 夜
```

| 规则 | 说明 |
|------|------|
| 标题性质 | 不得写成剧情摘要、动作 beat 或主题解释 |
| slugline 组成 | `内景/外景 + 场所 + 日/夜` |
| 编号复用 | 同一集内完全相同的 slugline 必须沿用同一个场景编号 |
| 新场景判断 | **只有**以下情况可视为新场景：日/夜不同，或真实地点/空间范围变化 |
| 不触发新场景 | 规则宣告、角色入场、公告、能力觉醒等叙事 beat 变化 |
| 连续 slugline | 同一 slugline 首次出现时写标题，后续 beat 直接接正文 |

---

## Screenplay Projection Definition（剧本化投影定义）

本技能中的"剧本化"不是把小说句子换成更像剧本的抽象描述，而是把上游信息投影为**三类可执行材料**：

| 类型 | 定义 | 示例 |
|------|------|------|
| **可见** | 镜头能拍到的身体、表情、物件、文字、光线、空间、位置、运动和屏幕/黑板显影 | 角色动作、表情特写、环境描写、道具特写 |
| **可听** | 现场或声音设计能听到的对白、旁白、机械提示、脚步、铃声、摩擦、尖叫、静默后的环境声 | 对白、独白、旁白、音效 |
| **可执行** | 演员、导演、美术、声音部门拿到后能直接做动作、站位、表演、道具或声音处理 | 表演提示、场面调度、心理反应 |

**核心要求**：`画面`、`动作画面`、`对白画面`、`音效画面`、`旁白画面`、`系统画面`、`环境描写`、`道具特写`、`心理反应`、`表演提示` 都必须优先具象化和可感知化。它们不得停留在概念判断、主题解释、作者评论、比喻性结论或读者感受上。

---

## Concrete Visual Rule（具体画面规则）

> **画面字段必须回答"摄影机看见什么"，而不是"观众理解什么"。**

### 禁止写入画面字段的内容类型

| 类型 | 示例 | 修复方式 |
|------|------|----------|
| 抽象概念 | `规则测试开始`、`压抑气氛继续`、`现实身份被覆盖`、`人数压力`、`底牌`、`幸运还是诅咒` | 转成可见物：黑板文字、系统字、课桌、手指、目光、灯光、屏幕、道具状态 |
| 解释性因果 | `因为没有人敢缺席`、`第一次意识到人数本身就是规则`、`确认队友候选` | 转成行为链：动作序列、道具状态、群体反应 |
| 作者判断或主题句 | `这是一场小型审判`、`不做灾害奇观化`、`真正的规则` | 删除，或转为可见压力承托 |
| 心理或感受替代 | `不敢靠近`、`正面摊牌的爽快`、`像在等什么发生` | 转成身体执行：呼吸、眼神、停顿、手指、坐姿、退半步、避开视线 |
| 纯章节/任务说明 | `第二节课是课堂作业`、`规则测试开始`、`没有字数限制` | 删除，或改为可见动作/道具 |
| 内部规则泄露 | `本场按上游原文顺序承接`、`说话者的视线`、`不新增事件结果` | 删除，仅作为内部执行约束 |

---

## Dramatic And Performance Projection（戏剧与表演投影）

高质量剧本化必须把"发生了什么"继续投影成"这场戏如何被演员和导演执行"。该层只强化上游已有信息，不新增剧情事实。

### 必做转换映射

| 上游信息 | 投影目标 | 具体承托方式 |
|-----------|----------|--------------|
| 场景功能 | `entry_state / pressure_source / turning_point / exit_state` | 落入具体画面、声音、道具、表演或群像字段 |
| 潜台词 | 行为策略（试探、隐瞒、求证、施压、求同盟、拖延） | 通过停顿、避视、反问、道具动作、身体距离或声线变化呈现 |
| 心理变化 | 演员任务 | 至少给出角色目标、阻碍、策略或外显动作中的两项 |
| 权力关系 | 场面调度 | 通过站坐、高低、远近、门口/讲台/窗边占位、群体视线和道具归属表现 |
| 沉默与反应 | 可见/可听余波 | 默认不得用新增对白替代上游没有写出的潜台词；只有非引号客观叙事满足 `narration-to-voice-adaptation-contract.md` 时，才可形成 source-grounded 派生语音 |

### 越权禁止

`2-编剧` screenplay layer 只负责剧本文本投影、声画字段分流和可拍性基础承接。导演创作判断和表演工艺分别交给 `4-导演` 与 `5-表演`，**不得提前写**：

- 机位、景别、镜头运动
- 分镜编号
- `分镜明细预设` 字段

---

## Required Subject Marking（主体标记要求）

| 字段类型 | 格式示例 |
|----------|----------|
| 对白 | `对白（林寂，呼吸发紧）：“这什么情况？”` |
| 独白 | `独白（林寂）：“国运？副本？SSS级？”` |
| 内心独白 | `内心独白（林寂）：“她发现了。”` |
| 旁白 | `旁白（系统提示）：“天道系统·全球公告。”` |
| 音效 | `音效（高跟鞋）：“嗒、嗒、嗒。”` |

所有对白、内心独白、旁白都必须显式带主体。对白还必须显式带语态或角色状态。音效必须显式带来源；来源不可见时可写 `音效（不可见来源）`。

---

## Field Content Restrictions（字段内容限制）

### FR-5：声音字段纯度

| 规则 | 说明 |
|------|------|
| 只写声音本体 | 不写时间说明、事件说明或叙述概括 |
| 禁止示例 | `音效（铃声）：“八点四十分铃声。”`（这是时间说明） |
| 正确示例 | `音效（铃声）：“叮铃铃——”` |

### FR-6：动作字段纯度

- 必须写客观可拍文本：身体行为、神态、语气、呼吸、停顿、重心、空间位移、道具操作、生理反应
- **禁止主观意图词**：`试图`、`想要`、`打算`、`意图`、`准备借此`、`为了让/为了掩饰`、`想借此`
- 上游写出明确速度或力度时**必须保留**
- 上游没有速度信号时，只在表演需要时补轻量节奏词，不得为"更燃"改变动作结果

### FR-7：心理反应字段锚定

- 必须写明确主体的可感知反应，不写无主体心理结论
- 只能靠文字解释才能成立的内容，应改入 `独白（角色）` / `内心独白（角色）`
- 已能拆入具体字段的内容，优先拆入
- **不得**新增未锚定对白、幻象、回忆、事件、因果、答案或人物动机；客观叙事派生语音必须按专项合同留证

---

## Frontmatter（最小元数据）

逐集编导稿必须包含以下 frontmatter：

```yaml
---
项目名: <项目名>
集数: 第N集
stage: 2-编剧
source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
output_path: projects/aigc/<项目名>/2-编剧/第N集.md
adaptation_mode: faithful_screenplay_projection
dialogue_lock: true
audio_visual_pairing: required
slugline_policy: stable_by_location_time
peak_visual_policy: strengthen_existing_source_payoff
enrichment_mode: none
---
```

可选字段（按项目需要）：`source_coverage`、`scene_count`、`review_status`

**限制**：不得把 frontmatter 变成剧情摘要替代正文。

---

## Minimum Scene Content（场景最小内容）

每个场景至少包含一条正式剧本画面字段（见 Allowed Field Titles）。其中：

| 字段 | 承载内容 | 禁止内容 |
|------|----------|----------|
| `环境描写` | 地点、空间结构、自然条件、光照状态、承载面、围护面、静置物件、整体氛围 | 人物动作、对白引出、剧情结果、心理解释、固定承接规则 |
| `动作画面` | 可拍摄的身体动作或空间运动 | 小说章节名、心理解释、背景说明、抽象判断 |
| `对白画面` | 对白附近的具体可见承托 | 说明性模板句、复述对白内容 |
| `道具特写` | 物件的可见状态、已有信息、归属压力、规则显影或状态变化 | 角色心理解释、推理结论、新增规则功能 |

---

## Allowed Field Titles（允许的字段标题）

> 以下为 `2-编剧` script layer 允许使用的全部正式字段。除以下字段外，不得新增其他解析体系或摄影方案字段。

| 类别 | 字段名称 |
|------|----------|
| **环境** | `环境描写` |
| **动作** | `角色动作`、`动作画面`、`角色造型` |
| **调度** | `场面调度`、`群像画面`、`表情特写` |
| **道具** | `道具特写`、`系统画面`、`规则显影`、`现实灾难画面` |
| **对白** | `对白（角色名，语态/状态短语）`、`对白画面` |
| **独白** | `独白（角色）`、`独白画面`、`内心独白（角色）`、`内心独白画面` |
| **旁白** | `旁白（主体）`、`旁白画面` |
| **声音** | `音效（来源）`、`音效画面` |
| **表演** | `心理反应`、`表演提示` |
| **转场** | `转场` |

---

## Internal Constraint Boundaries（内部约束边界）

> 以下内容只能作为**内部执行约束**，不能进入 canonical 剧本正文。

| 约束类型 | 示例 |
|----------|------|
| 任务说明 | `本场按上游原文顺序承接...` |
| 模板句 | `说话者的视线、手部动作、身体距离和对手反应就近承托对白` |
| 规则复述 | `引号内不加入动作`、`不新增事件结果` |
| 字段说明 | `对白画面：...就近承托对白` |
| 章节标记 | `第二节课是课堂作业`、`规则测试开始` |

正文使用中文双引号。

---

## Cross-Reference Index（交叉引用索引）

本契约中定义的规则在其他 reference 文档中的对应位置：

| 规则编号 | 内容摘要 | 对应文档 |
|----------|----------|----------|
| FR-1 | 事实保真 | `script-adaptation-contract.md` §Artistic Transformation Boundary |
| FR-2 | 信息量保真 | `field-routing-and-audio-visual-contract.md` §Audio-Visual Pairing |
| FR-3 | 对话冻结 | `field-routing-and-audio-visual-contract.md` §Dialogue Freeze |
| 派生语音 | 客观叙事转对白/独白 | `narration-to-voice-adaptation-contract.md` |
| FR-4 | 场景标题规范 | `field-routing-and-audio-visual-contract.md` §Scene Title Contract |
| FR-5 | 声音字段纯度 | `field-routing-and-audio-visual-contract.md` §Sound Literal Rule |
| FR-6 | 动作字段纯度 | `field-routing-and-audio-visual-contract.md` §Action Field Dynamics |
| FR-7 | 心理反应锚定 | `field-routing-and-audio-visual-contract.md` §Psychological Reaction Field Anchor |
| 画面规则 | Concrete Visual Rule | `field-routing-and-audio-visual-contract.md` §Concrete Visual Rule |
| 字段标题 | Allowed Field Titles | `field-routing-and-audio-visual-contract.md` §Allowed Field Titles |

> **注意**：其他文档在引用本契约规则时，只需注明规则编号（如 `FR-1`），不得重复规则内容。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 输出是否写入 canonical `projects/aigc/<项目名>/2-编剧/第N集.md`，frontmatter 是否包含 `source_episode_path` 并可回指上游逐集正文？ | `GATE-SCRIPT-01` / `GATE-SCRIPT-02` | `FAIL-PATH` / `FAIL-SOURCE` | `../SKILL.md#N1-INTAKE` / `../SKILL.md#N7-SCRIPT-WRITEBACK` | `source_episode_path`、`output_path` 与 `reference_load_manifest` 记录路径、集号和加载边界 |
| FR-1 事实保真是否成立：没有压缩、摘要、删减剧情事实，没有自由改写因果或重排事件顺序？ | `GATE-SCRIPT-03` | `FAIL-FAITHFULNESS` | `../SKILL.md#N5-SCRIPT-DRAFT` / `../SKILL.md#N6R-SCRIPT-REPAIR` | `faithful_projection_trace` 逐段记录上游事实、输出字段和顺序对齐 |
| FR-2 信息量保真是否成立：新增 frontmatter、slugline、字段标签和画面化改写只服务投影，没有替代正文、删除信息或新增第二套解析体系？ | `GATE-SCRIPT-03` / `GATE-SCRIPT-10` | `FAIL-FAITHFULNESS` / `FAIL-CONCRETE-VISUAL` | `../SKILL.md#N4-FIELD` / `../SKILL.md#N5-SCRIPT-DRAFT` | `field_projection_map` 与 `faithful_projection_trace` 记录每条新增字段的上游依据 |
| FR-3 对话冻结是否成立：上游已有对白逐字保真、真实角色名、语态/状态短语不改含义、引号内无动作，且客观叙事派生语音没有替代或改写上游对白？ | `GATE-SCRIPT-04` | `FAIL-DIALOGUE` | `../SKILL.md#N5-SCRIPT-DRAFT` | `dialogue_lock_map` 记录上游对白、输出对白、角色名、语态依据和派生语音隔离风险；`narration_to_voice_adaptation_map` 记录非对白来源 |
| FR-3 长对白节拍是否成立：上游单段长对白只被拆成连续原文片段，片段拼回逐字等于上游对白，且断句服务戏剧动作、气口和可见承托？ | `GATE-SCRIPT-23` | `FAIL-LONG-DIALOGUE-BEAT` | `../SKILL.md#N4-FIELD` / `../SKILL.md#N5-SCRIPT-DRAFT` | `long_dialogue_beat_map` 记录 source_dialogue、exact_text_segment、recomposed_dialogue、dramatic_action 和 paired_visual_field |
| FR-4 场景标题是否符合阿拉伯数字编号 + `内景/外景 场所 - 日/夜`，同一 slugline 只首次打印，不因叙事 beat 变化重复开场？ | `GATE-SCRIPT-07` | `FAIL-SLUGLINE` | `../SKILL.md#N3-SCENE` | `scene_slugline_table` 与 `scene_order_trace` 记录场景编号、slugline、首次出现和复用 |
| 剧本化投影是否只使用允许字段，将上游信息转成可见、可听、可执行材料，而不是改写版小说、概要或自由发挥剧本？ | `GATE-SCRIPT-06` / `GATE-SCRIPT-10` | `FAIL-SCENE-VISUAL` / `FAIL-CONCRETE-VISUAL` | `../SKILL.md#N4-FIELD` / `../SKILL.md#N5-SCRIPT-DRAFT` | `field_projection_map.allowed_field_check` 记录正式字段、上游锚点和可拍性 |
| FR-5/FR-6/FR-7 是否成立：声音字段只写声音本体，动作字段客观可拍，心理反应有明确主体和可感知反应？ | `GATE-SCRIPT-08` / `GATE-SCRIPT-11` / `GATE-SCRIPT-10` | `FAIL-ACTION-PURITY` / `FAIL-SOUND-LITERAL` / `FAIL-CONCRETE-VISUAL` | `../SKILL.md#N4-FIELD` | `sound_literal_risk_map`、`objective_action_purity_evidence` 与 `concrete_visual_risk_map` |
| 内部任务说明、模板句、规则复述、字段说明或章节标记是否只作为内部约束，没有泄露到 canonical 剧本正文？ | `GATE-SCRIPT-12` | `FAIL-PLACEHOLDER-LEAK` | `../SKILL.md#N5-SCRIPT-DRAFT` / `../SKILL.md#N6R-SCRIPT-REPAIR` | `placeholder_leak_risk_map` 记录泄露文本、所在字段和删除/改写动作 |
