# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/04-全局预设` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 指定风格只被原样复述 | 风格转译层 | 回到 12 维模型，把风格名拆成媒介、色彩、光影、材质、构图和禁区 | `N3A-DECLARED` 固定 `declared_style_interpretation` 证据 | 不看原风格名也能执行生成方向 |
| 参考图解析像主观感想 | 视觉事实层 | 按 12 维重新观察，去掉无法从画面事实支撑的剧情臆测 | `FAIL-04-IMAGE-PARSE` 回到 `N3B-IMAGE-PARSE` | 每个维度能指出图像证据 |
| 多张参考图被简单平均 | 参考图汇流层 | 建立 `reference_merge_decision`，明确主图、辅图、反例图、权重和冲突处理 | `FAIL-04-REF-MERGE` 回到 `N3B-IMAGE-PARSE` | 多图权重、冲突和采用/剔除理由可复查 |
| 参考图主体或版权表达污染全局风格 | 迁移边界层 | 拆出 `transferable_traits` 与 `do_not_import`，只迁移底层风格语法 | reference mode 固定去污染审计 | 全局风格不复制角色身份、完整构图或受保护组合 |
| 自动解析脱离 `02` 全本剧本 | 上游真源层 | 重新读取 `output/[项目名]/02-剧本处理/`，建立 `story_style_evidence` | `N3C-STORY-AUTO` 固定读取优先级 | 风格判断可回指剧本场景、情绪、材质或视觉母题 |
| 全局风格被单个场景绑架 | 汇流抽样层 | 区分 `global_style` 与 `scene_variations`，保留局部变体但不改全局基调 | review 检查 story-wide motif 而非单点漂亮场景 | 全局预设能覆盖全本而不是只服务一场 |
| 自动解析缺全本覆盖 | 故事覆盖层 | 补 `story_coverage_map`，记录读取范围、覆盖单元、遗漏范围、dominant patterns 和 outliers | `FAIL-04-STORY-COVERAGE` 回到 `N3C-STORY-AUTO` | 全局风格来自跨单元证据 |
| 自动解析把候选主体当成资产清单 | 下游边界层 | 补 `group_candidate_map` 与 `design_subject_candidate_map`，并统一标 `candidate_from_story_source` | `N4B-COLLECTION` 检查候选状态和证据 | 候选能服务下游但不冒充清单/设计稿 |
| 缺少 300-500 字全局风格提示词 | 母稿缺失层 | 按 `north_star.yaml` 口径补 `global_style_prompt`，写成中文自然段并包含媒介属性 | `N4A-GLOBAL-PROMPT` 固定字数、媒介属性和场景化策略门禁 | 下游可直接抽取全片风格母稿 |
| 全局风格被误解为单一前缀 | 概念建模层 | 补 `global_style_collection`，包含 `group_style_set` 与 `design_subject_style_set` | `N4B-COLLECTION` 固定“并集式总集合”口径 | 分组、角色、场景、道具都有可消费风格投影 |
| 英文关键词堆砌且重复 | 关键词稳定性层 | 合并同义词，按核心媒介、色彩、光影、材质、构图、特效排序 | `keyword_dedup_evidence` 成为必填报告证据 | keywords 短而具体，模型可理解 |
| 在世艺术家姓名被当作唯一风格锚 | 权利敏感层 | 转译为视觉特征描述，除非用户明确要求保留姓名 | `living_artist_guard_result` 纳入 review | 不依赖敏感姓名也能表达风格 |
| 输出格式与参考图解析和自动解析不一致 | Schema 汇流层 | 回到统一 JSON schema，所有模式都写同构字段 | `N4C-STRUCTURE` 固定 12 维必填和 source_mode | 下游 `05/06` 只需消费一种结构 |
| 输出路径漂移到 `02` 或旧 runtime | BYKJ 路由层 | 移回 `output/[项目名]/04-全局预设/` | 父级和阶段合同都固定 BYKJ output 路径 | manifest 中 output_root 正确 |

## Repair Playbook

1. 先判断失败属于输入取证、模式判定、显式风格转译、参考图解析、故事源归纳、JSON 汇流、版权边界还是输出路径。
2. 若模式错判，优先修 `N2-MODE`；不要在错误模式内继续补字段。
3. 若参考图解析空泛，先重看画面事实，再补英文关键词；不要先堆风格热词。
4. 若参考图模式含多图，先补主图/辅图/反例图权重、冲突处理和 `do_not_import`，再写全局母稿。
5. 若自动解析缺覆盖，先补 `story_coverage_map`、`group_candidate_map`、`design_subject_candidate_map`，再归纳风格。
6. 若缺少全局风格母稿，先补 300-500 字 `global_style_prompt`，再补关键词和 JSON 字段。
7. 若全局风格只是单一前缀，补组别风格集合和设计主体风格集合；候选主体必须标明不是资产清单。
8. 若自动解析结果与故事不贴合，回到 `02` 剧本的场景、情绪、材质和视觉母题证据。
9. 若字段齐全但下游不可用，优先检查 global_style_prompt、global_style_collection、keywords、negative_keywords 和 scene_variations 的可执行性。
10. 若发生路径或多真源问题，先修输出目录和 manifest，再处理内容细节。

## Reusable Heuristics

- `04-全局预设` 的难点不是“生成一个好看的风格名”，而是让三种入口都收束到同一个可消费 JSON schema。
- `global_style_prompt` 是全局风格母稿，不是可选摘要；它应采用 `.agents/skills/aigc/0-初始化/templates/north-star.template.yaml` 的 `全局风格.全局风格提示词` 口径。
- 全局风格是并集式总集合：既要能被分组抽取为组别风格，也要能被角色、场景、道具设计主体消费。
- 参考图解析要先看画面事实，再写风格关键词；自动解析要先回指故事源，再归纳审美。
- 多图参考不是平均值；主图定总体语法，辅图补局部，反例只进入禁区。
- 自动解析不是从故事中挑最漂亮的一场，而是从全本覆盖中找反复出现的视觉母题和场景类型。
- 全局风格应能覆盖全本，局部强烈场景适合写进 `scene_variations`，不应替代 `global_style`。
- 英文关键词最有价值的顺序通常是：媒介/风格 -> 色彩 -> 光影 -> 材质 -> 构图 -> 氛围 -> 渲染/特效。
- 负面词不是垃圾桶；它应明确排除错媒介、错年代、错光影、错质感和质量缺陷。
- 对通用图像生成和分镜下游来说，具体视觉词比抽象情绪词更稳定；情绪词需要由光影、色彩、构图和材质承托。
- BYKJ 阶段输出目录优先于原 AIGC runtime；本阶段只产出 `output/[项目名]/04-全局预设/`。
