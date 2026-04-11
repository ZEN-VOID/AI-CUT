# aigc 3-明细 / Execution Flow

本文件承载 `aigc 3-明细` 的 canonical landing、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- 阶段索引：`projects/<项目名>/编导/detail-stage-index.json`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 子路径证据目录：
  - `projects/<项目名>/编导/evidence/1-分镜表现/`
  - `projects/<项目名>/编导/evidence/2-角色表现/`
  - `projects/<项目名>/编导/evidence/3-运镜手法/`
  - `projects/<项目名>/编导/evidence/4-场景氛围/`
  - `projects/<项目名>/编导/evidence/5-摄影美学/`
  - `projects/<项目名>/编导/evidence/6-转场特效/`
- 运行时布局真源：`.agents/skills/aigc/_shared/project-runtime-layout.md`

## Council Runtime Contract (Mandatory)

进入 `3-明细` 或其可直达子技能时，必须先读取：

- `projects/<项目名>/team.yaml`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`

执行规则：

1. 若 `team.yaml` 不存在、`enabled != true`、或全部成员为空，走普通路径。
2. 若启用且 `roles.supervision.members` 非空，先以 subagents 模式调用 `监制` 顾问团，获取执行一致性、资源感与可拍性建议。
3. 主代理整合 `监制` 顾问意见后，再产出本轮脚本草案与阶段产物。
4. 在 `projects/<项目名>/编导/validation-report.md` 写作前后，若 `roles.review.members` 非空，则调用 `评审` 顾问团给出 PASS/返工意见。
5. 无论顾问团是否启用，最终 canonical 写回权都保留给主代理。
6. 若运行环境不能真实并发 subagents，允许降级为顺序读取 agent 文档并模拟顾问纪要，但必须显式说明降级。

## Mandatory Workflow

1. 读取 `projects/<项目名>/team.yaml`，并按需加载 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 读取 `1-规划` 已完成产物与 `2-组间` 已 patch 的 episode root，锁定 grouped source。
3. 若顾问团启用且 `roles.supervision.members` 非空，先调用 `监制` 顾问团，再进入阶段路由。
4. 先完整读取 `projects/<项目名>/编导/第N集.json`；若不存在，先回退到 `2-组间` 完成首次建根，不得再假定 `1-分集` 已提前创建根文件。
5. 判断本轮任务属于哪个唯一子路径，或是否要按默认顺序串行推进多个子路径。
6. 每个子路径只能在既有统一根文件上 `patch-in-place`，不得另起平行正文。
7. 每轮扩写都要同步写入本阶段或子路径证据侧车。
8. 在阶段级 `validation-report.md` 前后按需调用 `评审` 顾问团。
9. 结束后输出阶段验收与下一步唯一推荐入口。
