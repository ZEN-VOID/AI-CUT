# Stage Tuning Schemes

本文件展开 `$fine-tuning` 针对 AIGC `2-美学` 到 `10-画布` 的阶段专属多轮调优方案。它只展开 `SKILL.md` 已声明的方案和验收细则，不新增入口、输出路径、完成门或 owning stage 权限。

## Shared Scheme Rules

- 每个调优对象先建立 `baseline_snapshot`，再进入候选调优。
- 默认 2 轮，最多 3 轮。第 1 轮解决保真和结构问题，第 2 轮提升质量和参考应用，第 3 轮只用于关闭明确 fail code。
- 每轮必须输出 `round_goal`、`diagnosis`、`candidate_patch`、`delta_from_baseline`、`risk`、`next_round_target`。
- 每个方案必须执行 `Comparison Acceptance Matrix`：基线、候选、阶段方案、source truth、reference principle、production feasibility 六列同时出现。
- 外部知识包含但不限于作品拉片、摄影/美术/编剧教材、论文、官方模型文档、provider 限制和网络资料；当资料可能变化或用户要求最新时，必须核验来源。

## Scheme 2 - Aesthetic Suite

Tuning objects:

- `类型风格.md`
- `画面基调/全局风格协议.md`
- `场景风格`、`角色风格`、`道具风格`、`分镜风格`、`摄影风格` 协议

Tuning directions:

- 题材类型是否真正来自 `1-分集` 全量故事源，而不是泛化标签。
- 标志性元素是否可迁移到主体、编剧、分镜和图像阶段。
- 高质量参考是否被抽象为视觉原则，而非照搬作品或空泛大师名。
- 六路风格协议是否互相支持，且不互相污染 owner 边界。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-source-fit` | 修正题材与故事源贴合度 | 对照分集故事源，标出压迫结构、核心关系、空间/物件/情绪信号，删除泛化风格词 | source anchor list、removed generic terms | 每条核心风格判断至少有 1 个故事源锚点 |
| `R2-reference-uplift` | 引入高质量审美参照 | 抽象作品/影像/美术/摄影参考为色彩、材质、构图、节奏、空间原则 | reference principle table | 参考原则可本地化，且有禁止照搬边界 |
| `R3-downstream-coherence` | 强化下游可继承性 | 检查 `Global Style Prompt`、六路协议和 downstream handoff 是否一致 | downstream inheritance matrix | `3-主体`、`4-编剧`、`6-分镜`、`9-图像` 可直接消费 |

Comparison acceptance:

- `type_style_fit >= 4/5`
- `non_generic_visual_language >= 4/5`
- `six_protocol_coherence >= 4/5`
- fatal fail: 题材标签无源锚点、参考资料照搬、全局风格与细目协议冲突。

## Scheme 3 - Subject Design

Tuning objects:

- `主体注册表.md`
- `subject-registry.yaml`
- 场景、角色、道具的清单、设计稿、生成请求和主体图证据

Tuning directions:

- 主体命名、归并和去重是否忠于故事源与 `2-美学`。
- 资产设计是否具有可视辨识度、生成可执行性和跨镜一致性。
- 角色、场景、道具三域是否互相补足而非重复解释。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-registry-fidelity` | 修正主体真源 | 对照 `1-分集`、`2-美学/类型风格.md` 和既有 registry，处理漏项、重名、错名和越权新增 | registry diff、source anchor list | 主体增删改都有 source anchor 和 owner reason |
| `R2-design-specificity` | 提升设计辨识度 | 为每个主体补足材质、轮廓、尺度、使用痕迹、功能关系、情绪/社会身份信号 | design delta table | 设计信息可视、可生成、不可被通用描述替代 |
| `R3-generation-readiness` | 强化生成可执行性 | 检查多视图、参考图、prompt atoms、负面禁区和三域一致性 | generation readiness checklist | 生成请求能被 `9-图像` 消费，不制造主体冲突 |

Comparison acceptance:

- `registry_consistency >= 4/5`
- `visual_distinctiveness >= 4/5`
- `generation_readiness >= 4/5`
- fatal fail: 分组或图像阶段新增未登记主体、角色/场景/道具命名冲突、设计稿由套句替换产生。

## Scheme 4 - Screenwriting

Tuning objects:

- `4-编剧/第N集.md`
- 声画字段、对白、独白/旁白转译、节奏、高潮、尾钩和下游 handoff

Tuning directions:

