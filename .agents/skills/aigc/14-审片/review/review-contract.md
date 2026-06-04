# Review Contract

## Verdict

本复核合同服务 `SKILL.md#Review Gate Binding` 和 `review/review-gate.md`。它不新增审片入口、节点、fail code 或输出路径，只定义 final review 的汇流口径。

| verdict | meaning | required evidence |
| --- | --- | --- |
| `pass` | 视频本体、prompt / 分镜组匹配和创作质量三层均通过，且无阻断 finding | 真实视频证据、source anchor、method_selection、finding list、operation plan |
| `conditional_pass` | 视频可用但非优先候选，或只适合特定剪辑/上下文 | 条件说明、风险、替代候选或补拍建议 |
| `rerun_required` | prompt 可执行但模型单次失败，或素材局部瑕疵阻断使用 | model_problem 证据、rerun operation、无需改组理由 |
| `repair_required` | prompt、分组、资产、声音或 LibTV 节点证据指向上游可修问题 | owner、patch scope、授权状态、changed_files |
| `blocked` | 缺视频、缺 source、缺证据、LibTV 未下载或节点不唯一 | fail_code、rework_target、最小澄清项 |

## Review Flow

1. 先读 `SKILL.md#Convergence Contract`，确认 `CV-1` 到 `CV-6` 是否通过。
2. 再读 `review/review-gate.md` 的 gate 和 failure routing。
3. 对每个未通过 gate 输出 `FAIL-REVIEW-*`、rework target 和报告证据。
4. 只在所有必需 gate 通过后给出 final verdict。

## Boundary

- 本文件不替代真实视频理解。
- 本文件不替代 `10-分组`、LibTV prompt、源层技能或项目 `MEMORY.md` 的 owning source。
- 本文件不允许把本地 checklist 伪装为外部 provider 复核。
