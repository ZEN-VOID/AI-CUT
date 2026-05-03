# Shot Planning Integration Contract

本文件定义 `3-摄影` 在输出 `分镜明细：分镜N` 前的强制汇流层。它的目的不是新增审美术语，而是确保 `references/` 中的节拍、画面节奏、高点策略、连续性、摄影语法、功能性影视投影、动态运镜、自然成稿和技法库真实进入思维与执行。

## Core Rule

每个 `visual_unit` 在写出 `分镜1:`、`分镜2:` 前，必须先形成内部 `shot_design_plan`。该计划不默认输出到正文，但必须支配最终 `分镜N` 的数量、顺序、入口、摄影语法、运动、落点、衔接和下游消费 payload。

禁止直接从画面句子跳到 `分镜N` 文案。若无法说明某个 `分镜N` 对应的节拍触发、节奏密度、连续性入口、摄影语法选择、功能 payload、运镜路径和交出点，该分镜视为随机分镜，必须删除或重写。

## Required Plan Fields

| field | source contract | purpose |
| --- | --- | --- |
| `visual_unit_function` | `types/visual-unit-type-map.md`、`visual-matching-contract.md` | 当前画面句子的摄影任务：建立空间、执行动作、显影信息、承托表演、制造危险或完成反应 |
| `functional_payload` | `functional-cinematic-projection-contract.md` | 为每个分镜锁定 shot_function、visible_subject、action_phase、camera_movement_plan、composition_anchor、light_color_material 和 downstream consumability |
| `beat_sequence` | `beat-analysis-contract.md` | 每个分镜对应一个观看策略变化，不能按固定数量灌水 |
| `shot_count_decision` | `beat-analysis-contract.md`、`visual-rhythm-analysis-contract.md` | 明确本 visual_unit 为什么是 1/2/3/4 镜；2 镜不得作为默认值，只能作为真实两段观看策略的结果 |
| `rhythm_profile` | `visual-rhythm-analysis-contract.md` | 决定分镜数量、句子密度、运动复杂度、转场强度和停顿感 |
| `continuity_entry` | `shot-continuity-contract.md` | 当前画面从上一注意力落点、声音、动作、光色或空间轴线如何进入 |
| `transition_profile` | `transition-design-contract.md` | 场景变化、空间重置、注意力转交、动作/声音/形态/光色/文字接口是否需要普通切镜、软桥接、匹配剪辑或高能转场 |
| `camera_grammar_plan` | `cinematic-technique-library.md`、`dynamic-lens-language-contract.md`、`shot-continuity-contract.md` | 为每个节拍裁决景别梯度、景深/焦点、镜头视角、镜头类型、构图、光影、色彩、运镜方式、速度曲线、停点和变化动机 |
| `functional_projection_plan` | `functional-cinematic-projection-contract.md` | 将每个计划分镜投影为主体、动作相位、运镜计划、构图锚点、光色/材质、空间接口、连续性交接和下游消费点 |
| `technique_selection` | `cinematic-technique-library.md`、`dynamic-lens-language-contract.md` | 从 `camera_grammar_plan` 中选择最小充分且必须显式进入成稿的 1-2 个摄影选择 |
| `natural_output_strategy` | `natural-shot-detail-writing-contract.md` | 决定哪些参数必须显式写、哪些内化为画面动作，避免模板腔和参数清单 |
| `intra_unit_handoff` | `dynamic-lens-language-contract.md` | 同一 `visual_unit` 内相邻 `分镜N` 如何从上一个终点接到下一个起点 |
| `next_handoff` | `shot-continuity-contract.md` | 最后一条分镜把注意力交给下一画面哪个入口 |

## Planning Procedure

1. 先用一句内部判断锁定 `visual_unit_function`，不得把一个低信息动作硬做成高密度段落。
2. 从 `Beat Trigger Matrix` 中选择真实触发点，生成 `beat_sequence`；弱触发合并，强触发拆开。
3. 形成 `shot_count_decision`：先允许 1 镜成立，再验证是否存在第二个真实观看策略；只有关键揭示、群像扩散、动作分相、空间重置或高点承托才继续扩展到 3-4 镜。
4. 用 `rhythm_profile` 校准分镜数量：低信息收敛，关键揭示或高点发散；分镜变多必须带来新的注意力、信息、动作相位或情绪压力。若当前批次出现大量同数分镜，尤其 2 镜集中，必须抽样复判并修正 `shot_count_decision`。
5. 用 `continuity_entry` 承接前 3 个画面单位中的最近落点；不能每个画面重新发明一套风格。
6. 若发生场景变化、空间重置、注意力转交、动作承接、声音先行、形态/颜色匹配、信息显影或高点断裂，先建立 `transition_profile`，明确交出点、进入点和转场强度；没有强接口时优先普通切镜或软桥接。
7. 建立 `camera_grammar_plan`：景别变化像呼吸，视角变化有权力/主观/观察/空间动机，景深和焦点负责注意力交接，镜头类型和构图服务空间压力或信息显影。
8. 建立 `functional_projection_plan`：没有主体、动作相位、运镜计划、构图锚点、光色/材质、连续性交接或下游消费意义的 beat 不能写成分镜。
9. 为每个 beat 选择技法时遵守“最小充分”：只选择能服务当前 beat 的参数和运镜策略，不把技法库当菜单随机抽样。
10. 用 `natural_output_strategy` 压缩显式参数：每条分镜只写当前节拍最关键的 1-2 个摄影选择，其余通过具体画面、动作、遮挡、光色和落点表达。
11. 写 `分镜N` 时，让每条分镜的起点来自 `continuity_entry` 或上一条分镜的终点；让每条分镜的终点成为下一条分镜的入口或 `next_handoff`。
12. 最终文案必须能反推 `shot_design_plan`：读者能看出为什么有这些分镜、为什么按这个顺序、摄影机为什么这样动或不动，景别/视角/焦点为什么这样变化，以及下游图像/视频应消费哪些主体、动作、运镜、构图、光色和空间关系；但不得像计划表一样逐项暴露内部字段。

