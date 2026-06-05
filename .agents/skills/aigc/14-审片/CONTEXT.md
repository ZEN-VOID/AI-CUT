# Context: aigc 14-审片

本文件是 `14-审片` 的经验层知识库。调用同目录 `SKILL.md` 时必须同时加载本文件。它不改写审片主合同，只保存实际素材审查、落盘和源层升级中的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 16000
hard_limit_chars: 32000
status: ok
last_checked_at: 2026-06-04
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 视频把单组拉成多 beat 蒙太奇 | `10-分组` 组正文过载或焦点不稳 | 把组内容改成单一可生成目标，后续 beat 留给下一组 | 审片后把“15 秒素材承载不住的多 beat”写入 `10-分组` 修复经验 | 新组正文有唯一主体、唯一镜头意图和清楚出场接口 |
| 文件名无法回推分镜组 | `13-画布` 下载命名漂移 | 重命名或在审片报告标注命名异常，先不改内容 | `13-画布` 输出合同固定 `<group_id>.mp4` / `<group_id>-a.mp4` | 审片入口能从文件名直接定位 `10-分组` |
| 单次瑕疵被误升源层 | 源层升级门过松 | 降级为 rerun-only finding | 源层升级必须多例、可复现、能定位 source owner | 报告中有重复证据和直接原因 |
| 审片报告替代分组真源 | 落盘边界错误 | 把可执行修复写回 `10-分组`，报告只留证据与决策 | landing contract 固定 report 与 canonical source 分工 | 后续 `13-画布` 不需要读审片报告才能消费修复 |
| 视频中出现近景伪字或伪字幕 | 生成素材瑕疵或上游要求书册近景 | 若文字不是剧情关键，建议 rerun；若近景不可避免，改组降低可读文字压力 | 分组正文避免让 AIGC 在近景生成可读长文 | 画面要求转为纹理、名册边缘或不可读书写 |
| prompt 清楚但视频没有执行核心动作 | `model_problem` 或单次 seed 漂移 | 标为 `rerun_only`，不要先改分组 | prompt 匹配 pass 必须记录 prompt 证据和模型未执行证据 | 报告能说明 prompt 已清楚、视频实际缺失什么 |
| prompt 本身同时要求多个主体/动作/风格 | `prompt_problem` 或分组过载 | 修 `10-分组`，降低内容密度和审美词空泛度 | prompt alignment pass 先查矛盾、过载和不可拍动作 | 新 prompt 有唯一焦点、可拍动作和明确停点 |
| 技术可用但创作平庸 | 创作质量 pass 缺失或审美目标过低 | 给 `conditional_pass` 或建议重跑，不直接当优先候选 | 审片必须区分“无硬伤”和“有创作价值” | 报告含反平庸、艺术方向和美学完整性判断 |
| 视频清晰但像正面摆拍资料图 | 摄影沉浸感层 | 判断 prompt 是否已有低角度/前景/透视/发现路径；有则 rerun-only，缺则回修 `8-摄影` 或 `10-分组`，光源/色温/空气问题回修 `9-光影` | review-dimensions 固定 `Viewer Immersion Subcheck` | 报告区分 `flat_observer_view` 与 `immersive_camera_view` |
| 用户提供好/坏示例但未转化为维度 | 示例学习链路缺失 | 提炼可观察维度后再比较，不只写“更像/不像” | 好/坏示例必须进入 `example_calibration`，稳定经验再写 CONTEXT | 报告说明靠近好示例和落入坏示例的具体点 |
| 只看 prompt / 分组文本就给审片结论 | 真实视频内容分析门缺失 | 立即补采关键帧、联系表和音频事实，先写 `observed_content_summary` 再判断 | `SKILL.md` 与证据合同固定 real video understanding gate | 报告能先说明视频里实际发生了什么，并回指证据 |
| LibTV 链接审片停留在远端节点 JSON | LibTV intake 层缺失 | 用 `libtv node` 保存远端 query，再用 `libtv download` 下载真实视频，之后抽帧审片 | LibTV 入口必须固定 `N0-LIBTV-INTAKE -> N1/N3`，远端 URL 只作生成路线证据 | 报告同时有 `libtv_input`、本地视频路径、ffprobe 和关键帧/联系表 |
| 画布名或视频名模糊导致审错节点 | LibTV target resolution 层 | 画布名必须 `libtv project list --name` 唯一命中；视频名默认只在 group_id 明确时使用 | 多命中阻断并要求 URL/project UUID/node key，不凭画面猜 | `libtv_input.projectUuid` 和 `video_node_key` 唯一 |
| 远端 prompt 被 `{{Portrait N}}` 或绑定表污染 | LibTV prompt hygiene 层 | 保存修复前 node query，修干净 prompt，final query 确认无污染后再 rerun | `GATE-REVIEW-15` 固定 prompt hygiene 和 rerun closure | 报告有 before/after query、task id、result URL、queue record |
| 顾问与复核流程启用时只本地模拟审片顾问 | 顾问请教层 | 回到项目 `team.yaml` 和共享团队顾问合同；不可用时直接使用本地流程 | `review_advisor_packet` 或本地 checklist 固定记录 node/pass/gate、角色视角和可执行指导 | packet 或本地 checklist 能回指审片节点与修复建议 |
| 顾问与复核流程的顾问只给泛泛审美评价 | 顾问问题质量层 | 回到当前 `N3-EVIDENCE` / `N4-COMPARE` / `N5-LANDING` 节点，从 evidence、judgment、gate 和 rework target 派生问题 | 顾问输出必须转成 `must_check / must_not_accept / quality_bar / rerun_or_repair_guidance` | packet 中每条采纳意见都能影响证据补强、质量门、错配归因或落点风险 |
| 审片变成固定流程打勾 | 方法选择层缺失 | 先用真实视频摘要选择 method palette，再判断 finding | `GATE-REVIEW-16` 固定 selected / skipped methods 和用户关注点覆盖 | 报告中有 `method_selection`，能解释为什么查或不查表演、摄影、声音、道具等方法 |
| finding 只写“重跑/修分组”但无法执行 | operation design 层缺失 | 每条重要 finding 写 candidate operations、chosen operation 和拒绝其他操作理由 | `GATE-REVIEW-17` 固定 operation 与 landing 分离 | 报告能说明是同 prompt 重跑、修 LibTV prompt、拆组、修资产引用、修图片顺序、修声音策略还是补证 |
| 审片包存在 `steps/` 节点展开并被 references 反复引用 | runtime spine 节点真源漂移 | 删除 `steps/` 节点载体，把 N0-N7、Mermaid、gate、fail code 和返工目标收回 `SKILL.md` | references 的 Review Gate Mapping 只回指 `SKILL.md#Thinking-Action Node Map` 与对应合同 | 模块引用中无 `steps/video-review-workflow`，`SKILL.md` 能独立说明最小审片路径 |
| 审片合同缺少量化证据数、注意力再集中、检查点或评估 prompts | Skill 2.0 最新 runtime-spine 缺槽 | 在 `SKILL.md` 补 Quantifiable Execution Criteria、Attention Concentration、Checkpoint、Evaluation Prompt Contract，并新增 `test-prompts.json` | 每次升级都同步 README、CHANGELOG 和引用检查 | `test-prompts.json` 至少 3 条，且 `SKILL.md` 包含 B10-B14 控制块 |
| 审片 verdict 像固定打分模板 | scripted verdict layer | 标记 `FAIL-REVIEW-SCRIPTED-VERDICT`，回到真实视频摘要、证据到 finding 映射和 LLM 判断 | Review Gate 固化 verdict authorship | verdict 能说明具体帧/音频/分组证据如何导致结论 |

