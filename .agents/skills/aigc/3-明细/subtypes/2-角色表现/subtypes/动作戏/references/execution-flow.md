# aigc 3-明细 / 2-角色表现 / 动作戏 / Execution Flow

本文件承载 `动作戏` 叶子的统一写位、sidecar 与返回 patch 规则。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].角色表现`
- 执行报告：`projects/<项目名>/编导/evidence/2-角色表现/动作戏-第N集.md`
- 本叶子未被调度时不得写占位，不得参与聚合

## Council Runtime Inheritance (Mandatory)

`动作戏` 不单独定义顾问团运行时，而是强制继承 `3-明细` 根技能与 `2-角色表现` 父技能的顾问团合同。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对动作层执行逻辑、拍摄资源感与可落地性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。

## Mandatory Workflow

1. 完整读取 `projects/<项目名>/编导/第N集.json`，并锁定命中的分镜组与分镜明细。
2. 先确认父级 `2-角色表现` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 锁定动作段的 `目标 -> 阻力 -> 结果` 主链，把抽象动作拆成可见节拍链。
4. 为关键节拍补 `因果 -> 受力 -> 位置变化`，并让环境或道具参与动作。
5. 在爆点后补余波、喘息、受伤或短静默，避免动作只有起势没有回收。
6. 将稳定结果写入 evidence sidecar，并返回本镜级 `角色表现` patch 供父技能聚合。
