# Spatial Continuity Contract

本文件定义 `分镜画面` 在同一场景、多分镜、正反打和角色移动中的三维空间一致性规则。空间一致性不是把场景参照图当作平面背景复用，而是先建立当前桥段的 3D 空间模型，再把每个分镜中的角色、道具和机位落到该模型中。

## Core Principle

- 场景参照图只提供环境风格、材质、结构线索和可见锚点，不等于每个分镜都应使用同一面背景。
- 每个同场景分镜必须在同一个三维空间模型中定位：角色站位、身体朝向、视线方向、起始点、终止点、移动轨迹、前后景遮挡、关键道具相对位置、门窗/桌椅/通道等固定锚点和镜头轴线。
- 当前 prompt 可以因正反打、反向机位、角色转身或移动而显示完全不同的墙面或背景面，但必须能回溯到同一个空间坐标关系。
- `Primary anchor` 和 `Support anchors` 必须由当前四段式分镜的单镜画面真相优先决定，而不是直接继承三段式分镜组的主场景名称。若某组归属“大阪城军议间”，但当前单镜实际画面是城门、黑瓦飞檐、战船桅杆、海图、密报纸面、油绢或其他蒙太奇 / 插入 / 转场画面，则主锚点必须重投影到这些当前可见对象；分组场景只保留为风格、剧情归属或后续空间回接线索。

## 3D Space Model

组织 prompt 前，先用 `8-分组`、上一生成图、场景设计图和分镜明细建立轻量空间模型：

```yaml
space_model:
  scene_id:
  fixed_anchors:
    - anchor:
      position_relation:
  axis_definition:
    x_axis: "left-right relation in the room"
    y_axis: "foreground-background / north-south relation"
    z_axis: "height relation"
  camera_axis:
    line_of_action:
    screen_direction_rule:
  characters:
    - name:
      start_position:
      end_position:
      movement_path:
      facing_direction:
      eyeline_target:
      occlusion_relation:
  props:
    - name:
      position_relation:
```

不要求输出真实数学坐标，但必须输出可审查的相对空间关系。优先使用“相对于固定锚点”的描述，例如“林寂站在教师讲台右前方，面向教室后排；红苹果在她与第一排课桌之间”。

## Fixed Anchor Locking Method

固定锚点锁定不是“找一个好看的背景”，而是建立一套跨镜头不漂移的空间参照系。每个同场景桥段必须按以下步骤执行：

1. **列出候选锚点**
   从 `8-分组`、场景设计图、上一生成图和分镜文本中提取不会随角色动作移动的对象：门、窗、讲台、黑板、桌椅阵列、床、楼梯口、走廊拐角、柱子、柜台、祭坛、车门、路牌、桥栏、灯源、墙面装饰、地面边线等。

2. **筛选主锚点和辅助锚点**
   主锚点优先满足三项：稳定不移动、可在多个镜头中推断、能定义空间方向。辅助锚点用于确认深度和遮挡。每个场景至少锁定 `1` 个主锚点和 `2` 个辅助锚点；若信息不足，必须记录 `insufficient_spatial_evidence`。

3. **定义三轴**
   用锚点定义相对坐标，而不是凭直觉写左右：
   - `x_axis`: 场景内左右关系，例如黑板左端到教室门。
   - `y_axis`: 深度关系，例如讲台到后排、走廊入口到尽头、门外到室内。
   - `z_axis`: 高度关系，例如楼梯上下、阳台/一楼、站立/坐下/俯身。

4. **锁定角色相对锚点**
   每个角色都写成“相对锚点的位置”，例如“角色 A 在讲台右前方一米，背对黑板，面向后排门口”，而不是“角色 A 在左边”。当机位反向时，屏幕左右可能反转，但锚点关系不能反转。

5. **锁定移动路径**
   若角色移动，必须记录 `start_anchor -> path_anchor -> end_anchor`。例如“从走廊拐角进入门框，沿第一排课桌外侧走到讲台前”。移动路径不得穿越不可穿越锚点，如墙、桌阵、栏杆，除非剧情明确。

6. **锁定镜头轴线**
   用主锚点和角色关系定义 line of action。对话、追逐、对峙、交接等都必须有轴线说明；反打、侧拍、俯拍可以改变可见背景面，但不得让角色相对轴线无理由跳边。

7. **逐镜投影**
   每个分镜都把 3D 模型投影成当前画面：当前可见锚点、不可见但仍约束角色位置的锚点、角色在前/中/后景的位置、镜头朝向和背景面。不可见锚点仍应在 `Spatial Continuity Plan` 中保留。

8. **漂移检查**
   prompt 交付前检查：角色是否瞬移、视线是否闭合、道具是否跳位、背景面变化是否由机位解释、遮挡是否符合前后景、移动路径是否穿帮。任一失败必须返工。

