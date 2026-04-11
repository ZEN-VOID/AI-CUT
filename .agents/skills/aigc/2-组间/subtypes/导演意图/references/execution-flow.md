# 导演意图执行流程细则

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].组间设计.导演意图`
- thinking sidecar：`projects/<项目名>/编导/thinking/导演意图-第N集.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本叶子只对父级本轮 `selected_subskills[]` 命中的分镜组返回 patch；未调度则与总 `json` 无关

## Mandatory Workflow

1. 读取 `全局风格`、`类型元素`、`1-规划/3-分组` 与完整的 `projects/<项目名>/编导/第N集.json`。
2. 先确认父级 `2-组间` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止，不写占位、不补空字段。
3. 先锁定本集总导演命题与观看方式，再逐组裁决导演设计、部门翻译层、情绪推进与下游加载提示。
4. 将稳定结论压成命中分镜组的 `导演意图` field patch；完整三段式过程、组级比较与思维链只进入 `thinking sidecar`。
5. 本叶子不再创建 `导演意图/第N集.md`、第二份 episode 文件或平行总稿。
6. 父级聚合器负责把本叶子 patch 合并回统一根文件，并在阶段验收里只记录本轮实际调度到的叶子。

## Council Runtime Inheritance

`导演意图` 不单独定义顾问团运行时，而是强制继承上层 `2-组间` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对逐组表达目标、执行一致性与可拍性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `2-组间` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。
