# Transition Anchor Contract

本文件定义原画面性字段标题下相邻时间段之间「过渡锚点」的标准描述格式和执行规则。过渡锚点是连接相邻时间段的视觉/听觉接口，确保镜头流转连贯而非断裂。本契约是 `shot-continuity-contract.md` 的延续，专注于同一画面字段内部的连续性设计。

## Example Usage Guard

本文件所有示例、正例、反例和标准格式仅用于说明过渡锚点的判断逻辑，不是固定分镜模板。执行具体任务时，不得复用示例中的武器、鱼鳞、链条、礁石、句式或动作组合；必须从当前画面句子的真实运动体、接触点、声音、光色和连续性需求中生成自己的过渡锚点。

## Core Rule

每个原画面性字段标题下的 `时间段` 之间必须存在**物理因果链过渡**。相邻时间段的交接处必须找到：同一运动体的位置延续、同一道具的形态变化、同一声音的时序延伸，或同一光色的明暗过渡。

当前输出格式要求过渡锚点直接融合进相邻 `[起始秒-结束秒]` 句子，而不是另起“过渡说明”“镜头连接”或内部字段。第一段句尾承担 `exit_position / outgoing_tail / previous_lighting`，下一段句首承担 `entry_condition / incoming_tail / transition_light`；如果读者需要查看内部计划才能理解 A 如何接到 B，说明过渡锚点没有投影到成稿。

**禁止**：
- 在两个分镜之间留下"因果黑洞"——动作A直接跳到结果C，中间没有B
- 用硬切代替过渡锚点描述
- 把"断裂""制造断裂"当作优点描述，除非断裂本身是叙事意图
- 把过渡锚点写成独立说明行，破坏原字段标题下连续时间段的自然分镜正文

## Transition Anchor Types

### 1. 运动延续锚点（Movement Continuity Anchor）

描述同一运动体在相邻时间段间的位置、速度、方向变化。

| anchor_field | description |
| --- | --- |
| `exit_position` | 运动体在本分镜结尾的位置 |
| `entry_condition` | 运动体在下一分镜入口的初始状态 |
| `transition_frame` | 连接两者的内部 0.2-0.5 秒过渡锚点描述，必须融入相邻 `[起始秒-结束秒]` 句子，不单独落盘成箭头行 |
| `velocity_curve` | 速度变化：加速/匀速/减速/急停 |

**标准格式**：
```
[起始秒-结束秒]：<当前运动描述>；<本镜终点位置/速度>。
[下一起始秒-下一结束秒]：<承接上一段终点的过渡锚点>，<下一运动的起点和延续方式>。
```

**示例**：
```
✅ [起始秒-结束秒]：十字枪刃以水平横扫擦过画面中轴，枪尖从左缘进入右缘；金属刃面在雾光里划出一道蓝冷横线。
[下一起始秒-下一结束秒]：枪尖咬入鱼篓边缘，篾条在刃压下崩裂，银鳞从裂口挤射而出；镜头用快速甩镜跟住鳞片在雾光中拉出的弧形轨迹。

❌ [起始秒-结束秒]：十字枪刃以水平横扫擦过画面中轴。
[起始秒-结束秒]：鱼鳞在雾光中拉出弧形轨迹。（没有枪刃接触鱼篓的过渡）
```

### 2. 道具形态锚点（Prop State Anchor）

描述同一道具在相邻时间段间的形态变化。

| anchor_field | description |
| --- | --- |
| `object_identity` | 道具在同一原字段时间段组内保持唯一指认 |
| `previous_state` | 道具在上一分镜结尾的状态 |
| `transition_state` | 道具在过渡帧的形态变化瞬间 |
| `next_state` | 道具在下一分镜入口的状态 |

**标准格式**：
```
[起始秒-结束秒]：<道具当前状态>；<与上一段的因果关系>。
[下一起始秒-下一结束秒]：<承接上一段的道具形态变化瞬间>，<道具在下一时间段的延续状态>。
```

**示例**：
```
✅ [起始秒-结束秒]：枪尾短链从画面右侧甩入前景，铁环在雾里拖出一道冷弧。
[下一起始秒-下一结束秒]：倒钩咬进肩胛，布料在铁尖崩裂，碎片挂在刃上；链条带着后生身体向后拖行，布片在雾里轻抖。

❌ [起始秒-结束秒]：枪尾短链甩入前景，倒钩咬进肩胛。
[起始秒-结束秒]：后生身体撞向礁角。（没有倒钩接触肩胛、布料崩裂的过渡）
```

### 3. 声音时序锚点（Sound Timeline Anchor）

描述声音在相邻时间段间的延续或衰减。

| anchor_field | description |
| --- | --- |
| `sound_source` | 声音来源的实体 |
| `sound_type` | 声音类型：撞击/拖行/嗡鸣/回响 |
| `incoming_tail` | 上一分镜声音的尾音 |
| `outgoing_source` | 下一分镜声音的来源变化 |

