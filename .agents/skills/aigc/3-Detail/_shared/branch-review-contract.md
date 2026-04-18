# 3-Detail Branch Review Contract

## Purpose

本文件定义 `3-Detail` 在 branch-owned 重构后的默认评审路径。

核心目标：

- review 尽量发生在“未被压缩前”的 branch 粒度
- parent 只做 coherence / ownership / commit gate
- team system 不再主要评审“压扁后的 merged prose”
- 当前默认评审顺序也跟随 branch 串行写回顺序，而不是把无序号叶子误读成并发 reviewer 队列

## Review Layers

### Layer 1. branch review

目标对象：

- `projects/aigc/<项目名>/3-Detail/<owner>/<branch-name>/第N集.branch-patch.json`

检查重点：

1. 该 branch 的创作判断是否成立
2. `thinking_process` 是否真正支撑 `patch_payload`
3. `target_json_paths[]` 是否越权
4. 该 branch 是否把别的 branch 负责的语义偷偷吞进来

### Layer 2. owner bundle review

目标对象：

- `水月/第N集.field-patch.json`
- `镜花/第N集.field-patch.json`

检查重点：

1. branch bundle 是否只是 deterministic assembly
2. 是否出现跨 branch 折中改写
3. `review_status` 与 `branch_sidecars[]` 是否一致

### Layer 3. stage coherence review

目标对象：

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/3-Detail/validation-report.md`

检查重点：

1. 八个 branch 是否形成同一作品语法
2. branch-owned canonical 字段是否已落盘
3. compatibility projection 是否越权盖过 canonical 字段
4. `ready` 是否只因结构完整，而不是因气质成立

## Default Reviewer Bias

### `水月`

- `1-角色表现`
  - 优先：小说组 / 演员组 / 导演组
- `2-运动表现`
  - 优先：导演组 / 武术组 / 摄影组
- `3-氛围表现`
  - 优先：作品维度 / 摄影组 / 设计组
- `4-视觉强化`
  - 优先：导演组 / 作品维度 / 摄影组

### `镜花`

- `1-分镜构图`
  - 优先：导演组 / 摄影组
- `2-摄影美学`
  - 优先：摄影组 / 作品维度 / 导演组
- `3-运镜手法`
  - 优先：导演组 / 摄影组 / 武术组
- `4-转场特效`
  - 优先：导演组 / 剪辑思维近似 reviewer / 作品维度

## Hard Rules

1. branch review findings 先回流 branch owner，不直接由 stage 父层代修。
2. owner bundle review 不得把多个 branch 改写成一条折中 prose。
3. stage coherence review 可以要求补 compatibility projection，但不得牺牲 canonical branch-owned field。
4. `used_subagents: true` 只代表 reviewer runtime 成立，不代表作品气质已经成立。
5. 若父层已声明按编号顺序串行执行，则 review 也必须面向“当前已部分写好的 root + 当前 branch patch”进行，不得脱离 progressive commit 上下文抽空评判。

## Validation Signals

- 若 branch process sidecar 缺少 `thinking_process / patch_payload / review_trace`
  - 视为 branch review 输入不完整
- 若 bundle sidecar 出现非 owner 的 target path
  - 视为 ownership 冲突
- 若 shared root 只剩 legacy 字段，没有 branch-owned object
  - 不得进入新的 `ready`
