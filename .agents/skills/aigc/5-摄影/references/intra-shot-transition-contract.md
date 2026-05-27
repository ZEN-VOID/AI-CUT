# Transition Anchor Contract

本文件定义分镜间「过渡锚点」的标准描述格式和执行规则。过渡锚点是连接相邻分镜的视觉/听觉接口，确保镜头流转连贯而非断裂。本契约是 `shot-continuity-contract.md` 的延续，专注于分镜明细内部的连续性设计。

## Example Usage Guard

本文件所有示例、正例、反例和标准格式仅用于说明过渡锚点的判断逻辑，不是固定分镜模板。执行具体任务时，不得复用示例中的武器、鱼鳞、链条、礁石、句式或动作组合；必须从当前画面句子的真实运动体、接触点、声音、光色和连续性需求中生成自己的过渡锚点。

## Core Rule

每个分镜块的 `分镜N` 之间必须存在**物理因果链过渡**。相邻分镜的交接处必须找到：同一运动体的位置延续、同一道具的形态变化、同一声音的时序延伸，或同一光色的明暗过渡。

**禁止**：
- 在两个分镜之间留下"因果黑洞"——动作A直接跳到结果C，中间没有B
- 用硬切代替过渡锚点描述
- 把"断裂""制造断裂"当作优点描述，除非断裂本身是叙事意图

## Transition Anchor Types

### 1. 运动延续锚点（Movement Continuity Anchor）

描述同一运动体在相邻分镜间的位置、速度、方向变化。

| anchor_field | description |
| --- | --- |
| `exit_position` | 运动体在本分镜结尾的位置 |
| `entry_condition` | 运动体在下一分镜入口的初始状态 |
| `transition_frame` | 连接两者的0.2-0.5秒过渡帧描述 |
| `velocity_curve` | 速度变化：加速/匀速/减速/急停 |

**标准格式**：
```
分镜1（约X秒）：<当前运动描述>；<本镜终点位置/速度>。
→ 过渡帧（约0.2-0.5秒）：<运动体在接触点的瞬间状态>。
分镜2（约X秒）：<下一运动的起点和延续方式>。
```

**示例**：
```
✅ 分镜1（约1秒）：十字枪刃以水平横扫擦过画面中轴，枪尖从左缘进入右缘；金属刃面在雾光里划出一道蓝冷横线。
→ 过渡帧（约0.3秒）：枪尖咬入鱼篓边缘的瞬间，篾条在刃压下崩裂，银鳞从裂口挤射而出。
分镜2（约1秒）：鱼鳞在雾光中拉出弧形轨迹，镜头用快速甩镜跟住鳞片飞行曲线。

❌ 分镜1（约1秒）：十字枪刃以水平横扫擦过画面中轴。
分镜2（约1秒）：鱼鳞在雾光中拉出弧形轨迹。（没有枪刃接触鱼篓的过渡）
```

### 2. 道具形态锚点（Prop State Anchor）

描述同一道具在相邻分镜间的形态变化。

| anchor_field | description |
| --- | --- |
| `object_identity` | 道具在同一分镜组内保持唯一指认 |
| `previous_state` | 道具在上一分镜结尾的状态 |
| `transition_state` | 道具在过渡帧的形态变化瞬间 |
| `next_state` | 道具在下一分镜入口的状态 |

**标准格式**：
```
分镜N（约X秒）：<道具当前状态>；<与上一镜的因果关系>。
→ 过渡帧（约0.2-0.5秒）：<道具形态变化的瞬间>。
分镜N+1（约X秒）：<道具在下一镜的延续状态>。
```

**示例**：
```
✅ 分镜1（约1秒）：枪尾短链从画面右侧甩入前景，铁环在雾里拖出一道冷弧。
→ 过渡帧（约0.3秒）：倒钩咬进肩胛的瞬间，布料在铁尖崩裂，碎片挂在刃上。
分镜2（约1.5秒）：链条带着后生身体向后拖行，挂在枪尖的布片在雾里轻抖。

❌ 分镜1（约1秒）：枪尾短链甩入前景，倒钩咬进肩胛。
分镜2（约1.5秒）：后生身体撞向礁角。（没有倒钩接触肩胛、布料崩裂的过渡）
```

### 3. 声音时序锚点（Sound Timeline Anchor）

描述声音在相邻分镜间的延续或衰减。