**标准格式**：
```
[起始秒-结束秒]：<当前声音描述>，<声音持续状态>。
[下一起始秒-下一结束秒]：<上一声音的尾音如何转接>，<下一声音的起点及其与上一声音的关系>。
```

**示例**：
```
✅ [起始秒-结束秒]：铁链拖行的咔哒声在礁石上留下回响，每一声都像是数着步子。
[下一起始秒-下一结束秒]：最后一节链环磕在石棱上，撞击声突然变闷，被布料撕裂的脆响盖过；肩胛处的衣料在枪尖下崩裂。

❌ [起始秒-结束秒]：铁链拖行声在礁石上留下回响。
[起始秒-结束秒]：布料撕裂的脆响。（没有声音之间的过渡说明）
```

### 4. 光色明暗锚点（Light Color Anchor）

描述光色在相邻时间段间的明暗过渡。

| anchor_field | description |
| --- | --- |
| `previous_lighting` | 上一分镜的光色状态 |
| `transition_light` | 过渡帧的光色变化 |
| `next_lighting` | 下一分镜的光色状态 |
| `light_motivation` | 光变的原因（道具遮挡、动作遮光、自然变化） |

**标准格式**：
```
[起始秒-结束秒]：<当前光色状态>，<光源位置>。
[下一起始秒-下一结束秒]：<上一光色如何变化到下一光色>，<光源变化原因>。
```

## Transition Anchor 位置规则

### 分镜块内位置

| 时间段数量 | 过渡锚点位置 | 规则 |
| --- | --- | --- |
| 2 个时间段 | 第一段结尾→第二段开头 | 必须有 1 个过渡帧 |
| 3 个时间段 | 第一段结尾→第二段开头；第二段结尾→第三段开头 | 必须有 2 个过渡帧 |
| 4+ 个时间段 | 每两个相邻时间段之间 | 必须有（N-1）个过渡帧 |

### 过渡帧时长规则

| 运动速度 | 过渡帧时长 | 说明 |
| --- | --- | --- |
| 高速运动（甩镜、急摇） | 0.2-0.3秒 | 接近硬切但有因果 |
| 中速运动（横移、跟拍） | 0.3-0.5秒 | 保持连贯感 |
| 慢速/静止（特写、定格） | 0.5-1秒 | 允许节奏呼吸 |

## Continuity Profile Integration

在 `shot-continuity-contract.md` 的 `continuity_profile` 基础上，增加 `transition_anchor` 字段：

| field | question |
| --- | --- |
| `intra_shot_transition` | 当前原字段时间段组内相邻时间段之间是否存在物理因果链过渡 |
| `transition_type` | 运动延续/道具形态/声音时序/光色明暗（可多选） |
| `transition_duration` | 过渡帧时长估算（0.2-0.5秒/0.5-1秒） |
| `causal_gap` | 是否存在因果黑洞（无过渡的断裂）；若有，必须说明是否为叙事意图 |
| `anchor_evidence` | 过渡锚点的具体描述（可被下游验证） |
| `inline_projection` | 过渡锚点是否已投影到上一时间段句尾或下一时间段句首，而不是单独挂说明 |

## Decision Rules

1. **因果链强制**：所有相邻时间段之间必须存在物理因果过渡，除非：
   - 叙事意图要求强断裂（惊吓、规则打断、记忆闪回）
   - 断裂本身是节奏设计（急停后突然爆发）
   - 断裂已在 `transition_design_contract` 中被标记为合法

2. **过渡帧优先级**：
   - 动作镜头 > 静止镜头（动作镜头更依赖连续性）
   - 高速运动 > 慢速运动（高速更需要因果链）
   - 跨景别切换 > 同景别延续（同景别切换更难察觉过渡）

3. **描述精度**：
   - 过渡帧必须描述**可见的物理状态变化**
   - 禁止使用"瞬间""突然""飞快"等模糊词代替具体过渡
   - 声音过渡可以没有视觉表现，但必须有时序描述

4. **验收门槛**：
   - 每个原字段时间段组内，相邻时间段之间的过渡锚点描述覆盖率应达到 100%
   - 覆盖率 = 有过渡锚点描述的相邻时间段对数 / 总相邻时间段对数

## Anti-Patterns

### 因果黑洞类

- ❌ 第一段：枪刃横扫。第二段：鱼鳞飞出。（没有刃-篓接触的瞬间）
- ❌ 第一段：拳头挥出。第二段：对手倒地。（没有击中的过渡）
- ❌ 第一段：链条甩出。第二段：人撞上礁石。（没有钩-肉接触的瞬间）

### 模糊替代类