## Repair Playbook

1. 先从文件名锁定 `group_id`，不要先凭画面猜剧情。
2. 找到 `10-分组/第N集.md` 中对应组，再看视频；否则容易把生成偏差当成剧情事实。
3. 审片描述分三层：实际画面、与分组预期差异、可执行修复。
4. 如果视频素材好但分组文档不适合 15 秒生成，优先修 `10-分组`，不是把视频判死。
5. 如果只是手、脸、伪字、运动抖动等局部生成瑕疵，通常建议 rerun，不改分组。
6. 只有当同类问题跨多个素材反复出现，且能指向 `13-画布` 命名/输出、`10-分组` 字数/桥接、`8-摄影` 可动性合同或 `9-光影` 光影可执行合同，才进入源层候选。
7. 同组变体比较时，先判断变体共同问题，再判断单变体优劣；共同问题更可能上游可修。
8. prompt 错配先归因，不要把“视频不一致”笼统写成失败；prompt 过载和模型未执行的修复路径不同。
9. 创作质量判断必须说清楚画面为什么平庸或高级，不能只用“好看”“电影感”“氛围不足”这类无证据词。
9.5. 遇到人物行走、入场、压迫、群像或空间建立视频，额外检查观众位置：正面平视全信息展示通常是 `flat_observer_view`，低角度、贴地前景、遮挡、透视、手持微晃和发现过程才更接近 `immersive_camera_view`。
10. 用户给好/坏示例时，先抽取维度，再比较目标视频；稳定可迁移的鉴赏判断才沉淀到本文件。
11. 真实视频内容分析必须先于 verdict：先描述真实画面、主体、动作、空间、节奏、关键物和音频事实，再谈 prompt 匹配、创作质量和上游修复。
12. 若本轮执行顾问与复核流程，先把 `team.yaml` 监制组相关智能顾问团作为审片监制请教；问题必须绑定当前审片节点，让顾问围绕证据缺口、prompt 归因、创作质量门、示例校准和落点越权风险给参谋，不问泛泛“好不好”。
13. LibTV 链接或画布名审片时，先把远端目标标准化为 `projectUuid + video_node_key + downloaded_video_path`；只有下载并抽帧后才进入审片判断。
14. LibTV 画布名多命中、视频节点多命中或只给画布不给视频名时，优先阻断澄清；不要为了继续流程从画布节点列表里猜一个视频。
15. 远端 node query 中的 `params.prompt`、`taskInfo` 和 `imageList/mixedList` 是 prompt 对照证据，不是视频内容证据；真实内容仍以本地视频关键帧和联系表为准。
16. 审片方法不是固定表。真实视频理解后先选方法：人物表演明显就查表演，镜头语言关键就查摄影，音轨存在就查声音，关键物/文字出现就查道具和伪影，同组多变体就查候选片比较。
17. landing 和 operation 要分开写。`group_repair` 是层级，具体操作可能是改 prompt、拆组、并组、修资产引用或修图片顺序；`rerun_only` 也要区分同 prompt 重跑和换 seed/model 重跑。
18. `SKILL.md` 是 N0-N7 节点唯一真源。引用历史步骤文档时，应改为回指 `SKILL.md#Thinking-Action Node Map` 和具体节点名，不再恢复 `steps/`。
19. 结构升级后要同时检查 `test-prompts.json`、Module Loading Matrix、Module Trigger Matrix、Review Gate Binding 和 README 目录树；少任何一项都容易让 skill 看似完整但无法回归评估。
20. 审片表格、评分项和脚本可辅助覆盖检查，但不能生成 verdict、finding、prompt 归因或 operation。字段齐全但结论像替换素材名的模板，应直接返工。