## Internal Plan Shape

```text
shot_design_plan:
  visual_unit_function: <当前画面摄影任务>
  shot_count_decision: <为什么是 1/2/3/4 镜；2 镜必须说明第二个真实观看策略>
  rhythm_profile: <收敛/标准/发散/断裂的内部判断，不输出标签>
  continuity_entry: <承接上一落点、声音、动作、光色或空间轴线>
  transition_profile: <如触发，记录场景/空间/注意力/动作/声音/形态/光色/文字接口、交出点、进入点和转场强度>
  beats:
    - beat: <节拍1的观看策略变化>
      trigger: <BT-xx>
      camera_grammar_plan:
        shot_scale_path: <景别梯度：建立/调度/加压/揭示/回收>
        angle_strategy: <平视/低角度/高角度/俯拍/仰拍/过肩/主观/窥视及其动机>
        depth_focus_plan: <景深与焦点如何承接注意力>
        lens_and_composition: <镜头类型、构图锚点、前中后景或遮挡关系>
        light_color_motion: <光色母题与运镜速度/停点如何配合>
      functional_payload:
        shot_function: <本镜影视功能>
        visible_subject: <可见主体>
        action_phase: <动作/信息/反应相位>
        camera_movement_plan: <运镜方式、方向、速度、停点、焦点/景别变化、交接接口>
        composition_anchor: <构图锚点>
        light_color_material: <光色/材质/视觉母题>
        downstream_consumability: <图像/视频可消费点>
      technique: <从 camera_grammar_plan 中显式进入成稿的必要项>
      natural_output_strategy: <显式写哪些关键选择，哪些内化成自然画面文字>
      start: <镜头起点>
      path: <运动路径与速度曲线>
      end: <注意力落点>
      handoff: <交给下一分镜或下一画面的接口>
```

该结构只作为内部计划或执行报告证据，不作为逐集摄影稿正文的固定输出字段。

## Output Sufficiency Gate

每个 `分镜N` 必须至少满足以下七点：

1. `start` 明确：从哪个景别、焦点、空间位置、动作、声音或光色接口进入。
2. `path` 明确：使用哪类镜头、运镜方向、速度曲线和焦点/景别变化。
3. `end` 明确：落到哪个人物、道具、文字、危险源、反应或转场接口。
4. `motivation` 明确：能看出该运动服务信息揭示、动作相位、情绪压力、空间关系或转场。
5. `handoff` 明确：多分镜时相邻分镜首尾相接，最后一镜能交给下一画面。
6. `downstream_payload` 明确：能抽取主体、动作、运镜、构图锚点、光色/材质和图像/视频可消费点。
7. `camera_grammar` 明确：景别、视角、景深/焦点、镜头类型或构图变化至少有一个真实服务当前节拍，且变化不破坏连续性。
8. `naturalness` 合格：读起来不是字段展开、参数清单或模板填空。

## Anti-Patterns

- 只因为“想更电影感”就把一个画面拆成多个分镜。
- 只因为模板里有 `分镜2` 就把每个画面写成 2 镜。
- `分镜1`、`分镜2`、`分镜3` 彼此都在重新描述同一个状态，没有新的观看策略。
- 每条分镜都换一套技法，读不出上一镜如何进入下一镜。
- 分镜数量确实变多了，但没有主体、动作、信息或情绪的递进。
- 分镜读起来顺，但下游无法判断该画谁、摄影机怎么动或为什么不动、构图锚点是什么、光色如何继承。
- 分镜出现景别、视角、焦点或镜头类型变化，但变化没有服务节拍、空间、信息、情绪或交接，只是为了显得专业。
- 只写“推近”“特写”“压迫感”，没有起点、路径、落点和交出点。
- 为了证明起点、路径、速度、落点齐全，把每条分镜都写成同一个“从……以……变化到……最终……”骨架。
