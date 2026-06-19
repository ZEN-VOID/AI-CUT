# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-编剧` 的经验层知识库，不是第二份主合同。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件只沉淀可复用判断经验、失败模式和修复打法；不改写 `SKILL.md` 的输入、输出、gate 或模块授权。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-06-16
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 剧本像小说复述 | 小说转译层 | 回 `N3`，把陈述拆成画面、动作、对白、独白、声音或道具证据 | `narration_to_voice_adaptation_map` 必须留证 | 删除旁白后观众仍能理解关键行动 |
| 未指定模式时误用解说剧 | 模式路由层 | 回 `N1`，确认 `screenplay_mode_decision.default_applied=true` 且 `screenplay_mode=zhengju` | `GATE-SCR-25` 阻断无显式信号却使用 `jieshuoju` | Source Manifest 和 frontmatter 均写 `screenplay_mode: zhengju` |
| 显式解说剧仍把陈述性 source 改成角色对白/独白 | 模式字段投影层 | 回 `N3/N6`，把陈述性 source 全部改为 `旁白（叙述者/指定主体）` + `旁白画面`，上游已有对白才保留对白字段 | `narration_to_voice_adaptation_map.mode_policy=jieshuoju_narration_only` 必须覆盖陈述性 source anchor | `GATE-SCR-25` 通过，且每条陈述性旁白都有就近 `旁白画面` |
| 解说剧没有先做 source 单元类型化 | 模式覆盖证据层 | 回 `N3`，建立 `jieshuoju_source_unit_coverage_map`，先判定 `source_unit_type` 再落字段 | `GATE-SCR-25` 要求 coverage map 覆盖 source 单元，不能只看旁白数量 | 每个 source 单元都有 `landing_policy`、`fidelity_operation` 和 `coverage_status` |
| 解说剧把可见动作/环境也重复旁白化 | 模式字段投影层 | 回 `N3/N6`，将 `visible_action`、`environment_state` 落回正式画面字段，只让陈述性解释进旁白 | `source_unit_type` 区分可见材料与陈述性材料 | coverage map 中 `visible_action/environment_state` 不是 `narration_pair` |
| 解说剧用概要替代完整 source | 保真覆盖层 | 回 `N3`，把 `summary/fact_drop/cause_reorder` 修成 `verbatim/sentence_split/light_oralization/pronoun_resolution/visual_split` | `risk_check` 中 summary/fact_drop/cause_reorder 必须为 false | source 单元顺序、事实和因果能拼回原 source |
| 解说剧退化成连续旁白清单或方括号小标题 | 字段节奏层 | 回 `N3/N6`，删除 `【开场定调】` 等方括号叙事小标题，把段落功能移入 `jieshuoju_field_variety_map`，并用环境/动作/道具/群像/系统/转场字段打断连续旁白 | `GATE-SCR-25` 和 `FAIL-SCR-JIESHUOJU-FIELD-MONOTONY` 阻断字段单调 | `max_narration_pair_run<=3` 或有 montage 例外；正文无 `【...】` 叙事小标题 |
| 节奏只有“快、爽、燃” | 节奏承托层 | 回 `N4`，为每个节奏机制补 source anchor 和承托字段 | 节奏机制必须绑定题材/叙事画像 | 任一节奏点都能在正文找到字段 |
| 高潮变成新增剧情结果 | 保真与高潮层 | 回 `N5`，只强化上游已有高点的声画和行动落点 | `climax_treatment_map` 区分 source fact 与 treatment | 高潮删去强化后，上游结果仍不变 |
| 尾钩只是抽象悬念 | 集末落点层 | 回 `N5`，改成最后可见/可听/可感受的小落点 | 尾钩必须记录 hook_type 和下一集未闭合问题 | 观众能说出“最后看到/听到/感到什么” |
| 声画同步写成分离清单或旧式锚点标题 | 字段投影层 | 回 `N6`，删除 `【声画同步锚点】`，把声音字段就近配对为 `对白画面/独白画面/内心独白画面/旁白画面/音效画面` | `audio_visual_pairing_map` 是正文内嵌证据，不只在报告里 | 正文中每条声音出现时，下一条或相邻字段有对应画面承托 |
| 长对白/旁白/独白共用一个泛化画面 | 长声音字段节拍层 | 回 `N6`，按 `§10.3 Long Voice Field Beat Segmentation` 把长声音字段拆成多个节拍，每个节拍配独立画面承托，每 2-3 节拍插入非说话者信息 | `long_voice_beat_map` 必须进入执行报告；80字以上声音字段不得共用泛化画面 | 每个节拍的 `*画面` 反映该节拍内容，不是同一泛化承托 |
| 同一画面被相邻字段重复表述 | 字段连续性层 | 回 `N6`，把同一时刻/同一主体/同一动作链的画面字段合并，或写明主体、空间、时间、信息变化的分界条件 | 正式写回必须留 `same_frame_continuity_map` | 下游按字段分组时不会把同一可见承托拍成两个画面 |
| 剧本画面化被误写成比喻或概念 | 白描式字段层 | 回 `N6` 并加载 `../_shared/anti-abstract-language-contract.md`，把“像/仿佛/宿命感/灵魂碎裂/压迫感拉满”等替换为主体、动作、空间、道具、声音、光照、身体状态或时间变化 | `plain_visualization_audit` 进入报告证据；删掉比喻/概念后字段仍可拍、可听、可演 |
| 剧本像模板套壳或同义改写批量稿 | 源层主创缺失层 | 废弃候选稿，回 `N6` 基于本集 source、题材画像、节奏证据和声画字段重新 LLM 主创，不做表层润色 | `GATE-SCR-19` 独立阻断脚本、映射表、规则模板、关键词锚点替换、句式轮换和同义改写 | `anti_scripted_draft_audit` 无重复句式和锚点替换风险 |
| 编剧跳过 `类型风格.md` 或只复述题材标签 | 阶段顺序与类型风格继承层 | 回 `N1/N2`，加载 `2-美学/类型风格.md`，把主题材、标志性元素和题材专属表现技巧投影到本集节奏、高潮、尾钩和声画策略 | `Type Style Application Map` 必须进入执行报告；正式主链缺 `类型风格.md` 不得 pass | `type_style_application_map` 能说明每条继承规则如何影响本集局部剧本决策 |
| 编剧跳过 `3-主体/主体注册表.md` 或自行改名角色/场景/道具 | 主体命名真源继承层 | 回 `N1/N2`，加载 `3-主体/主体注册表.md`，把角色、场景、道具 canonical name 投影到本集剧本命名 | `Subject Registry Application Map` 必须进入执行报告；正式主链缺主体注册表不得 pass | `subject_registry_application_map` 能说明剧本主体命名如何对齐注册表 |
| 编剧只读取 `3-主体/主体注册表.md`，但项目已有 `场景/2-设计` 或 `场景/3-生成` 时没有匹配场景设计/场景图 | 场景资产上下文继承层 | 回 `N1/N2/N3`，建立 `scene_asset_context_manifest` 和 `Scene Asset Integration Map`；只读映射到场景标题、环境白描、连续性和 handoff | `GATE-SCR-24` 阻断“已存在场景资产但未映射/被当作剧情真源/prompt/镜头”的情况 | `scene_asset_integration_map` 有 used_for、script_landing、boundary_check 或 N/A |
| 编剧读取了 `1-分集`、`2-美学`、`3-主体` 和项目上下文，但没有说明这些上下文如何引导创作方向 | 上游方向矩阵缺失层 | 回 `N1/N2`，把每类上游上下文拆成剧情真源、题材方向、主体命名、长期约束或 side context，并写成 `upstream_creative_direction_matrix` | `GATE-SCR-23` 阻断只列“已读取/已参考”；执行报告必须给出 direction_role、used_as、script_decision、script_landing 和 boundary_check | `upstream_creative_direction_matrix` 能证明上游如何影响节奏、声画、主体命名、高潮和尾钩，且没有越权覆盖 source 或注册表 |
| 误把 imported director 规则当导演稿 | 模块边界层 | 回 `Imported Reference Adaptation Contract`，只保留承托，不写导演/表演/镜头 | `GATE-SCR-14` 阻断下游越权 | 正文无机位、景别、运镜、prompt |
| 报告只写“已参考”但无执行证据 | 报告证据层 | 回 `N8`，补 `Execution Decision Trace`、`Reference Execution Matrix`、`Rule Evidence Map`、`N/A Justification`、`Repair Log` | `GATE-SCR-16` 把缺失证据列为阻断项 | 每份触发 reference 都有 applied_to/evidence_in_output 或 n/a_reason |

