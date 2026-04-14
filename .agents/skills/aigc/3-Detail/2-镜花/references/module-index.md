# 模块总索引

## 作用

本文件是 `2-镜花` 内部编号主链与叶子模块的总索引。

它回答四个问题：

1. 顶层四个编号模块为什么必须串行
2. 每个分类内部哪些叶子可以并发思考，哪些必须串行
3. 每个模块补什么，不该补什么
4. 各阶段 patch 如何最终汇流成单一组级 `镜花` prose

## 水月继承总则

- `1-水月` 是 `2-镜花` 的第一事实层。
- 顶层四个编号模块都只能围绕 `1-水月` 已提供的信息组织镜头语言，不得自行新增关键剧情事实。
- `0-Init + 2-Global` 的职责是调节“怎么拍、怎么显化、怎么统一风格”，不是改写“发生了什么”。
- 每组在进入 `1-分镜表现` 之前，必须先抽出一条 `水月承接`，作为后续切镜、摄影、运镜、转场的共同锚。

## 顶层执行顺序

| 顶层模块 | 顺序语义 | 主职责 | 禁止越权 |
| --- | --- | --- | --- |
| `1-分镜表现` | 必须第 1 阶段执行 | 锁定组内分镜数、插入点与构图骨架，形成 shot spine | 不直接决定色彩、镜头速度或转场花样 |
| `2-摄影美学` | 必须第 2 阶段执行 | 在已锁定 shot spine 上补光影、色彩、质感 | 不越权改分镜数或插入点 |
| `3-运镜手法` | 必须第 3 阶段执行 | 在已锁定分镜与摄影前提上补变化、组合、速度 | 不反向改写摄影基调或转场收益 |
| `4-转场特效` | 必须第 4 阶段执行 | 先判衔接问题与直切优先，再只在有叙事收益时补组内/组间转场与特效 | 不喧宾夺主，不把整组写成效果展示 |

## 链内执行规则

### `1-分镜表现`

| 叶子模块 | 执行方式 | 作用 |
| --- | --- | --- |
| `1-切换` | 严格先执行 | 估算默认时长内需要切成多少镜，以及每镜时段 |
| `2-插入` | 严格第二步 | 在 `1-水月` prose 中找到自然插入点，形成分镜标记骨架 |
| `3-构图` | 严格第三步 | 为每个分镜标记补构图与视线组织 |

### `2-摄影美学`

- 进入 `光影 / 色彩 / 质感` 之前，必须先完成：`回看摄影底座 -> 锁视觉控制线 -> 收束摄影执行策略`。
- `光影 / 色彩 / 质感` 可并发思考。
- 汇流顺序固定为：`光影 -> 色彩 -> 质感`。
- `光影` 产出后必须补 `group_lighting_note`，再进入摄影总协调。
- 汇流原则：先确定照明和影调，再叠色彩气候，最后压入材料与表面质感，并收束成单一组级摄影判断。

### `3-运镜手法`

- `变化 / 组合 / 速度` 可并发思考。
- 汇流顺序固定为：`变化 -> 组合 -> 速度`。
- 汇流原则：先确定镜头是否需要运动变化，再决定组合关系，最后决定速度和节奏。

### `4-转场特效`

- 进入叶子前，先完成“衔接问题类型 -> 直切是否最强”的分支闸门判断。
- `组内 / 组间 / 特效` 可并发思考。
- 汇流顺序固定为：`组内 -> 组间 -> 特效`。
- 汇流原则：先定直切与问题类型，再保内部切接顺滑，再看组间衔接，最后只补必要特效。

## 汇流顺序

1. 先锁组锚点和默认时长。
2. 先锁 `水月承接`，确认本组镜头语言所依托的上游事实。
3. 用 `1-分镜表现` 形成 shot spine。
4. 在不改动 shot spine 且不脱离 `水月承接` 的前提下补 `摄影美学`。
5. 在不打乱摄影基调和上游事实的前提下补 `运镜手法`。
6. 最后只补最有叙事收益的 `转场特效`。
7. 把四阶段 patch 一次性融成组级 `镜花` prose。
8. 做 `2000` 字预算裁剪，再写回 canonical 文件。

## Ownership Rules

- 分镜数、秒位切分、插入点归 `1-分镜表现`
- 光位、影调、色温、材质归 `2-摄影美学`
- 运动路线、组合方式、节奏速度归 `3-运镜手法`
- 切接收益、组间衔接与必要特效归 `4-转场特效`
- 最终 prose 的统一文风、去重、裁剪归父 skill 的 `N8/N9`

## 配置真源规则

- `3-Detail` 共享节点包真源为：`.agents/skills/aigc/3-Detail/references/node-pack-contract.md`。
- `3-Detail` 共享创作引导真源为：`.agents/skills/aigc/3-Detail/references/creative-guidance-contract.md`。
- `references/` 下所有分类模块与叶子模块统一使用 `module-spec.yaml` 作为执行配置真源。
- `module-guide.md` 是节点解释层，负责 why / anti-pattern / 审美尺度；不得反向改写 `module-spec.yaml`。
- `module-spec.yaml` 至少要声明：`module_id / module_level / purpose / triggers / must_answer / patch_contract / merge_policy / quality_gates`。
- 每个 branch / leaf 目录都必须与 `module-spec.yaml` 配对一个 `module-guide.md`。
- 统一结构校验入口：`.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`
- `route-profile.yaml` 负责决定哪类镜花组型该重打哪些阶段与叶子；`examples.md` 与 `creative-review-rubric.md` 负责创作示范与验收。
- 创作引导校验入口：`.agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py`
- 不允许再以 `README.md` 充当叶子模块的唯一规范真源。

## 叶子模块回链

- `references/1-分镜表现/module-spec.yaml`
- `references/1-分镜表现/1-切换/module-spec.yaml`
- `references/1-分镜表现/2-插入/module-spec.yaml`
- `references/1-分镜表现/3-构图/module-spec.yaml`
- `references/2-摄影美学/module-spec.yaml`
- `references/2-摄影美学/光影/module-spec.yaml`
- `references/2-摄影美学/色彩/module-spec.yaml`
- `references/2-摄影美学/质感/module-spec.yaml`
- `references/3-运镜手法/module-spec.yaml`
- `references/3-运镜手法/变化/module-spec.yaml`
- `references/3-运镜手法/组合/module-spec.yaml`
- `references/3-运镜手法/速度/module-spec.yaml`
- `references/4-转场特效/module-spec.yaml`
- `references/4-转场特效/组内/module-spec.yaml`
- `references/4-转场特效/组间/module-spec.yaml`
- `references/4-转场特效/特效/module-spec.yaml`