- 小说事实、事件顺序、人物关系和主体命名保真。
- 抽象叙述是否转成可拍、可听、可演的声画材料。
- 短剧节奏、高潮和尾钩是否有可感落点，而非口号式强化。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-source-fidelity` | 关闭事实和命名偏差 | 对照原文、`类型风格.md`、`主体注册表.md`，修正剧情、角色、道具和场景名 | source-to-script map | 不改变核心事件顺序和关系 |
| `R2-audiovisualization` | 提升可拍可听可演 | 把心理、抽象、评论句转为动作、声音、视线、物件和空间变化 | A/V field delta | 每个关键情绪点有可见/可听/可演材料 |
| `R3-rhythm-hook` | 强化节奏、高潮和尾钩 | 调整场景节拍、信息释放、冲突升级和尾钩画面落点 | rhythm map、hook test | 高潮和尾钩来自剧情压力，不靠新设定硬拧 |

Comparison acceptance:

- `source_fidelity >= 4/5`
- `audiovisual_actionability >= 4/5`
- `rhythm_climax_hook >= 4/5`
- fatal fail: 改写核心事实、对白不冻结、尾钩新增无源事件、主体命名与 registry 不一致。

## Scheme 5 - Director Annotation

Tuning objects:

- `5-导演/第N集.md`
- 导演批注、镜头意图、场面调度、表演空间、声音/视线/节奏组织

Tuning directions:

- 导演批注是否补充导演判断，而不是复述剧本。
- 场面调度是否基于人物目标、空间关系和声音/视线。
- 批注是否能被 `6-分镜` 消费。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-intent-clarity` | 明确每个画面点的导演意图 | 标出人物目标、冲突方向、观众注意力和情绪转折 | director intention table | 每条批注有独立导演价值 |
| `R2-staging-sound-space` | 提升调度可执行性 | 补空间位置、视线、声音、入出场、遮挡、距离和节奏组织 | staging delta map | 调度可拍，不改剧情事实 |
| `R3-storyboard-handoff` | 强化分镜继承 | 把导演意图转成分镜可消费的构图、主体、陪体、背景和节拍提示 | storyboard seed matrix | `6-分镜` 能直接承接 |

Comparison acceptance:

- `director_value_added >= 4/5`
- `staging_actionability >= 4/5`
- `storyboard_handoff_quality >= 4/5`
- fatal fail: 批注改写剧本事实、只复述原文、调度不可拍或与 `2-美学` 冲突。

## Scheme 6 - Storyboard Split

Tuning objects:

- `6-分镜/第N集.md`
- 分镜秒段、景别、景深、构图形式、主体陪体背景描述

Tuning directions:

- 分镜拆分是否承托原剧本画面点和导演意图。
- 每条分镜是否可见、可构图、可进入图像/摄影阶段。
- 秒段、景别、构图和空间连续性是否成立。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-shot-coverage` | 修正分镜覆盖和秒段 | 对照导演稿，检查缺漏、重复、秒段断裂和过密/过疏 | shot inventory、time continuity table | 画面点覆盖完整，秒段连续 |
| `R2-composition-depth` | 提升画面结构 | 优化景别、景深、构图、主体/陪体/背景关系 | composition delta table | 每条分镜具备明确视觉层次 |
| `R3-downstream-clarity` | 强化后续摄影/图像可消费 | 检查分镜是否能产生运镜、分组和图像 prompt atoms | downstream atom map | 下游无需重新猜主体和空间 |

Comparison acceptance:

- `shot_coverage >= 4/5`
- `visual_composition >= 4/5`
- `downstream_clarity >= 4/5`
- fatal fail: 改剧情/对白、秒段不连续、分镜只堆形容词、主体关系不可见。

## Scheme 7 - Camera Movement Injection

Tuning objects:

- `7-摄影/第N集.md`
- 镜头角度、镜头类型、速度曲线、焦点行为和连续性

Tuning directions:

- 运镜是否服务叙事、注意力和情绪，而不是设备词堆叠。
- 运镜是否继承 `2-美学/摄影风格` 与 `6-分镜` 画面结构。
- 焦点、速度、角度和镜头类型是否可执行。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-motivation` | 修正运镜动机 | 对每条分镜标出叙事目标、注意力目标和情绪目标，再匹配镜头行为 | motivation map | 运镜不是孤立设备动作 |
| `R2-continuity-focus` | 提升连续性和焦点叙事 | 优化焦点转移、速度曲线、角度变化、前后镜衔接 | continuity/focus delta | 运镜能接上前后分镜 |
| `R3-non-repetition` | 去除套句和重复 | 扫描重复句式、泛化运动词和不必要复杂动作，改为局部动机化表达 | repetition audit | 连续多镜不靠同一模板变化 |

Comparison acceptance:

- `camera_motivation >= 4/5`
- `continuity_focus >= 4/5`
- `non_repetition >= 4/5`
- fatal fail: 改写分镜原文、堆设备参数、焦点行为不可执行、同句式批量替换。

## Scheme 8 - Storyboard Grouping

Tuning objects:

- `8-分组/第N集.md`
- 分镜组边界、组级风格、首帧衔接、回龙帧、YAML 主体统计

Tuning directions:

- 组边界是否适合约 15 秒生产单元。
- 首帧衔接和组级风格是否帮助图像/视频阶段稳定生成。
- YAML 主体统计是否只读引用 `subject-registry.yaml`。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-boundary-production` | 修正组边界 | 对照摄影稿和时长，调整过短、过长、跨情绪/空间不当的组 | group boundary diff | 组边界生产可执行且情绪/空间完整 |
| `R2-style-first-frame` | 强化组级风格和首帧衔接 | 把全局风格整理成单行，优化入场/出场/首帧衔接 | style/first-frame delta | 图像和视频阶段能直接消费 |
| `R3-yaml-subject-check` | 校准 YAML 统计 | 对照 `subject-registry.yaml` 检查角色、场景、道具引用和缺漏 | YAML subject audit | 不新增主体，不错绑主体 |

Comparison acceptance:

- `group_boundary_quality >= 4/5`
- `first_frame_continuity >= 4/5`
- `yaml_subject_accuracy >= 4/5`
- fatal fail: 分组新增主体、组边界破坏连续性、YAML 与 registry 不一致、全局风格变成多段散文。

## Scheme 9 - Image Stage

Tuning objects:

- 分镜画面 prompt
- 分镜故事板 prompt / layout
- 分镜平面图空间描述
- 图像侧车、imagegen plan、生成结果和 provider 返回形态

Tuning directions:

- 主体、场景、道具绑定是否来自 `3-主体` 与 `8-分组`。
- prompt 是否有可见画面原子、空间关系和风格边界。
- provider 返回是否符合路线：单镜画面应是多张单独 bitmap，故事板才是拼图/contact sheet。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-binding-fidelity` | 修正主体和 source 绑定 | 对照 registry、分组稿、图像侧车，修正主体、场景、道具和分镜 ID | binding map | prompt 中每个关键主体都有 source |
| `R2-visual-atoms-layout` | 提升视觉原子和空间构图 | 优化构图、光线、材质、空间层次、动作瞬间、负面禁区 | visual atom delta | 画面可生成且不泛化 |
| `R3-provider-result-check` | 对照 provider 输出形态 | 检查实际图像、拼图误判、画幅、主体错绑和结果质量 | result comparison table | 输出形态符合叶子路线 |

Comparison acceptance:

- `subject_binding >= 4/5`
- `visual_prompt_actionability >= 4/5`
- `provider_shape_match >= 4/5`
- fatal fail: 单镜路线产出 contact sheet 被判成功、prompt 主体错绑、参考图照搬、平面图与故事板混淆。

## Scheme 10 - Canvas Stage

Tuning objects:

- `10-画布/libTV画布流/第N集/` 执行证据
- LibTV 项目空间/画布映射、素材上传、imageList、视频节点、prompt hygiene、settings、run/rerun 和 final query

Tuning directions:

- AIGC 项目名、LibTV 项目空间、单集画布和节点 ID 是否层级正确。
- imageList 顺序、主体参照和图像输入是否符合分镜组。
- 视频 prompt、节点参数和运行证据是否可复盘。

Multi-round plan:

| round | objective | actions | evidence | pass_gate |
| --- | --- | --- | --- | --- |
| `R1-layer-mapping` | 修正 LibTV 层级和 source group | 对照 `8-分组`、项目空间、画布 UUID、节点 ID，修正错绑 | layer mapping audit | projectSpaceId / folderId 与 canvas uuid 不混淆 |
| `R2-image-order-prompt` | 提升素材顺序和 prompt hygiene | 校准 imageList 顺序、主体参照、节点 prompt、settings 和视频边界 | image order diff、prompt hygiene table | 每个节点能追到 source group 和图片 |
| `R3-run-evidence` | 完整运行证据和 rerun 决策 | 检查 run id、video node instance id、final query、失败重跑原因 | run/rerun evidence log | 节点唯一、运行证据可复盘 |

Comparison acceptance:

- `libtv_layer_mapping >= 4/5`
- `image_order_prompt_hygiene >= 4/5`
- `run_evidence_completeness >= 4/5`
- fatal fail: projectSpaceId 当作画布 UUID、节点名只用分镜组 ID、素材顺序错乱、无 final query 证据却判完成。

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 每个 `2-10` 阶段是否有独立调优方案？ | 缺任一阶段方案、方案无轮次或无验收焦点即失败 | `FAIL-FT-SCHEME-DETAIL` | `references/stage-tuning-schemes.md` | scheme id list |
| 阶段方案是否只展开主 `SKILL.md` 已授权规则？ | 新增入口、输出路径、完成门或 owning stage 权限即失败 | `FAIL-FT-REFERENCE-OVERREACH` | `SKILL.md.Module Loading Matrix` | overreach row |
| 每个方案是否包含多轮调优与比对验收机制？ | 少于 2 轮、无 comparison acceptance 或无 fatal fail 即失败 | `FAIL-FT-REFERENCE-GATE` | `references/stage-tuning-schemes.md` | round table and acceptance rows |
