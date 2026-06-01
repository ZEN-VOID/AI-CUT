# Dynamic Shot Detail Contract

本文件定义原画面性字段标题下 `时间段` 的动态化描述方式。目标是让最终作品有流畅感、丝滑感和连续观看的运动逻辑，而不是静态参数堆叠。

## Example Usage Guard

本文件中的句法模式、方向参照和示例只用于内部构思或卡壳时辅助，不是成稿模板。执行具体任务时，不得连续套用这些句式，也不得复用示例对象或镜头组合；最终输出必须根据当前画面句子的动作、注意力路径、时值和交出点重新组织自然句。

## Core Rule

每个 `时间段` 默认写成“时间中的变化”，而不是“静态画面说明”。句子必须回答：

| question | requirement |
| --- | --- |
| 起点是什么 | 镜头从哪个景别、视角、焦点、空间位置或视觉信息开始 |
| 过程怎么动 | 推、拉、摇、移、升降、环绕、跟随、甩镜、焦点拉移或组合运镜如何发生 |
| 速度如何变化 | 静止、极慢、慢速、中速、快速、急停、变速或呼吸式缓动 |
| 需要停留多久 | 该镜是快速通过、标准承接、读秒停留还是长停顿；正文必须以 `[起始秒-结束秒]` 显式展示 |
| 终点落在哪里 | 最终落到哪个人物、道具、文字、反应、危险源或转场接口 |
| 为什么这样动 | 运动服务哪一个节拍：信息揭示、情绪加压、权力转移、空间压迫或边界交出 |
| 属于哪个画面点 | 运动服务正上方哪条画面句子；段落连续性只提供入口、落点或视觉母题，不能让镜头失去当前归属 |
| 镜头是否包裹动作 | 镜头类型、运动和构图从一开始建立，人物动作在该镜头内部完成，而不是动作结束后再补一句运镜 |
| 方向是否有参照 | 运动方向、入画、退场和视线必须相对镜头、摄像机或画面边界表达，避免只写“向前/后退/左边/右边” |
| 观众如何发现 | 是否从遮挡、局部、虚化、脚步、衣摆、门框或低机位前景开始，再逐步释放主体和空间关系 |

## Dynamic Sentence Patterns

以下句法只用于内部构思或卡壳时辅助，不是成稿模板。连续输出时必须变化句式，优先遵守 `natural-shot-detail-writing-contract.md` 的自然中文要求：

- `从 <起始景别/视角/焦点> 起，以 <运镜方式 + 速度> 过渡到 <终点信息>，让 <戏剧效果>。`
- `先 <静态压住/建立关系>，再 <焦点/景别/视角变化>，最后 <落点或切点>。`
- `<组合运镜1> 接 <组合运镜2>，速度从 <速度A> 变为 <速度B>，在 <关键物/脸/文字> 上急停。`
- `借 <动作/声音/光变/形态> 做匹配，把镜头从 <当前画面> 丝滑带到 <下一注意力点>。`
- `保持 <镜头类型/视角> 不动，让 <角色/道具/文字> 在框内完成变化，直到 <切换点>。`

## Combination Movement Library

| combo | use when | dynamic cue |
| --- | --- | --- |
| 慢推 + 焦点拉移 | 危险或文字从背景变成主信息 | 从人物反应慢推，焦点丝滑滑到黑板字、门缝或红色道具 |
| 横移 + 前景遮挡 | 角色被空间和制度切割 | 镜头沿课桌边横移，让前景桌角/窗帘周期性遮住主体 |
| 跟拍 + 急停 | 人物行动突然被规则或危险锁住 | 跟随动作中速推进，在点名、声响或显影瞬间急停 |
| 俯拍下降 + 低角度切入 | 群体无助转为权力压迫 | 从棋盘式俯拍降到讲台低角度，权力关系完成翻转 |
| 环绕 + 景深收窄 | 人物被包围或心理空间塌缩 | 环绕半圈，同时从深景深收成浅景深，只剩脸和危险色块 |
| 声音先行 + 光变切入 | 转场需要顺滑而高能 | 让下一声高跟鞋/铃声先进来，再用冷白闪动或黑板波纹切画面 |
| 固定机位 + 框内运动 | 规则碾压、制度不可动摇 | 镜头不动，人物被迫走入/退出构图，压迫来自框线本身 |
| 手持微晃 + 稳定落点 | 恐惧蔓延但信息仍需清楚 | 前半微晃跟随群像，后半稳定落到关键手指、眼睛或道具 |

