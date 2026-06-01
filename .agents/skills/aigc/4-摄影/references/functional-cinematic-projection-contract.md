# Functional Cinematic Projection Contract

本文件定义 `4-摄影` 的功能性底线：`分镜画面` 不是好看的镜头句子，也不是随机摄影术语拼接；它必须把上游画面句子转化为下游 `5-分组`、`7-图像`、`8-视频` 可消费的影视事实，尤其要给出可执行的运镜策略。

## Example Usage Guard

本文件中所有示例、字段样句和反模式仅用于说明功能投影、非复述性和 payload 完整度的判断方法，不是分镜正文模板。执行具体任务时，不得复用示例中的主体、动作、字段组合或句式；必须从当前画面句子的真实观看任务、下游消费需求和 `shot_design_plan` 重新生成。

## Core Rule

每个 `时间段` 必须先回答“这一时间段在影视上解决什么问题”，再回答“摄影机为什么这样动、怎么动、何时停、停多久、如何交接”，最后回答“它如何被图像/视频工具执行”。若一条分镜删掉后不影响主体、动作、信息、空间、情绪、节奏、时值、连续性、运镜策略或下游生成锚点，它就是伪分镜，必须删除或重写。

每个 `时间段` 还必须回答“它服务哪条上游画面句子”。段落级连续运镜、视觉母题或材质链只能作为当前镜头的进入点、落点、交出锚点或光色继承，不能让镜头失去逐画面点归属。

### Content Paraphrase Is Not Shot Detail

`分镜画面` 不是把正上方画面句子拆成镜头 1/2/3，也不是把原句名词替换成“中景/特写/镜头跟着”。每条 `时间段` 必须通过源句复述扣除测试：去掉上游原句已有的主体名词、动作结果和道具事实后，剩余文本仍能读出摄影机如何看、如何动或为什么不动、在哪里停、焦点/构图/光影如何组织、如何交给下一注意力点。

若一条分镜只是在复述“谁做了什么、物件是什么、画面里有什么”，即使加上景别词，也不合格。合格分镜必须至少新增一个真实摄影决策：机位/景别/视角、运镜路径与速度、停点与时值、焦点/景深、构图锚点、光线结果、方向参照、表演微动态或连续性交接；这些选择必须改变观众观看方式，而不是给原句贴摄影术语。

## Rule Stack Projection

`4-摄影` 的种种细则不是可选装饰，而是同一条分镜的决策栈。每个 `时间段` 必须能回指下列至少一组有效来源：

| source layer | must influence |
| --- | --- |
| `visual-matching-contract.md` | 该时间段处理哪条可见信息，而不是凭空新增画面 |
| `visual-sequence-alignment-contract.md` | 该时间段如何在段落连续性中保持当前画面点归属，避免跨块外溢 |
| `beat-analysis-contract.md` | 为什么这里需要切分或维持同一时间段 |
| `visual-rhythm-analysis-contract.md` | 该时间段应收敛、标准展开、发散强化还是断裂 |
| `shot-duration-decision-contract.md` | 该时间段应快速通过、标准承接、读秒停留还是长停顿，以及为什么 |
| `peak-shot-language-contract.md` | 若是高点，如何用时间段密度、停顿、读秒、反应或余波强化 |
| `shot-continuity-contract.md` | 从上一注意力落点、轴线、运动方向或光色如何进入 |
| `transition-design-contract.md` | 若发生场景变化或其他边界风险，如何记录交出点、进入提示和连续性风险 |
| `cinematic-technique-library.md` | 选择哪种最小充分的摄影技法，而不是随机术语 |
| `ai-video-prompt-execution-contract.md` | 让镜头先行包裹动作，补方向参照、光线结果和表演微动态，保证下游视频提示词稳定 |
| `dynamic-lens-language-contract.md` | 运镜的起点、路径、速度变化、停点和交接 |
| `natural-shot-detail-writing-contract.md` | 如何把上述决策写成自然但不丢功能 payload 的中文 |

## Functional Payload

