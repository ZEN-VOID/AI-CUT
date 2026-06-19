# Polishing Built-in Acceptance Contract

本文件承载 `story-polishing` 的阶段内置验收合同。它只展开 `4-润色/SKILL.md#Built-in Acceptance Contract`，不得外包给独立 `story/review`，也不得写出父层 `review/第V卷.validation.json`。

## Acceptance Scope

| dimension | checks |
| --- | --- |
| `source_anchor` | 是否读取唯一 `3-初稿` 源章、目标 `4-润色` 路径和既有目标稿状态 |
| `minimal_repair` | 是否保留初稿事实、段落骨架、句群起伏、人物声口和章末牵引 |
| `regression_structure_logic` | 润色是否损坏结构兑现、连续性、逻辑自洽、人物一致性、时间线或任务汇聚 |
| `chinese_prose` | 是否去掉明显翻译腔、说明腔、流程腔和公式化解释 |
| `genre_texture_density` | 是否保留并强化当前题材和当前场面实际承载的题材质感、场景密度、信息延迟、对白锋利度、人物在场反应、视觉可读性、句群节奏和命中的细节扩写焦点；未承载焦点不得作为扣分项 |
| `detail_expansion` | 命中动作设计、内心戏、氛围压力、科技元素、赛博质感、玄幻能力或言情拉扯等适用细节扩写焦点时，是否锁定 source anchor、affected span、selected repair packages 和 no-new-fact boundary；未命中焦点是否 N/A |
| `genre_scene_integrity` | 命中类型化场面修复时，是否锁定 source anchor、affected span、项目题材轴、场景功能轴和必要 subtype repair package，且没有改事实、改结果或题材越界 |
| `anti_ai_features` | 是否按 `_shared/ai-feature-detection-checklist.md` 五层检测清单（词法/句法/篇章/人物/叙事）逐层定位具体 AI 腔坏点并输出 `detection_report`，不允许泛化洗稿 |
| `reader_pull` | 悬念、冲突压力、情绪推进、章末钩子和读者追读力是否没有弱化 |
| `volume_voice_consistency` | **（卷级维度）** 同一人物在卷内各章的对白风格（句式/用词/修辞/口头禅）是否一致；触发条件：卷级审计 `character_arc_integrity` 子项 FAIL |
| `creative_authorship` | 是否由 LLM-first 润色，脚本和模板没有生成正文 |
| `output_state` | frontmatter、标题、canonical path、验收包和状态 hook 是否正确 |

## Acceptance Packet

验收包写入 `projects/story/<项目名>/4-润色/第N卷/第N章.acceptance.json`，至少包含：

- `acceptance_status`
- `accepted_manuscript_stage`
- `accepted_manuscript_refs`
- `dimension_results`
- `critical_issues`
- `rework_targets`
- `handoff_targets`
- `acceptance_ref`

终稿 `pass` 必须声明 `accepted_manuscript_stage = 4-润色`，并在 `handoff_targets` 中包含 `return`。若项目显式跳过润色，则不得使用本技能伪造通过，应回到 `3-初稿` 验收包声明例外。

## Volume-Level Acceptance Aggregation

当卷内所有章的终稿验收均 PASS 后，必须自动聚合卷级验收包，并触发卷级质量审计（详见 `_shared/volume-audit-contract.md`）：

### Volume Acceptance Packet Schema

卷级验收包写入 `projects/story/<项目名>/4-润色/第V卷/volume.acceptance.json`，至少包含：

- `volume_ref`: 卷号标识
- `aggregation_status`: `complete` / `pending` / `partial`
- `chapter_statuses`: `{ chapter_ref: { acceptance_status, score, path } }`
- `volume_summary`: `{ total_chapters, pass_count, avg_dimension_scores }`
- `volume_quality_audit`: 卷级 6 维度质量审计结果（按 `_shared/volume-audit-contract.md` 执行）
- `handoff_targets`: 当 `aggregation_status == complete` 且卷级审计通过时自动包含 `return`
- `blockers`: 当存在未完成章时的阻断原因列表
- `aggregation_ref`: 指向各章验收包的引用

### Aggregation Rules

1. 卷内所有章验收 PASS → `aggregation_status = complete` → 触发卷级质量审计（P5A-VOLUME-AUDIT）
2. 卷级审计 `PASS` 或 `PASS_WITH_WARNINGS` → `handoff_targets = [return]` → 自动触发 `return` 卫星技能
3. 卷级审计 `NEEDS_REWORK` → 阻断 return，按 `volume_quality_audit.rework_recommendations` 路由到对应章/规划进行修复
4. 存在任意章验收未完成或 FAIL → `aggregation_status = pending` → 不触发卷级审计和 return

### Volume Completion Gate

下列条件同时满足时才可触发自动 return：

