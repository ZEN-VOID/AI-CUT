# Step 5 Debt Switch

> Canonical module route: `references/step-5-data-writeback/module-spec.md`
> 当前角色：Step 5 appendix。根 `SKILL.md` 不再直接路由到本文件。

## 默认策略

- 债务利息默认关闭。
- 只有两种情况允许开启：
  - 用户明确要求开启；
  - 项目已显式启用债务追踪。

## 执行命令

```bash
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" index accrue-interest --current-chapter {chapter_num}
```

## 执行后要求

- 在 Step 5 输出中标注本次是否执行了利息计算。
- 若执行，输出结果摘要：处理债务数、累计利息、是否出现逾期。
- 若未执行，明确标注 `debt_interest: skipped (default off)`。
