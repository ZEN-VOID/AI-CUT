# Review Heuristics

本文件保存 `4-Review` 的稳定维护经验。它不覆盖 `SKILL.md`、`references/` 或 `_shared/` 的强制合同。

## Runtime Heuristics

- 卷级终验先看 aggregate JSON，再看 sidecar；sidecar 是证据，不是 gate。
- 子技能并发成立的前提不是目录分开，而是同一轮 fact pack 已锁定。
- source trace 是返工成本控制器；没写清 source owner，后续通常会多返一轮。
- `PASS` 不是完美无瑕，而是无 blocking issue 且下游有明确 handoff。

## Maintenance Heuristics

- 调整维度存在性、权重、hook 或 report filename 时，先改 registry。
- 调整维度内审查细则时，先改对应 child `SKILL.md + CONTEXT.md`。
- 调整结构化字段时，同步 child output contract、checker schema、示例和 runner 消费点。
- `_shared/` 当前是兼容运行时载体；未来若迁移路径，先做全仓引用扫描，再动文件。

## Upgrade Heuristics

- 根 `SKILL.md` 保留首尾合同和动态引用，避免重新长成父层百科。
- `references/` 讲父层边界，`steps/` 讲执行节点，`review/` 讲门禁，`types/` 讲分型。
- `templates/output-template.md` 只对齐 Output Contract，不新增第二套命名或路径规则。