## Shot-Specific Anchor Projection

每个四段式分镜都必须执行 `shot_anchor_projection`。这是从三段式分镜组空间模型投影到当前单镜画面的必经步骤，尤其用于蒙太奇、插入镜、道具特写、转场镜头、旁白画面、远景建立镜头和同组内临时换地点画面。

### Trigger Cases

以下情况必须重投影锚点，不得沿用分组场景的默认主锚点：

- 当前 `分镜N` 的画面主体不是分组主场景中的核心结构，例如分组场景写“大阪城军议间”，但单镜画面写黑瓦飞檐、城门、城墙、雨夜战船、海图朱线或密报纸面。
- 当前镜头是旁白蒙太奇、证据链插入、形态匹配转场、微距道具特写、远景建立镜头、过场环境镜头或不包含角色的空间 / 道具主体镜头。
- 当前镜头的 `Focus on` 明显落在物件、纹理、光源、门窗、船帆、桅杆、纸面、布料、刀锋、油绢、铜镜、木牌、血迹、水面等局部主体，而不是场景总空间。
- 当前分镜组在同一 `## x-y-z` 内压缩多个地点或视觉层，例如“黑木崖火场与高野山镜廊”“日出号甲板至琉球王宫偏殿”。

### Projection Order

1. **读取当前单镜真相**：只看当前四段式分镜对应的 `分镜N`、其直接 `旁白画面 / 动作画面 / 道具特写 / 转场 / 环境描写` 和必要入场/出场桥段，不把整组后续动作合并进来。
2. **判定画面主体类型**：在 `character_action`、`prop_insert`、`environment_establishing`、`montage_insert`、`transition_match`、`macro_texture`、`ship_or_route`、`crowd_or_battlefield`、`dialogue_blocking` 等类型中选择最贴近当前镜头的一项或两项。
3. **抽取当前可见候选锚点**：优先从当前单镜画面中的固定对象抽取，例如飞檐、城门、船桅、跳板、桌面纸张、朱线、刀尖、布纹针脚、铜镜边、窗棂、酒葫芦、船舷、港口木栈、盐袋、暗巷刀鞘。
4. **筛选单镜主锚点**：选择最能定义当前构图和动作/视线/材质关系的对象作为 `primary_anchor`。它必须在当前画面中可见或被当前分镜明细强约束，不得只是分组场景里的常规家具或背景。
5. **保留桥段空间回接**：如果当前主锚点不是分组主场景锚点，仍可在 `supporting_anchors` 或 `scene_space_model` 中记录分组场景锚点，用于说明它是视觉蒙太奇、转场或证据链的一部分，但不能抢占 `primary_anchor`。
6. **定义单镜三轴**：围绕当前主锚点定义 `x/y/z`，例如飞檐到城门的垂直下摇、海图朱线的路线轴、油绢纤维的表面轴、船头到船尾的深度轴、港口水线到暗巷的威胁轴。
7. **写入英文 prompt 本体**：`Primary anchor:` 与 `Support anchors:` 必须使用单镜重投影后的结果；`Spatial blocking:` 必须说明当前主体如何相对这些锚点布置。

### Evidence Requirements

`Spatial Continuity Plan` 中必须能看到：

- `shot_anchor_projection_status: projected_from_current_frame | inherited_scene_anchor_with_reason | insufficient_spatial_evidence`
- `source_frame_anchor_evidence`: 当前单镜文本中支持主锚点的短证据。
- `primary_anchor`: 当前单镜主锚点。
- `supporting_anchors`: 当前单镜辅助锚点；可包含分组场景回接锚点，但必须标明用途。
- `anchor_source_priority`: `current_shot_truth > previous_generated_frame > scene_reference_image > group_scene_default`。

只有当当前单镜画面确实就是分组主场景整体空间，且主场景锚点也在当前画面中承担构图中心时，才允许 `inherited_scene_anchor_with_reason`。

## Anchor Pattern Library

以下是除正反打外，常见需要空间锚定的桥段类型：

