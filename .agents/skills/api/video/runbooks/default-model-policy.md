# 视频 API 默认模型治理 Runbook

本文件是 `.agents/skills/api/video/` 下“默认模型如何选”的共享真源。  
脚本级单一真源是 `shared/default_model_policy.py`；各 provider `SKILL.md / CONTEXT.md / references/api.md / agents/openai.yaml` 只允许回指本 runbook，并声明自己的 provider 特有过滤条件、别名兼容链与当前解析结果。

## 1. 真源边界

- 父级规范真源：
  - `../SKILL.md`
  - `../CONTEXT.md`
  - 本 runbook `default-model-policy.md`
- 脚本级真源：
  - `../shared/default_model_policy.py`
- 子技能可维护的本地差异：
  - 本 provider 的候选模型集合
  - 哪些模型可算“通用默认值”
  - 同版本内部的档位排序
  - 旧别名兼容回退链
  - 当前解析结果与验证证据

## 2. 规则族

### 2.1 `highest-available-general`

- 语义：在本 provider 当前允许或已登记的模型集合中，先过滤掉不适合当默认值的专用变体，再选择当前可用最高版本的通用模型。
- 共享 helper：`select_highest_model(...)` 或 `select_latest_by_version(...)`
- 适用 provider：
  - `kling`
  - `runway`
  - `veo`
  - `luma`
  - `vidu`
  - `minimax`
- 子技能必须显式声明：
  - 使用哪一个共享 helper
  - 本地过滤条件是什么
  - 当前解析结果是什么

### 2.2 `rolling-latest-quality-alias`

- 语义：若上游官方把稳定别名定义为“当前最新质量优先档”，则默认模型直接跟随该滚动别名，不再把旧长模型号硬编码成默认值。
- 适用 provider：
  - `seedance`
- 子技能必须显式声明：
  - 哪个别名代表“当前最新质量优先档”
  - 哪个别名代表速度优先或低成本试跑
  - 当前官方文档是否仍维持该别名语义

### 2.3 非本次收束范围的其他规则族

- `highest-verified-available`：命名上的更高版本若未实测可用，不得盲目前移。当前适用于 `grok`。
- `highest-tier-candidate-ladder`：默认先尝试最高档位，再按兼容候选链回退。当前适用于 `sora`。

## 3. 执行规则

1. 用户显式传入 `--model` 或等价字段时，默认模型治理不覆盖用户意图；只允许做该 provider 已声明的兼容别名回退。
2. 未显式传入模型时，必须按本 runbook 归属的规则族决定默认值。
3. provider 文档不得各自重写完整选择算法；完整算法只保留在共享 helper 和本 runbook。
4. provider 文档可以写“当前解析结果”，但必须同时写明该结果来自哪条共享规则，而不是本文件自定义的新规则。
5. 需要新增或删除模型时，先改脚本中的本地模型集合与 provider 过滤条件，再更新当前解析结果说明；不要先改文案。

## 4. 子技能落地矩阵

| provider | 规则族 | 脚本真源 | provider 特有差异 |
| --- | --- | --- | --- |
| `kling` | `highest-available-general` | `select_highest_model` | `master/turbo` 档位排序；`sound` 门槛依赖版本 |
| `runway` | `highest-available-general` | `select_highest_model` | `family_rank` 与 `ratio` 默认值绑定 |
| `veo` | `highest-available-general` | `select_highest_model` | 排除 `frames/components` 专用模型 |
| `luma` | `highest-available-general` | `select_latest_by_version` | `ray-2 / ray-v2 / ray2` 同版本偏好与别名回退 |
| `vidu` | `highest-available-general` | `select_highest_model` | 仅 `Vidu-*` 通用模型可作为默认；`mix` 变体排除 |
| `minimax` | `highest-available-general` | `select_latest_by_version` | 仅 `Hailuo-*` 家族参与默认值解析 |
| `seedance` | `rolling-latest-quality-alias` | 脚本常量 `DEFAULT_MODEL=\"seedance\"` | `seedance-fast` 作为速度优先滚动别名 |

## 5. 漂移排查

- 症状：多个 provider 都写“默认模型自动选最高版本”，但条件、过滤器或当前值各说各话。
- 直接原因：默认模型治理没有父级真源，算法和文案散落在子技能自身。
- 规则源：
  - `../SKILL.md`
  - `../CONTEXT.md`
  - 本 runbook
  - `../shared/default_model_policy.py`
- Meta Rule Source：
  - 仓库根 `AGENTS.md` 中的 `Root-Cause First`
  - `Canonical Source Governance Contract`
  - `Skill Composition & Semantics`

## 6. 维护动作

- 若只是当前解析结果变化：
  - 更新 provider 脚本的模型集合或过滤条件
  - 更新 provider `SKILL.md / references/api.md / agents/openai.yaml` 中的“当前解析结果”
- 若规则族变化：
  - 先更新本 runbook 与共享 helper
  - 再让受影响 provider 回指新的规则族
- 若发现某 provider 需要新的规则族：
  - 先在父级 `SKILL.md / CONTEXT.md` 和本 runbook 中建模
  - 再回写到子技能
