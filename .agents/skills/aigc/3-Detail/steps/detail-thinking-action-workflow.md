# 3-Detail Thinking-Action Workflow

本文件是 `3-Detail` 的 Skill 2.0 `steps/` 真源，承载节点、分支、汇流和返工门。根 `SKILL.md` 只保留入口摘要；执行细节以本文件为准。

## Business Requirement Analysis

| slot | locked answer |
| --- | --- |
| `business_goal` | 将 `2-Global/episode_root.json` 细化为可被下游消费的镜级 detail root。 |
| `business_object` | `projects/aigc/<项目名>/3-Detail/第N集.json` 与 `validation-report.md`。 |
| `constraint_profile` | 上游只有组级 seed，本阶段必须自行锁镜数、镜级正文、主体锚定与所有镜级字段。 |
| `success_criteria` | JSON 与报告均可通过 validator，且字段可见、可拍、可连续、可被下游抽取。 |
| `non_goals` | 不重写 `2-Global`，不恢复旧子技能主链，不另建思考 sidecar。 |
| `complexity_source` | 镜头切分、字段边界、知识转译、局部 patch 与阶段 closure。 |
| `topology_fit` | 串行主干 + 条件返工 + 单点汇流。 |

## Node Spine

`N0 -> N1 -> N2 -> N3 -> N4 -> N5 -> N6 -> N7 -> N8`

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N0` | 锁定任务与唯一输出 | 用户请求、父级路由、本技能 Output Contract | 判定当前是否属于 `3-Detail`；锁 `第N集.json + validation-report.md`；确认 LLM-first 主创 | `output_mode=detail_root+stage_report` | 成功进 `N1`，失败回父级路由 | 未锁唯一输出前不得读写运行时文件 |
| `N1` | 锁输入范围与知识域 | `2-Global/episode_root.json`、既有 `第N集.json`、`types/type-map.md` | 锁 episode/group/shot/field scope；判断 patch 类型；选择知识域与 bundle | `type_profile`、`knowledge_mode`、`selected_bundles` | 成功进 `N2`，失败回 `N0` | scope 与 knowledge mode 未明确不得写字段 |
| `N2` | `P1-分镜构图` | `groups[].global`、`references/模板字段填写指南.md`、分镜/导演知识包 | 决定 `分镜数`；拆每镜 `时间 / 剧本正文 / 主体锚定 / 分镜构图`；校准方向、视线与空间 | `detail.分镜数`、`分镜列表`、`translation_targets` | 成功进 `N3`，失败回 `N1` 或 `N2` | 镜数、时间、正文切分点或主体锚定不稳时禁止后序字段启动 |
| `N3` | `P2-角色表现` | `N2` 骨架、`references/编剧手册.md`、导演知识包 | 写 `动作戏 / 对话戏 / 内心戏`；明确人物目的、障碍、反应点 | `角色表现`、`applied_passes=P2` | 成功进 `N4`，失败回 `N2` 或 `N3` | 不得把角色表现写成机位、光影或构图 |
| `N4` | `P3-氛围表现` | `N2-N3`、`references/编剧手册.md`、摄影知识包 | 写 `层次 / 空间诗学 / 意境`；让气息来自空间、天气、材质与声光条件 | `氛围表现`、`applied_passes=P3` | 成功进 `N5`，失败回 `N2` 或 `N4` | 不得只写抽象 mood 词 |
| `N5` | `P4-摄影表现` | `N2-N4`、`references/镜头语言.md`、电影摄影知识包 | 写 `光影 / 色彩 / 质感`；让摄影服务当前戏剧骨架 | `摄影表现`、`applied_passes=P4` | 成功进 `N6`，失败回 `N2` 或 `N5` | 不得堆器材、焦段、曝光参数替代视觉判断 |
| `N6` | `P5/P6-运镜与转场` | `N2-N5`、`references/镜头语言.md`、分镜调度知识包 | 写 `运镜手法` 与 `转场特效`；只补最小必要衔接收益 | `运镜手法`、`转场特效`、`applied_passes=P5,P6` | 成功进 `N7`，失败回 `N2`、`N5` 或 `N6` | 反向改镜数、正文切分点或主体锚定即失败 |
| `N7` | `P7-验收` | `第N集.json`、`review/review-contract.md`、validator | 跑 stage validator；写 `Layered Trace`、校验结果、学院派知识证据；判定 `pass/rework/stop` | validator 结果、report 路径、fail code | `pass` 进 `N8`，`rework` 回指定节点，`stop` 记录阻塞 | 无 validator 结果或无 report 不得 closure |
| `N8` | One-Shot Closure | `N7` report 与 verdict | 写 `思考过程 / 关键证据 / 风险/例外 / 下一入口`；确认无第二真源 | `Thinking-Action Closure` 或 `Closure Triad` | 成功完成，失败回 `N7` | closure 四段不全不得宣告完成 |

## Branch And Rework Rules

- `episode_scope`：从 `N1` 进入，允许全量重建整集。
- `group_scope`：从 `N2` 进入，只 patch 命中组。
- `shot_scope`：若触及骨架从 `N2` 进入；若只触及后序字段，从字段节点进入。
- `field_scope=角色表现`：从 `N3` 进入。
- `field_scope=氛围表现`：从 `N4` 进入。
- `field_scope=摄影表现`：从 `N5` 进入。
- `field_scope=运镜手法/转场特效`：从 `N6` 进入。
- `closure_scope`：只从 `N7/N8` 进入，不得改业务 JSON。

## Convergence Gate

`3-Detail` 的唯一汇流点是 `N7 -> N8`。汇流时必须同时满足：

1. `第N集.json` 是唯一 canonical root。
2. `validation-report.md` 记录结构验收、知识证据和返工入口。
3. closure 四段写入同一份 stage report。
4. 任一返工都能定位到具体节点。

## Failure Routing

| symptom | direct cause | rework entry |
| --- | --- | --- |
| 镜数与分镜列表不一致 | 骨架未锁稳 | `N2` |
| 每镜正文缺失或整组复制 | 正文切分未完成 | `N2` |
| 角色表现写成机位 | 字段边界串位 | `N3` |
| 氛围只剩形容词 | 空间承载缺失 | `N4` |
| 摄影表现堆器材参数 | 知识转译失败 | `N5` |
| 运镜或转场改了骨架 | 后序节点越权 | `N2` 或 `N6` |
| 报告无知识证据 | 验收槽位缺失 | `N7` |
| 报告无 closure 四段 | 结案闭环缺失 | `N8` |
