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
| 必需 | `projects/<项目名>/3-Detail/第N集.json` | 由 `2-Global` 已 seed 的 shared episode root；默认第一结构化输入 |
| 可选 | `projects/<项目名>/2-Global/全局风格.md` | 兼容回退或审计时使用的项目级风格底座 |
| 可选 | `projects/<项目名>/2-Global/类型元素.md` | 兼容回退或审计时使用的项目级类型化导演协议 |
| 可选 | `projects/<项目名>/2-Global/导演意图.md` | 兼容回退或审计时使用的当前集按组导演构思主稿 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/<项目名>/3-Detail/第N集.json` | 当前集唯一 episode 根文件 |
| validation | `projects/<项目名>/3-Detail/validation-report.md` | 阶段验收与返工入口 |
| internal artifacts | `plan + patch / note / report` | skill 内部能力链返回的思考计划与局部增量 |

## Naming Contract

- `detail_mission_brief`
- `scope_plan`
- `bootstrap_patch`
- `skeleton_plan`
- `skeleton_patch`
- `core_patch_set`
- `finish_patch_set`
- `camera_decision_note`
- `camera_academy_hit_note`
- `cinematography_brief`
- `cinematography_academy_hit_note`
- `group_lighting_note`
- `continuity_note`
- `continuity_report`
- `audit_report`
- `writeback_patch_set`
- `synthesis_report`

## Field Slot Contract

| 内部能力链 | 默认返回 | 主字段槽位 | 说明 |
| --- | --- | --- | --- |
| `scope_bootstrap_engine` | `plan + patch + report` | `metadata`、命中切片索引、`组间设计` 继承校验、bootstrap 落点 | 锁定写回范围、上游 seed 完整性与根文件存在性 |
| `shot_skeleton_engine` | `plan + patch + report` | `分镜ID`、`时间段`、shot coverage、组级拆镜顺序 | 先给骨架，不直接写完整 shot 文案 |
| `structural_staging_engine` | `patch + note + report` | `分镜表现`、`景别`、`镜头属性`、`镜头框架`、`镜头类型`、`镜头视角`、`场景及方位`、`角色及站位和穿搭`、`道具及状态` | 负责空间结构、观看路径、镜头描述子槽、几何关系与道具底座 |
| `performance_engine` | `patch + note + report` | `角色表现`、`角色及站位和穿搭` 的表演补丁 | 吸收内心 / 动作 / 对手戏三种子模式 |
| `atmosphere_engine` | `patch + note + report` | `场景氛围` | 负责时间感、空气感与情绪气候 |
| `camera_movement_engine` | `patch + note + report` | `运镜手法` | 先锁默认叙事路线与运动动机，条件生成 `camera_academy_hit_note`，再形成默认路线并条件追加挑战方案 |
| `cinematography_engine` | `patch + note + report` | `摄影美学` | 先回看项目级摄影底座，再产出光位 / 组级光影推进 / 色彩子证据，最后合成 final look |
| `transition_fx_engine` | `patch + note + report` | `转场特效` | 只在存在明确叙事收益时补强 |
| `continuity_review_engine` | `note + report` | completeness / continuity / readability verdict | 不直接生成业务字段 |
| `source_audit_engine` | `report` | schema / lineage / overreach verdict | 不直接生成业务字段 |

## Merge Precedence

1. `scope_bootstrap_engine` 先锁命中切片、`组间设计` 继承完整性与 preset 保护范围。
2. `shot_skeleton_engine` 先锁 shot skeleton。
3. `structural_staging_engine` 中由节拍/景别与构图判断先行，再收束镜头描述子槽、空间/道具底座与几何关系。
4. `performance_engine` 只在已锁 skeleton 上补表演，不得反向重排镜序。
5. `camera_movement_engine` 里 `叙事派` 是默认主路由；需先生成 `narrative_route_note -> movement_reason_note -> camera_academy_hit_note`，再形成默认 patch；挑战方案只作为对照，不自动覆盖。
6. `cinematography_engine` 中先生成 `cinematography_brief`、视觉控制线与 `cinematography_academy_hit_note`，再并行产出光位与色彩子补丁，随后串行补 `group_lighting_note`，最后由摄影总协调合成最终 `摄影美学`。
7. `transition_fx_engine` 先判断是否需要转场，再判断是否需要特效桥接。
8. `continuity_review_engine` 与 `source_audit_engine` 只读合成后的 candidate，不反向写业务字段。

## Hard Rules

1. `projects/<项目名>/3-Detail/第N集.json` 是唯一 canonical 输出。
2. 所有内部能力链只能返回 `plan + patch / note / report`，不能直接落盘 JSON。
3. 没有 `shot_skeleton_engine` 产出的 skeleton，不得让其他能力链自行发明 `分镜ID` 或改写镜序。
4. `2-Global` 已 seed 的 `组间设计` 默认只允许继承与消费；若需改写，必须在 `report` 中显式说明返工原因。
5. 读取到 `respect_storyboard_presets` 或 `preserve_only` 时，不得越权重排已锁定的 shot order。
6. `continuity_review_engine` 与 `source_audit_engine` 拥有 veto / rework 建议权，但不拥有 canonical 写回权。