## Reusable Heuristics

- 审片不是“评价好不好看”，而是判断素材是否可作为该分镜组的 canonical candidate，以及上游该如何修。
- 好的审片 finding 必须能回答：哪里错、为什么错、改哪里、为什么不是只重跑。
- `10-分组` 是最常见修复落点，因为它直接决定单条 15 秒视频的内容密度、焦点和首尾状态。
- 源层优化要克制；单个素材的模型失败不应污染长期技能合同。
- 命名规范是审片能力的一部分。找不到 group_id，就无法稳定对照分镜组真源。
- Prompt 匹配不是简单判一致/不一致，关键是判断错配 owner：prompt 写错、prompt 过载、模型没执行、还是证据不足。
- 反平庸审片要把“技术可用”和“创作优先级”分开；没有明显崩坏的视频也可能因为库存感、无记忆点或节奏平铺而不值得选。
- 没有 `observed_content_summary` 的审片报告不合格；关键帧和联系表只是证据载体，必须由 LLM 把它们转化为对真实视频内容的理解分析。
- 顾问与复核流程下，顾问是审片参谋，不是最终裁判；主 agent 必须用真实视频证据和本技能合同裁决 verdict、landing 和写回范围。
- `libtv download` 是 LibTV 审片入口的分水岭：下载前只能做目标解析和生成路线核验，下载后才允许做视频本体、prompt 匹配和创作质量 verdict。
- 重新提交不是审片的默认动作；只有用户明确要求或 landing 合同授权时，才在 prompt hygiene 通过后执行 `libtv node --run` 并写 task/final query 证据。
- 固定流程只负责自动化，不负责替代判断。高质量审片要能解释“为什么这条视频需要查这些点”，并能把结论落到具体操作。
- 对审片类 Skill 2.0 包，最容易漂移的是“证据流程”和“判断流程”分裂；保持 `N3` 真实视频理解、`N4` 方法选择、`N5` operation 设计在 `SKILL.md` 同一条注意力路径里，比维护独立 steps 文档更稳。
- 审片的“形式完整”经常掩盖模板化判断；真正可用的 verdict 必须把至少一个可回指视频证据、分组预期和 chosen operation 连起来。

## Aesthetic Calibration Heuristics

- 从用户好/坏示例对比中学习时，必须转写为可观察条件、质量判断、修复动作和适用范围；项目专属口味写项目 `MEMORY.md`，跨项目可复用鉴赏经验才写入本节。