## Repair Playbook

1. 先锁 source、集号、输出路径和改写授权。
2. 检查 `reference_load_manifest` 是否包含用户指定 8 个 copied references 和新增节奏合同。
3. 先检查 `screenplay_mode_decision`：无显式模式时必须是 `zhengju`；显式 `jieshuoju` 时，必须先有 `jieshuoju_source_unit_coverage_map`，陈述性 source 不得转派生对白/独白/内心独白。
4. 检查 `2-美学/类型风格.md` 和 `3-主体/主体注册表.md` 是否已进入 source/context manifest；缺失时先补对应上游，存在时把题材规则写成 `type_style_application_map`，把主体命名写成 `subject_registry_application_map`。
5. 在进入正文前先检查 `upstream_creative_direction_matrix`：`1-分集` 是剧情真源，`2-美学/类型风格.md` 是题材方向，`3-主体/主体注册表.md` 是命名真源，项目记忆/上下文是长期约束；每项必须有 used_as、script_decision、script_landing 和 boundary_check。
6. 若已有 `3-主体/场景/2-设计`、`3-主体/场景/3-生成` 或 `design-manifest.yaml`，先建立 `scene_asset_context_manifest`；只把场景资产用于场景标题、环境白描、空间连续性和 handoff，不能覆盖 source 事实、注册表或写 prompt/镜头。
7. 检查题材画像是否能解释节奏，不解释就回 `N2`。
8. 检查场景标题是否包含天气后缀；未知天气用 `天气待定` 并报告 followup。
9. 对新增对白/独白逐条查 source anchor、voice owner、知识依据和语音预算；若是 `jieshuoju`，先查每个 source 单元的 `source_unit_type` 和 `landing_policy`，陈述性 source 只能查旁白主体和 `旁白画面`，可见动作/环境不得重复旁白化；再查 `jieshuoju_field_variety_map`，正文不得出现方括号叙事小标题或连续 4 组以上无承托旁白对。
10. 对每个节奏机制查承托字段；无承托就删机制或补正文落点。
11. 检查相邻画面字段是否其实是同一拍摄单位：同一主体、同一停顿、同一手部动作、同一道具状态、同一声源反应要合并；只有主体/空间/时间/信息/节奏功能变化时才保留连续字段。
12. 如果“画面化”变成比喻或概念，先删掉“像/仿佛/宿命/高级/压迫感”等词，再补可见身体动作、道具状态、空间距离、声源、光照和时间变化。
13. 用户指出“脚本化/偷懒/未思考/未差异化”时，不接受逐句润色；直接废弃候选稿，回 `N2-N6` 重建证据和正文。
14. 高潮只强化已有事件的声画/情绪/行动，不改结果。
15. 尾钩必须落在最后可感对象上，不接受“悬念拉满”类总结。
16. 报告服务修复和下游交接，必须能回指正文位置。
17. 报告不得写自由散文式“思考过程”；必须写可审计的 `Screenplay Mode Decision`、`Execution Decision Trace`、`Reference Execution Matrix` 和 `Upstream Creative Direction Matrix`。

