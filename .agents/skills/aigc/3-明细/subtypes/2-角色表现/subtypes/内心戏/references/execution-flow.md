# aigc 3-明细 / 2-角色表现 / 内心戏 / Execution Flow

本文件承载 `内心戏` 叶子的统一写位、sidecar 与返回 patch 规则。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].角色表现`
- 执行报告：`projects/<项目名>/编导/evidence/2-角色表现/内心戏-第N集.md`
- 本叶子未被调度时不得写占位，不得参与聚合

## Council Runtime Inheritance (Mandatory)

`内心戏` 不单独定义顾问团运行时，而是强制继承 `3-明细` 根技能与 `2-角色表现` 父技能的顾问团合同。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对主观渗漏、可拍性与节奏控制提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。

## Mandatory Workflow

1. 完整读取 `projects/<项目名>/编导/第N集.json`，并锁定命中的分镜组与分镜明细。
2. 先确认父级 `2-角色表现` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 锁定当前内压来源、主观泄漏路径与可见锚点，禁止直接堆抽象情绪词。
4. 优先用目光、停顿、姿态、呼吸、手部或空间压迫完成潜台词外化。
5. 仅在本层允许的镜级字段内生成 `角色表现` patch，并把完整推导写入 evidence sidecar。
6. 父技能负责统一聚合与写回，不在本叶子私造第二份主稿。
