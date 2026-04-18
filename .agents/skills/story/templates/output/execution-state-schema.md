# `STATE.json.workflow_runtime.execution_state` 结构说明

> 该对象用于承接 `story2026` 的全阶段执行状态，不替代 `STATE.json` 的其他运行态字段。
>
> 分工固定：
> - `STATE.json`：小说运行态与 workflow_runtime 根容器
> - `STATE.json.workflow_runtime.workflow_state`：当前 run 的断点与兼容 history
> - `STATE.json.workflow_runtime.execution_state`：全阶段 run registry / stage_progress / resume marker
> - `STATE.json.workflow_runtime.task_log`：追加式任务日志

```json
{
  "schema_version": "1.0",
  "updated_at": "",
  "active_run_id": null,
  "run_sequence": 0,
  "latest_resume_point": null,
  "stage_progress": {
    "0-init": {
      "stage_label": "初始化",
      "status": "idle",
      "latest_run_id": null,
      "latest_command": null,
      "current_step": null,
      "resume_ready": false,
      "last_started_at": null,
      "last_completed_at": null,
      "last_failed_at": null,
      "last_cleared_at": null
    },
    "3-drafting": {
      "stage_label": "起草层",
      "status": "idle",
      "latest_run_id": null,
      "latest_command": null,
      "current_step": null,
      "resume_ready": false,
      "last_started_at": null,
      "last_completed_at": null,
      "last_failed_at": null,
      "last_cleared_at": null
    }
  },
  "runs": [],
  "artifacts_index": {}
}
```

## 关键字段

- `active_run_id`
  - 当前活动 run；没有活动任务时为 `null`。
- `latest_resume_point`
  - 最近一次可恢复入口，供 `resume` 和诊断工具读取。
- `stage_progress`
  - 每个 stage 的最新状态摘要，适合 UI / CLI 快速展示。
- `runs`
  - 近期 run 注册表，记录命令、状态、步骤、重试次数和产物摘要。
- `artifacts_index`
  - run 级与 step 级 artifacts 的轻量索引，不替代实际产物文件。
