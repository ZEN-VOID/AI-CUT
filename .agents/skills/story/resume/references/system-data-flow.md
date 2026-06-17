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
├── 3-初稿/           # drafting 阶段正文真源（第N卷/第N章.md + 第V卷.写作日志.yaml）
├── 2-卷章/legacy/           # 卷纲/章纲（legacy fallback）
├── 2-卷章/整体规划.md    # 规划真源（整书）
├── 2-卷章/第1卷/卷规划.md # 规划真源（当前卷）
├── 2-卷章/第1卷/第1章.md  # 规划真源（当前章）
├── 0-初始化/        # north_star.yaml / story-source-manifest.yaml / init_handoff.yaml
├── 1-设定/          # 世界观/力量体系/角色卡
└── .webnovel/
    ├── index.db            # SQLite 索引
    └── archive/            # 归档数据
```

补充：
- `3-初稿/` 是当前恢复链路的唯一正文根目录。
- `3-初稿` 根技能直接承担正文主创；`正文/` child 不再作为默认目录树的一部分。

### 当前结构核心变化
- **chapter-native drafting**: `3-初稿` 直接装配上下文并通过豆包生成章节正文
- **规划入口切换**: drafting/query/resume 默认先读 `整体规划.md + 当前卷/卷规划.md + 当前章.md`
- **无 XML 标签**: 纯正文写作，Data Agent AI 自动提取实体
- **SQLite 存储**: entities/aliases/state_changes 迁移到 index.db
- **STATE.json 精简**: 保持 < 5KB，主要包含 progress/protagonist_state/strand_tracker/disambiguation
- **执行状态三件套**: `STATE.json.workflow_runtime.workflow_state` 记当前断点，`STATE.json.workflow_runtime.execution_state` 记全阶段 run，`STATE.json.workflow_runtime.task_log` 记追加式事件链

</instructions>

## Review Gate Mapping

No independent gate. This file is a redirect and quick reference only; authoritative data-flow gates live in `../../query/references/system-data-flow.md` and `$story-resume` maps runtime boundary checks through `SKILL.md#Review Gate Binding`.