## Reusable Heuristics

- 好的短剧节奏不是更短，而是更少无功能信息、更早暴露压力、更晚完全解释答案。
- 小说里的“他终于明白了”通常不能直接进剧本；要转成角色看见证据、听见声音、说出一句话或改变动作。
- 字段越多不等于画面越清楚；如果两个字段描述同一可见事实，下游更可能误拆拍摄单位，应优先合并成一个信息密度更高的画面字段。
- 白描式剧本字段让下游直接消费事实：谁在什么位置、做了什么、声音从哪来、光照到哪里、道具状态如何变化；删掉比喻和概念词后，拍摄单位仍然清楚。
- 爽点不是角色赢了，而是压迫关系被观众看见地反转。
- 迷你彩蛋尾钩适合过渡集；大反转尾钩适合冲突集。不要在每集硬造大反转。
- AIGC 视频下游最怕漂移：人物、地点、声音、物件和状态要在剧本字段里提前交代清楚。
- 防偷懒的关键不是要求“全量套规则”，而是要求全量审计、选择性触发和 N/A 必证；报告里没有证据的位置，通常就是下次返工入口。
- 锚点不是差异化本身；把角色名、地点名、道具名换掉但保留同一节奏句式和同一尾钩模板，应按源层主创失败处理。
- `2-美学/类型风格.md` 是分集后的题材类型真源；`4-编剧` 可以做单集副题材校准，但不得无证据推翻其中的主题材、标志性元素和题材专属表现技巧。
- `3-主体/主体注册表.md` 是分集和美学后的主体命名真源；`4-编剧` 可以在剧情中自然使用主体，但不得静默新增、改名或把同一主体拆成多个称呼真源。
- 已有场景设计和场景图是视觉/空间 side context，不是剧情真源；它们能帮助剧本少写漂移地点和模糊环境，但不能让编剧反向新增事件、复制 prompt 或写镜头。
- `Upstream Creative Direction Matrix` 是进入正文前的方向锁定，不是事后报告装饰；它应把“上游输入物”翻译成“本集应该怎样写、写在哪里、不能越过什么边界”。
- `screenplay_mode` 是进入正文前的模式锁定：未指定就是 `正剧`，不要因为 source 叙述较多而自行切到 `解说剧`；只有显式 `解说剧` 才把陈述性 source 全部落为 `旁白/旁白画面`。
- `解说剧` 的第一步不是写旁白，而是做 source 单元覆盖：已有对白冻结，可见动作/环境进画面字段，陈述性事实/背景/时间桥/关系/结果/规则才进 `旁白/旁白画面`；混合句必须双落点。
- `解说剧` 的第二步是做字段节奏：段落功能进入报告，不进正文方括号标题；正文用真实场景标题和正式视觉字段承托旁白，否则会变成有画面的有声书稿。