每个 `时间段` 必须能从正文中抽取以下 payload。它们不需要以字段形式显式输出，但必须能被读者和下游技能稳定还原：

| payload | required meaning |
| --- | --- |
| `shot_function` | 建立空间、执行动作、显影信息、承托表演、制造危险、完成反应、转场交接、强化高点中的一种或组合 |
| `visible_subject` | 当前画面真正可见的主主体；可以是人物、群体、道具、文字、门窗、光源或危险源 |
| `action_phase` | 预备、执行、结果、反应、停顿、显影、进入、退出、转交中的明确相位 |
| `camera_movement_plan` | 运镜方式、运动方向、速度曲线、停点、焦点/景别变化和交接接口；静止镜头也必须说明“为什么不动” |
| `shot_duration_decision` | 时值等级、内部估算范围、正文显示秒数和时值理由；必须以 `[起始秒-结束秒]` 显式落盘，并能从运动速度、停点和可读性反推 |
| `dialogue_time_budget` | 当前时间段是否承载对白、旁白、画外音或听者反应；如命中，时间范围必须满足台词量下限或说明跨段延续 |
| `camera_plan` | 机位/景别/景深/镜头类型中最影响该镜功能的选择，并与 `camera_movement_plan` 配合 |
| `composition_anchor` | 画面构图的稳定锚点：前景遮挡、门框、课桌行列、黑板、手、眼、道具、文字、光斑等 |
| `light_color_material` | 可被图像和视频工具继承的光线、颜色、材质或视觉母题 |
| `continuity_handoff` | 从上一段如何进入，或把注意力交给下一段/下一画面的哪个可见接口；场景变化时必须能还原上一画面交出点和下一画面进入点 |
| `unit_ownership` | 当前时间段归属的上游画面句子，以及没有提前吞入后文动作、对白反应、记忆段或道具揭示的证据 |
| `ai_video_prompt_execution` | 镜头是否从起点包裹动作、人物/镜头运动是否有相对画面或摄像机的方向参照、光线是否写成可见结果、情绪是否落到表演微动态；不要求显式字段落盘，但必须能从正文稳定还原 |

## Gradient Shot Detail Sufficiency

分镜画面完整性采用梯度模型，而不是要求每条 `[起始秒-结束秒]` 都完整展开全部维度。15 项是维度池，不是逐段字段清单；每段应按画面任务、信息重要性、动作复杂度、情绪强度、段落位置和下游生成风险选择足够维度。

总原则：分镜画面规则服务创作质量，不服务分镜堆砌。分镜增加、描述加密或镜头复杂化的唯一理由，是产生新的观看结果、动作相位、信息揭示、情绪压力、空间关系、时值必要性或下游执行稳定性。删掉无损失的镜头必须删并或重写。

| grade | trigger | required sufficiency |
| --- | --- | --- |
| `L0-basic` | 低信息过场、简单动作、空间承接、恢复槽位 | 归属、镜头功能、起点/路径/落点、时值、交接、非复述；低信息镜头可以短，但必须能看出摄影机如何看和如何收住 |
| `L1-standard` | 常规动作、普通环境、一般关系变化、标准展开槽位 | 在 L0 上增加可见主体、动作相位、构图锚点、光线结果、方向参照；能指导生图和视频基本执行 |
| `L2-emphasis` | 规则显影、重要道具、对白潜台词、人物反应、空间重置、关键揭示 | 在 L1 上增加焦点/景深策略、表演微动态、注意力路径、上下镜连贯；能承托表演、读秒、信息显影或关系变化 |
| `L3-peak` | 高潮、惊吓、认知反转、强情绪、set-piece、连续声画打点 | 在 L2 上增加节奏停顿/爆发理由、反应余波、过渡锚点、AI 视频稳定性证明；每段必须有独立结果或不可删理由 |

### Gradient Decision Inputs

梯度由以下输入共同决定，不由“想写得更高级”决定：

1. `information_importance`：是否有新信息、规则、危险、关系变化。
2. `action_complexity`：单一动作、动作分相、碰撞、追逐、多人调度或 set-piece。
3. `emotional_intensity`：普通反应、压抑停顿、崩溃、醒悟、惊吓。
4. `downstream_risk`：AI 视频是否容易断姿态、错方向、跳轴、光线漂移或表演不可见。
5. `sequence_position`：铺垫、加速、峰值、恢复、交出。
6. `readability_need`：是否承载对白、旁白、文字、道具、微表情或规则可读性。

### Sufficiency Dimension Pool

成稿不输出下列字段标签，但按梯度需要从正文中稳定反推出相应信息：

| item | requirement |
| --- | --- |
| `unit_ownership` | 这条时间段服务哪一句上游画面句子，且未提前吞入后文动作、对白反应、记忆段或道具揭示 |
| `shot_function` | 这一时间段解决的影视任务：建立空间、执行动作、揭示信息、承托表演、制造危险、完成反应、强化高点或交出下一段 |
| `entry` | 镜头从哪个景别、机位、焦点、空间位置、声音、动作或光色接口进入 |
| `visible_subject` | 当前真正可见的主主体或主注意力点 |
| `action_phase` | 当前时间段处于预备、执行、结果、反应、停顿、显影、进入、退出或转交中的哪一相位 |
| `camera_path` | 摄影机如何运动或为什么静止；方向、速度曲线、停点、焦点/景别变化必须可读 |
| `attention_anchor` | 观众注意力被哪个构图锚点锁住，如前景遮挡、门框、桌线、手、眼、文字、光斑、阴影边界 |
| `camera_grammar` | 景别、视角、景深、焦点、镜头类型或构图选择中至少一项真实服务当前节拍 |
| `lighting_result` | 光线造成的可见结果：照亮、遮蔽、反光、压暗、轮廓分离、阴影边界或背景层次 |
| `duration_reason` | `[起始秒-结束秒]` 与镜头语言、对白量、可读性、停顿或压缩理由一致；非 `slow_burn/hold` 的 3 秒以上时间段必须有必要性证据，情绪类 `slow_burn/hold` 必须有可见微动态、静止压力、极慢运动或框内变化 |
| `performance_microdynamic` | 情绪落成呼吸、视线、咬肌、眉心、手指、肩膀、喉结、步伐、身体重心等可见物理动作 |
| `exit_and_handoff` | 镜头最后停在哪里，如何收住或交给下一段/下一画面 |
| `direction_reference` | 人物/镜头运动相对摄像机或画面边界明确，如朝镜头、远离镜头、从画面左侧进入、停在右侧三分之一 |
| `prop_admission` | 道具、反射、倒影、涟漪、桌面、纸张、杯子等只有在互动、关键信息、规则/证据/危险源或必要环境交代时成为焦点 |
| `non_paraphrase` | 删除源句已有主体、动作、道具和事实后，仍能读出机位、路径、速度、停点、焦点、构图、光线结果或交接方式 |

### Anti-Piling Rule

低信息时间段可以短，甚至只用一段；高信息时间段可以加密，但每一段都必须带来新观看价值。不得为了满足维度池而把 L0/L1 画面写成 L3，也不得把“完整性”理解为术语堆叠、参数清单或固定多段模板。合格的短时间段仍应保留当前梯度所需的关键组合；否则它只是画面内容复述。

## Downstream Consumability

面向后续 AIGC 生图和视频，`分镜画面` 必须具备：

