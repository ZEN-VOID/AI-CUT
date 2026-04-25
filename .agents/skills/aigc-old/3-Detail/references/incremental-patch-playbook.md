# 3-Detail Incremental Patch Playbook

本文件细化 `3-Detail` 的增量 patch、返工重入与局部 scope 保留策略。
若与主 `SKILL.md` 冲突，以主合同为准。

## Purpose

- 让 `3-Detail` 支持局部修补，而不是每次都整集重跑。
- 让增量 patch 保持 `P1-分镜构图` 的结构优先，不因为补后序字段而偷改骨架。
- 让 `validation-report.md` 能明确说明本轮 patch scope、保留项和返工入口。

## Patch Scope

### `episode_scope`

- 命中整集 `第N集.json`
- 允许重建整集 `groups[]`
- 常见于首次落盘或上游 `2-Global` 发生大范围变化

### `group_scope`

- 只命中一个或多个 `分镜组ID`
- 只 patch 指定组的 `detail.*`
- 未命中组必须保留既有确认内容

### `shot_scope`

- 只命中指定 `分镜ID`
- 适用于局部镜头质量修补
- 不能顺手重写同组其他镜头

### `field_scope`

- 只命中指定字段：
  - `角色表现`
  - `氛围表现`
  - `摄影表现`
  - `运镜手法`
  - `转场特效`
- 不得越权改写同镜其他已确认字段

### `closure_scope`

- 只修 `validation-report.md`
- 只允许重进 `N7/N8`
- 不得借修 closure 顺手改业务 JSON

## Re-entry Matrix

| patch 类型 | 最小返工入口 | 必须重跑 | 禁止动作 |
| --- | --- | --- | --- |
| `episode_scope` | `N1` | `N1 -> N8` | 把旧局部 patch 当成整集不变量 |
| `group_scope` | `N2` | 命中组 `N2 -> N8` | 顺手覆盖未命中组 |
| `shot_scope` | `N2` 或字段对应节点 | 命中镜头的必要节点到 `N8` | 同组全镜默认重写 |
| `field_scope=角色表现` | `N3` | `N3 -> N8` | 反向改 `时间 / 剧本正文 / 主体锚定 / 分镜构图` |
| `field_scope=氛围表现` | `N4` | `N4 -> N8` | 改镜数或正文切分点 |
| `field_scope=摄影表现` | `N5` | `N5 -> N8` | 抢写构图骨架 |
| `field_scope=运镜手法/转场特效` | `N6` | `N6 -> N8` | 倒逼结构重写而不回 `N2` |
| `closure_scope` | `N7` 或 `N8` | `N7 -> N8` | 改业务 JSON 伪装成 closure 修补 |

## Hard Rules

1. 增量 patch 必须保留未命中 scope 的既有确认内容。
2. 只要改动触及 `时间 / 剧本正文 / 主体锚定 / 分镜构图 / 分镜数`，一律视为骨架层 patch，必须回 `N2`。
3. 后序字段 patch 不得绕过 `N7/N8`；局部修补后仍要重写阶段报告。
4. `closure_scope` 不能拿来掩盖业务 JSON 已过期的问题。
5. 任何 patch 都不得把 legacy projection 当第一真源。

## Patch Decision Rules

### 何时必须回 `N2`

- 镜数不成立
- 镜级正文切分点错位
- 主体锚定失真
- `分镜构图` 无法支撑后续字段
- 空间关系、轴线、视线链混乱

### 何时可以从后序字段节点进入

- 骨架稳定，只是 `角色表现` 空泛
- 氛围只剩形容词，没有空间承载
- 摄影表现像器材清单
- 运镜与转场收益不足，但不影响骨架成立

### 何时只能修 closure

- JSON 已稳定，validator 也通过
- 报告缺 `思考过程 / 关键证据 / 风险/例外 / 下一入口`
- 知识证据有，但 closure 不可复核

## Validation-Report Patch Notes

只要是增量 patch，`validation-report.md` 推荐补充以下信息：

- `patch_scope`
- `reentry_node`
- `preserved_scope`
- `touched_groups`
- `touched_shots`
- `touched_fields`

最低写法要求：

1. 说明本轮只改了哪些 scope。
2. 说明哪些 scope 明确保留未动。
3. 说明为什么选择这个返工入口，而不是整集重跑。

## Common Failure Patterns

| symptom | direct_cause | immediate_fix |
| --- | --- | --- |
| 只想补 `角色表现`，却顺手改了镜数 | 没锁 `field_scope` 与返工入口 | 回到 `N3` 前重锁 scope，结构改动另回 `N2` |
| 只修一个 shot，却把整组重写了 | 没锁 `shot_scope` | 回到 patch 决策，保留未命中镜头 |
| closure 修完了，但 JSON 仍是旧的 | 把 `closure_scope` 当业务补丁 | 回 `N7/N8` 外，重新进入正确业务节点 |
| 为了省事全量覆盖 `detail.分镜列表` | 没区分 `group_scope / shot_scope` | 回到 `N1` 或 `N2` 重新锁 patch 边界 |

## Minimal Healthy Pattern

一轮健康的增量 patch，至少应满足：

1. patch scope 唯一明确。
2. 返工入口唯一明确。
3. 未命中 scope 明确保留。
4. 若动骨架，显式回 `N2`。
5. 最终仍回到 `N7/N8` 重写阶段 closure。