- ❌ "枪刃突然削开鱼篓"（用"突然"掩盖过渡缺失）
- ❌ "画面一裂，鳞片已经飞在空中"（用"一裂"代替因果描述）
- ❌ "来不及看清，人已经撞上去了"（用叙事借口掩盖连续性断裂）

### 自毁式断裂类

- ❌ "制造断裂"作为优点描述（除非是叙事意图）
- ❌ "硬切到下一动作"（硬切不是过渡锚点）
- ❌ "用镜头断裂表现震惊"（震惊应通过角色反应镜头而非分镜断裂表现）

## Audit Checklist

每个原字段时间段组在输出前必须通过以下检查：

| # | 检查项 | 标准 | 若不合格 |
| --- | --- | --- | --- |
| 1 | 因果链覆盖率 | 相邻时间段对 100% 有物理因果过渡 | 重写时间段或合并 |
| 2 | 过渡帧可见性 | 过渡帧描述的是可见物理状态，非模糊词 | 替换为具体描述 |
| 3 | 道具唯一性 | 同一道具在原字段时间段组内状态可追溯 | 补全道具状态链 |
| 4 | 声音时序 | 声音在时间段间有延续或衰减描述 | 补全声音过渡 |
| 5 | 叙事意图标注 | 若存在因果黑洞，必须标注为"叙事断裂" | 若非叙事意图则补过渡 |
| 6 | 过渡帧时长 | 符合速度-时长对照表 | 按表格调整 |

## Output Format

完整原字段标题下时间段输出格式：

```text
<上游画面性字段标题>：
[起始秒-结束秒]：<第一段完整描述，包含当前运动/道具/光色的具体状态>；<本镜终点可见落点>。
[下一起始秒-下一结束秒]：<第二段描述，融入物理因果链的过渡锚点>；<本镜终点可见落点>。
[下一起始秒-下一结束秒]：<第三段描述，延续第二段末尾锚点>。
```

---

**关联契约**：
- `shot-continuity-contract.md` — 镜头连续性基础规则
- `transition-design-contract.md` — 边界交出和场景切换规则
- `visual-sequence-alignment-contract.md` — 段落级视觉序列对齐规则

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does every adjacent `时间段 -> 时间段+1` pair inside one block have a physical causal transition unless a narrative fracture is explicitly justified? | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `steps/cinematography-workflow.md#N6-CONTINUITY` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | intra-shot transition coverage ratio and causal-gap samples |
| Are transition anchors written inline into adjacent time-range sentences rather than as separate transition notes, so the current output format remains a continuous natural storyboard text? | `GATE-CINE-15D` / `GATE-CINE-18` | `FAIL-CINE-05AB` / `FAIL-CINE-05G` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` / `steps/cinematography-workflow.md#N7-INJECT` | `inline_projection` samples and cleanup of detached transition-note lines |
| Is each transition frame a visible physical state change rather than a vague word such as "suddenly", "hard cut" or "too fast to see"? | `GATE-CINE-15D` / `GATE-CINE-08` | `FAIL-CINE-05AB` / `FAIL-CINE-05B` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` / `steps/cinematography-workflow.md#N7-INJECT` | before/after transition-frame lines and visible-state evidence |
| Are movement continuity anchors tracking exit position, entry condition, transition frame and velocity curve for the same moving body or object? | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `steps/cinematography-workflow.md#N6-CONTINUITY` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | movement anchor samples and velocity/position continuation checks |
| Are prop state anchors using one stable object identity and traceable previous, transition and next states rather than jumping from action to result? | `GATE-CINE-15D` / `GATE-CINE-24` | `FAIL-CINE-05AB` / `FAIL-CINE-05S` | `steps/cinematography-workflow.md#N6-CONTINUITY` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | prop identity/state chain evidence and admitted-prop justification |
| Do sound timeline anchors state the source, incoming tail, interruption or outgoing source so sound bridges do not become abstract continuity claims? | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | sound source/tail/turnover samples |
| Do light/color anchors explain previous light, transition light, next light and motivation without contradicting the scene light baseline? | `GATE-CINE-15D` / `GATE-CINE-30` | `FAIL-CINE-05AB` / `FAIL-CINE-05Y` | `steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | light-color transition samples and baseline compatibility notes |
| If a causal gap remains, is it marked as legitimate narrative rupture, memory flash, scare interruption or rhythm break rather than accidental discontinuity? | `GATE-CINE-15D` / `GATE-CINE-05` | `FAIL-CINE-05AB` / `FAIL-CINE-05D` | `steps/cinematography-workflow.md#N5-RHYTHM` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | fracture justification and rhythm intent evidence |
| Are examples and output formats treated as illustrative, not copied as fixed action, prop, duration or transition wording? | `GATE-CINE-17A` / `GATE-CINE-18` | `FAIL-CINE-05REF` / `FAIL-CINE-05G` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N7-INJECT` | reference non-template statement and example-pattern cleanup |