## Flow And Silkiness Rules

- 动态不是乱动；镜头运动必须有起点、路径、速度曲线和终点。
- 动态不是动作后的补丁；AI 视频更稳定的写法是先建立镜头和构图，再让人物动作在镜头内部发生。
- 丝滑感来自注意力连续：观众上一秒看的东西，必须自然牵引到下一秒看的东西。
- 镜头不是被动记录，而是选择观众先看什么、后理解什么；低角度、前景遮挡、浅景深和慢拉必须服务观看任务，不能只作为“电影感”装饰。
- 正面平视只有在明确需要中立观察、制度压迫或固定框线时才保留；否则应考虑机位高度、透视拉伸、前景层次或观众发现路径，避免全信息平铺造成摆拍感。
- 丝滑感不能覆盖画面点归属：连续运镜可以顺接相邻块，但当前块的主体、动作、信息和对白承托必须属于正上方画面句子。
- 组合运镜最多选 2-3 个动作；超过 3 个动作通常会显得炫技打架。
- 速度变化要有动机：慢是悬疑，快是冲击，急停是确认，变速是感知异常。
- 时值要有动机：文字和微表情需要读秒，低信息动作需要压缩，冲击镜需要短促，认知高点和关系高点才需要更长停顿。
- 对白时值要先满足台词量：镜头运动可以藏在听者反应、手部动作或空间压力里，但不能让关键台词没说完就被视觉切点截断。
- 若演员表演需要停顿，优先让镜头静止或极慢，不要用复杂运镜覆盖表演。
- 涉及行走、后退、入画、移位或视线转移时，必须使用相对镜头/画面的方向参照，例如“朝镜头走来”“远离摄像机”“从画面左侧进入并停在右侧三分之一处”。
- 边界交出要找接口：相似形态、同向动作、声音余波、光变、文字显影、颜色跳点；连接方式留给 `5-分组`。

## Static Anti-Patterns

避免以下写法：

- `中景，浅景深，低角度，冷白光，压迫感强。`
- `镜头推进，氛围紧张。`
- `男人走进房间坐下后，镜头缓慢推进。`
- `正面平视拍完整人物走来，画面清晰。`
- `低角度拍摄，画面更有电影感。`
- `人物向前走，随后后退。`
- `特写道具，突出诡异。`
- `使用高级运镜，让画面丝滑。`

应改为：

- `从中景平视压住林寂僵硬的上半身，以极慢推轨贴近到近景，景深从中景深收窄成浅景深，焦点最终停在他从白光里重新合焦的瞳孔上。`
- `镜头先固定在黑板冷白字上，借教鞭敲击声做声音先行，随后慢速下摇到学生们同步停住的嘴唇，最后急停在赵德发发抖的手指。`
- `低角度镜头从门口开始缓慢推进，男人朝镜头方向走进房间，在椅子前坐下的过程中画面持续靠近，最后停在他的半身近景。`
- `低角度镜头贴近地面，先让前景脚步和衣摆遮住半个画面；人物朝镜头走来时透视把身体拉长，镜头轻微手持后退，直到脸进入上方三分之一处。`

## Output Requirement

每个 `时间段` 的内部检查结构：

```text
[起始秒-结束秒] <自然写出起点、观看动作、速度变化、时值理由和落点；只显式保留当前节拍不可缺少的摄影选择。>
```

