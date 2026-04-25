# 4-Design / 1-清单 / Shared List Output Contract

## Purpose

- 本文件是 `4-Design/1-清单` 四个 sibling leaf 的共享输出治理真源。
- 它回答三件事：
  1. 哪个文件是每个类目的 canonical business truth。
  2. 哪些文件是研究真源与 bridge 真源。
  3. `_manifest.json` 在清单阶段的统一地位是什么。

## Canonical Layering

### Business Truth Triad（场景 / 角色 / 道具强制对齐）

`场景 / 角色 / 道具` 当前统一采用三真源：

1. `<领域>清单.json`
   - 对象池、identity、coverage、group/shot 回链真源。
2. `<领域>研究.json`
   - 证据账本、研究结论、可读展示卡与质量诊断真源。
3. `<domain>_design_bridge.json`
   - 下游 `2-设计` 直参、prompt-ready 字段、负面约束与 continuity guard 真源。

三真源不是三份平行总稿：每份只拥有自己的字段边界，禁止互相复制成同构大包。

### Audit Sidecar（所有 sibling leaf 可对齐）

1. `_manifest.json`
   - 审计与批处理侧车。
   - 记录输入、输出、统计、模式与提示信息。
   - 不是业务事实真源，不得承载对象研究或设计结论。

### Derived / Future Sidecars

- `服装`
  - `服装研究.json`
  - `costume_design_bridge.json`

## Naming Matrix

| 领域 | catalog truth | research / bridge truth | audit sidecar |
| --- | --- | --- | --- |
| `场景` | `场景清单.json` | `场景研究.json`、`scene_design_bridge.json` | `_manifest.json` |
| `角色` | `角色清单.json` | `角色研究.json`、`role_design_bridge.json` | `_manifest.json` |
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
- `design_context`
- `quality_overview`
- `props[].design_context`

禁止做法：

- 用 `_manifest.json` 承载对象池事实。
- 把 `研究.json` 或 `*_design_bridge.json` 复制成第二份对象池。
- 把 `<领域>清单.json` 写成研究结论或 prompt bridge 的唯一来源。
- 三真源字段职责不清，导致下游不知道该消费哪一份。

## Transition Rule

- `场景/1-清单` 历史产物 `第N集.json` 降级为 legacy alias。
- 新写出默认统一为 `场景清单.json`。
- 旧仓 `场景研究.json / scene_design_bridge.json` 在当前仓恢复为三真源成员，但必须遵守字段边界，不得与 `场景清单.json` 抢对象池主权。
- 下游消费方在迁移期可兼容读取 legacy alias，但所有新合同、脚本默认值和示例路径都必须回指 `场景清单.json`。

## Selection Verdict

“三业务真源 + 一个 audit manifest” 是当前最优结构，原因如下：

1. `清单 / 研究 / bridge` 分别承载 identity、evidence/research、design handoff，职责清楚。
2. 场景、角色、道具三条 leaf 的输出形态一致，便于下游 `2-设计` 稳定路由。
3. `_manifest.json` 仍只做审计侧车，避免业务事实被批处理元数据污染。
