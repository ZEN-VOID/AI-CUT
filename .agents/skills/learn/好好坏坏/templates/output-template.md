# Output Template

## Output Contract Alignment

- Required output: 源层调优后的目标 skill 改动，以及包含 `good_signals`、`bad_signals`、`source_owner`、`patch_surface`、`sync_scope`、`validation_checks`、`review_gate`、`learning_writebacks`、`residual_risks` 的 good/bad contrast summary。
- Output format: 目标文件 patch、必要同步面、最终中文摘要；用户要求报告时渲染为 Markdown。
- Output path: 默认原地修改目标 skill；报告类派生产物按用户要求写入 `reports/`。
- Naming convention: 报告使用 `好好坏坏-YYYYMMDD.md`；机器可读键保持 ASCII 安全字符。
- Completion gate: 通过结构/引用检查、样例解释检查、过拟合检查和本地 review gate；若 reviewer 降级，报告阻断来源和未启动项。

## Contrast Summary

| field | value |
| --- | --- |
| `target_skill_ref` |  |
| `task_stage_or_output` |  |
| `selected_type_packages` |  |
| `review_gate` |  |

## Diagnosis Matrix

| contrast_id | good_signal | bad_signal | requirement_or_source_basis | direct_output_cause | source_owner | patch_action | validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `C1` |  |  |  |  |  |  |  |

## Source Patch Plan

| patch_surface | reason | sync_scope | validation_check |
| --- | --- | --- | --- |
|  |  |  |  |

## Changes Made

-

## Evidence

-

## Review Result

- Verdict:
- Residual risks:
- Learning writebacks:
