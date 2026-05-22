# Context: aigc 8-图像 / A-分镜画面

本文件是 `A-分镜画面` 的经验层知识库，不是执行日志。调用同目录 `SKILL.md` 时必须同时加载本文件。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 24000
hard_limit_chars: 48000
status: ok
last_checked_at: 2026-04-26
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 四段式 `分镜ID` 断链 | `6-分组` 提取层 | 回到分镜组标题、上游运镜单元和 frame landing 判断重新建索引 | 先产出 shot index，再写 prompt | `x-y-z-N` 可回指源组、`source_camera_units` 与 `frame_landing_reason` |
| prompt 变成组级摘要 | 镜级边界层 | 只保留当前 frame landing 的画面与必要桥段上下文 | 模板中固定 `source_group_id`、`source_camera_units`、`frame_landing_type` 和 `frame_landing_reason` | prompt 只描述单帧画面 |
| 英文 prompt 超过 800 English words | prompt 压缩层 | 删除重复背景、保留核心动作与主体 | 审查时统计 `integrated_prompt` 的 English word count | 每条 <= 800 English words |
| north_star 被改写为摘要 | 风格直引层 | 重新从 `north_star.yaml` 原字段复制 | step2 固定三行直引，不翻译、不润色 | 三项与源 YAML 完全一致 |
| 主体引用猜测绑定 | 参照证据层 | 删除猜测路径，只保留存在的图片文件 | 多视图优先、主图次之、无图留空 | manifest 路径全部存在 |
| imagegen 批量任务混成一个 prompt | batch 分发层 | 每个 `分镜ID` 独立任务、独立输出名 | 计划文件按 shot_id 列任务数组 | 一镜一 prompt、一镜一输出 |
| 本地参照图只写入路径但未进入对话上下文 | imagegen source semantics | 生成前逐张 `view_image` 已绑定本地图片并标注角色 | 在 handoff 与 review gate 固化 `view_image` 前置门禁 | results/report 记录 `reference_input_status: visible_in_conversation_context` |
| 同场景画面站位走位断裂 | prompt continuity layer | 当前 prompt 组织前先 `view_image` 同场景上一分镜生成图，提炼站位、朝向、遮挡、道具相对位置和镜头轴线 | 在 prompt assembly 与 review gate 固化 `previous_frame_context_status` 前置门禁 | prompt/report 记录上一图路径、可见状态、连续性约束或缺失原因 |
| 批量生成被并发化导致连续性断链 | batch execution topology | 改为按 `shot_id` 严格串行逐镜执行，当前镜完成结果记录后再进入下一镜 | 在 handoff、workflow 与 review gate 固化 `execution_order` / `serial_index` / `previous_shot_status` | plan/results 顺序连续，无并发、分片并跑或跳过前镜痕迹 |
| 批量生图边执行边补后续 prompt | prompt package topology | 先为指定范围完整生成 `第N集-分镜画面-prompts.md`、manifest、plan，再进入 imagegen | 在 workflow、handoff 与 review gate 固化 `prompt_package_status: complete_before_imagegen` | prompts 文档覆盖全部目标 `shot_id`，时间顺序先于 imagegen results |
| 空间一致性退化成平面背景复用 | 3D spatial planning layer | 建立 `space_model`，重写角色起点/终点/移动轨迹、固定锚点、对话轴线和视线闭合关系 | 在 prompt assembly、spatial contract 与 review gate 固化 `Spatial Continuity Plan` | prompt/report 能解释正反打相对背景面和角色三维站位 |
| 固定锚点选择过弱导致空间漂移 | anchor lock layer | 重新筛选主锚点和辅助锚点，优先选不移动、跨镜可推断、能定义方向的场景结构 | 固化“候选锚点 -> 主锚点 -> 辅助锚点 -> 三轴 -> 逐镜投影 -> 漂移检查”流程 | `Spatial Continuity Plan` 能说明角色/道具相对锚点关系 |
| 分组主场景锚点误套到蒙太奇或插入镜 | shot anchor projection layer | 对每个四段式分镜按当前单镜真相重投影 `Primary anchor` / `Support anchors` | 在 spatial contract、workflow、review gate 固化 `shot_anchor_projection_status` 与 `source_frame_anchor_evidence` | prompt 中的主锚点能从当前 `Source truth` 直接找到证据，而不是只来自三段式分镜组场景 |
| 只用 north_star 文字风格导致画面不像场景参照图 | scene visual style lock layer | prompt 前先 `view_image` 场景参照图，提炼光影、色调、氛围和材质，再写固定提示词 | 在 prompt assembly、workflow、review gate 固化 `scene_visual_style_lock_status` | prompt/report 记录场景图视觉风格锁，英文 prompt 含 `Match the scene reference image's visual style, lighting, color palette, and atmosphere.` |
| prompt 从人物动作摘要开始导致空间和年代漂移 | scene/frame identity layer | 先补 `scene_frame_identity`：年代/空间功能/环境声或氛围基底/材质光影、camera identity、相对方向和光线结果 | 在 prompt assembly 固化 `scene_frame_identity` 与共享 `scene-shot-identity-contract.md` | 英文 prompt 本体先锁定场景/画面/镜头身份，再写主体动作 |
| 光线只写来源，生图光影不受控 | lighting result layer | 把 left/right/top light 改成相对镜头位置 + 照亮对象 + 阴影/轮廓分离结果 | `Scene Reference Visual Style Lock.lighting_notes` 与英文 prompt 都写光线结果 | prompt 能回答光照亮哪里、阴影落在哪里、主体如何从背景分离 |
| 英文 prompt 退化为字段拼接或中文源句翻译 | prompt authorship layer | 回到单个四段式分镜和输入上下文，LLM 重写自然英文 AIGC 画面提示词，删除 `Source truth:` 中文粘贴、`focus on` 中文原文和审查字段串接 | 在 prompt assembly 固化“固定开头 + 画面构图 + 主体空间 + 主体运动 + 场景环境 + 光影氛围 + 摄影技术参数 + 视觉风格 + Avoid”，并把 integrated prompt 上限改为 800 English words | 最终英文 prompt 本体自然流畅、无中文源句残留、包含景别、只描述分镜帧开场构图状态 |
| 把上游 `分镜1/分镜2` 直接当成分镜帧 ID | frame landing extraction layer | 先判断 frame landing：开场构图、动作决定瞬间、反应帧、道具/证据插入、环境压迫帧、群像调度帧；再编号四段式 ID | 在 group source extraction 固化 `source_camera_units`、`frame_landing_type`、`frame_landing_reason`，允许一个上游分镜映射多个分镜帧或多个字段合并为一个分镜帧 | shot index 能证明最后一段编号来自 frame landing serial，而不是机械继承上游 `分镜N` |

## Repair Playbook

1. 先判断本轮是 `prompt_only`、`single_shot_generate`、`episode_batch_generate`、`shot_batch_generate`、`repair` 还是 `review_only`。
2. 任何 prompt 问题先检查 `shot index`，确认是否真的锁定到单个 frame landing，而不是机械继承上游 `分镜N`。
3. 若主体槽位缺图，先判断是设计生成阶段未产出图片，还是已有 JSON 但图片文件不存在；不得把 JSON 文件当作图片参照。
4. 对角色、场景、道具名称只做精确名与规范别名匹配；泛词如“学生”“窗户”“文具”必须谨慎，无法对应主体时留空。
5. 批量生成前先审查完整 prompt 包与 reference manifest，确认指定范围所有 `shot_id` 都已写入 prompts 文档，避免错误在批量任务中被放大。
6. imagegen 输出必须持久化到项目目录；不能只留下 `$CODEX_HOME/generated_images` 路径。
7. built-in `image_gen` 使用本地参照图时，路径记录不够；必须先 `view_image` 让图片进入对话上下文。确无绑定图片时才记录 `reference_input_status: no_reference_images_bound` 并走 text-prompt-only。
8. 新画面 prompt 组织时，若当前镜与上一镜同场景且上一镜已有生成图，先 `view_image` 上一图；没有上一图时写清 `previous_image_missing`，不要凭源稿想象上一张已生成图长什么样。
9. 批量生成不是边写 prompt 边生图的队列，而是“完整 prompts 文档前置 + 串行 imagegen”的两阶段流水；不要为了吞吐把不同 `shot_id` 拆给多个 worker，否则上一画面回看和结果回写会失去真源顺序。
10. 空间一致性先做 3D 定位，再写画面 prompt；正反打出现完全不同墙面时，不应判为场景漂移，先检查是否符合对话轴线和视线闭合。
11. 锁定固定锚点时，先列候选，再选主锚点和辅助锚点；不要直接把“教室背景”“走廊背景”当成锚点，必须落到门、窗、讲台、桌阵、楼梯口、拐角等可定位结构。
12. 三段式分镜组的场景名不能自动决定所有四段式分镜的主锚点；遇到蒙太奇、转场、道具微距、路线图、战船远景、城门飞檐建立镜头时，先用当前单镜画面重投影锚点，再把分组场景锚点作为辅助回接。
13. 场景参照图风格锁必须发生在 prompt 组织前；不要先写完 prompt 再补一句“参考场景图”。先看图，再把光影、色调、氛围、材质和暗部/高光形态转成当前镜头可执行的视觉约束。
13.1. 写英文 prompt 前先补 `scene_frame_identity`：这是什么年代/功能空间，环境和材质带来什么身份，摄影机从哪里看，人物动作相对镜头/画面如何发生。若第一句只能读出人物动作，重写开头。
13.2. 检查每个 `lighting_notes` 和英文 prompt：光线必须写出照亮对象、阴影位置和轮廓分离结果；已有场景参照图光影时，优先继承其结果，不要叠加冲突新光源。
14. 最终英文 prompt 本体不能把结构化字段顺序粘起来。先理解 `shot_id` 对应的当前分镜帧，再用自然英文重写为生成器提示词；审查字段只做证据，不直接成为 prompt 文本。必须包含景别，且作为分镜帧提示词时只锁定镜头开始的构图状态，不展开运镜全过程。
15. `6-分组` 的 `分镜1/分镜2` 是视频运镜中心，不是本阶段分镜帧真源。进入 prompt 前先判断 frame landing；一个上游分镜可拆成多个分镜帧，一个分镜帧也可合并多个上游字段。判断结果必须写入 shot index，而不是让 ID 显得像直接继承 `分镜N`。

