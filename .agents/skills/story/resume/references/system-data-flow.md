---
name: system-data-flow-redirect
purpose: 重定向到权威版本
---

<context>
此文件已迁移到统一位置，避免多版本不同步问题。
</context>

<instructions>

## 权威版本位置

`../query/references/system-data-flow.md`

## 加载方式

```bash
cat "${SKILL_ROOT}/../query/references/system-data-flow.md"
```

## 快速参考

### 目录结构
```
项目根目录/
├── 正文/           # 正文章节文件
├── Drafting/           # drafting 阶段中间产物
├── Planning/legacy/           # 卷纲/章纲（legacy fallback）
├── Planning/8-全息地图.json  # 规划真源
├── Cards/         # 世界观/力量体系/角色卡
└── .webnovel/
    ├── state.json          # 权威状态
    ├── workflow_state.json # 当前 run 断点 + 兼容 history
    ├── execution_state.json # 全阶段执行状态（stage_progress / runs / resume marker）
    ├── task_log.jsonl      # 追加式任务日志
    ├── index.db            # SQLite 索引
    └── archive/            # 归档数据
```

### 当前结构核心变化
- **双 Agent 架构**: Context Agent (读) + Data Agent (写)
- **规划入口切换**: drafting/query/resume 默认先读 `Planning/8-全息地图.json`
- **无 XML 标签**: 纯正文写作，Data Agent AI 自动提取实体
- **SQLite 存储**: entities/aliases/state_changes 迁移到 index.db
- **state.json 精简**: 保持 < 5KB，主要包含 progress/protagonist_state/strand_tracker/disambiguation
- **执行状态三件套**: `workflow_state.json` 记当前断点，`execution_state.json` 记全阶段 run，`task_log.jsonl` 记追加式事件链

</instructions>
