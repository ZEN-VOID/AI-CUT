# Drafting Built-in Acceptance Contract

本文件承载 `story-drafting` 的阶段内置验收合同。它只展开 `3-初稿/SKILL.md#Built-in Acceptance Contract`，不得外包给独立 `story/review`，也不得写出父层 `review/第V卷.validation.json`。

## Acceptance Scope

| dimension | checks |
| --- | --- |
| `source_context` | 是否加载 story 根、阶段 `CONTEXT.md`、项目 MEMORY/CONTEXT、三层 planning、north_star、对象真源和监制包 |
| `structure_realization` | 本章 planning 的事件、冲突、任务、线索和伏笔是否被写成戏，而不是摘要式提到 |
| `continuity` | 同卷前文存在时是否完整承接事实、线索、关系、道具、卷目标和文气 |
| `logic_self_consistency` | 因果链、能力边界、世界规则、例外代价和 source truth 是否自洽 |
| `character_consistency` | 人物行为、动机、关系压力、成长承接、对白声口和社会身份语言是否成立 |
| `presence_texture` | 关键人物反应是否由当前压力、欲望、身份和关系驱动；场景颗粒是否服务冲突、信息、空间限制和读者牵引 |
| `genre_scene_fit` | 命中类型化场面时，是否建立项目题材轴、场景功能轴和必要 subtype package；场面强化是否服务当前章义务、人物压力、信息推进和章末牵引 |
| `timeline` | 时间锚、事件顺序、持续时长和伏笔静默窗口是否越线 |
| `task_convergence` | 章级任务是否从属于卷级任务，支流任务是否汇聚、转挂或显式开放 |
| `prose_reader_pull` | 是否具备现场感、句群起伏、对白潜台词、心理暗流、读者牵引和章末钩子；**是否通过 AI 腔五层检测（详见 `_shared/ai-feature-detection-checklist.md`）** |
| `creative_authorship` | 是否由 LLM-first 主创，脚本和模板没有生成正文 |
| `output_state` | frontmatter、标题、canonical path、验收包和状态 hook 是否正确 |
| `anti_ai_features` | AI 腔系统化检测：是否按五层检测清单（词法/句法/篇章/人物/叙事）逐层检测并输出 `detection_report`；不允许用泛化"更自然"替代具体坏点定位 |

## Acceptance Packet

验收包写入 `projects/story/<项目名>/3-初稿/第N卷/第N章.acceptance.json`，至少包含：

- `acceptance_status`
- `accepted_manuscript_stage`
- `accepted_manuscript_refs`
- `dimension_results`
- `critical_issues`
- `rework_targets`
- `handoff_targets`
- `acceptance_ref`

初稿 `pass` 只授权进入 `4-润色`；`handoff_targets` 不得包含 `return`。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 candidate draft 交付，并 handoff 到 `4-润色` |
| `pass_with_followups` | 可交付，但有非阻断后续项；仍需进入 `4-润色` |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target 后重新验收 |
| `blocked` | 缺少关键输入、权限或写回授权 |

## Failure Codes

| fail_code | dimension | default_rework_target |
| --- | --- | --- |
| `FAIL-DRAFT-CONTEXT` | source_context | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N4-SUPERVISION` |
| `FAIL-DRAFT-STRUCTURE` | structure_realization | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-CONTINUITY` | continuity | `SKILL.md#N3-CONTINUITY` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-LOGIC` | logic_self_consistency | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-CHARACTER` | character_consistency | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-PRESENCE-TEXTURE` | presence_texture | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-GENRE-SCENE` | genre_scene_fit | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-TIMELINE` | timeline | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-TASK` | task_convergence | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-PROSE-PULL` | prose_reader_pull | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-AUTHORSHIP` | creative_authorship | `SKILL.md#LLM-First Creative Authorship Contract` |
| `FAIL-DRAFT-WRITEBACK` | output_state | `SKILL.md#N7-WRITEBACK-STATE` |

## Gate Rule

不得宣布完成：

- 缺少必需输入或未加载项目记忆/相关项目上下文。
- 缺少监制包或正式降级记录。
- planning 义务只被摘要提到，没有转成可感知的事件、关系压力或现场动作。
- 同卷前文、因果、人物、时间线或任务汇聚出现断带。
- 人物反应只是表演通道堆叠，或场景颗粒只是氛围装饰，不能推动冲突、信息、关系或章末牵引。
- 类型化场面没有 `type_package_manifest` 或 `genre_scene_route`，把武侠动作当默认写法，机械套题材包，命中 subtype 却没有真实加载路径，或新增无源事实、能力规则、关系转折、剧情结果和第三正文真源。
- 正文保留 planning 标题句法、执行层标签或流程术语。
- 正文缺少现场发现、读者牵引或章末钩子。
- 主要人物对白无法区分身份、关系和意图。
- 脚本以规则拼接、模板填充或启发式补写替代 LLM 主创正文。
- 输出不是 canonical path，或未同步生成 `第N章.acceptance.json`。
- 覆盖已有章节时没有授权。