- `aggregation_status == complete`
- 卷级审计 `audit_status ∈ {PASS, PASS_WITH_WARNINGS}`
- 卷内各章的 `handoff_targets` 均包含 `return`（或具备显式 skip-polish 标注）
- 卷级验收包的 `handoff_targets` 明确为 `[return]`
- `STATE.json` 中卷级执行状态已更新

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 accepted polished manuscript 交付，并 handoff 到 `return` |
| `pass_with_followups` | 可交付且可 handoff，但必须在验收包中记录 residual followups |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target 后重新验收 |
| `blocked` | 缺少源章、权限或写回授权 |

## Failure Codes

| fail_code | dimension | default_rework_target |
| --- | --- | --- |
| `FAIL-POLISH-SOURCE` | source_anchor | `SKILL.md#P1-SOURCE-LOCK` |
| `FAIL-POLISH-SCOPE` | minimal_repair | `SKILL.md#P3-REPAIR-PLAN` |
| `FAIL-POLISH-REGRESSION` | regression_structure_logic | `SKILL.md#P3-REPAIR-PLAN` / `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-PROSE` | chinese_prose | `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-TEXTURE` | genre_texture_density | `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-DETAIL-EXPANSION` | detail_expansion / genre_texture_density | `SKILL.md#P3-REPAIR-PLAN` / `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-GENRE-SCENE` | genre_scene_integrity | `SKILL.md#P3-REPAIR-PLAN` / `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-AI-FEATURES` | anti_ai_features | `SKILL.md#P3-REPAIR-PLAN` / `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-READER-PULL` | reader_pull | `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-AUTHORSHIP` | creative_authorship | `SKILL.md#LLM-First Creative Authorship Contract` |
| `FAIL-POLISH-WRITEBACK` | output_state | `SKILL.md#P6-WRITEBACK-STATE` |
| `FAIL-POLISH-VOL-SYSTEMIC` | volume_voice_consistency / volume rhythm / strand | `SKILL.md#P3-REPAIR-PLAN` → `_shared/volume-systemic-repair-contract.md` |

## Gate Rule

不得宣布完成：

- 缺少 `3-初稿` 源章。
- 润色改动核心事实、人物关系、因果链、时间线或章末牵引。
- 润色造成结构兑现、连续性、人物一致性或任务汇聚回退。
- 润色把初稿清洗成短句均匀、通用顺滑或摘要式文本。
- AI 腔坏点没有被具体定位，只有泛化"更自然"的洗稿口号。
- 当前题材和当前场面实际承载的题材质感、场景密度、人物反应、视觉可读性、信息延迟、句群节奏或追读力被磨平。
- 命中适用细节扩写焦点时，没有锁定 source anchor、affected span、selected repair packages 和 no-new-fact boundary；或把动作、内心戏、氛围、科技、赛博、玄幻、言情细节扩成新设定、新结果、新关系转折或整章加料；或把无关候选焦点当成所有题材必修项。
- 类型化场面修复没有锁定 source anchor、affected span、`repair_type_package_manifest` 和 `genre_scene_route`，命中 subtype 却没有真实加载路径，或把局部修复扩大成武侠化默认、题材包机械套用、改胜负/关系结果/能力规则。
- 为了修"人物、氛围或光影"新增无源剧情事实、实体光源、天气、烟雾、气味或独立装饰段。
- 脚本以规则拼接、模板填充或启发式补句替代 LLM 主创正文。
- 输出不是 canonical path，或未同步生成 `第N章.acceptance.json`。
- `acceptance_status=PASS` 但 `handoff_targets` 未包含 `return`。
- 覆盖已有润色稿时没有授权。

## Quantified Scoring Anchors

为提升验收一致性和跨 LLM/跨时间可比性，每个终稿验收维度增加 0-10 分量表。评分仅作为诊断参考，不影响现有 PASS/FAIL 判定逻辑。`dimension_scores` 作为 `stage_acceptance_packet` 的补充字段。

### 通用评分锚点

| 分数 | 等级 | 通用描述 |
| --- | --- | --- |
| 0 | 不可用 | 维度完全未达标，存在硬伤或严重遗漏 |
| 3 | 勉强可用 | 有基本覆盖但大面积空洞、浮于表面 |
| 5 | 合格 | 满足基本要求，无明显硬伤，但缺乏亮点 |
| 7 | 良好 | 超越基本要求，有可感知的质感或深度 |
| 10 | 优异 | 达到人力编辑水准，有鲜明的文体个性和可交付品质 |

### 各维度详细锚点

#### `source_anchor`（源章锚定）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 源章未加载，或凭记忆/planning 替代源章生成润色稿 |
| 5 | 源章已加载，target path 正确 |
| 7 | 源章完整回读，并有 before/after 对比意识 |

