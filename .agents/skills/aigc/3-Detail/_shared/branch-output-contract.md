# 3-Detail Branch Output Contract

## Purpose

本文件定义 `3-Detail` 在 branch-owned 重构后的输出真源。

目标不是取消最终 `.json`，而是取消“语义压缩式聚合”：

- branch skill 各自围绕同一 `episode root + group scope` 创作
- 每个 branch 同时产出 `思维·执行 sidecar + 字段 patch`
- 父层只做 deterministic assembly / ownership gate / review gate
- 不再要求父层把多个 branch 的高质量结果压成一条短促 prose 才算“merge”
- 当前 `3-Detail` 默认不按 branch 并发写 shared root，而是按父层显式采用的编号顺序串行推进

## Canonical Carriers

### 1. branch process sidecar

- 路径模式：
  - `projects/aigc/<项目名>/3-Detail/水月/<branch-name>/第N集.branch-patch.json`
  - `projects/aigc/<项目名>/3-Detail/镜花/<branch-name>/第N集.branch-patch.json`
- 用途：
  - 保留该 branch 的思维·执行过程
  - 保留该 branch 的 `target_json_paths[]`
  - 保留该 branch 的局部字段 patch
  - 保留该 branch 的自检与 review trace

### 2. parent bundle sidecar

- 路径模式：
  - `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`
  - `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`
- 用途：
  - 只做 branch patch 集合与 review 状态总账
  - 记录 `branch_sidecars[]`
  - 记录 `group_patches[].branch_patches`
  - 允许保留 `compatibility_projection`，但不得在这里重新创作

### 3. shared root

- 路径模式：
  - `projects/aigc/<项目名>/3-Detail/第N集.json`
- 用途：
  - 唯一业务真源
  - 接收 branch-owned canonical 字段
  - 允许保留 legacy 兼容投影字段
  - 不再要求 legacy 投影字段承担唯一真相

## Hard Rules

1. branch skill 必须写自己的 process sidecar，不得只把结果塞给父层。
2. parent bundle sidecar 只允许 deterministic assembly，不允许二次文学压缩。
3. shared root 的 canonical 真相改为与 child skill 包名同名的 branch-owned field objects：`角色表现 / 运动表现 / 氛围表现 / 视觉强化 / 分镜构图 / 摄影美学 / 运镜手法 / 转场特效`。旧字段名 `人物表演锚点 / 人物表演 / 动作路径 / 动作调度 / 空间氛围 / 视觉抓手 / 视觉焦点 / 构图骨架 / 构图策略 / 摄影策略 / 运镜策略 / 转场策略 / 分镜表现` 只保留为兼容别名或过渡投影。
4. 若多个 branch 命中同一路径，必须在 branch review 或 parent gate 阶段阻塞，不能让父层“折中改写”。
5. team review 默认先看 branch process sidecar，再看 bundle，再看 shared root。
6. 当前 `3-Detail` 的默认写回路径是按编号顺序串行执行 branch；后一 branch 必须先回读当前已部分写好的 `projects/aigc/<项目名>/3-Detail/第N集.json` 与上一步 sidecar，再生成自己的 patch。
7. 无序号叶子只表示目录名不承载顺序，不得据此推断 shared root 可并发写入；是否并发必须由显式合同单独声明。
8. 整个 `3-Detail` shared root 默认执行“反抽象”写法：所有 canonical 字段与 compatibility projection 都应优先落具体可见的动作、位置、物件、光气、构图或关系证据，不得用“情绪成立/关系压力/电影感更强/主抓手更稳”这类抽象总结句代替。
9. `角色表现.动作戏` 不得写成景别、机位、运镜或镜头速度术语；若一句话更像镜头说明，应回流 `分镜构图 / 运镜手法` 或 shot descriptor 槽，而不是留在表演字段。
10. legacy 兼容投影中的 `分镜表现` 视为 deprecated alias；若仍保留，只能写“构图向、可见、具像”的兼容摘要，不得写抽象观感总结。后续 contracts 应优先迁移到 `分镜构图` 对象语义。
11. 不得用 `…`、半截短语或模板残片代替语义压缩；凡出现硬截断痕迹，视为源层压缩机制失效，应回到上游具体画面句重写。

## Default Branch Path Map

### `1-水月`

- `1-角色表现`
  - 负责：`分镜明细[].角色表现`
- `2-运动表现`
  - 负责：`分镜明细[].运动表现`
- `3-氛围表现`
  - 负责：`分镜明细[].氛围表现`
- `4-视觉强化`
  - 负责：`分镜明细[].视觉强化`

### `2-镜花`

- `1-分镜构图`
  - 负责：`分镜明细[].分镜构图`
- `2-摄影美学`
  - 负责：`分镜明细[].摄影美学`
- `3-运镜手法`
  - 负责：`分镜明细[].运镜手法`
- `4-转场特效`
  - 负责：`分镜明细[].转场特效`

## Compatibility Policy

- `角色背景面 / 角色站位走位 / 道具及状态 / 分镜表现`
  - 仍允许存在于 shared root
  - 但它们在新结构下属于 compatibility projection
- 若继续保留 `分镜表现`
  - 默认按 deprecated alias 处理
  - 必须写成构图向、可见、具像的兼容摘要
  - 不得直接复用 `视觉抓手.镜头消费提示` 或抽象导演意图原句
- 新生成流程必须优先写 branch-owned object，再决定是否派生 legacy 字段
- legacy 字段不得反向覆盖 branch-owned canonical 字段

## Validation Hooks

- branch process sidecar 校验入口：
  - `.agents/skills/aigc/3-Detail/scripts/validate_branch_process_sidecar.py`
- parent bundle 校验入口：
  - `.agents/skills/aigc/3-Detail/1-水月/scripts/validate_watermoon_output.py`
  - `.agents/skills/aigc/3-Detail/2-镜花/scripts/validate_jinghua_output.py`
- stage 校验入口：
  - `.agents/skills/aigc/3-Detail/scripts/validate_stage_output.py`
