# 4-主体执行流程细则

## Canonical Landing

- 阶段根目录：`projects/<项目名>/主体/`
- 阶段索引：`projects/<项目名>/主体/subject-stage-index.md`
- 阶段验收：`projects/<项目名>/主体/validation-report.md`
- 子路径落点：
  - `projects/<项目名>/主体/1-清单/`
  - `projects/<项目名>/主体/2-设计/`
  - `projects/<项目名>/主体/3-审计/`
  - `projects/<项目名>/主体/4-面板/`

## Mandatory Workflow

1. 读取 `projects/<项目名>/team.yaml`，并按需加载 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 读取上层 `.agents/skills/aigc/SKILL.md + CONTEXT.md` 与 `3-明细` 已有产物。
3. 若顾问团启用且 `roles.planning.members` 非空，先调用 `策划` 顾问团，再进入阶段路由。
4. 判断当前任务是主体抽取、主体设计、设计复核，还是面板布局。
5. 若主链未完成，优先进入 `1-清单` 或 `2-设计`，不默认跳向 `3-审计 / 4-面板`。
6. 在阶段级 `validation-report.md` 前后按需调用 `评审` 顾问团。
7. 产出统一落在 `projects/<项目名>/主体/`，不得散落到其他阶段目录。
8. 每轮结束后输出下一步唯一推荐入口，并把稳定经验回写 `CONTEXT.md`。

## Council Runtime Contract

进入 `4-主体` 或其可直达子技能时，必须先读取：

- `projects/<项目名>/team.yaml`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`

执行规则：

1. 若 `team.yaml` 不存在、`enabled != true`、或全部成员为空，走普通路径。
2. 若启用且 `roles.planning.members` 非空，先以 subagents 模式调用 `策划` 顾问团，获取主体池、结构与资产路线建议。
3. 主代理整合 `策划` 顾问意见后，再产出本轮主体草案与阶段产物。
4. 在 `projects/<项目名>/主体/validation-report.md` 写作前后，若 `roles.review.members` 非空，则调用 `评审` 顾问团给出 PASS/返工意见。
5. 无论顾问团是否启用，最终 canonical 写回权都保留给主代理。
6. 若运行环境不能真实并发 subagents，允许降级为顺序读取 agent 文档并模拟顾问纪要，但必须显式说明降级。
