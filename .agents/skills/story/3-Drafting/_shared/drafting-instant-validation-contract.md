# Drafting Instant Validation Contract

本文件定义 `3-Drafting` 的 step-after-write 即时审计合同。

## Canonical Source

即时审计维度、step hook 映射、终验 mandatory 规则的单一真源固定为：

- `../../4-Validation/_shared/validation-dimension-registry.yaml`

本文件只定义：

- `3-Drafting` 如何消费 registry
- step 失败后的回退与重写顺序
- `7-润色` 完成后的候选终稿边界

## Core Rule

`3-Drafting` 不再是“7 道工序一路写到最后再统一发现问题”的单线流程。

新合同固定为：

1. 当前 step 写回 `第N集.md`
2. 父层读取 registry 中当前 `step_id` 对应的 validation dimensions
3. 立即运行这些 inline validators
4. 若 hook 失败，先在当前 step 或最早受影响 step 修复
5. 只有当前 step 对应 hook 通过，才允许进入下一个 step
6. 下一个 step 的正式执行，必须以上一个 step“已写回且已通过 hook”的 root 为输入；不得跳过 gate 做批量串改。

## True Serial Gate

`3-Drafting` 的正式运行模式固定为：

- `Step 1` 单独起盘、单独写回、单独跑 `Step 1` hook
- `Step 2` 单独改稿、单独写回、单独跑 `Step 2` hook
- 依此类推直到 `Step 7`

以下行为一律视为违约：

- 把多个 step 合并成一次总改稿后再统一写回
- 在 `Step N` hook 未通过前提前执行 `Step N+1` 的正式写回
- 先生成 `Step 1-7` 全套正式 patch，再倒序或批量补跑 hooks
- 把“step 内部草稿比较”伪装成“已完成正式 step”

## Failure Routing Order

### A. 当前 step 局部问题

- 条件：
  - issue 的 `rework_target_step == 当前 step`
  - `source_layer_owner == 3-Drafting`
- 动作：
  - 立即在当前 step 重写
  - 重跑当前 step 的 inline hooks

### B. 更早 step 的累积问题

- 条件：
  - issue 的 `rework_target_step` 指向更早 drafting 节点
- 动作：
  - 回退到最早受影响 step
  - 从该 step onward 重新执行
  - 不允许只修当前 step 然后硬推进

### C. 上游 source truth 问题

- 条件：
  - issue 的 `source_layer_owner` 指向 `0-Init / 1-Cards / 2-Planning`
- 动作：
  - 立即停止 drafting 主链
  - 转 `back_to_source_contract`
  - 不允许继续把正文当成兜底层硬修

## Candidate Final Draft Rule

- `7-润色` 完成后，如果它对应的 inline hooks 通过：
  - 当前集获得 `candidate_final_draft` 状态
- 这不等于最终 `PASS`
- 只有进入 `4-Validation` 终验层并拿到 `validation_status = PASS`：
  - 才能变成 `validated_final_draft`

## Process Log Rule

每个 drafting step 的 `process_log_entry` 必须补充：

- `instant_validation_summary`
- `instant_validation_refs`
- `rework_route_hint`

目的：

- 让 `resume/` 能知道当前 step 是否已通过 inline gate
- 让 `4-Validation` 能看到 drafting 阶段已经做过哪些即时修复

## Extension Rule

若未来新增或调整 validation 维度：

1. 优先改 `validation-dimension-registry.yaml`
2. 再改对应 validator child package
3. `3-Drafting` 父层只需要继续按 registry 取 hook，不应手工扩写 7 个 step 的维度名单
