# 输入与上下文装配

## 必需输入

1. `projects/<项目名>/1-Planning/3-分组/第N集.md`
2. `projects/<项目名>/3-Detail/第N集.json`
3. `projects/<项目名>/0-Init/north_star.yaml`
4. `projects/<项目名>/0-Init/init_handoff.yaml`

## 补充输入

1. `projects/<项目名>/1-Planning/3-分组/第N集.grouping.json`
2. `projects/<项目名>/0-Init/story-source-manifest.yaml`
3. `projects/<项目名>/2-Global/全局风格.md`
4. `projects/<项目名>/2-Global/类型元素.md`
5. `projects/<项目名>/2-Global/导演意图.md`

## 上下文裁剪规则

- `scope_bootstrap_engine`
  - 读取全量上游证据、现有 root file、已 seed 的 `组间设计`、用户显式范围与 preset 保护模式。
  - 若命中组的 `组间设计.出场角色及穿搭` 为空，需在 `scope_plan` 中标记为 `pending_group_costume_backfill`。
  - 进入 skeleton 前，必须在 `reference_anchor_note` 中补齐 `叙事内核 / Previous End / Current Mission / Next Start / 情绪引导`；若项目存在 `00-故事` 或等价故事源，应优先从该真源提炼观众体感目标。
- `shot_skeleton_engine`
  - 读取当前集全量分组正文、grouping JSON、shared root 中命中组的 `组间设计`。
  - 若分组正文来自 `1-Planning/3-分组` 且包含 `tail-hook` 预映或下一组借入首拍，必须先标记 `hook_preview_span`；该借入段默认不算当前组 canonical beat，只能作为“将收未收”的预映证据。
  - 进入镜序切分前，先继承组总时长与 `pace_tier`；若当前组后续命中密度预算裁决，skeleton 只能为其服务，不能反向偷改节拍与镜数预算真源。
- `structural_staging_engine`
  - 读取命中组/镜的 skeleton、`组间设计.导演意图`、`组间设计.全局风格` 与现有 draft。
  - 进入 `beat_map` 前必须先区分 `canonical beats` 与 `hook preview`；`hook preview` 只有在当前组确实需要独立的 anticipatory reaction / overhang shot 时，才允许转成额外分镜。
  - `SB-2 / SB-3` 必须调用 `scripts/detail_density_quantizer.py`，按 `动作阶段点 + 台词气口点 + 焦点切换点 + 结构转折点` 联合分段生成 `candidate beat segments`，再结合 `pace_tier + expansion/compression headroom` 给出 `preferred_shot_count + shot_budget_floor/ceiling`。
  - `SB-14` 必须调用 `scripts/validate_detail_output.py` 校验 episode JSON 中的实际镜数是否落在预算区间内；超出区间则直接返工。
  - 在 `SB-4` 到 `SB-9` 之间，必须补齐 `景别节奏预判` 与 `POV 策略预判`，并在命中镜头窗口内完成 `节奏曲线验证 / 心理距离深度审视 / 反直觉检验`；窗口大小按当前命中镜头序列确定，不预设固定镜数。
  - 在 `SB-13` 写回前，必须额外锁定每镜 `shot-local envelope`：`主任务 / 主焦点 / 景别 / 空间锚点 / 观看路径 / 允许运动强度`。后续表演、氛围、运镜、摄影只能在该 envelope 内补字段，不得另起一套粒度解释。
- `performance_engine`
  - 读取命中镜的 skeleton、构图/空间 draft、`组间设计.导演意图` 中对应情绪/动作/关系线索，以及 `reference_anchor_note` 中已转译的角色表达锚点。
  - 若项目存在 `2.1.1-角色清单` 或等价角色源，需补齐 `Character Arc`：角色此刻极力想掩饰的内容是什么。
  - 若命中 `对手戏模式`，基于当前空间/站位与冲突关系提炼攻守、距离、让压、回避、逼近、断开等行为策略。
  - 若存在 Dialogue & Interaction KB，可条件提炼 `Selected Technique + Application Logic`，但只能落成当前镜的表演与互动策略，不能越权改写运镜/摄影。
  - `Subtext Visualization` 必须落成一个可拍微动作，明确“当嘴巴在撒谎时，身体哪一处在说真话”。
  - 若当前组仍需回填 `出场角色及穿搭`，应同步沉淀 `角色名-服装简述` 的组级摘要素材，但不得把服装重新塞回 shot-level 常驻字段。
- `atmosphere_engine`
  - 读取命中镜的空间 draft、`组间设计.全局风格`、`组间设计.导演意图` 与现有摄影草案。
- `camera_movement_engine`
  - 读取命中镜的 core draft、`组间设计.类型元素`、`组间设计.导演意图`，以及 `references/分镜表现.md` 已产出的 `academy_hit_note`（若有）。
  - 仅在默认运镜路线与运动动机已经成立时，吸收 `academy_hit_note` 中已经转译好的运动相关提示，整理为 `camera_strategy_note`。
  - 比较同目标变体时额外读取场景氛围 draft；挑战方案额外读取风格禁区。
- `cinematography_engine`
  - 先读取命中镜的 skeleton、组级节奏、运镜、氛围，以及 `组间设计.全局风格 / 类型元素 / 导演意图`。
  - 先收束 `cinematography_strategy_note`，再供光位与色彩阶段共享。
  - 光位与色彩阶段共享 `cinematography_brief + visual_control_note + cinematography_strategy_note`。
  - 组级光影推进阶段额外读取 `lighting_patch` 与组内镜序。
  - 总协调阶段再读取 `group_lighting_note + color_patch + cinematography_strategy_note`。
