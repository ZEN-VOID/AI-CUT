# Review Dimensions Contract

本合同定义 `8-审片` 的核心审片维度。所有判断必须基于真实视频证据、prompt / 分镜组证据或用户提供的示例证据，避免空泛审美口号。

## Dimension 1: Video Intrinsic Problems

审查视频本身是否可用，即使暂时不看 prompt 也要先判断素材是否存在硬伤。

| sub_dimension | checks | typical landing |
| --- | --- | --- |
| `basic_waste` | 明显变形、扭曲、主体崩坏、画面破碎、黑屏、冻结、严重闪烁、编码损坏 | `rerun_only` 或阻断 |
| `logic_reasonability` | 空间关系、动作因果、物理运动、角色动机、镜头连续性是否合理 | `group_repair` / `rerun_only` |
| `consistency` | 角色身份、服装、道具、场景、光线、镜头方向、首尾状态是否稳定 | `group_repair` / `source_escalation` |
| `common_aigc_artifacts` | 手脸崩坏、肢体多余、伪文字、主体漂移、物体融化、遮挡穿帮、时间抖动、无意义镜头运动 | 多数为 `rerun_only`，重复出现才上游排查 |

## Dimension 2: Prompt Alignment

审查视频是否与用户 prompt、`4-分组` 真源和 `7-视频` 生成证据一致。

| verdict | meaning | required action |
| --- | --- | --- |
| `matched` | 核心主体、动作、空间、风格和约束均基本执行 | 继续创作质量判断 |
| `partially_matched` | 核心目标实现，但关键约束或局部信息缺失 | 记录 finding，判断是否 rerun 或改 prompt |
| `mismatched` | 主体、事件、场景、风格或禁止项明显错配 | 阻断使用，做错配归因 |
| `not_enough_prompt_evidence` | prompt / 分组证据不足以判断 | 降级为 `review_only`，说明缺口 |

### Mismatch Attribution

不一致时必须区分原因：

| owner | use when | repair route |
| --- | --- | --- |
| `prompt_problem` | prompt 缺关键信息、互相矛盾、单条塞入太多 beat、动作不可拍、审美词空泛、负面约束不清 | 修 `4-分组` 或 `7-视频` prompt 组装 |
| `model_problem` | prompt 清楚、可执行，但视频未遵循；或是手部、文字、物理、身份漂移等常见生成失败 | `rerun_only`，必要时换路线或模型参数 |
| `evidence_gap` | 缺少 prompt、manifest、关键帧或对应分组，无法可靠归因 | `review_only` |
| `mixed_cause` | prompt 过载放大了模型弱点，或 prompt 清楚但模型多次稳定失败 | 报告中拆分直接修复和源层候选 |

## Dimension 3: Creative Quality

审片必须能判断“能不能用”，也要判断“值不值得用”。创作质量判断不是主观喜恶，而是基于可观察的画面、节奏和叙事效果。

| sub_dimension | anti-banal question | weak signal | strong signal |
| --- | --- | --- | --- |
| `anti_banal` | 画面是否只是泛化、模板化、库存感的漂亮片段 | 通用氛围、无明确叙事功能、没有记忆点 | 一个清晰独特的视觉动作、情绪转折或信息推进 |
| `art_direction` | 美术、服装、场景、材质是否服务项目世界观 | 好看但脱离人物/时代/场景 | 视觉选择能强化角色关系、场景压力和主题 |
| `cinematography` | 构图、镜头运动、景别和光线是否有效 | 漂浮运镜、无目的推拉、主体不稳 | 镜头调度让信息更清楚、情绪更强 |
| `rhythm` | 15 秒内的节奏是否有可感知结构 | 平铺、堆叠、乱切、没有停点 | 起承停点清楚，首尾状态可接下一组 |
| `aesthetic_integrity` | 风格是否统一且有辨识度 | 滤镜感、廉价质感、色彩互相打架 | 色彩、光影、材质、表演同向服务同一表达 |

## Verdict Rule

最终 verdict 必须综合三层：

1. 视频本体是否可用。
2. 视频是否匹配 prompt / 分镜组。
3. 视频作为创作素材是否有足够质量。

任一层出现阻断级问题，不能给 `pass`。创作质量弱但无硬伤时，可给 `conditional_pass`，并说明是“可用但不优先选用”还是“需要更高审美目标重跑”。
