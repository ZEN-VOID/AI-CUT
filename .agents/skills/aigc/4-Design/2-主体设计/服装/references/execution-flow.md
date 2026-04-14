# Execution Flow

## Minimal Flow

1. 读取 `服装清单.json / 服装研究.json / costume_design_bridge.json`，锁定 `selected_costumes[]`。
2. 读取 `Init + 2-Global + 3-Detail/第N集.json`，组装 `mission_brief_costume_design`。
3. 调度 `服装统筹` 生成批次、优先级与返工入口。
4. 在同一 tranche 并行运行：
   - `廓形层次设计师`
   - `材质纹样设计师`
   - `配饰连续性设计师`
5. 调度 `服装一致性复核`，只返回冲突 note / report。
6. 父 skill 聚合 patch，写回 `服装设计.json + [costume_id]-[canonical_label].md`。
7. 调度 `提示词架构师`，生成 `costume_design_prompt.json`。
8. 调度 `真源审计`，检查 evidence lineage、路径与越权项。

## Rework Policy

- `廓形与材质冲突`：回到 `廓形层次设计师 + 材质纹样设计师`
- `配饰与 continuity 冲突`：回到 `配饰连续性设计师`
- `prompt 与 canonical facts 脱链`：回到 `提示词架构师`
- `evidence 缺失或越权`：回到 `真源审计` 指定的返工入口