- **图像可画性**：能生成单帧画面。必须包含清楚主体、姿态/动作、构图锚点、环境关系、光色或材质落点。
- **运镜可执行性**：能指导视频镜头。必须包含运镜方式、运动方向、速度感、焦点/景别变化、停点、动作相位或转场接口；固定机位也要体现框内运动和停住的理由。
- **视频可动性**：能生成连续镜头。必须让下游知道镜头如何开始、如何移动或保持、何时停、`[起始秒-结束秒]` 对应的停留依据、需要快速通过还是读秒停留、焦点转到哪里、如何接下一段。
- **视频提示词可改写性**：能按“镜头与构图 -> 人物与动作 -> 情绪可见细节 -> 光线结果 -> 环境承托”的顺序稳定改写为提示词；动作不先于镜头孤立发生，方向不含混，光线不只停留在光源名或效果词。
- **分组可切性**：能让 `5-分组` 判断该时间段是否和前后画面同组；不得把空间、主体和动作写得漂浮。
- **逐点可回指性**：能让 `5-分组`、`7-图像`、`8-视频` 判断当前时间段来自哪一条上游画面句子；不得把多个上游点熔成不可拆的长镜。
- **连续性可追踪**：能让 `7-图像` 和 `8-视频` 继承上一段的主体、空间轴线、光色母题和注意力落点。
- **边界交出可执行性**：场景变化、空间重置或高点余波必须让下游知道上一画面从哪个声音、动作、光色、文字、空间出口或反应交出，并给出下一画面可能的进入提示；不在本阶段写连接方案。

## Professional Cinematic Function

专业影视化不是术语密度，而是每个选择都有功能：

| weak/random | functional |
| --- | --- |
| `镜头慢慢推进，氛围更紧张。` | `镜头贴着课桌边缘慢推，路径被桌角切成窄线，最后停在他握紧的手；紧张来自手指发白和脸被空间切开。` |
| `使用高级转场衔接下一镜。` | `教鞭敲桌的声音先进入下一画面，切点落在黑板粉笔灰震落的一瞬。` |
| `低角度展现压迫感。` | `讲台从画面下沿压上来，黑板字悬在学生头顶，老师只露出拿教鞭的手。` |
| `特写规则文字，突出重要信息。` | `粉笔字占满画面左半边，右侧虚着林寂的眼睛；焦点从字尾慢慢拉到他瞳孔里的反光。` |

## Rejection Rules

以下情况必须判为功能性失败：

- 只是把上游画面句子拆成动作前后顺序、人物/物件特写或“先看 A 再看 B”，没有新增摄影机如何看、如何动、何时停、焦点如何转、光影如何组织或如何交接。
- 把原句名词和动作结果替换成“中景/特写/跟拍/推进”等术语后，仍无法抽取 `camera_movement_plan / composition_anchor / light_color_material / continuity_handoff`。
- 只是在表达上顺、句式好看，但不能抽取主体、动作、构图锚点、光色、运镜方式、速度曲线和停点。
- 分镜能抽取动作和构图，但无法判断该时间段应快速通过、标准承接、读秒停留还是长停顿。
- 分镜缺少 `[起始秒-结束秒]`，或时间范围与镜头语言/对白量不一致。
- 分镜之间没有新的观看策略，只是重复同一个状态的不同说法。
- 分镜作为段落读起来顺，但当前时间段无法回指正上方画面句子。
- 当前块提前包含后文画面点的主体动作、对白反应、记忆段、道具揭示或完整转场方案。
- 摄影术语与当前剧情功能无关，例如普通对话硬加复杂环绕、低信息动作硬加创意连接方案。
- 场景变化没有交出点和进入点，或只写“转场到下一场”但下游无法判断画面如何衔接。
- 下游图像阶段无法判断该画面该画谁、站哪里、看什么、光从哪里来。
- 下游视频阶段无法判断摄影机怎么动、为什么这样动、何时停、停多久、焦点转到哪里、如何接下一段。
- 只写“运动感”“镜头流动”“丝滑推进”，没有具体运镜路径、速度变化、停点或交接接口。
- 分镜正文无法稳定改写为 AI 视频提示词：镜头是动作后的补丁，人物运动缺少相对镜头/画面的方向参照，光线只写“侧光/顶光/电影感”，或情绪只写抽象词而没有微表情、身体联动、呼吸、手部或视线变化。

## Repair Rule

修复顺序固定为：

