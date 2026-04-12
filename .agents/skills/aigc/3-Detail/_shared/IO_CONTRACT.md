# 3-Detail Shared I/O Contract

本文件是 `aigc/3-Detail` 的输入输出、命名与 field-slot 合成单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/<项目名>/1-Planning/3-分组/第N集.md` | 当前集组级主输入 |
| 可选 | `projects/<项目名>/1-Planning/3-分组/第N集.grouping.json` | 组序、锁轴与机读 handoff |
| 必需 | `projects/<项目名>/0-Init/north_star.yaml` | 项目目标与风格方向 |
| 必需 | `projects/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段高层 handoff |
| 可选 | `projects/<项目名>/0-Init/story-source-manifest.yaml` | 预设、锁轴、保真模式证据 |
| 必需 | `projects/<项目名>/2-Global/全局风格.md` | 项目级风格底座 |
| 必需 | `projects/<项目名>/2-Global/类型指导.md` | 项目级类型化导演协议 |
| 必需 | `projects/<项目名>/2-Global/导演意图.md` | 当前集按组的导演构思主稿 |
| 可选 | `projects/<项目名>/3-Detail/第N集.json` | 已有 episode 根文件，供增量 patch 使用 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/<项目名>/3-Detail/第N集.json` | 当前集唯一 episode 根文件 |
| validation | `projects/<项目名>/3-Detail/validation-report.md` | 阶段验收与返工入口 |
| handoff | `agents_plan + patch / note / report` | subagents 返回给父 skill 的思考计划与局部增量 |

## Naming Contract

- `mission_brief`
- `selected_groups`
- `selected_agents`
- `subagent_brief_<role>`
- `context_packet_<role>`
- `agents_plan_<role>`
- `plan_patch_分镜规划`
- `artifact_patch_<role>`
- `review_note_连续性复核`
- `audit_report_真源审计`
- `synthesis_report`

## Field Slot Contract

| 角色 | 默认返回 | 主字段槽位 | 说明 |
| --- | --- | --- | --- |
| `分镜规划` | `plan_patch + report` | `分镜ID`、`时间段`、shot coverage、组级拆镜顺序 | 先给骨架，不直接写完整 shot 文案 |
| `分镜构图` | `artifact_patch + note` | `分镜表现`、`场景及方位` 的构图补强、`角色及站位和穿搭` 的几何关系与穿搭显著特征 | 负责画面可读性与主体关系 |
| `景观设计` | `artifact_patch + note` | `场景及方位`、`道具及状态` | 负责空间结构、环境元素与道具状态 |
| `氛围设计` | `artifact_patch + note` | `场景氛围` | 负责时间感、空气感与情绪气候 |
| `内心戏指导` | `artifact_patch + note` | `角色表现` | 负责心理活动与情绪内压 |
| `动作戏指导` | `artifact_patch + note` | `角色表现`、`角色及站位和穿搭` 的动作调度补充 | 负责动作节奏与肢体因果 |
| `对手戏指导` | `artifact_patch + note` | `角色表现`、`角色及站位和穿搭` 的关系调度补充 | 负责多角色关系张力 |
| `叙事派` | `artifact_patch + note` | `运镜手法` | 默认路线，优先信息传达与叙事推进 |
| `炫技派` | `artifact_patch + note` | `运镜手法` 的挑战方案 | 只有在显式需要时参与对照 |
| `摄影师` | `artifact_patch + note` | `摄影美学` | 负责摄影总协调与镜头语言合成 |
| `光影美学大师` | `artifact_patch + note` | `摄影美学` 的光线子补丁 | 提供主辅光、明暗戏剧性 |
| `色彩美学大师` | `artifact_patch + note` | `摄影美学` 的色彩子补丁 | 提供色板、色温与情绪色 |
| `转场设计` | `artifact_patch + note` | `转场特效` 或组间过渡 note | 负责衔接与视觉过渡 |
| `特效设计` | `artifact_patch + note` | `转场特效` 的特效子补丁 | 负责必要特效与边界说明 |
| `连续性复核` | `review_note + report` | completeness / continuity / readability verdict | 不直接生成业务字段 |
| `真源审计` | `audit_report` | schema / lineage / overreach verdict | 不直接生成业务字段 |

## Merge Precedence

1. `分镜规划` 先锁 shot skeleton。
2. `景观设计` 先给空间与道具底座，`分镜构图` 再补画面构图与主体关系。
3. `角色表现` 族群按命中问题合成到 `角色表现`，如涉及站位、关系或服装显著特征调整，由父 skill 统一回写 `角色及站位和穿搭`。
4. `叙事派` 是 `运镜手法` 默认主路由；`炫技派` 只作为对照方案，不自动覆盖默认路线。
5. `摄影师` 负责 `摄影美学` 的最终合成；光影与色彩大师只提供子补丁。
6. `转场设计` 先给叙事过渡；`特效设计` 只在必要时补强特效说明。
7. `连续性复核` 与 `真源审计` 只读合成后的 draft，不反向写业务字段。

## Hard Rules

1. `projects/<项目名>/3-Detail/第N集.json` 是唯一 canonical 输出。
2. 所有 subagents 只能返回 `agents_plan + patch / note / report`，不能直接落盘 JSON。
3. 没有 `分镜规划` 的 shot skeleton，不得让专业角色自行发明 `分镜ID` 或改写镜序。
4. 读取到 `respect_storyboard_presets` 或 `preserve_only` 时，不得越权重排已锁定的 shot order。
5. `连续性复核` 与 `真源审计` 拥有 veto / rework 建议权，但不拥有 canonical 写回权。
