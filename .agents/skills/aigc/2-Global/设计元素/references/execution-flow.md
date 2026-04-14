# 设计元素执行流参考

本文件是 `aigc/2-Global/设计元素` 的执行顺序参考真源，用于细化主 `SKILL.md` 中的思行网络与返工顺序。

## Fixed Order

1. 锁主输入与 episode / phase 范围
2. 锁时代路由与世界观约束
3. 归纳 grouped script 的全剧阶段变化
4. 先出服装定调，再出建筑场景定调
5. 汇流为阶段成长矩阵
6. 按模板写回 `设计元素.md`
7. 做时代正确性、双设计线与下游 handoff QA

## Evidence Priority

1. `projects/<项目名>/1-Planning/3-分组/第N集.md`
2. `projects/<项目名>/1-Planning/3-分组/执行报告.md`
3. `projects/<项目名>/1-Planning/episode-split-plan.json`
4. `projects/<项目名>/0-Init/north_star.yaml`
5. `projects/<项目名>/0-Init/init_handoff.yaml`
6. 已有 `projects/<项目名>/2-Global/全局风格/全局风格设计.md`（若存在）

## Node-Level Guidance

### 1. `N1-INPUT-LOCK`

- 必须确认 grouped script 是否能覆盖当前项目需要定调的关键阶段。
- 若只有局部阶段证据，允许先写“当前已知阶段矩阵”，但必须显式标注证据边界。

### 2. `N2-ERA-WORLD-ROUTE`

- 时代判型由 `3-分组` 的叙事现实首先决定，`0-Init` 只补世界观边界。
- 若是架空古代、近未来现代等混合世界，先锁 dominant era，再写允许侵入的次级语汇。

### 3. `N3-PHASE-SYNTHESIS`

- 不是只看故事发生在哪里，而是看人物身份、社会秩序、材质条件、空间密度和文明压力如何变化。
- 若 grouped script 已出现明确阶段跃迁，阶段矩阵必须显式响应。

### 4. `N4-COSTUME-DIRECTION`

- 服装定调至少回答：轮廓、层次、材料、纹样/结构、色谱、佩饰、运动感、人格气质。
- 现代/未来题材优先写“设计语法”，古代题材优先写“史实与地域约束”。

### 5. `N5-SCENE-DIRECTION`

- 建筑场景定调至少回答：建筑语言、空间秩序、材料工法、开口/围合关系、陈设密度、氛围压力。
- 不只写 interior，必须覆盖能代表世界观的建筑场景母体。

### 6. `N6-EVOLUTION-ARC`

- 推荐至少写 `开端 / 发展 / 转折 / 后段` 四段，或按项目已有阶段命名。
- 阶段变化要能回答“为什么变”“变到哪里”“什么不能变”。

### 7. `N8-QA-CONVERGENCE`

- QA 最少检查四件事：
  1. 时代正确性
  2. 服装/建筑双线完整性
  3. 阶段变化是否可执行
  4. 下游是否能直接继承

## Rework Shortcuts

- 时代不稳：回 `N2`
- 只有静态总则：回 `N3/N6`
- 服装正确但场景失真：回 `N5`
- 场景正确但服装失真：回 `N4`
- 输出结构错位：回 `N7`