| pattern | fixed anchors | must lock | common failure |
| --- | --- | --- | --- |
| 追逐 / 逃跑 | 门、走廊拐角、楼梯口、路灯、车辆、墙角 | 追逃双方起点、间距、转弯方向、前后景、终点 | 追赶者和被追者左右关系跳变，或距离无理由变化 |
| 进门 / 出门 | 门框、门内外地面线、门把手、室内主物件 | 门外/门内方向、进入落点、镜头在门哪一侧 | 角色刚进门却出现在房间深处，或门内外方向反了 |
| 多人围站 / 对峙 | 桌子、尸体、讲台、火堆、中心道具 | 每人相对中心物的位置、朝向、距离、视线目标 | 人物绕中心物无理由换位 |
| 绕物移动 | 桌、床、车、柜台、祭坛、柱子 | 绕行方向、当前位于物体哪一侧、遮挡物前后关系 | 角色穿过固定物，或绕行方向前后不一致 |
| 上下楼 / 垂直空间 | 楼梯扶手、平台、栏杆、上下楼口 | 谁在上方/下方、仰俯视、上下移动方向、z 轴高度差 | 上下关系被拍成同一平面 |
| 过肩 / 主观视角 | 观察者肩线、被观察者、视线目标、两人间中心线 | 观察者位置、被观察者位置、肩线方向、视线闭合 | 主观视角位置与上一镜角色位置不一致 |
| 进入遮挡 / 离开遮挡 | 门框、柱子、窗帘、书架、人群、车辆 | 遮挡物前后层级、角色出现/消失方向 | 角色从不可能的位置冒出，遮挡层级反了 |
| 道具交接 | 双方手部位置、桌面、托盘、地面落点 | 递出方向、接收方向、道具移动路径、最终落点 | 道具在未交接前后跳位 |
| 群体移动 / 队列 | 队首、队尾、门、通道边线、路标 | 队列方向、主角在队伍中的位置、队伍前后关系 | 主角从队尾无理由跳到队首 |
| 同场景换机位 | 主锚点、角色轴线、可见背景面 | 机位在哪侧、镜头看向哪里、为什么背景变化 | 把换机位误判为换场景，或背景变了但轴线不成立 |
| 环绕 / 旋转镜头 | 中心人物/物体、地面标记、光源、背景面序列 | 镜头绕行方向、每一角度对应的背景面 | 环绕方向反复变化，背景面顺序错乱 |
| 分层空间窥视 | 窗、门缝、栏杆、玻璃、监控屏 | 观察者层、被观察者层、视线穿过的介质 | 观察者与被观察者空间层级混淆 |
| 坐下 / 起身 / 俯身 | 椅子、桌沿、床边、地面、角色脚位 | 身体高度变化、脚位是否移动、手扶锚点 | 起身后位置平移，或高度关系不合理 |
| 物体坠落 / 抛掷 | 起手点、轨迹经过锚点、落点、遮挡物 | 抛物线方向、落点相对锚点、谁在轨迹前后 | 物体飞行方向与角色动作方向相反 |
| 车辆 / 电梯 / 门禁移动 | 车门、电梯门、按钮、轨道、道路方向 | 进入/离开方向、载具朝向、停靠点、相对人位 | 车门方向、道路方向或电梯内外关系跳变 |

## Character Blocking Requirements

每个同场景分镜 prompt 必须明确：

1. 角色在 3D 空间中的当前位置，而不是只写“在教室里”。
2. 若角色移动，写清 `start_position -> movement_path -> end_position`。
3. 若角色不移动，写清其相对固定锚点、面对方向、视线目标和与其他角色的距离关系。
4. 若画面只显示半身、背影、肩后视角或局部，仍需在 prompt 或 `Spatial Continuity Plan` 中保留其场景内真实位置。
5. 遮挡关系必须服从空间顺序：谁在前景、谁在中景、谁被门框/桌椅/身体遮挡。

## Shot Reverse Shot

正反打对话戏尤其不能把背景一致性误解为同一张平面背景：

- 相邻分镜组可能分别拍摄对话双方，因此背景面可以是镜像相对的南北面、东西面或房间两端。
- 反打镜头应保持同一条对话轴线或明确说明越轴理由；角色左右屏幕方向、视线方向和肩线关系必须自洽。
- 若 A 看向 B，A 的 eyeline 与 B 的位置必须能在 3D 空间中闭合；反打中 B 的视线应反向对应 A 的位置。
- 当背景面完全不同，prompt 应明确这是由于机位反向、过肩、正反打或角色转身造成，而不是场景漂移。
- 正反打中可见墙面变化应写成“opposite wall / reverse angle / over-the-shoulder from B toward A”等空间关系，而不是简单复制上一镜背景。

## Prompt Integration

`Integrated AIGC image prompt` 必须消费 `Spatial Continuity Plan`：

- 在英文 prompt 中写入当前角色的三维站位、朝向、视线、移动轨迹和关键锚点。
- 若是正反打，写明 camera side、reverse angle、opposite background plane、line of action 和 eyeline match。
- 允许为了画面清晰压缩细节，但不得删除会导致角色瞬移、轴线跳变或背景面误读的空间关系。

## Failure Modes

以下情况必须返工：