## Reusable Heuristics

- `6-分组` 的 `## 1-1-1` 是组，不是镜；组内的 `分镜1` 是上游运镜证据，不自动对应 `1-1-1-1`。四段式最后一段来自 frame landing serial。
- `组间连接件` 默认不属于 `8-图像/A-分镜画面` 的执行对象；建立 shot index、组织 prompt、绑定参照和生图时都应忽略，避免连接件被误当成镜级连续性证据。
- 生图 prompt 允许做画面表现增量，例如构图、焦段、光比、材质、遮挡、空间压力；不允许改变谁在做什么、在哪里、关键道具是什么。
- 多视图图像比主图更适合作为 imagegen 的主体连续性参照；但只有真实图片文件存在时才算可绑定。
- 对没有图片的主体，保留文字 prompt 通常比绑定错误图片更安全。
- 整集批量时最容易出错的是复用上一镜参照槽位；每个分镜都应独立从角色、场景、道具列表重算槽位。
- 已绑定本地参照图必须在生成前通过 `view_image` 可见化；否则只能算路径证据，不能算已传入视觉参照。
- 同场景连续镜最容易出现角色瞬移或镜头轴线跳变；上一生成图是实际视觉状态，优先级高于对上一镜文字描述的想象，但不能覆盖当前 `6-分组` 的动作事实。
- 从上一图提炼连续性时，优先记录相对关系而不是绝对方位，例如“林寂在课桌左侧、面向黑板，红苹果位于桌面前缘”，这样更适合迁移到当前 prompt。
- 串行执行的关键证据不是“计划里有顺序”，而是 `imagegen-results.json` 和报告能证明每一镜在前一镜完成后才进入下一镜。
- prompt package 前置的关键证据不是“即将生成”，而是 `第N集-分镜画面-prompts.md` 已经覆盖指定范围全部目标分镜，且 `imagegen-plan.json` 的每个任务都能回指对应 prompt block。
- 背景面一致不等于空间一致；正反打中南北墙、东西墙或房间两端互为背景是正常现象，关键是角色位置、视线和对话轴线能在同一个 3D 模型中闭合。
- `Spatial Continuity Plan` 优先写固定锚点和相对关系，例如“讲台-第一排课桌-后门”构成深度轴，而不是只写“same classroom background”。
- 好锚点通常具备三个特征：不会被角色移动、跨镜头可推断、能定义方向；弱锚点如“墙面”“背景”“地面”只有在绑定到具体门窗、边线、光源或家具后才可用。
- 追逐、进出门、围站、绕物、上下楼、遮挡出现、道具交接、队列移动和同场景换机位，都是比正反打更容易暴露空间漂移的锚定场景。
- 蒙太奇和插入镜的强锚点通常不是“场景最大物”，而是“当前帧支配物”：飞檐/城门、桅杆/船帆、海图朱线、密报纸边、封蜡裂纹、刀尖、布纹针脚、油绢纤维、铜镜边、窗棂、酒葫芦停点、港口水线等。
- 风格锁定要分层：north_star 决定项目级审美边界，场景参照图决定当前场景的具体光线、色温、色调、雾气、材质和密度。两者都要进 prompt，不能用其中一个替代另一个。
- 画面身份要早于动作。年代明确的审问空间、当代私人房间、旧式居民空间即使发生同样动作，英文 prompt 的材质、光线、声音氛围和空间规则也应不同。
- 生图模型不会自动理解“左边打光”。先锁定 camera axis，再写光线从画面哪一侧进入、照亮哪部分脸/墙/地面、阴影如何落下或轮廓如何分离。
- 好的 `Integrated AIGC image prompt` 读起来应像一段成熟的英文分镜帧生图指令，而不是 source 字段、continuity 字段、anchor 字段和 negative 字段的拼接。固定开头只负责声明画幅、质量和 `Shot ID`；真正的画面判断必须落在构图、主体空间、主体运动、场景环境、光影氛围、摄影参数和全局视觉风格中。
- 分镜帧落点不是“每看到一个 `分镜N` 就生成一条”。更稳的做法是先问：这一帧是否有独立可见构图和叙事职责？如果只是运镜过程中的路径描述，合并；如果同一运镜内出现独立物证、人物反应或动作结果，拆出新的 frame landing。
