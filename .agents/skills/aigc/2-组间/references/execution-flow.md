# 2-组间阶段执行流程细则

## Canonical Landing

- 阶段运行时根：`projects/<项目名>/编导/`
- 统一根文件：`projects/<项目名>/编导/第N集.json`
- thinking sidecar：`projects/<项目名>/编导/thinking/`
- 阶段验证报告：`projects/<项目名>/编导/validation-report.md`
- 运行时布局真源：`.agents/skills/aigc/_shared/project-runtime-layout.md`

## Council Runtime Contract

进入 `2-组间` 或其可直达子技能时，必须先读取：

- `projects/<项目名>/team.yaml`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`

执行规则：

1. 若 `team.yaml` 不存在、`enabled != true`、或全部成员为空，走普通路径。
2. 若启用且 `roles.supervision.members` 非空，先以 subagents 模式调用 `监制` 顾问团，获取执行一致性、资源感与可拍性建议。
3. 主代理整合 `监制` 顾问意见后，再产出本轮组间草案与阶段产物。
4. 在 `projects/<项目名>/编导/validation-report.md` 写作前后，若 `roles.review.members` 非空，则调用 `评审` 顾问团给出 PASS/返工意见。
5. 无论顾问团是否启用，最终 canonical 写回权都保留给主代理。
6. 若运行环境不能真实并发 subagents，允许降级为顺序读取 agent 文档并模拟顾问纪要，但必须显式说明降级。

## Mandatory Workflow

1. 读取 `projects/<项目名>/team.yaml`，并按需加载 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 读取 `projects/<项目名>/Init/` 与 `projects/<项目名>/规划/` 的已有产物。
3. 若顾问团启用且 `roles.supervision.members` 非空，先调用 `监制` 顾问团，再进入阶段路由。
4. 判断当前请求属于三个子路径中的哪一个唯一主入口。
5. 若目标是 `导演意图`，先检查 `全局风格`、`类型元素` 与必要的规划容器是否存在。
6. 若请求混入节奏蓝图裁决，先检查 `projects/<项目名>/规划/4-节奏/第N集.md` 是否存在；不存在则回退补该规划层 handoff。
7. 若目标子路径合同缺失，停止向下伪造，返回缺口与补建落点。
8. 若目标子路径合同存在，则先检查 `projects/<项目名>/编导/第N集.json` 是否存在；若不存在，先基于 shared bootstrap template 自动创建，并从 `story-source-manifest.yaml`、`规划/第N集.md` 与 `1-分集` 结果回填 `metadata.source_profile`，再进入对应子技能执行。
9. 在阶段级 `validation-report.md` 前后按需调用 `评审` 顾问团。
10. 将阶段产物与阶段验收结论 patch 回 `projects/<项目名>/编导/第N集.json` 与 `projects/<项目名>/编导/validation-report.md`。
11. 返回唯一推荐的下一阶段入口。

## Handoff Rule

- `2-组间` 是 `1-规划` 与 `3-明细` 之间的组间设计真源层。
- `全局风格 + 类型元素` 组成全组共享底座与分组动态偏置规则。
- `导演意图` 是按集承载、按组执行的导演设计加载层。
- 分组后的节奏蓝图由 `1-规划/4-节奏` 提供，`2-组间` 默认只读取并继承，不在本阶段重建第二份真源。
- 完成阶段后，唯一默认 handoff 方向是 `3-明细`。
