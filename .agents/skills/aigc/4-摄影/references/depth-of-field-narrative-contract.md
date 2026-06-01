# Depth of Field Narrative Contract

本文件定义景深的叙事功能裁决规则。景深不只是技术参数，而是控制观众注意力和叙事信息的工具。景深决定什么被看见、什么被忽略、什么在同一时刻被允许呈现。

## Example Usage Guard

本文件所有策略表、典型错误示例和修复样句仅用于说明景深叙事判断，不是固定输出模板。执行具体任务时，不得机械复用示例中的焦点对象、字段句式或景深组合；必须按当前画面信息、注意力路径、隐藏/揭示需求和 `shot_design_plan` 重新裁决。

## Core Rule

景深 = 注意力控制。不是"光圈开大拍虚化背景"的技术操作，而是"此刻我让观众看哪里、不看哪里"的叙事决策。

景深控制的是观众的眼睛——他们在看画面中的哪一个点，是否允许他们同时看到前景和背景，是否允许他们选择自己的注意力焦点。

## Depth of Field Strategy Taxonomy

### 基础景深策略表

| strategy_id | 策略名称 | narrative_function（叙事功能） | audience_effect（观众效果） | execution_cue |
| --- | --- | --- | --- | --- |
| `DF-01` | shallow_focus_subject（主体浅焦） | 只有主体清晰，其他全部虚化 | 观众只能看主体，无法分心看其他 | 光圈开到最大/焦距拉长/主体远离背景 |
| `DF-02` | shallow_focus_background（背景浅焦） | 背景清晰，主体反而虚化 | 真正重要的在后面；观众产生"看错了"的认知翻转 | 前景主体虚化，焦点落在背景上的重要信息 |
| `DF-03` | rack_focus_A_to_B（焦点转移） | 焦点从 A 移到 B，强制注意力转移 | 观众的注意力被迫跟随焦点移动 | 拍摄时在 A 和 B 之间切换焦点；或后期拉焦 |
| `DF-04` | deep_focus_all（全景深） | 前景、中景、背景全部清晰 | 观众自由选择注意力焦点；建立空间感和真实感 | 使用小光圈/广角镜头/主体与背景距离近 |
| `DF-05` | split_diopter（分割焦面） | 前后同时清晰，但不在同一平面 | 打破自然视觉，制造不安和异常感 | 使用分割焦点附件/双焦点技术 |
| `DF-06` | soft_focus_emotional（柔焦叙事） | 整体柔焦，画面缺乏锐度 | 梦境/回忆/主观/情感过度主导现实 | 使用柔焦滤镜/扩散光源/特定焦距 |
| `DF-07` | pull_focus_tease（拉焦揭示） | 焦点缓慢移动，逐步揭示 | 制造期待感；观众在等待焦点落到正确位置 | 使用微速拉焦（超过 2 秒）或渐进式焦点变化 |

### 景深策略应用场景表

| scenario | 推荐的景深策略 | 理由 |
| --- | --- | --- |
| 主体需要被隔离 | DF-01 shallow_focus_subject | 让观众无法分心，只专注于主体 |
| 需要制造认知翻转 | DF-02 shallow_focus_background | 让观众"看错"，意识到真正重要的在别处 |
| 需要强制注意力转移 | DF-03 rack_focus_A_to_B | 焦点从 A 到 B 是最强制的注意力引导 |
| 建立空间感和真实感 | DF-04 deep_focus_all | 让观众看到完整空间，不做任何注意力干预 |
| 需要打破常规视觉 | DF-05 split_diopter | 前后同时清晰违反自然视觉，产生不安 |
| 梦境/回忆/主观场景 | DF-06 soft_focus_emotional | 柔焦传递"这不是现实"的信号 |
| 需要悬念和期待 | DF-07 pull_focus_tease | 缓慢拉焦让观众等待焦点落定 |
| 规则显影/信息揭示 | DF-01 或 DF-03 | 隔离主体或强制引导注意力到信息 |
| 群像混乱场景 | DF-04 deep_focus_all | 让观众自己发现混乱中的焦点 |
| 恐怖压迫场景 | DF-01 + DF-05 | 隔离主体+异常前后同时清晰，增强压迫感 |

## Depth of Field as Narrative Rhythm

景深变化本身是叙事节奏工具：

