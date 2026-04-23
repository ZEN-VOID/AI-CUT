# 3-Detail Field Fill Contract

## Purpose

本文件定义当前 `3-Detail` 单技能模式下的字段填写真源。

- `3-Detail` 在根技能内完成字段填写
- canonical 输出只有一个：
  - `projects/aigc/<项目名>/3-Detail/第N集.json`

## Canonical Carriers

### 1. canonical detail root

- 路径：
  - `projects/aigc/<项目名>/3-Detail/第N集.json`
- 作用：
  - 唯一业务真源
  - 承载 `meta + groups[].global/detail`

### 2. stage validation report

- 路径：
  - `projects/aigc/<项目名>/3-Detail/validation-report.md`
- 作用：
  - 记录本轮验收、阻塞、根因上溯和 closure
  - 记录学院派知识证据：`knowledge_mode / knowledge_domain / selected_bundles / applied_passes / translation_targets`
  - 记录知行合一 closure 四段：`思考过程 / 关键证据 / 风险/例外 / 下一入口`

### 3. legacy compatibility utilities

- `.agents/skills/aigc/3-Detail/legacy/compat/`

说明：

- 迁移修复脚本与旧 sidecar/schema 兼容包装层统一收口到这里。
- 新执行默认不依赖它们，不把它们当成当前主链必需输入或输出。

## Hard Rules

1. `1-分镜构图` 固定先行，并首先写出 `分镜数 + 分镜列表` 骨架。
2. 后续 pass 都直接写向同一颗 detail root，不再先写 parent bundle 再回收。
3. 当前摄影字段统一使用根模板中的 canonical 名称，不再沿用旧命名。
4. 若 legacy/compat 中的旧 sidecar 或迁移工具仍被调用，它们只能作为补证或迁移输入，不得抢当前根技能的写回权。
5. 若本轮实际读取 `knowledge-base/电影学院派/*`，必须把 bundle 选择与转译落点写入 `validation-report.md`；若未采用，也必须写 `unused_with_reason`，防止“挂名接入”。
6. `思考过程` 只允许进入 `validation-report.md` 的 closure 段，不得另起第二真源 sidecar。

## Default Pass Ownership

| pass | 直接写入字段 |
| --- | --- |
| `1-分镜构图` | `detail.分镜数`、`分镜列表.<分镜ID>.时间 / 剧本正文 / 主体锚定 / 分镜构图` |
| `2-角色表现` | `分镜列表.<分镜ID>.角色表现` |
| `3-氛围表现` | `分镜列表.<分镜ID>.氛围表现` |
| `4-摄影表现` | `分镜列表.<分镜ID>.摄影表现` |
| `5-运镜手法` | `分镜列表.<分镜ID>.运镜手法` |
| `6-转场特效` | `分镜列表.<分镜ID>.转场特效` |

## Validation Hooks

- stage 校验入口：
  - `.agents/skills/aigc/3-Detail/scripts/validate_stage_output.py`
- 参考模块校验入口：
  - `.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`
  - `.agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py`
- 迁移兼容入口：
  - `.agents/skills/aigc/3-Detail/legacy/compat/backfill_script_bridge.py`
