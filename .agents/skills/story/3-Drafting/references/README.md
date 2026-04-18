# Drafting References

`3-Drafting/references/` 现在采用“两层路由 + 模块内 appendix / leaf-notes”治理：

1. 根 `SKILL.md` 只路由到 `references/<module>/module-spec.md`
2. 各 step 模块按需再进入 `writing-craft-catalog` 或自己的 appendix
3. step appendix 下沉到各自模块目录；craft 叶子文档下沉到 `writing-craft-catalog/leaf-notes/`

## 层级关系

- Tier 1：工作流 step 模块
  - `step-1-context-contract`
  - `step-2-style-pass`
  - `step-3-review-gate`
  - `step-4-polish-gate`
  - `step-5-data-writeback`
- Tier 2：跨 step 的 craft 目录模块
  - `writing-craft-catalog`
- Tier 3：模块内 appendix / craft notes
  - `references/<step-module>/appendix-*.md`：只作为对应 step 模块的附属 appendix
  - `references/writing-craft-catalog/leaf-notes/*.md`：只作为 `writing-craft-catalog` 的 leaf craft notes

## 加载规则

1. 先由主 [`SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/SKILL.md) 判定当前 step。
2. 进入对应 `module-spec.md`，由该模块决定是否需要进一步加载 appendix 或 `writing-craft-catalog`。
3. `writing-craft-catalog` 只服务 Step 1 / 2B / 4 的局部强化，不单独启动工作流。
4. 若 leaf note 与 step 模块发生冲突，以根 `SKILL.md` 与 step `module-spec.md` 为准。

## 模块索引

| 模块 | 类型 | 何时加载 | 与谁协作 | 入口 | 局部经验层 |
| --- | --- | --- | --- | --- | --- |
| `step-1-context-contract` | `step-playbook` | Step 1 或执行包失焦返工 | 可串 `writing-craft-catalog` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-1-context-contract/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-1-context-contract/CONTEXT.md) |
| `step-2-style-pass` | `step-playbook` | Step 2B | 可串 `writing-craft-catalog` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-2-style-pass/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-2-style-pass/CONTEXT.md) |
| `step-3-review-gate` | `step-playbook` | Step 3 | 强依赖 `4-Validation` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-3-review-gate/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-3-review-gate/CONTEXT.md) |
| `step-4-polish-gate` | `step-playbook` | Step 4 | 可串 `writing-craft-catalog` | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-4-polish-gate/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-4-polish-gate/CONTEXT.md) |
| `step-5-data-writeback` | `step-playbook` | Step 5 | 与 `data-agent` 对齐 | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-5-data-writeback/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/step-5-data-writeback/CONTEXT.md) |
| `writing-craft-catalog` | `craft-playbook` | Step 1 / 2B / 4 命中 craft 症状或题材 hook | 不单独持有流程路由权 | [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/writing-craft-catalog/module-spec.md) | [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/references/writing-craft-catalog/CONTEXT.md) |

## 报告

- 本轮 references 架构报告：
  - [`reference-architecture-report-20260408.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/reports/reference-architecture-report-20260408.md)
- `think-think` 显式设计快照已下沉到各 `module-spec.md`，不再额外维护第二份根级报告真源。
