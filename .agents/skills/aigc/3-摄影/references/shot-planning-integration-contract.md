# Shot Planning Integration Contract

本文件定义 `3-摄影` 在输出 `镜头语言：分镜N` 前的强制汇流层。它的目的不是新增审美术语，而是确保 `references/` 中的节拍、画面节奏、连续性、动态运镜和技法库真实进入思维与执行。

## Core Rule

每个 `visual_unit` 在写出 `分镜1:`、`分镜2:` 前，必须先形成内部 `shot_design_plan`。该计划不默认输出到正文，但必须支配最终 `分镜N` 的数量、顺序、入口、运动、落点和衔接。

禁止直接从画面句子跳到 `分镜N` 文案。若无法说明某个 `分镜N` 对应的节拍触发、节奏密度、连续性入口、运镜路径和交出点，该分镜视为随机分镜，必须删除或重写。

## Required Plan Fields

| field | source contract | purpose |
| --- | --- | --- |
| `visual_unit_function` | `types/visual-unit-type-map.md`、`visual-matching-contract.md` | 当前画面句子的摄影任务：建立空间、执行动作、显影信息、承托表演、制造危险或完成反应 |
| `beat_sequence` | `beat-analysis-contract.md` | 每个分镜对应一个观看策略变化，不能按固定数量灌水 |
| `rhythm_profile` | `visual-rhythm-analysis-contract.md` | 决定分镜数量、句子密度、运动复杂度、转场强度和停顿感 |
| `continuity_entry` | `shot-continuity-contract.md` | 当前画面从上一注意力落点、声音、动作、光色或空间轴线如何进入 |
| `technique_selection` | `cinematic-technique-library.md`、`dynamic-lens-language-contract.md` | 为每个节拍选择最小充分的景别、景深、视角、镜头类型、运镜、速度、构图、光影、色彩或转场 |
| `intra_unit_handoff` | `dynamic-lens-language-contract.md` | 同一 `visual_unit` 内相邻 `分镜N` 如何从上一个终点接到下一个起点 |
| `next_handoff` | `shot-continuity-contract.md` | 最后一条分镜把注意力交给下一画面哪个入口 |

## Planning Procedure

1. 先用一句内部判断锁定 `visual_unit_function`，不得把一个低信息动作硬做成高密度段落。
2. 从 `Beat Trigger Matrix` 中选择真实触发点，生成 `beat_sequence`；弱触发合并，强触发拆开。
3. 用 `rhythm_profile` 校准分镜数量：低信息收敛，关键揭示或高点发散；分镜变多必须带来新的注意力、信息、动作相位或情绪压力。
4. 用 `continuity_entry` 承接前 3 个画面单位中的最近落点；不能每个画面重新发明一套风格。
5. 为每个 beat 选择技法时遵守“最小充分”：只选择能服务当前 beat 的参数，不把技法库当菜单随机抽样。
6. 写 `分镜N` 时，让每条分镜的起点来自 `continuity_entry` 或上一条分镜的终点；让每条分镜的终点成为下一条分镜的入口或 `next_handoff`。
7. 最终文案必须能反推 `shot_design_plan`：读者能看出为什么有这些分镜、为什么按这个顺序、为什么这样运动。

## Internal Plan Shape

```text
shot_design_plan:
  visual_unit_function: <当前画面摄影任务>
  rhythm_profile: <收敛/标准/发散/断裂的内部判断，不输出标签>
  continuity_entry: <承接上一落点、声音、动作、光色或空间轴线>
  beats:
    - beat: <节拍1的观看策略变化>
      trigger: <BT-xx>
      technique: <景别/景深/视角/镜头类型/运镜/速度/构图/光影/色彩/转场中的必要项>
      start: <镜头起点>
      path: <运动路径与速度曲线>
      end: <注意力落点>
      handoff: <交给下一分镜或下一画面的接口>
```

该结构只作为内部计划或执行报告证据，不作为逐集摄影稿正文的固定输出字段。

## Output Sufficiency Gate

每个 `分镜N` 必须至少满足以下五点：

1. `start` 明确：从哪个景别、焦点、空间位置、动作、声音或光色接口进入。
2. `path` 明确：使用哪类镜头、运镜方向、速度曲线和焦点/景别变化。
3. `end` 明确：落到哪个人物、道具、文字、危险源、反应或转场接口。
4. `motivation` 明确：能看出该运动服务信息揭示、动作相位、情绪压力、空间关系或转场。
5. `handoff` 明确：多分镜时相邻分镜首尾相接，最后一镜能交给下一画面。

## Anti-Patterns

- 只因为“想更电影感”就把一个画面拆成多个分镜。
- `分镜1`、`分镜2`、`分镜3` 彼此都在重新描述同一个状态，没有新的观看策略。
- 每条分镜都换一套技法，读不出上一镜如何进入下一镜。
- 分镜数量确实变多了，但没有主体、动作、信息或情绪的递进。
- 只写“推近”“特写”“压迫感”，没有起点、路径、落点和交出点。
