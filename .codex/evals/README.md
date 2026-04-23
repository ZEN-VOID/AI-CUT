# Eval Harness

本目录用于保存仓库级评测、回归检查与审计样例，不等同于业务运行时目录。

## 当前定位

当前仓库仍处于 HARNESS 引导期与 `aigc.bootstrap_compat` 改造窗口，因此 `.codex/evals/` 的最小职责是：

- 为审计脚本、治理脚本和后续回归检查预留固定根目录
- 承接可重复的最小评测样例、评分器说明与未来 hook/eval 入口
- 避免把评测资产散落在技能目录、报告目录或临时脚本旁边

## 当前最小入口

- `scripts/aigc_harness_audit.py`
- `scripts/aigc_skill_audit.py`

它们目前仍偏“结构与合同审计”，还不是完整的内容质量评测套件；但后续所有 harness 级 eval 都应优先回收到本目录，而不是新开平行根。

## 建议内容形态

```text
.codex/evals/
├── fixtures/
├── scorecards/
├── regression/
└── README.md
```

说明：

- `fixtures/`
  - 放最小样例输入、样例项目快照或审计基准数据
- `scorecards/`
  - 放评分口径、通过标准、维度定义
- `regression/`
  - 放回归用例、预期输出摘要、diff 说明

## AIGC 侧使用原则

对 `.agents/skills/aigc/`：

- 先保证 `registry + routes + runbook + templates + audit` 稳定
- 再逐步把阶段级回归样例和 cross-stage eval 收到本目录
- 在 `bootstrap_compat` 窗口内，允许先以审计脚本为主，不要求一次补齐所有内容评测

## 反漂移要求

1. 不要把 `.codex/evals/` 当成报告归档目录；报告仍应进入 `reports/`。
2. 不要把项目运行时产物直接塞进 eval 根目录；样例应是可重复、可裁剪、可回归的最小包。
3. 新增正式 eval 套件时，应同步更新：
   - `HARNESS.md`
   - 对应 runbook / registry / audit 说明

