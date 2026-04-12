# Execution Flow

## Minimal Flow

1. 读取 `角色清单.json`，锁定 `selected_roles[]`。
2. 读取 `Init + 2-Global + 3-Detail/第N集.json`，组装 `mission_brief_role_design`。
3. 调度 `设计统筹` 生成批次、优先级与返工入口。
4. 对每个命中角色先运行 `形象建模`。
5. 在统一视觉锚点下并行运行：
   - `服装设计`
   - `妆容设计`
   - `个性塑造`
6. 调度 `角色一致性复核`，只返回冲突 note / report。
7. 调度 `真源审计`，检查 evidence lineage、路径与越权项。
8. 父 skill 聚合 patch，写回 `character_design.json + [角色名].md + _manifest.json`。

## Writeback Policy

- 只更新命中角色。
- 只更新命中字段。
- 角色顺序以 `角色清单.json` 为准。
- 已存在角色卡时优先 patch-in-place，不整稿覆盖。

## Rework Policy

- `视觉锚点冲突`：回到 `形象建模`
- `服装与性格冲突`：回到 `服装设计 + 个性塑造`
- `妆容与年龄感冲突`：回到 `妆容设计`
- `跨角色辨识度不足`：回到 `角色一致性复核` 指定角色重做
- `evidence 缺失或越权`：回到 `真源审计` 指定的返工入口
