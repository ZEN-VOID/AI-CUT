# AIGC Learn Output Template

**重要声明**：本模板是可选的**执行副产物**，不是任务完成标志。

执行型改进的完成标志是：
- `N8-AUDIT` 通过（`pass` 或 `pass_with_followups`）
- `changed_files` 包含实际修改的技能文件
- `audit_result` 显示协调审计通过

报告只是追溯和审计凭证，仅在以下情况生成：
- 用户明确要求生成报告
- 需要审计追溯时
- 需要记录执行摘要供后续参考

## Output Contract Alignment

| field | mapping |
| --- | --- |
| **核心执行产物** | `changed_files`（实际修改的技能文件）、`audit_result`（协调审计通过）、`residual_risks` |
| **可选报告副产物** | 仅在用户要求或需要审计追溯时生成 |
| Output format | 核心产物默认对话交付；报告仅在用户要求时使用本模板生成 |
| Output path | 核心产物不落盘；报告仅在用户要求时落到 `reports/aigc-learn-YYYYMMDD.md` |
| Naming convention | kebab-case with `YYYYMMDD`；evidence sidecar slugs ASCII-safe |
| **Completion gate** | **审计通过（pass / pass_with_followups）+ changed_files 已验证 = 任务完成**，不需要报告 |

## Template

> **警告**：以下模板仅用于可选的报告副产物。默认执行时不需要生成此报告。

```markdown
# AIGC Learn Report — Optional Byproduct

> 本报告是执行副产物，不是任务完成标志。完成任务的标准是：审计通过 + changed_files 已验证。

## Execution Summary

- **learning_object**:
- **target_scope**:
- **mode**:
- **writeback_permission**:
- **audit_result**: [pass / pass_with_followups]
- **changed_files**: [实际修改的技能文件列表]

## Source Digest（证据锚点）

- source_kind:
- source_locator:
- source_owner:
- captured_at:
- credibility:
- license_boundary:
- evidence_units:
- gaps:

## Key Findings

| item | finding | landing |
| --- | --- | --- |

## Changed Files

| file | action | summary |
| --- | --- | --- |
| | | |

## Audit Result

- mode:
- verdict:
- checks:
- degraded_reason:

## Residual Risks

- |

## Deposition Note

- next_learning_deposition:
```