不得机械照抄这个句式。成稿必须呈现动态变化，但应让技术判断藏在自然画面文字中。

每个 `[起始秒-结束秒]` 还必须能反推内部 `shot_design_plan`：起点、路径、速度、时值等级、终点、节拍动机和交出点缺一不可。简短可以成立，但不能短到只剩“镜头推进”“特写压迫”“转场丝滑”这类无法执行的概括；长停顿也可以成立，但必须通过对白承托、可读信息、框内细微变化、表演压力或高点读秒体现，不得只是把气氛拉长；也不能为了显得完整而把内部字段逐项摊开。

若某条分镜会进入视频生成链路，还必须能反推 `ai_video_prompt_execution_profile`：镜头和构图先行，动作在镜头内部完成，方向参照明确，重要光影写出结果，表演情绪有可见微动态。缺任一项时不得靠“电影感”“连续感”补足。

若一个动态句把多个相邻画面单位连成单条长镜，导致无法判断当前句属于哪条上游字段，必须按 `visual-sequence-alignment-contract.md` 拆回逐画面点：当前块只保留自己的起点、路径、落点和交出锚点，下一块另写自己的进入和主体动作。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does every `[起始秒-结束秒]` read as a change across time with start point, path or stillness reason, speed, duration, endpoint and beat motivation? | `GATE-CINE-08` | `FAIL-CINE-05B` / `FAIL-CINE-05L` | `steps/cinematography-workflow.md#N5.2-DURATION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` / `steps/cinematography-workflow.md#N7-INJECT` | dynamic path samples, duration reasons and rewritten static lines |
| Is the camera or composition established before character action, so movement is wrapped inside the shot rather than appended after the action? | `GATE-CINE-15A` | `FAIL-CINE-05N` / `FAIL-SHOT-IDENTITY-01` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | AI video execution samples showing camera-first order |
| Are movement direction, entry, exit and sightline described relative to camera, frame edge or space anchor? | `GATE-CINE-15A` / `GATE-CINE-26` | `FAIL-DIRECTION-REF-01` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | direction-reference corrections for walking, retreating, entering, exiting or looking |
| Does the shot create a viewer discovery path with foreground, concealment, partial reveal, focus shift or low-angle/front-layer motivation when full frontal display would be flat? | `GATE-CINE-31` / `GATE-CINE-15A` | `FAIL-CINE-05Z` / `FAIL-SHOT-IDENTITY-02` | `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | discovery path samples and justified front-facing exceptions |
| Does smoothness preserve current `visual_unit` ownership instead of merging adjacent units into a single orphaned long shot? | `GATE-CINE-04D` | `FAIL-CINE-05M` | `references/visual-sequence-alignment-contract.md` / `steps/cinematography-workflow.md#N3.5-SEQUENCE-ALIGN` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | `unit_ownership_map` checks and split-back repairs |
| Are combination movements limited to 2-3 motivated actions, with speed and duration tied to suspense, impact, readability, dialogue or performance? | `GATE-CINE-16` / `GATE-CINE-04B` | `FAIL-CINE-05I` / `FAIL-CINE-05L` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` / `steps/cinematography-workflow.md#N5.2-DURATION` | combination movement samples and speed/duration justifications |
| Is final language natural and varied, avoiding repeated dynamic sentence patterns, parameter stacks or generic "silky/cinematic" claims? | `GATE-CINE-18` | `FAIL-CINE-05G` | `steps/cinematography-workflow.md#N7-INJECT` | natural-language review samples and template-pattern cleanup |
| Are sentence patterns, direction examples and sample objects used only as internal aids, not as reusable output templates? | `GATE-CINE-17A` / `GATE-CINE-18` | `FAIL-CINE-05REF` / `FAIL-CINE-05G` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N7-INJECT` | reference non-template statement and repaired example-like output |