1. 先回到上游画面句子，锁定当前镜头必须解决的剧情/信息/动作功能。
2. 对候选时间段做源句复述扣除测试：删除上游原句已有名词、动作和事实后，若只剩景别词或空泛效果词，直接判为伪分镜。
3. 抽取并补齐 `visible_subject / action_phase / camera_movement_plan / shot_duration_decision / composition_anchor / light_color_material / continuity_handoff / unit_ownership / ai_video_prompt_execution`。
4. 按 Rule Stack Projection 回查节拍、节奏、镜头时值、峰值、连续性、技法库和动态运镜细则，重新选择最小充分的摄影与运镜策略。
5. 最后才进入 `natural-shot-detail-writing-contract.md`，把功能 payload 写成自然中文。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does each `时间段` solve a real film function, and would deleting it lose information, relation, action result, emotional pressure, viewing discovery, rhythm, duration, continuity or downstream anchor? | `GATE-CINE-28` / `GATE-CINE-15` | `FAIL-CINE-05W` / `FAIL-CINE-05H` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `shot_narrative_function`, delete-loss checks and kept/deleted shot samples |
| Can every shot be traced to its owning upstream `visual_unit`, without absorbing later action, dialogue reaction, memory insert, prop reveal or full transition solution? | `GATE-CINE-04D` | `FAIL-CINE-05M` | `references/visual-sequence-alignment-contract.md` / `steps/cinematography-workflow.md#N3.5-SEQUENCE-ALIGN` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `unit_ownership` / `unit_ownership_map` evidence and forbidden-bleed repairs |
| Does each shot pass the source paraphrase subtraction test, leaving real camera decisions after source nouns, actions and facts are removed? | `GATE-CINE-15B` | `FAIL-CINE-05R` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N7-INJECT` | paraphrase-subtraction samples and before/after repaired lines |
| Can the final wording expose functional payload such as subject, action phase, movement plan, duration, camera plan, composition anchor, light/material, continuity handoff and AI video execution? | `GATE-CINE-15` | `FAIL-CINE-05H` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | payload extraction samples and missing-payload repairs |
| Does the shot use L0/L1/L2/L3 gradient sufficiency according to information, action, emotion, downstream risk, sequence position and readability, instead of overfilling or underwriting? | `GATE-CINE-15C` | `FAIL-CINE-05AA` | `references/functional-cinematic-projection-contract.md#Gradient-Shot-Detail-Sufficiency` / `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | gradient samples and low/high information sufficiency decisions |
| Are dimension-pool details included only when they naturally exist in the current visual unit, and folded into natural language rather than labels? | `GATE-CINE-23` | `FAIL-CINE-05Q` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N7-INJECT` | `dimension_coverage` evidence and naturalized dimension rewrites |
| Does the shot remain consumable by image, grouping and video stages, including clear visible subject, pose/action, composition, light/material, movement, duration and continuity? | `GATE-CINE-15` / `GATE-CINE-15A` | `FAIL-CINE-05H` / `FAIL-CINE-05N` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | downstream payload extraction and AI video prompt execution checks |
| Are props, reflections, ripples, table objects, paper edges or other objects admitted only for interaction, key information, rule/evidence/danger or necessary environment? | `GATE-CINE-24` | `FAIL-CINE-05S` | `references/visual-matching-contract.md#Prop-Admission-Overlay` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `prop_admission` samples and deleted/de-emphasized object shots |
| Does every displayed `[start-end秒]` time range match movement, readability, dialogue/voiceover budget, pause or compression reason? | `GATE-CINE-04B` / `GATE-CINE-04C` | `FAIL-CINE-03B` / `FAIL-CINE-03C` / `FAIL-CINE-05L` | `steps/cinematography-workflow.md#N5.2-DURATION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `shot_duration_decision`, dialogue budget and long/short shot samples |
| Are examples and field samples used only to demonstrate judgment, not copied as shot prose or payload templates? | `GATE-CINE-17A` / `GATE-CINE-18` | `FAIL-CINE-05REF` / `FAIL-CINE-05G` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N7-INJECT` | reference non-template statement and template-pollution repair evidence |