- `transition_fx_engine`
  - 读取组内/组间衔接证据、命中镜 finish draft 与风格禁区。
- `continuity_review_engine`
  - 只读取合成后的 candidate，不读未采用草稿。
- `source_audit_engine`
  - 只读取最终 candidate、schema、I/O contract 与输出落点。

# 默认执行流程

## Tranche 0. 输入与阶段门

- 读取 `Init / Planning / shared episode root` 真源；`2-Global/*.md` 仅在兼容回退或审计时补读。
- 生成：
  - `detail_mission_brief`
  - `scope_plan`
  - `preset_manifest`
  - `reference_anchor_note`
  - `bootstrap_patch`（仅兼容回退时）

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
    - 从上游继承的 `组间设计`
    - 哪些初始化预设元素必须在镜头里被看见
    - 哪些参考锚点需要转译进后续表现链
    - 这一段的 `叙事内核 / Previous End / Current Mission / Next Start / 情绪引导`
    - 哪些文本属于当前组 canonical 叙事拍点，哪些只是 `tail-hook` 预映
    - 当前组继承的 `pace_tier` 与组时长边界
    - preset / lock-axis 不得越权的边界

## Tranche 2. Core 并行

- `structural_staging_engine`
  - 先行输出 `staging_patch`
  - 同时锁定 `景别节奏预判`、`POV 策略预判` 与命中镜头窗口的验证结论
  - 同时输出 shot-local envelope，作为本 tranche 其余支链的公共上游约束
- `performance_engine`
  - 内部串行顺序：
    - `锁表演主轴`
    - `锁角色化表达通道`
    - `对手戏策略细化（条件）`
    - `锁 Character Arc 隐匿项`
    - `锁 Dialogue & Interaction 技巧（条件）`
    - `锁可见信号`
    - `锁潜台词微动作`
    - `组装叙事性表演链`
    - `强化传神度与共情`
    - `越权清理`
  - 输出 `performance_patch`
  - 需要时附带 `performance_note`，供运镜/摄影在不越权前提下捕捉微表情与动作重点
- `atmosphere_engine`
  - 输出 `atmosphere_patch`

本 tranche 不是“各链各自定义镜头粒度”的自由并行，而是“共享同一 shot-local envelope 的受约束并行”。`performance_engine` 与 `atmosphere_engine` 只有在 `structural_staging_engine` 已锁定每镜任务包络后，才允许补各自字段。

补充说明：

- `performance_engine` 虽然属于 `Tranche 2` 并行支链，但其内部节点必须串行完成，不能跳过角色化表达、`Character Arc` 隐匿项或直接把情绪词写进字段。
- `Dialogue & Interaction` 技巧只在对手戏或互动密集镜条件触发；它属于表演链内部策略判型，不单独形成新的并行支链。
- `camera_movement_engine` 与 `cinematography_engine` 只能消费 `performance_note` 中的捕捉提示，不能反向改写角色行为逻辑。
- 若 `performance / atmosphere` 发现当前 `preferred_shot_count` 或 `shot-local envelope` 无法承载内容，正确回退入口是 `SB-2/3/4`，不是在本地复制组级句子填满多个 shot。

## Tranche 3. Finish 并行

- `camera_movement_engine`
  - 串行生成：
    - `narrative_route_note`
    - `movement_reason_note`
    - `camera_strategy_note`
    - `narrative_camera_patch`
  - 过程输出 `camera_variant_note`
  - 条件输出 `showcase_camera_note`
- `cinematography_engine`
  - 串行生成：
    - `cinematography_brief`
    - `visual_control_note`
    - `cinematography_strategy_note`
  - 并行生成：
    - `lighting_patch`
    - `color_patch`
  - 再串行生成：
    - `group_lighting_note`
  - 再串行合成：
    - `cinematography_patch`
- `transition_fx_engine`
  - 输出 `transition_note` 或 `fx_patch`

补充说明：

- `camera_movement_engine` 与 `cinematography_engine` 的并行，前提是 `分镜表现` 已锁定景别、空间、观看路径与运动强度边界；它们只负责把同一镜头任务做成更可拍的运动与视觉实现，不得借 finish 链补做第二轮“拆镜/并镜/重定景别”。
- 若 finish 链判断“同一组需要 2 套运镜逻辑或 3 套光色逻辑”才能成立，应回到 `Tranche 1/2` 重判镜头粒度，而不是默认把组级语法复制到多个 shot 上。

## Tranche 4. 父级聚合

- 把 `skeleton_patch + core_patch_set + finish_patch_set` 聚合为 `detail_candidate`。
- 在命中组聚合时，依据当前有效镜头补齐 `组间设计.出场角色及穿搭`；若确无角色出场，显式写 `无出场角色`。
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
  - `final_output.main_content.分镜组列表`
- 写回 `projects/<项目名>/3-Detail/validation-report.md`
- 仅在 `第N集.json` 与 `validation-report.md` 已真实存在且 validator 返回 `PASS` 后，才同步 `projects/<项目名>/project_state.yaml`
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
- `camera_strategy_note`
- `cinematography_brief`
- `visual_control_note`
- `cinematography_strategy_note`
- `group_lighting_note`
- `continuity_note`
- `continuity_report`
- `audit_report`
- `writeback_patch_set`
- `synthesis_report`

最终 canonical artifact 只能由父 skill 写回。