- 只用场景参照图当平面背景，没有定位角色在 3D 空间中的站位。
- 当前镜头是蒙太奇、插入镜、转场或道具特写，却直接沿用分组主场景锚点，导致 `Primary anchor` 与 `Source truth` 不匹配。
- 同一角色在连续镜头中无理由瞬移、转向或跨越固定锚点。
- 正反打镜头要求同一背景面，或背景面变化没有由机位反向/轴线关系解释。
- 角色视线无法在空间中闭合，例如 A 看向右侧但 B 被设定在 A 的左侧。
- 道具相对位置漂移，例如桌面道具在没有移动事件时从角色前方跳到身后。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 同场景分镜是否先建立轻量 3D `space_model`，而不是把场景参照图当作每镜复用的平面背景？ | `G3B-3D-SPATIAL-CONTINUITY` | `FAIL-FRAME-SPATIAL` | `N4B-SPATIAL` | `Spatial Continuity Plan` 包含 `space_model`、fixed anchors、axis_definition、camera_axis、角色/道具相对位置。 |
| 固定锚点是否经过候选列举、主/辅锚点筛选、三轴定义、角色相对锚点、移动路径、镜头轴线和漂移检查，而不是只写“同一场景背景”？ | `G3B-3D-SPATIAL-CONTINUITY` | `FAIL-FRAME-SPATIAL` | `N4B-SPATIAL` | plan 记录 `candidate_anchors`、`primary_anchor`、至少两个 `supporting_anchors`、`x/y/z axis`、`movement_paths`、`drift_check`。 |
| 每个四段式分镜是否执行 `shot_anchor_projection`，从当前单镜真相重投影 Primary/Support anchors，而非直接继承三段式分组主场景锚点？ | `G3E-SHOT-ANCHOR-PROJECTION` | `FAIL-FRAME-SHOT-ANCHOR` | `N4B-SPATIAL` | plan 记录 `shot_anchor_projection_status`、`source_frame_anchor_evidence`、`anchor_source_priority: current_shot_truth > previous_generated_frame > scene_reference_image > group_scene_default`。 |
| 蒙太奇、插入镜、道具特写、转场、路线图、战船远景或同组临时换地点画面是否把主锚点落到当前可见主体，而不是沿用分组主场景常规家具/背景？ | `G3E-SHOT-ANCHOR-PROJECTION` | `FAIL-FRAME-SHOT-ANCHOR` | `N4B-SPATIAL` / `N4-PROMPT` | prompt 与 plan 中的 `Primary anchor` 可从当前 `source_frame_anchor_evidence` 直接找到；分组场景锚点只作 supporting / continuity 回接。 |
| 追逐、进出门、围站、绕物、上下楼、过肩、遮挡、道具交接、队列、换机位、环绕、窥视、起坐、抛掷、载具移动等桥段是否匹配对应锚定模式？ | `G3B-3D-SPATIAL-CONTINUITY` | `FAIL-FRAME-SPATIAL` | `N4B-SPATIAL` | plan 记录 `anchor_pattern`、固定锚点、must lock 项和 common failure 检查结果。 |
| 每个角色是否有 3D 当前位置、起点/终点/移动轨迹、身体朝向、视线目标、前中后景和遮挡关系？ | `G3B-3D-SPATIAL-CONTINUITY` | `FAIL-FRAME-SPATIAL` | `N4B-SPATIAL` / `N4-PROMPT` | `character_positions` 与英文 prompt 本体均写入相对锚点的站位、走位、朝向、视线和 occlusion。 |
| 正反打、过肩、反向机位或对话戏是否保持 line of action、screen direction、opposite background plane 和 eyeline match，而不强求同一背景面？ | `G3B-3D-SPATIAL-CONTINUITY` | `FAIL-FRAME-SPATIAL` | `N4B-SPATIAL` / `N4-PROMPT` | plan / prompt 记录 camera side、reverse angle、opposite wall/background plane、line of action、eyeline match；背景变化有机位解释。 |
| `Integrated AIGC image prompt` 是否实际消费 Spatial Continuity Plan，将角色三维站位、移动轨迹、关键锚点、轴线和正反打逻辑写进英文画面语言？ | `G3D-PROMPT-DESIGN-SYSTEM` | `FAIL-FRAME-PROMPT-SYSTEM` | `N4-PROMPT` | 英文 prompt 本体可见 `Primary anchor` / `Support anchors` 的自然表达、spatial blocking、camera axis、background plane logic，而非只停留在结构化字段。 |
| 漂移检查是否能发现角色瞬移、视线不闭合、道具跳位、移动路径穿越不可穿越锚点、遮挡层级错误或背景面无法解释？ | `G3B-3D-SPATIAL-CONTINUITY` | `FAIL-FRAME-SPATIAL` | `N4B-SPATIAL` / `N6-REVIEW` | review note 记录 `drift_check` 项；失败项指向具体 `shot_id`、锚点和返工节点。 |