| depth_change_pattern | narrative_meaning | typical_usage |
| --- | --- | --- |
| 变浅（深→浅） | 聚焦 / 压迫 / 注意力收拢 | 情绪高潮 / 规则宣判 / 角色内心收敛 |
| 变深（浅→深） | 自由 / 疏离 / 信息展开 | 紧张释放 / 空间展开 / 角色内心开放 |
| 焦点拉移 | 注意力转移 / 叙事重心变化 | 信息切换 / 角色观察 / 危险转移 |
| 浅→深→浅（大波浪） | 先收拢再展开再收拢 | 完整的情绪弧线：压抑→释放→再压抑 |
| 浅→深（小步快跑） | 渐进式信息揭示 | 多个焦点转移连成悬念链 |

## Integration with Shot Design Plan

每个 `shot_design_plan` 必须包含景深叙事相关字段：

| field | type | required | description |
| --- | --- | --- | --- |
| `depth_strategy` | enum | 是 | 使用 DF-01 至 DF-07 编码 |
| `depth_narrative_function` | string | 是 | 一句话说明这个景深选择对观众注意力做什么（不得只写"虚化背景"，必须写具体的叙事目的） |
| `depth_change_point` | string | 否 | 如果景深在镜头内发生变化，说明变化点和原因 |
| `what_is_blurred` | string | 否 | 明确什么被虚化、什么被保留（当 DF-01 时：背景被虚化；当 DF-02 时：主体被虚化） |
| `why_blurred` | string | 否 | 为什么让这部分虚化（信息需要隐藏？需要观众关注主体？） |

### 典型错误示例

| 错误写法 | 正确写法 |
| --- | --- |
| `景深：f/1.4` | `depth_strategy: DF-01（主体浅焦）；depth_narrative_function: 观众只能看主体，无法分心看背景中的危险提示；what_is_blurred: 背景虚化（但不包含真正的危险源，仅虚化次要环境）` |
| `焦点落在角色脸上` | `depth_strategy: DF-03（焦点转移）；depth_narrative_function: 注意力从角色表情转移到墙上的规则文字；depth_change_point: 对白第三句时焦点从角色脸拉至墙面` |

## Focus Pull and Narrative Synchronization

焦点拉移（rack focus）必须与叙事节奏同步：

| narrative_beat | focus_pull_timing | rationale |
| --- | --- | --- |
| 信息首次可读 | 此刻拉焦到信息 | 焦点落点 = 信息揭示点 |
| 角色注意到某物 | 角色眼神方向后的 0.5-1 秒拉焦 | 延迟拉焦制造"她看到了"的悬念 |
| 声音引导注意力 | 声音来源出现后的 0.3-0.5 秒拉焦 | 声音和画面同步，不让观众困惑"声音从哪里来" |
| 危险逼近 | 危险首次出现在画面边缘时拉焦 | 焦点到危险 = 观众意识到危险 |
| 角色内心变化 | 表情变化时拉焦到表情细节 | 特写+浅焦强化内心变化的可读性 |

## Failure Modes

### FM-01: 景深只是默认值无叙事理由

**症状**：每个镜头的景深都是"开大光圈虚化背景"，没有说明为什么。

**诊断**：检查是否每个镜头都有 `depth_narrative_function` 字段，且该字段说明的不是技术参数而是叙事目的。

**修复**：为每个镜头补充景深叙事理由。如果只是为了"好看"而虚化背景，这不是叙事决策。

### FM-02: 场景间景深无变化

**症状**：整集或整场用同样的景深策略（大部分都是 DF-01），景深没有参与叙事节奏。

**诊断**：检查景深策略分布。如果超过 70% 是 DF-01，说明景深没有作为叙事工具使用。

**修复**：引入 DF-02（背景清晰）、DF-04（全景深）、DF-05（分割焦点）等策略，让景深成为情绪变化的调节器。

### FM-03: 焦点拉移与叙事不同步

**症状**：焦点在"规则文字出现"时没有拉到文字，或者拉焦时机与角色眼神不一致。

**诊断**：检查焦点拉移时间点是否与叙事节拍对齐。焦点拉移是最强烈的注意力引导，必须与叙事节奏同步。

**修复**：按照"焦点拉移与叙事同步表"调整拉焦时机。

### FM-04: 背景虚化时虚化了重要信息

**症状**：为了景深美观看似好看，把背景虚化，但背景中有重要的危险源或信息。

**诊断**：检查被虚化的内容是否包含关键叙事信息。如果虚化了危险提示，观众的恐惧体验会被削弱。

**修复**：在虚化背景时，明确说明被虚化的内容不包含关键信息，或者使用 DF-02（背景清晰但主体虚化）反转景深叙事。

### FM-05: 柔焦被滥用为"情绪感"

**症状**：任何情绪场景都用柔焦（DF-06），导致柔焦失去其"非现实"的叙事含义。