| anchor_field | description |
| --- | --- |
| `sound_source` | 声音来源的实体 |
| `sound_type` | 声音类型：撞击/拖行/嗡鸣/回响 |
| `incoming_tail` | 上一分镜声音的尾音 |
| `outgoing_source` | 下一分镜声音的来源变化 |

**标准格式**：
```
分镜N（约X秒）：<当前声音描述>，<声音持续状态>。
→ 过渡帧（约0.2-0.5秒）：<声音在分镜间的延续或转接>。
分镜N+1（约X秒）：<下一声音的起点>，<与上一声音的关系>。
```

**示例**：
```
✅ 分镜1（约1秒）：铁链拖行的咔哒声在礁石上留下回响，每一声都像是数着步子。
→ 过渡帧（约0.3秒）：最后一节链环磕在石棱上，撞击声突然变闷，被布料撕裂声切断。
分镜2（约1秒）：布料撕裂的脆响盖过链声，肩胛处的衣料在枪尖下崩裂。

❌ 分镜1（约1秒）：铁链拖行声在礁石上留下回响。
分镜2（约1秒）：布料撕裂的脆响。（没有声音之间的过渡说明）
```

### 4. 光色明暗锚点（Light Color Anchor）

描述光色在相邻分镜间的明暗过渡。

| anchor_field | description |
| --- | --- |
| `previous_lighting` | 上一分镜的光色状态 |
| `transition_light` | 过渡帧的光色变化 |
| `next_lighting` | 下一分镜的光色状态 |
| `light_motivation` | 光变的原因（道具遮挡、动作遮光、自然变化） |

**标准格式**：
```
分镜N（约X秒）：<当前光色状态>，<光源位置>。
→ 过渡帧（约0.2-0.5秒）：<光色变化的瞬间>。
分镜N+1（约X秒）：<下一光色状态>，<光源变化原因>。
```

## Transition Anchor 位置规则

### 分镜块内位置

| 分镜数量 | 过渡锚点位置 | 规则 |
| --- | --- | --- |
| 2个分镜 | 分镜1结尾→分镜2开头 | 必须有1个过渡帧 |
| 3个分镜 | 分镜1结尾→分镜2开头；分镜2结尾→分镜3开头 | 必须有2个过渡帧 |
| 4+个分镜 | 每两个相邻分镜之间 | 必须有（N-1）个过渡帧 |

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
| `intra_shot_transition` | 当前分镜块内相邻分镜之间是否存在物理因果链过渡 |
| `transition_type` | 运动延续/道具形态/声音时序/光色明暗（可多选） |
| `transition_duration` | 过渡帧时长估算（0.2-0.5秒/0.5-1秒） |
| `causal_gap` | 是否存在因果黑洞（无过渡的断裂）；若有，必须说明是否为叙事意图 |
| `anchor_evidence` | 过渡锚点的具体描述（可被下游验证） |

## Decision Rules

1. **因果链强制**：所有相邻分镜之间必须存在物理因果过渡，除非：
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
   - 每个分镜块内，相邻分镜之间的过渡锚点描述覆盖率应达到 100%
   - 覆盖率 = 有过渡锚点描述的相邻分镜对数 / 总相邻分镜对数

## Anti-Patterns

### 因果黑洞类

- ❌ 分镜1：枪刃横扫。分镜2：鱼鳞飞出。（没有刃-篓接触的瞬间）
- ❌ 分镜1：拳头挥出。分镜2：对手倒地。（没有击中的过渡）
- ❌ 分镜1：链条甩出。分镜2：人撞上礁石。（没有钩-肉接触的瞬间）

### 模糊替代类

- ❌ "枪刃突然削开鱼篓"（用"突然"掩盖过渡缺失）
- ❌ "画面一裂，鳞片已经飞在空中"（用"一裂"代替因果描述）
- ❌ "来不及看清，人已经撞上去了"（用叙事借口掩盖连续性断裂）

### 自毁式断裂类

- ❌ "制造断裂"作为优点描述（除非是叙事意图）
- ❌ "硬切到下一动作"（硬切不是过渡锚点）
- ❌ "用镜头断裂表现震惊"（震惊应通过角色反应镜头而非分镜断裂表现）

## Audit Checklist

每个分镜块在输出前必须通过以下检查：

