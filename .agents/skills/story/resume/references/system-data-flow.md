---
name: system-data-flow-redirect
purpose: 重定向到权威版本
---

<context>
此文件已迁移到统一位置，避免多版本不同步问题。
</context>

<instructions>

## 权威版本位置

`../../query/references/system-data-flow.md`

## 加载方式

```bash
cat "${SKILL_ROOT}/../../query/references/system-data-flow.md"
```

## 快速参考

### 目录结构
```
项目根目录/
├── 3-Drafting/         # drafting 阶段正文真源（第N集.md + 写作日志.yaml）
├── 2-Planning/legacy/           # 卷纲/章纲（legacy fallback）
├── 2-Planning/全息地图.json  # 规划真源
├── 0-Init/        # north_star.yaml / story-source-manifest.yaml / init_handoff.yaml
├── 1-Cards/         # 世界观/力量体系/角色卡
└── .webnovel/
    ├── index.db            # SQLite 索引
    └── archive/            # 归档数据
```

补充：
- `3-Drafting/` 是当前恢复链路的唯一正文根目录。
- `正文/` 仅在旧项目兼容检测或 fallback 搜索时出现，不再作为默认目录树的一部分。

### 当前结构核心变化
- **七道工序 drafting**: `1-起盘 -> 2-节奏 -> 3-场景氛围 -> 4-角色刻画 -> 5-对白声口 -> 6-追读力强化 -> 7-润色`
- **规划入口切换**: drafting/query/resume 默认先读 `2-Planning/全息地图.json`
- **无 XML 标签**: 纯正文写作，Data Agent AI 自动提取实体
- **SQLite 存储**: entities/aliases/state_changes 迁移到 index.db
- **STATE.json 精简**: 保持 < 5KB，主要包含 progress/protagonist_state/strand_tracker/disambiguation
- **执行状态三件套**: `STATE.json.workflow_runtime.workflow_state` 记当前断点，`STATE.json.workflow_runtime.execution_state` 记全阶段 run，`STATE.json.workflow_runtime.task_log` 记追加式事件链

</instructions>