**诊断**：柔焦的叙事含义是"这不是现实"或"情感主导"。如果场景需要保持现实感，柔焦会破坏真实感。

**修复**：只在需要传递"梦境/回忆/主观"信号的场景使用柔焦。

## Depth of Field and Cinematography Technique Alignment

景深策略需要与摄影技术参数协调：

| depth_strategy | 适配的光圈 | 适配的焦距 | 适配的拍摄距离 | 技术说明 |
| --- | --- | --- | --- | --- |
| DF-01 主体浅焦 | f/1.4 - f/2.8 | 85mm+ | 主体远离背景 | 光圈越大焦距越长，背景越虚化 |
| DF-02 背景浅焦 | f/1.4 - f/2.8 | 50-85mm | 主体靠近镜头 | 前景虚化，背景保持相对清晰 |
| DF-03 焦点转移 | f/2.8 - f/4 | 35-50mm | 适中 | 需要在 A 和 B 上都能保持可接受的清晰度 |
| DF-04 全景深 | f/8 - f/16 | 24-35mm | 主体靠近背景 | 小光圈+广角实现最大景深 |
| DF-05 分割焦面 | 需要特殊附件 | 任何 | 前后同时对焦 | 需要双焦点技术或分割焦面附件 |
| DF-06 柔焦 | 任何 | 任何 | 任何 | 使用柔焦滤镜或扩散技术 |
| DF-07 拉焦揭示 | f/2.8 - f/4 | 50-85mm | 适中 | 微速拉焦需要精确控制 |

## Reusable Heuristics

1. **景深是观众注意力的开关**：每一次景深变化都是一次注意力引导决策，不是技术参数调整。
2. **虚化背景不是美化，是隐藏**：虚化掉的内容是"此刻不让观众看的内容"。必须清楚知道虚化的是什么、为什么虚化。
3. **焦点拉移是最强烈的注意力引导**：比任何运动、任何文字标注都强。当需要强制观众注意某物时，用焦点拉移。
4. **深景深让观众自由，但失去控制**：全景深（DF-04）让观众自己选择注意力，但无法控制他们的选择是否正确。
5. **景深变化即情绪变化**：景深从深变浅=收紧（压迫），从浅变深=释放（自由）。景深变化是观众情绪的隐喻。
6. **DF-02 是最容易被忽视的强大工具**：背景清晰但主体虚化（"真正重要的在后面"）是制造认知翻转的利器。
7. **柔焦是双刃剑**：柔焦（DF-06）传递"非现实"信号，如果场景需要现实感，不要用柔焦。
8. **焦点拉移必须与叙事同步**：拉焦时间点必须与信息揭示、角色眼神、声音来源等叙事节拍对齐，延迟或提前都会破坏叙事节奏。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does every meaningful depth choice name a narrative function for attention, hiding, revealing, isolating, subjective bias or spatial pressure rather than only a technical aperture or blur effect? | `GATE-CINE-29` | `FAIL-CINE-05X` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | `depth_of_field_narrative_plan` samples with `depth_strategy` and `depth_narrative_function` |
| Does depth strategy vary with narrative rhythm when needed, instead of defaulting most shots to shallow subject focus for beauty? | `GATE-CINE-29` / `GATE-CINE-16` | `FAIL-CINE-05X` / `FAIL-CINE-05I` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | strategy distribution sample and revised DF choices |
| Is every focus pull synchronized to information reveal, character gaze, sound source, danger entry or emotional change? | `GATE-CINE-29` / `GATE-CINE-31` | `FAIL-CINE-05X` / `FAIL-CINE-05Z` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` / `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` | focus-pull timing notes and attention target evidence |
| When something is blurred, is the blurred content identified and proven not to contain the necessary clue, threat or relationship information for this beat? | `GATE-CINE-29` / `GATE-CINE-31` | `FAIL-CINE-05X` / `FAIL-CINE-05Z` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` / `steps/cinematography-workflow.md#N6.4-FUNCTIONAL-PROJECTION` | `what_is_blurred` / `why_blurred` samples and suspense-leak checks |
| Is soft focus reserved for dream, memory, subjective or emotion-dominant states rather than generic feeling? | `GATE-CINE-29` | `FAIL-CINE-05X` | `steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR` | DF-06 usage justifications or repaired non-subjective shots |
| Do examples, typical error samples and technical alignment rows serve only as judgment aids rather than reusable output phrasing? | `GATE-CINE-17A` / `GATE-CINE-18` | `FAIL-CINE-05REF` / `FAIL-CINE-05G` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N7-INJECT` | report note that examples are not templates, plus any phrase/template cleanup |
