# github-issue CONTEXT

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 1866
current_lines: 60
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

### issue-local-fix-only

- 症状：Issue 表面问题被补丁遮住，但没有说明规则源、模板、脚本、校验器或共享 helper 是否需要同步修复。
- 根因层：标准流程第 2-4 步没有走完，只做了 Direct Cause，没有做 `Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
- 立即修复：补齐 layered trace，确认最高杠杆修复点；如果确实只有局部代码原因，也要在输出中说明为什么没有更高层规则源。
- 系统预防：把重复出现的同类遗漏沉淀到本文件，稳定后晋升到相关 runbook、validator 或 `SKILL.md`。
- 验证点：最终汇报能同时说明根因位置、修复点、验证结果和 Issue 关联方式。

### issue-validation-drift

- 症状：修复后只跑无关的大范围检查，或完全没有复现/验证 Issue 指向的问题。
- 根因层：验证没有绑定 Issue 的复现步骤、期望行为与影响范围。
- 立即修复：先做最贴近问题表面的最小充分验证，再按风险补充更广检查。
- 系统预防：在 PR 说明中固定列出“复现/验证了什么”，避免只写泛化测试名。
- 验证点：相关测试或质量检查通过，且能证明 Issue 指向的问题已修复。

### issue-linkage-lost

- 症状：代码已修，但提交或 PR 没有关联 Issue，后续无法自动关闭或追踪。
- 根因层：标准流程第 6-7 步遗漏。
- 立即修复：提交信息或 PR 描述补上 `Fixes #<issue>` 等可识别关联。
- 系统预防：收尾前检查 Issue 编号、分支、提交、PR 四者是否一致。
- 验证点：PR 与 Issue 页面能互相追溯。

### issue-input-under-specified

- 症状：用户只给了模糊问题描述，执行时直接猜修复范围。
- 根因层：标准流程第 1 步未先读取 Issue 详情、复现步骤、期望行为和影响范围。
- 立即修复：优先获取 Issue URL/编号并读取正文；缺少关键输入时先询问或在仓库内找可证据化线索。
- 系统预防：把“Issue 详情读取完成”作为进入定位阶段前的 gate。
- 验证点：后续定位与修复都能回指 Issue 中的具体症状或复现条件。

## Repair Playbook

1. 先回读同目录 `SKILL.md`，确认 issue 处理的源层追踪、验证和收束要求。
2. 读取 Issue 详情，先固定问题描述、复现步骤、期望行为和影响范围；没有这些信息时，不直接进入修复。
3. 定位时同时看运行产物、调用链和数据流，再继续上溯到规则源与元规则源。
4. 优先修能阻止复发的源层入口；只有确认源层不需要变更时，才只做局部代码修复。
5. 验证先贴近 Issue 表面，再按改动风险扩大；不要用无关大测试替代复现验证。
6. 收尾检查提交或 PR 是否包含 Issue 关联，最终说明根因位置、修复点和验证结果。
7. 若发现同类 issue 修复反复遗漏规则源、模板、脚本或校验器，同轮沉淀为可复用失败模式；稳定后再晋升到 `SKILL.md`、runbook 或相关脚本。

## Reusable Heuristics

- 这类命令最容易遗漏“规则源修复”，所以必须在执行前先回读正文里的 layered trace 要求。
- 若只修局部代码却没补规则入口、模板、脚本或校验器，通常不算真正闭环。
- Issue 修复的最小闭环不是“代码变了”，而是“症状可复现、原因可解释、修复可验证、关联可追踪”。
- 测试选择以 Issue 影响面为锚点：先证明目标问题消失，再考虑相邻回归。
- PR 描述不要只列改动文件；必须能让审阅者看出这次修复为什么对准了 Issue。

## Promotion Backlog

- 若多次出现忘记 `Fixes #<issue>` 的情况，考虑把 Issue 关联检查晋升到提交/PR runbook。
- 若多次出现只修局部、不追规则源的情况，考虑增加一个轻量 issue-close checklist。
- 若多次出现验证漂移，考虑为该命令补充“复现证据 -> 验证命令 -> 结果摘要”的固定 PR 模板段。
