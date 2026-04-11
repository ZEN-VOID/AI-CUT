# 3-视频生成路由策略细则

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VIDSUB-01 | 输入 | 是否已有稳定请求 JSON | `ready/missing` | 检查上游产物存在与完整度 | P0 |
| V-VIDSUB-02 | 路由 | 是否已明确 provider | `explicit/recommend_only` | 读取用户要求与现有计划 | P1 |
| V-VIDSUB-03 | 执行面 | provider 是否已有外部 skill | `skill_available/manual_only` | 结合仓内技能与任务要求 | P1 |

## Case To Strategy Map

| case_id | 触发谓词 | 主策略 | 通过标准 | fallback |
| --- | --- | --- | --- | --- |
| C-VIDSUB-01 | `V-VIDSUB-01=missing` | 停止并回上游补请求对象 | 不伪造提交计划 | 回 `1-提示词蒸馏/*` |
| C-VIDSUB-02 | `V-VIDSUB-01=ready and V-VIDSUB-02=explicit` | 直写对应 provider 的 handoff 包 | `submit-plan.json` 可直接交接 | 无 |
| C-VIDSUB-03 | `V-VIDSUB-01=ready and V-VIDSUB-02=recommend_only` | 写推荐主案 + 备选理由 | 下一入口清楚 | 等用户裁决 |
| C-VIDSUB-04 | `V-VIDSUB-03=manual_only` | 保留完整 handoff 包，不伪造本地执行 skill | 人工可直接接手 | 暂停 |
