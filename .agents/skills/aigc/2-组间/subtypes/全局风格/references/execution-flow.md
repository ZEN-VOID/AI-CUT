# 全局风格执行流程细则

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].组间设计.全局风格`
- thinking sidecar：`projects/<项目名>/编导/thinking/全局风格.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本叶子只对父级本轮 `selected_subskills[]` 命中的目标组返回 patch；未调度则与总 `json` 无关

## Mandatory Workflow

1. 读取 `projects/<项目名>/0-Init/`、`projects/<项目名>/Init/` 与 `1-规划` 结果，同时完整读取已落盘的 `projects/<项目名>/编导/第N集.json`。
2. 若当前 episode 根文件缺失，先回退 `1-规划/subtypes/1-分集` 完成 bootstrap，不在本叶子私造第二份主稿。
3. 先确认父级 `2-组间` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止，不写占位、不补空字段。
4. 解构叙事与世界约束，锁定观演距离、媒介属性、渲染技术栈、美学范式、节奏锚定与项目级导演协议。
5. 将稳定结论压成目标组的 `全局风格` field patch；项目级完整推导、比较与思维链只进入 `thinking sidecar`。
6. patch 只允许覆盖本叶子负责字段，不得另写 `style-bible.md`、第二份 episode 文件或平行汇总稿。
7. 父级聚合器负责把本叶子 patch 合并回统一根文件，并在阶段验收里只记录本轮实际调度到的叶子。

## Council Runtime Inheritance

`全局风格` 不单独定义顾问团运行时，而是强制继承上层 `2-组间` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对整体风格一致性、资源感与执行可达性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `2-组间` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。
