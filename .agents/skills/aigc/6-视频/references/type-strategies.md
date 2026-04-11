# 6-视频路由策略细则

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VIDEO-01 | 输入 | 是否已锁定 `编导/第N集.json` | `ready/missing` | 检查 canonical director root file | P0 |
| V-VIDEO-02 | 任务对象 | 当前是组级主体参照还是帧级参照 | `subject_group/frame/dual_frame/multi_image` | 结合用户目标与上游载体 | P1 |
| V-VIDEO-03 | 执行深度 | 当前停在请求整理还是已经进入提交 | `request_only/submit` | 结合用户指令与任务描述 | P1 |
| V-VIDEO-04 | 提交面 | 当前是否已拥有稳定请求 JSON | `request_ready/request_missing` | 检查 `6-视频` 子路径输出 | P1 |

## Case To Strategy Map

| case_id | 触发谓词 | 主策略 | 通过标准 | fallback |
| --- | --- | --- | --- | --- |
| C-VIDEO-01 | `V-VIDEO-01=missing` | 停止并报告上游缺口 | 不伪造请求 JSON | 回 `2-组间/3-明细` |
| C-VIDEO-02 | `V-VIDEO-02=subject_group` | 进入 `1-提示词蒸馏/全能参照` | 每个分镜组生成 1 条请求对象 | 无 |
| C-VIDEO-03 | `V-VIDEO-02=frame` | 进入 `1-提示词蒸馏/首帧参照` | 每个目标 `分镜ID` 生成 1 条请求对象 | 无 |
| C-VIDEO-04 | `V-VIDEO-02 in {dual_frame,multi_image}` | 报告目标子路径待补 | 不伪造未建合同 | 暂停 |
| C-VIDEO-05 | `V-VIDEO-03=submit and V-VIDEO-04=request_ready` | 进入 `3-视频生成` | 已有稳定请求对象与执行入口计划 | provider 运行时问题直接进对应 provider skill |
| C-VIDEO-06 | `V-VIDEO-03=submit and V-VIDEO-04=request_missing` | 停止并报告缺少可提交请求对象 | 不伪造 handoff 包 | 回命中的提示词蒸馏子路径 |