| # | 检查项 | 标准 | 若不合格 |
| --- | --- | --- | --- |
| 1 | 因果链覆盖率 | 相邻分镜对100%有物理因果过渡 | 重写分镜或合并 |
| 2 | 过渡帧可见性 | 过渡帧描述的是可见物理状态，非模糊词 | 替换为具体描述 |
| 3 | 道具唯一性 | 同一道具在分镜块内状态可追溯 | 补全道具状态链 |
| 4 | 声音时序 | 声音在分镜间有延续或衰减描述 | 补全声音过渡 |
| 5 | 叙事意图标注 | 若存在因果黑洞，必须标注为"叙事断裂" | 若非叙事意图则补过渡 |
| 6 | 过渡帧时长 | 符合速度-时长对照表 | 按表格调整 |

## Output Format

完整分镜块输出格式：

```text
动作画面：<动作描述>
分镜明细：
分镜1（约X秒）：<分镜1完整描述，包含当前运动/道具/光色的具体状态>；<本镜终点可见落点>。
→ 过渡帧（约0.2-0.5秒）：<过渡锚点描述——物理因果链的B点>。
分镜2（约X秒）：<分镜2描述，延续过渡帧的起点>；<本镜终点可见落点>。
→ 过渡帧（约0.2-0.5秒）：<第二个过渡锚点描述>。
分镜3（约X秒）：<分镜3描述，延续第二个过渡帧>。
```

---

**关联契约**：
- `shot-continuity-contract.md` — 镜头连续性基础规则
- `transition-design-contract.md` — 边界交出和场景切换规则
- `visual-sequence-alignment-contract.md` — 段落级视觉序列对齐规则

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does every adjacent `分镜N -> 分镜N+1` pair inside one block have a physical causal transition unless a narrative fracture is explicitly justified? | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `steps/cinematography-workflow.md#N6-CONTINUITY` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | intra-shot transition coverage ratio and causal-gap samples |
| Is each transition frame a visible physical state change rather than a vague word such as "suddenly", "hard cut" or "too fast to see"? | `GATE-CINE-15D` / `GATE-CINE-08` | `FAIL-CINE-05AB` / `FAIL-CINE-05B` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` / `steps/cinematography-workflow.md#N7-INJECT` | before/after transition-frame lines and visible-state evidence |
| Are movement continuity anchors tracking exit position, entry condition, transition frame and velocity curve for the same moving body or object? | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `steps/cinematography-workflow.md#N6-CONTINUITY` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | movement anchor samples and velocity/position continuation checks |
| Are prop state anchors using one stable object identity and traceable previous, transition and next states rather than jumping from action to result? | `GATE-CINE-15D` / `GATE-CINE-24` | `FAIL-CINE-05AB` / `FAIL-CINE-05S` | `steps/cinematography-workflow.md#N6-CONTINUITY` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | prop identity/state chain evidence and admitted-prop justification |
| Do sound timeline anchors state the source, incoming tail, interruption or outgoing source so sound bridges do not become abstract continuity claims? | `GATE-CINE-15D` | `FAIL-CINE-05AB` | `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | sound source/tail/turnover samples |
| Do light/color anchors explain previous light, transition light, next light and motivation without contradicting the scene light baseline? | `GATE-CINE-15D` / `GATE-CINE-30` | `FAIL-CINE-05AB` / `FAIL-CINE-05Y` | `steps/cinematography-workflow.md#N6.3-SCENE-VISUAL-CONSTRAINT` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | light-color transition samples and baseline compatibility notes |
| If a causal gap remains, is it marked as legitimate narrative rupture, memory flash, scare interruption or rhythm break rather than accidental discontinuity? | `GATE-CINE-15D` / `GATE-CINE-05` | `FAIL-CINE-05AB` / `FAIL-CINE-05D` | `steps/cinematography-workflow.md#N5-RHYTHM` / `steps/cinematography-workflow.md#N6.5-SHOT-PLAN` | fracture justification and rhythm intent evidence |
| Are examples and output formats treated as illustrative, not copied as fixed action, prop, duration or transition wording? | `GATE-CINE-17A` / `GATE-CINE-18` | `FAIL-CINE-05REF` / `FAIL-CINE-05G` | `review/review-contract.md#Reference-Review-Gate-Matrix` / `steps/cinematography-workflow.md#N7-INJECT` | reference non-template statement and example-pattern cleanup |
