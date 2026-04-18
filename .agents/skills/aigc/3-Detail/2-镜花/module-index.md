# 模块总索引

## 作用

本文件是 `镜花` 内部编号主链与叶子模块的总索引。

它回答四个问题：

1. 为什么先 `分镜构图`，再按当前序号继续推进后三类
2. 每个分类内部哪些叶子只是连续判断拆分，哪些必须显式串行吸收
3. 每个模块补什么，不该补什么
4. 各阶段 patch 如何最终汇流成 `分镜构图 / 摄影美学 / 运镜手法 / 转场特效`

## 水月继承总则

- `水月` 是 `镜花` 的实际 factual 前置，不是旁路增强层。
- 顶层四个编号模块都只能围绕固定 `剧本正文`、shared root 的 `分镜切换` 与 `水月` 已提供的信息组织镜头语言，不得自行新增关键剧情事实。
- `0-Init + 2-Global` 的职责是调节“怎么拍、怎么显化、怎么统一风格”，不是改写“发生了什么”。
- 每组在进入 `分镜构图` 之前，必须先抽出一条 `水月承接`，作为后续切镜、摄影、运镜、转场的共同锚。

## 顶层执行顺序

- `镜花` 的实际落镜默认承接 `2-Global` 已内化的固定 `分镜切换` 与 `水月` factual evidence，再进入本索引内的顶层阶段。
- former `1-切换` 的“先接受固定镜数、不得临场改数”已上收到 `2-Global`；`镜花` 不再单独暴露该叶子，而是在 `分镜构图` 内直接消费这一前置真值。

| 顶层模块 | 顺序语义 | 主职责 | 禁止越权 |
| --- | --- | --- | --- |
| `分镜构图` | 必须第 1 阶段执行 | 直接承接 inherited `分镜切换`，一体锁 `时间段 / slot / 构图 / descriptor / POV`，形成 shot spine | 不直接决定色彩、镜头速度或转场花样 |
| `摄影美学` | 在 `分镜构图` 之后按当前序号执行 | 在已锁定 shot spine 上补光影、色彩、质感 | 不越权改分镜数或 slot |
| `运镜手法` | 在 `摄影美学` 之后按当前序号执行 | 在已锁定 shot spine 上补变化、组合、速度 | 不反向改写摄影基调、构图骨架或转场收益 |
| `转场特效` | 在 `运镜手法` 之后按当前序号执行 | 先判衔接问题与直切优先，再只在有叙事收益时补组内/组间转场与特效 | 不喧宾夺主，不把整组写成效果展示 |

## 链内执行规则

### `分镜构图`

- former `1-切换` 逻辑已内化到 `2-Global` 的 fixed-shot-count 裁决；当前模块不再拆单独叶子。
- 当前 branch 先完成：`watermoon_inheritance + shot_count_plan + shot_slot_map`。
- 进入叶子后固定顺序为：`构图形式 -> 景别景深 -> 镜头类型`。
- 三个叶子分别回答：
  - `构图形式`：画面怎么站住，谁压谁，空间和轴线怎么成立。
  - `景别景深`：观众离多远，前中后景怎么分层，心理距离怎样变化。
  - `镜头类型`：观众怎么被带着看，并统领 `镜头框架 / 镜头视角` 等 descriptor 概念。
- `镜头类型` 在这里不是摄影器材；`景别景深` 在这里是观看深度层级，不是精确光圈参数。
- 若 slot 一落就破坏动作连续或空间连续，回退的对象是 shared root `分镜切换` 与 `水月` evidence，不是继续下游补词。

### `摄影美学`

- 进入 `光影 / 色彩 / 质感` 之前，必须先完成：`回看摄影底座 -> 锁 visual_control_line（主体控制 / 空间剥离 / 质感方向 / 观看压力） -> 收束 cinematography_strategy_note（稳定贯穿后续光位与色彩分支的判断）`。
- `光影 / 色彩 / 质感` 只是同一控制线下的连续判断拆分，不承载真实并发调度语义；三者必须共同消费同一条 `visual_control_line + cinematography_strategy_note`，且 `质感` 只允许沿已锁定的质感方向补可见表面行为。
- 汇流顺序固定为：`光影 -> 色彩 -> 质感`。

### `运镜手法`

- `变化 / 组合 / 速度` 只是默认路线成立后的连续判断拆分，不暗示可并发执行。
- 汇流顺序固定为：`变化 -> 组合 -> 速度`。
- 汇流原则：先确定镜头是否需要运动变化，再决定组合关系，最后决定速度和节奏。

