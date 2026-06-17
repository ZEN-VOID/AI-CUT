# Drafting Instant Validation Compatibility Contract

本文件定义 `3-初稿` 历史 step-after-write runtime 的兼容审计合同。

当前正式主路径已改为根级 `3-初稿` 直接执行 chapter-native 豆包正文创作；本文件只服务仍依赖旧批次日志/step ledger 的运行时与恢复链路，不再定义主技能的第一执行口径。

## Canonical Source

即时审计维度、step hook 映射、终验 mandatory 规则的单一真源固定为：

- `../SKILL.md#Built-in Acceptance Contract`
- `../review/review-contract.md`

本文件只定义：

- `3-初稿` 如何消费 registry
- step 失败后的回退与重写顺序
- `N5-CREATIVE-DRAFT` 完成后的候选初稿边界

## Core Rule

`3-初稿` 不再是“7 道工序一路写到最后再统一发现问题”的单线流程。

新合同固定为：

1. 当前 step 写回 `第N章.md`
2. 父层读取 registry 中当前 `step_id` 对应的 validation dimensions
3. 立即运行这些 inline validators
4. 若 hook 失败，先在当前 step 或最早受影响 step 修复
5. 只有当前 step 对应 hook 通过，才允许进入下一个 step
6. 下一个 step 的正式执行，必须以上一个 step“已写回且已通过 hook”的 root 为输入；不得跳过 gate 做批量串改。

## Runtime Command Chain

`3-初稿` 在 workflow runtime 中的正式命令链固定为：

`start-task -> start-step -> complete-step -> inline validation -> pass or block -> current-step rewrite / rewind / source-fix routing`

约束解释：

1. `start-task` 锁当前章 drafting run，但不放松任一步的串行 gate。
2. `start-step` 只允许进入“当前 registry 与 runtime 判定可进入”的 step。
3. `complete-step` 必须直接触发当前 step 的 inline validation batch；不得先记完成、后补 gate。
4. 若 batch 结果为 `block`，runtime 必须阻断后续 `start-step`，直到：
   - 当前 step 重写后重跑通过，或
   - 回卷到最早受影响 step 并重新执行，或
   - 改走 source fix。
5. 因此，“step 完成”在 drafting 语义里等于“写回并进入 gate”，不等于“天然可以开始下一步”。

## True Serial Gate

`3-初稿` 的正式运行模式固定为：

- `Step 1` 单独起盘、单独写回、单独跑 `Step 1` hook
- `Step 2` 单独改稿、单独写回、单独跑 `Step 2` hook
- 依此类推直到 `Step 8`

以下行为一律视为违约：

- 把多个 step 合并成一次总改稿后再统一写回
- 在 `Step N` hook 未通过前提前执行 `Step N+1` 的正式写回
- 先生成 `Step 1-8` 全套正式 patch，再倒序或批量补跑 hooks
- 把“step 内部草稿比较”伪装成“已完成正式 step”

## Failure Routing Order

### A. 当前 step 局部问题

- 条件：
  - issue 的 `rework_target_step == 当前 step`
  - `source_layer_owner == 3-初稿`
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
  - issue 的 `source_layer_owner` 指向 `0-初始化 / 1-设定 / 2-卷章`
- 动作：
  - 立即停止 drafting 主链
  - 转 `back_to_source_contract`
  - 不允许继续把正文当成兜底层硬修

## Candidate Draft Acceptance Rule

- `N5-CREATIVE-DRAFT` 完成后，如果即时 hooks 通过：
  - 当前章获得 `candidate_draft` 状态
- 这不等于初稿验收 `PASS`
- 额外硬门槛：
  - 当前章在 `第V卷.写作日志.yaml.chapter_step_history[chapter_ref]` 中已收满 8 条正式 step 记录
  - 当前章在 `第V卷.写作日志.yaml.chapter_hook_results[chapter_ref]` 中已收满 8 条对位 hook 结果
  - 不存在以 Step 8 汇总、批量补记或事后倒填冒充逐步留痕的情况
- 只有 `3-初稿` 自动执行 `N6-AUTO-ACCEPTANCE` 并拿到 `acceptance_status = PASS`：
  - 才能变成 `accepted_draft`
  - `handoff_targets` 只能包含 `4-润色`，不得包含 `return`

## Process Log Rule

每个 drafting step 的 `process_log_entry` 必须补充：

- `instant_validation_summary`
- `instant_validation_refs`
- `hook_status`
- `hook_checked_dimensions`
- `hook_checked_at`
- `rework_route_hint`
- 若项目主角启用了成长系统，且当前 step 为 `4 / 6 / 7`，优先补 `growth_axis_evidence`

目的：

- 让 `resume/` 能知道当前 step 是否已通过 inline gate
- 让 `3-初稿` 内置验收能看到 drafting 阶段已经做过哪些即时修复
- 让父层能够证明当前卷真实完成了 `chapter_refs x 8 步`，而不是只在卷末回填若干摘要

### Volume-Ready Gate Addendum

卷级 `candidate_volume_draft` 额外必须满足：

1. `chapter_step_history` 对当前卷全部 `chapter_ref` 全部写满，每章恰有 8 条正式 step 记录。
2. `chapter_hook_results` 对当前卷全部 `chapter_ref` 全部写满，每章恰有 8 条对位 hook 结果。
3. 任一章节若缺 step 记录、缺 hook 结果、顺序错位、或出现“卷末统一补记”的稀疏日志模式，卷级 gate 必须直接 `block`，不得生成初稿 PASS。

### Pre-Validation Quality Gate Addendum

在卷级 `candidate_volume_draft` 之后、正式 handoff `4-润色` 之前，父层还必须追加一轮卷级质量闸门：

1. 把结论写入 `第V卷.写作日志.yaml -> quality_gate_snapshot`
2. `quality_gate_snapshot` 至少包含：
   - `checkpoint_stage: pre_acceptance`
   - `accepted_at`
   - `verdict: ready_for_acceptance|rework_required_before_acceptance`
   - `guard_axes`
   - `representative_chapter_refs`
   - `primary_issues`
   - `priority_rework_targets`
   - `next_action: 3-初稿-acceptance|3-初稿-rework`
3. 默认必须经过 `../scripts/drafting_volume_quality_guard.py`
4. 若 guard 返回 `block`：
   - runtime / resume 下一稳定入口必须仍是 `3-初稿`
   - 不得把 `next_step` 继续写成 `review`
5. 若 guard 返回 `pass`，才允许把当前卷交给 `3-初稿` 内置验收；验收 PASS 后再交 `4-润色`

## Extension Rule

若未来新增或调整 validation 维度：

1. 优先改 `3-初稿/SKILL.md#Built-in Acceptance Contract`
2. 再改 `3-初稿/review/review-contract.md` 的维度展开
3. `3-初稿` 父层只需要继续按阶段内置验收合同取 hook，不应另建独立验收目录或平行 registry