## Quantified Scoring Anchors

为提升验收一致性和跨 LLM/跨时间可比性，每个验收维度增加 0-10 分量表。评分仅作为诊断参考，不影响现有 PASS/FAIL 判定逻辑。`dimension_scores` 作为 `stage_acceptance_packet` 的补充字段。

### 通用评分锚点

| 分数 | 等级 | 通用描述 |
| --- | --- | --- |
| 0 | 不可用 | 维度完全未达标，存在硬伤或严重遗漏 |
| 3 | 勉强可用 | 有基本覆盖但大面积空洞、浮于表面 |
| 5 | 合格 | 满足基本要求，无明显硬伤，但缺乏亮点 |
| 7 | 良好 | 超越基本要求，有可感知的质感或深度 |
| 10 | 优异 | 达到人力创作水准，有鲜明的文体个性和叙事张力 |

### 各维度详细锚点

#### `source_context`（源上下文完整性）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 缺少 2 项以上必需输入，或关键规划文件未加载 |
| 3 | 只加载了部分输入，遗漏了 north_star 或对象真源等关键上下文 |
| 5 | 必需输入全部加载，但监制包降级记录不充分 |
| 7 | 所有输入齐备，监制包完整吸收了顾问反馈 |
| 10 | 上下文深度整合，north_star/planning/cards/监制包有机融入创作决策 |

#### `structure_realization`（结构兑现）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | planning 义务完全未兑现，正文与规划脱节 |
| 3 | 主要事件兑现了约 50%，大量义务仅被摘要提及 |
| 5 | 所有 planning 义务被写成可感知的戏，但部分转译粗糙 |
| 7 | 义务全部兑现，事件推进有层次感和递进逻辑 |
| 10 | 义务不仅兑现，且产生了超越 planning 的叙事张力，戏与戏之间有因果链 |

#### `continuity`（连续性）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 与前文存在 2 处以上直接矛盾或完全无视前文章末状态 |
| 3 | 承接了主要事件，但遗漏了 1-2 处关键线索或道具状态 |
| 5 | 同卷前文的事实、关系、道具和压力线完整承接 |
| 7 | 承接精准，且有微妙的文气延续（如节奏、情绪调性） |
| 10 | 既有精确的事實承接，又有巧妙的伏筆回响和信息递进 |

#### `logic_self_consistency`（逻辑自洽）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 存在 2 处以上硬逻辑矛盾（能力、规则、因果冲突） |
| 3 | 主事件逻辑成立，但 1 处边缘细节与世界观规则冲突 |
| 5 | 本章内因果链、能力边界、世界规则完全自洽 |
| 7 | 自洽且例外/代价有合理解释，信息逐步揭示不跳跃 |
| 10 | 多线逻辑互相验证，因果链有层层递进的精密感 |

#### `character_consistency`（人物一致性）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 主要角色行为与前文设定直接矛盾 ≥ 2 处 |
| 3 | 角色动机模糊，或 1 处存在明显的 OOC（脱离角色设定） |
| 5 | 行为、动机、关系压力与社会身份语言全部成立 |
| 7 | 角色选择有内在逻辑，成长/变化有可追踪的推进 |
| 10 | 角色在压力下有符合设定但又出人意料的真实反应，声口高度辨识 |

#### `presence_texture`（人物在场与场景质感）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 关键人物反应缺失，场景空洞，或充满表演腔和脸色捷径 |
| 3 | 人物有基本反应，但仍有脸色、呼吸堆叠等表演痕迹 |
| 5 | 人物反应由压力/欲望驱动，场景颗粒服务冲突和信息推进 |
| 7 | 关键人物的微反应精准，场景感官颗粒少而准 |
| 10 | 人物在场感强烈，每个动作/沉默/空间反应都有含意，场景质感有电影级密度 |