### `转场特效`

- 进入叶子前，先完成“衔接问题类型 -> 直切是否最强”的分支闸门判断。
- `组内 / 组间 / 特效` 只是同一闸门后的连续判断拆分，不暗示可并发执行。
- 汇流顺序固定为：`组内 -> 组间 -> 特效`。
- 汇流原则：先定直切与问题类型，再保内部切接顺滑，再看组间衔接，最后只补必要特效。

## 汇流顺序

1. 先锁组锚点和默认时长。
2. 先锁 shared root 的 `分镜切换` 与 `水月承接`，确认本组镜头语言所依托的上游事实与既定镜数。
3. 先由 `分镜构图` 直接把既定镜数落成真实秒位窗口、slot 与画面骨架，形成 shot spine。
4. 在 `分镜构图` 内部，再按 `构图形式 -> 景别景深 -> 镜头类型` 固定顺序完成组级构图吸收。
5. 在不改动 shot spine 且不脱离 `水月承接` 的前提下，按当前序号串行补 `摄影美学 -> 运镜手法 -> 转场特效`。
6. 父层按稳定顺序把串行分支 patch 汇成四个 cinematic canonical 字段。
7. 若旧下游仍需读取，再保守派生 `shot_patches[]` compatibility projection。
8. 交给父层按 ownership merge 回 `projects/aigc/<项目名>/3-Detail/第N集.json`。

## Ownership Rules

- 分镜数继承、秒位切分、slot 映射与 `分镜构图` 归 `分镜构图`
- 光位、影调、色温、材质归 `摄影美学`
- 运动路线、组合方式、节奏速度归 `运镜手法`
- 切接收益、组间衔接与必要特效归 `转场特效`
- 最终四个 cinematic canonical 字段的合法性、去重和 merge 准备归父 skill 的 assembly gate
- 一旦 inherited `分镜切换` 已被 `分镜构图` 接受，后续阶段不得自行增减镜头数；若骨架不稳，只能回退到 shared root `分镜切换` + `分镜构图`

## 配置真源规则

- `3-Detail` 共享节点包真源为：`.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`。
- `3-Detail` 共享创作引导真源为：`.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`。
- 当前技能包内所有分类模块与叶子模块统一使用 package-local `module-spec.yaml` 作为执行配置真源。
- `module-guide.md` 是节点解释层，负责 why / anti-pattern / 审美尺度；不得反向改写 `module-spec.yaml`。
- `module-spec.yaml` 至少要声明：`module_id / module_level / purpose / triggers / must_answer / patch_contract / merge_policy / quality_gates`。
- 每个 branch / leaf 目录都必须与 `module-spec.yaml` 配对一个 `module-guide.md`。
- 统一结构校验入口：`.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`
- `route-profile.yaml` 负责决定哪类镜花组型该重打哪些阶段与叶子；`examples.md` 与 `creative-review-rubric.md` 负责创作示范与验收。
- 创作引导校验入口：`.agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py`
- 不允许再以 `README.md` 充当叶子模块的唯一规范真源。

## Sidecar 汇流原则

- `镜花` 的标准输出不是 `[分镜N ...]` 正文，而是 `分镜构图 / 摄影美学 / 运镜手法 / 转场特效`。
- `分镜构图` 负责 shot slot 映射与构图骨架，不再回写 `剧本正文`。
- `摄影美学`、`运镜手法`、`转场特效` 都必须依附同一条 shot spine。
- `shot_patches[]` 现在只是旧下游 fallback 的 compatibility projection。

## 叶子模块回链

- `1-分镜构图/module-spec.yaml`
- `1-分镜构图/构图形式/module-spec.yaml`
- `1-分镜构图/景别景深/module-spec.yaml`
- `1-分镜构图/镜头类型/module-spec.yaml`
- `2-摄影美学/module-spec.yaml`
- `2-摄影美学/光影/module-spec.yaml`
- `2-摄影美学/色彩/module-spec.yaml`
- `2-摄影美学/质感/module-spec.yaml`
- `3-运镜手法/module-spec.yaml`
- `3-运镜手法/变化/module-spec.yaml`
- `3-运镜手法/组合/module-spec.yaml`
- `3-运镜手法/速度/module-spec.yaml`
- `4-转场特效/module-spec.yaml`
- `4-转场特效/组内/module-spec.yaml`
- `4-转场特效/组间/module-spec.yaml`
- `4-转场特效/特效/module-spec.yaml`
