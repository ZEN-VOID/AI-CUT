# 4-Design / 1-主体清单 / Shared List Output Contract

## Purpose

- 本文件是 `4-Design/1-主体清单` 四个 sibling leaf 的共享输出真源。
- 它回答三件事：
  1. 哪个文件是每个类目的 canonical business truth。
  2. 哪些文件只是为下游设计准备的派生 sidecar。
  3. `_manifest.json` 在清单阶段的统一地位是什么。

## Canonical Layering

### Base Pair（所有 sibling leaf 强制对齐）

1. `<领域>清单.json`
   - 当前 episode 的唯一对象池真源。
   - 供后续阶段锁定 identity、coverage、group/shot 回链与统计口径。
2. `_manifest.json`
   - 审计与批处理侧车。
   - 记录输入、输出、统计、模式与提示信息。
   - 不是业务事实真源，不得承载对象研究或设计结论。

### Derived Sidecars（仅在该领域后续阶段确实需要时生成）

- `道具`
  - `道具研究.json`
  - `prop_design_bridge.json`
- `服装`
  - `服装研究.json`
  - `costume_design_bridge.json`
- `角色`
  - 无强制派生 sidecar；`1-清单` 只需稳定角色对象池。
- `场景`
  - 无强制派生 sidecar；`1-清单` 只需稳定场景对象池。

## Naming Matrix

| 领域 | canonical catalog | derived sidecars | audit sidecar |
| --- | --- | --- | --- |
| `场景` | `场景清单.json` | 无 | `_manifest.json` |
| `角色` | `角色清单.json` | 无 | `_manifest.json` |
| `道具` | `道具清单.json` | `道具研究.json`、`prop_design_bridge.json` | `_manifest.json` |
| `服装` | `服装清单.json` | `服装研究.json`、`costume_design_bridge.json` | `_manifest.json` |

## Common Output Shell

所有 `<领域>清单.json` 优先对齐以下最小壳：

1. `meta`
2. `<domain_objects[]>`
3. `group_<domain>_map`
4. `statistics`

允许的领域补充块：

- `presentation`
- `acceptance_notes`
- `groups_without_props`

禁止做法：

- 用 `_manifest.json` 承载对象池事实。
- 为了追求“文件数量统一”而给 `角色/场景` 强行补研究或 bridge。
- 把 `研究.json` 或 `*_design_bridge.json` 升格为对象池真源。

## Transition Rule

- `场景/1-清单` 历史产物 `第N集.json` 降级为 legacy alias。
- 新写出默认统一为 `场景清单.json`。
- 下游消费方在迁移期可兼容读取 legacy alias，但所有新合同、脚本默认值和示例路径都必须回指 `场景清单.json`。

## Selection Verdict

“一个 canonical catalog + 一个 audit manifest + 按需派生 sidecar” 是当前最优结构，原因如下：

1. 保留单一对象池真相，不让多个 JSON 争夺主权。
2. 不逼所有领域都生产同样数量的文件，避免角色/场景空转造稿。
3. 给道具/服装保留研究与 bridge，因为它们的 `2-设计` 确实以此为直接输入。
