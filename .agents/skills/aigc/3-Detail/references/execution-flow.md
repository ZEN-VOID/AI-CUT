# 输入与上下文装配

## 必需输入

1. `projects/<项目名>/1-Planning/3-分组/第N集.md`
2. `projects/<项目名>/2-Global/全局风格.md`
3. `projects/<项目名>/2-Global/类型指导.md`
4. `projects/<项目名>/2-Global/导演意图.md`
5. `projects/<项目名>/0-Init/north_star.yaml`
6. `projects/<项目名>/0-Init/init_handoff.yaml`

## 补充输入

1. `projects/<项目名>/1-Planning/3-分组/第N集.grouping.json`
2. `projects/<项目名>/0-Init/story-source-manifest.yaml`
3. `projects/<项目名>/3-Detail/第N集.json`

## 上下文裁剪规则

- `scope_bootstrap_engine`
  - 读取全量上游证据、现有 root file、用户显式范围与 preset 保护模式。
- `shot_skeleton_engine`
  - 读取当前集全量分组正文、grouping JSON、导演意图中的命中组段落。
- `structural_staging_engine`
  - 读取命中组/镜的 skeleton、导演意图、全局风格、现有 draft。
- `performance_engine`
  - 读取命中镜的 skeleton、构图/空间 draft、导演意图中对应情绪/动作/关系线索，以及 `reference_anchor_note` 中已转译的角色表达锚点。
- `atmosphere_engine`
  - 读取命中镜的空间 draft、全局风格、导演意图与现有摄影草案。
- `camera_movement_engine`
  - 读取命中镜的 core draft、类型指导、导演意图；比较同目标变体时额外读取场景氛围 draft；挑战方案额外读取风格禁区。
- `cinematography_engine`
  - 先读取命中镜的 skeleton、组级节奏、运镜、氛围、全局风格、类型指导、导演意图。
  - 需要时追加读取 `knowledge-base/电影学院派/电影摄影/影像的创造.md` 与 `knowledge-base/电影学院派/电影摄影/摄影创作技法.md`。
  - 命中知识库后先生成 `cinematography_academy_hit_note`，再供光位与色彩阶段共享。
  - 光位与色彩阶段共享 `cinematography_brief + visual_control_note + cinematography_academy_hit_note`。
  - 组级光影推进阶段额外读取 `lighting_patch` 与组内镜序。
  - 总协调阶段再读取 `group_lighting_note + color_patch + cinematography_academy_hit_note`。
- `transition_fx_engine`
  - 读取组内/组间衔接证据、命中镜 finish draft 与风格禁区。
- `continuity_review_engine`
  - 只读取合成后的 candidate，不读未采用草稿。
- `source_audit_engine`
  - 只读取最终 candidate、schema、I/O contract 与输出落点。

# 默认执行流程

## Tranche 0. 输入与阶段门

- 读取 `Init / Planning / 2-Global` 真源。
- 生成：
  - `detail_mission_brief`
  - `scope_plan`
  - `preset_manifest`
  - `reference_anchor_note`
  - `bootstrap_patch`（若根文件不存在）

## Tranche 1. Skeleton

- `shot_skeleton_engine`
  - 输出：
    - `skeleton_plan`
    - `skeleton_patch`
    - `skeleton_report`（若证据不足）
  - 至少锁定：
    - 本轮命中组与 `分镜ID`
    - `时间段`
    - 每镜 `coverage`
    - 哪些初始化预设元素必须在镜头里被看见
    - 哪些参考锚点需要转译进后续表现链
    - preset / lock-axis 不得越权的边界

## Tranche 2. Core 并行

- `structural_staging_engine`
  - 输出 `staging_patch`
- `performance_engine`
  - 内部串行顺序：
    - `锁表演主轴`
    - `锁角色化表达通道`
    - `锁可见信号`
    - `组装叙事性表演链`
    - `强化传神度与共情`
    - `越权清理`
  - 输出 `performance_patch`
  - 需要时附带 `performance_note`，供运镜/摄影在不越权前提下捕捉微表情与动作重点
- `atmosphere_engine`
  - 输出 `atmosphere_patch`

本 tranche 默认并行，但 merge precedence 仍按 `_shared/IO_CONTRACT.md` 执行。

补充说明：

- `performance_engine` 虽然属于 `Tranche 2` 并行支链，但其内部节点必须串行完成，不能跳过角色化表达或直接把情绪词写进字段。
- `camera_movement_engine` 与 `cinematography_engine` 只能消费 `performance_note` 中的捕捉提示，不能反向改写角色行为逻辑。

## Tranche 3. Finish 并行

- `camera_movement_engine`
  - 默认输出 `narrative_camera_patch`
  - 过程输出 `camera_variant_note`
  - 条件输出 `showcase_camera_note`
- `cinematography_engine`
  - 串行生成：
    - `cinematography_brief`
    - `visual_control_note`
    - `cinematography_academy_hit_note`
  - 并行生成：
    - `lighting_patch`
    - `color_patch`
  - 再串行生成：
    - `group_lighting_note`
  - 再串行合成：
    - `cinematography_patch`
- `transition_fx_engine`
  - 输出 `transition_note` 或 `fx_patch`

## Tranche 4. 父级聚合

- 把 `skeleton_patch + core_patch_set + finish_patch_set` 聚合为 `detail_candidate`。
- 严禁把任何单一能力链输出当成最终主稿。

## Tranche 5. Review / Audit

- `continuity_review_engine` 返回：
  - `continuity_note`
  - `continuity_report`
- `source_audit_engine` 返回：
  - `audit_report`
  - `writeback_patch_set`

只要任一阶段触发 veto，必须停止写回并进入返工。

## Tranche 6. Canonical Writeback

- patch-in-place 写回 `projects/<项目名>/3-Detail/第N集.json`
- 更新：
  - `metadata.document_phase`
  - `thinking_chain`
  - `final_output.main_content.分镜组列表`
- 写回 `projects/<项目名>/3-Detail/validation-report.md`
- 默认回接 `4-Design`

# 命名合同

- `detail_mission_brief`
- `scope_plan`
- `bootstrap_patch`
- `skeleton_plan`
- `skeleton_patch`
- `core_patch_set`
- `finish_patch_set`
- `camera_decision_note`
- `camera_variant_note`
- `cinematography_brief`
- `cinematography_academy_hit_note`
- `group_lighting_note`
- `continuity_note`
- `continuity_report`
- `audit_report`
- `writeback_patch_set`
- `synthesis_report`

最终 canonical artifact 只能由父 skill 写回。