#### `genre_scene_fit`（类型化场面适配）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 缺少 genre_scene_route，或把非武侠题材写成武侠动作 |
| 3 | 有 genre_scene_route 但执行粗糙，题材质感弱 |
| 5 | 双轴建立正确，场面强化服务当前章义务，无题材包机械套用 |
| 7 | 场面不仅有题材质感，且与人物压力/关系推进有机结合 |
| 10 | 类型场面成为人物弧线的有机部分，有该题材的经典场面设计水准 |

#### `timeline`（时间线）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 存在 2 处以上时间锚错位或事件顺序矛盾 |
| 3 | 主要时间线成立，但 1 处时间描述模糊 |
| 5 | 时间锚、事件顺序、持续时长和伏笔窗口全部成立 |
| 7 | 时间推进有节奏意识，时空转换顺畅 |

#### `task_convergence`（任务汇聚）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 章级任务与卷级任务脱节，或支流任务全部悬空 |
| 3 | 主要任务有推进，但 1-2 条支线被忽略 |
| 5 | 章级任务从属卷级，支流任务有汇聚/转挂/显式开放 |
| 7 | 任务线之间有交织和互相影响，汇聚有自然感 |

#### `prose_reader_pull`（文体读感与追读力）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 文本无法阅读（AI 腔严重、执行标签残留、说明腔） |
| 3 | 可读但平淡，缺乏句群起伏和读者牵引 |
| 5 | 有现场感、句群有起伏、对白有潜台词、章末有钩子 |
| 7 | 读感好，有微妙的情绪暗流和阅读期待管理 |
| 10 | 完全人力级读感，有鲜明的文体个性，翻页冲动强烈 |

#### `output_state`（输出形态）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | frontmatter 缺失、输出到非 canonical path、无验收包 |
| 3 | 格式部分错误（如 frontmatter 字段不完整） |
| 5 | frontmatter/标题/canonical path/验收包/状态 hook 全部正确 |
| 7 | 输出规范且验收包信息充分 |

### 题材维度权重配置

根据项目 `north_star.yaml.genre_contract.primary_genre`，验收时可参考以下权重配置：

| 题材 | source_context | structure | continuity | logic | character | presence | genre_scene | timeline | task | prose | output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 武侠 | 1.0 | 1.0 | 1.0 | 1.2 | 1.0 | 1.3 | 1.2 | 1.0 | 1.0 | 1.0 | 1.0 |
| 言情/甜宠 | 1.0 | 1.0 | 1.0 | 1.0 | 1.3 | 1.2 | 1.1 | 1.0 | 1.0 | 1.1 | 1.0 |
| 悬疑/侦探 | 1.0 | 1.2 | 1.3 | 1.3 | 1.0 | 1.0 | 1.2 | 1.2 | 1.1 | 1.0 | 1.0 |
| 玄幻/修仙 | 1.0 | 1.0 | 1.0 | 1.2 | 1.0 | 1.1 | 1.2 | 1.0 | 1.0 | 1.0 | 1.0 |
| 现实/年代 | 1.0 | 1.0 | 1.0 | 1.1 | 1.2 | 1.3 | 1.0 | 1.1 | 1.0 | 1.0 | 1.0 |
| 恐怖/灵异 | 1.0 | 1.1 | 1.0 | 1.1 | 1.0 | 1.3 | 1.2 | 1.0 | 1.0 | 1.2 | 1.0 |
| 默认 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

权重仅用于计算加权总分供趋势监控参考；不为 1.0 的维度标注 `*` 表示当前题材的侧重点。

### 不合格红线（Dimension Red Lines）

以下情况直接判定对应维度 FAIL，不得进入量化评分流程：

| 维度 | 红线条件 |
| --- | --- |
| `source_context` | 缺少三层 planning 中任意一层，或缺少 north_star.yaml |
| `structure_realization` | 本章 planning 的关键事件（冲突/转折/高潮）完全未兑现 |
| `continuity` | 与同卷前文存在直接事实矛盾 ≥ 2 处，或章末状态被完全无视 |
| `logic_self_consistency` | 能力/规则/因果存在不可调和的矛盾 ≥ 2 处 |
| `character_consistency` | 主要角色行为与前文设定直接矛盾 ≥ 2 处 |
| `presence_texture` | 所有关键场景的人物反应均为脸色/呼吸/眼神模板化描述 |
| `genre_scene_fit` | 命中类型化场面但未建立 genre_scene_route |
| `timeline` | 同一事件的时间锚冲突 ≥ 2 处 |
| `task_convergence` | 三条以上章级任务线处于悬空且未说明 |
| `prose_reader_pull` | 正文包含执行标签或超过 50% 段落为说明腔 |
| `output_state` | 输出到非 canonical path 或未生成验收包 |