#### `minimal_repair`（最小修补边界）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 整章重写式润色，丢失初稿骨架和人物气口 |
| 3 | 修补范围过大（超过 30% 内容被重写） |
| 5 | 修复了明确的坏点，段落骨架和字數分布基本不变 |
| 7 | 精准锁定 affected span，只修明确坏处，保留初稿纹理 |
| 10 | 最小修补的同时产生了显著的质量提升，改动 ≤ 15% 但读感明显改善 |

#### `regression_structure_logic`（结构/逻辑不回退）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 润色造成结构兑现/连续性/人物一致性 ≥ 2 处回退 |
| 3 | 1 处轻微回退（如段落重排导致连贯性受损） |
| 5 | 无结构、连续性、逻辑、人物、时间线回退 |
| 7 | 无回退且润色增强了逻辑链或因果清晰度 |

#### `chinese_prose`（中文表达）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 翻译腔/说明腔/流程腔未修补，或润色后反而更重 |
| 3 | 减少了明显翻译腔，但仍有公式化解释残留 |
| 5 | 去掉翻译腔、说明腔和流程腔，保留初稿的句群骨架 |
| 7 | 表达自然流畅，句群有节奏变化，没有通用顺滑化 |
| 10 | 中文表达有文体性格，长短句/断裂句/省略句有意识运用 |

#### `genre_texture_density`（题材质感与密度）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 润色磨平了初稿的题材质感或场景密度 |
| 3 | 保留了基本质感但信息/感官/密度有所损失 |
| 5 | 保留并适度增强了题材质感、场景密度和对白锋利度 |
| 7 | 质感精准增强，场景颗粒服务冲突/信息/关系 |

#### `genre_scene_integrity`（类型化场面完整性）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 类型化场面修复未锁定 source anchor 或 affected span |
| 3 | 有基本路由但修复效果弱或题材味仍模糊 |
| 5 | source anchor/affected span/双轴/subtype package 全部锁定且修复到位 |
| 7 | 修复精准且不溢出，场面功能增强与人物表现有机融合 |

#### `detail_expansion`（题材化细节扩写）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 细节扩写未锁定 source anchor / affected span，或新增设定、结果、关系转折 |
| 3 | 有局部增强，但 package 选择泛化，适用焦点不清，或把无关焦点混入修补 |
| 5 | selected packages、source anchor、affected span 和 no-new-fact boundary 清楚，局部增强不越界 |
| 7 | 细节扩写精准服务当前场面功能，before/after 有明显提升且未扩大范围 |
| 10 | 命中的动作、心理、氛围或题材元素与人物选择、信息推进和追读力高度融合，改动克制但效果显著，未命中焦点处理为 N/A |

#### `anti_ai_features`（AI 腔检测 — 按五层检测清单执行）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | AI 腔坏点未被识别，只用泛化表述声称"更自然" |
| 3 | 定位了部分 AI 腔但修复不够具体，或只检测了 1-2 层 |
| 5 | 五层均有检查，至少定位了 3 层的具体坏点，修复有 before/after 证据 |
| 7 | 五层系统检查完整，检测报告详尽，修复精细且有具体坏点对照（详见 `_shared/ai-feature-detection-checklist.md`） |

#### `reader_pull`（追读力）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | 润色弱化了悬念、冲突压力或章末钩子 |
| 3 | 追读力基本保持但部分场景的牵引感减弱 |
| 5 | 悬念、冲突压力、情绪推进和章末钩子没有弱化 |
| 7 | 追读力相较初稿有可感知的提升，读者期待管理更精准 |

#### `output_state`（输出形态）

| 分数 | 锚点描述 |
| --- | --- |
| 0 | frontmatter 缺失、输出到非 canonical path、无验收包 |
| 5 | 所有输出格式正确，handoff_targets 包含 return |
| 7 | 输出规范且验收包信息充分 |

### 不合格红线（Dimension Red Lines）

以下情况直接判定对应维度 FAIL，不得进入量化评分流程：

| 维度 | 红线条件 |
| --- | --- |
| `source_anchor` | 未加载 3-初稿 源章即生成润色稿 |
| `minimal_repair` | 润色改动核心事件、人物关系、能力规则或章末牵引 |
| `regression_structure_logic` | 润色造成结构兑现或人物一致性 ≥ 2 处回退 |
| `chinese_prose` | 润色后 AI 腔比初稿更重（如全文被磨成平均短句） |
| `genre_texture_density` | 磨平了初稿中关键的题材质感或场景密度 |
| `genre_scene_integrity` | 命中类型化场面但未锁定 source anchor 或 affected span |
| `detail_expansion` | 细节扩写新增设定、结果、关系转折、能力规则、独立强化层，或把无关候选焦点当成通用必修项 |
| `anti_ai_features` | AI 腔坏点未具体定位（仅有"更自然"的泛化声明） |
| `reader_pull` | 润色后章末钩子被删除或明显弱化 |
| `output_state` | PASS 但 handoff_targets 未包含 return |
