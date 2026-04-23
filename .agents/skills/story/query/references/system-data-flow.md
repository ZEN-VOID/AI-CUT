---
name: system-data-flow
purpose: 项目查询、恢复和运行时状态判断时加载，理解 story2026 最新真源分层与数据结构
---

<context>
此文件用于项目数据结构参考。Claude 已知一般文件组织，这里只补充网文工作流特定的目录约定和脚本职责。
</context>

<instructions>

## 目录约定

```
项目根目录/
├── 2-Planning/legacy/       # 卷纲/章纲/场景纲（legacy fallback）
├── 2-Planning/
│   ├── 整体规划.md         # 当前 primary planning truth（宏观）
│   ├── 第1卷/
│   │   ├── 卷规划.md       # 当前 primary planning truth（中观）
│   │   └── 第1章.md        # 当前 primary planning truth（微观）
│   ├── 全息地图.json      # 兼容投影 / 历史工件
│   └── 卷分片/            # 兼容投影 / actualization carrier
│       └── 第1卷.json
├── 0-Init/
│   ├── north_star.yaml           # 初始化长期合同（含 story_kernel / reader_promise / cards）
│   ├── story-source-manifest.yaml # 故事主源登记与 readiness
│   └── init_handoff.yaml         # cards/planning 入口种子与 unknowns
├── MEMORY.md             # 项目级创作记忆：偏好/口味/禁区/特殊元素/长期要求
├── 1-Cards/                # 角色卡/场景卡/物品卡（单卡真源：core/current_state/history）
├── 3-Drafting/           # drafting 阶段正文真源（第N卷/第N章.md + 第V卷.写作日志.yaml）
├── 5-Loopback/
│   └── 第V卷.loopback.json   # PASS 后 validated actualization artifact
├── STATE.json             # 项目入口与内联执行态唯一状态文件
└── .webnovel/
    ├── index.db            # SQLite 主存储：实体/别名/关系/状态变化/章节/场景
    ├── vectors.db          # RAG 向量数据库
    ├── summaries/          # 章节摘要（chNNNN.md）
    └── archive/            # 归档数据（不活跃角色/已回收伏笔）
```

说明：
- `3-Drafting/` 是当前唯一正文真源目录。
- `3-Drafting` 根技能本身就是章节正文主技能；旧的 `正文/` child 已退出现行结构。

## 架构变更说明

**核心变化**: 解决 `STATE.json` 膨胀问题（20章后 token 爆炸）

| 数据类型 | 旧版存储位置 | 当前存储位置 |
|----------|--------------|--------------|
| entities_v3 | `STATE.json` | **index.db** (entities 表) |
| alias_index | `STATE.json` | **index.db** (aliases 表) |
| state_changes | `STATE.json` | **index.db** (state_changes 表) |
| structured_relationships | `STATE.json` | **index.db** (relationships 表) |
| progress | STATE.json | STATE.json (保留) |
| protagonist_state | STATE.json | STATE.json (保留) |
| strand_tracker | STATE.json | STATE.json (保留) |
| disambiguation_* | STATE.json | STATE.json (保留) |
| current run / completed step order | 无统一真源 | **STATE.json.workflow_runtime.workflow_state** |
| stage progress / runs / resume marker | 无统一真源 | **STATE.json.workflow_runtime.execution_state** |
| append-only task events | 无统一真源 | **STATE.json.workflow_runtime.task_log** |

## 双 Agent 架构

```
写作前: Context Agent 读取数据 → 组装上下文包
        ├── 先读 部级/卷级/章级规划，兼容项目再回退到 全息地图
        ├── 从 STATE.json 读取精简数据（进度/配置）
        └── 从 index.db SQL 按需查询（实体/关系）

写作中: Writer 使用上下文包生成纯正文（无 XML 标签）

写作后: Data Agent 处理正文 → AI 提取实体 → 写入数据链
        ├── 写入 index.db（实体/别名/状态变化/关系）
        ├── 更新 STATE.json（进度/主角快照 + chapter_meta）
        └── 写入 summaries/chNNNN.md（章节摘要）

Context Agent (读) ←→ index.db + STATE.json ←→ Data Agent (写)
```

## 阶段总线（最新 0-5 系统）

```text
0-Init
  → 收集项目承诺与禁飞区
  → 生成 `0-Init/north_star.yaml + story-source-manifest.yaml + init_handoff.yaml`
  → 其中 `north_star.yaml.cards` 承担长期对象总规范

1-Cards
  → 基于 `north_star.yaml.cards` 建立角色/场景/物品真源：core / current_state / history

2-Planning
  → `1-部级 -> 2-卷级 -> 3-章级` 分形递进
  → primary truth 落到 `整体规划.md + 第N卷/卷规划.md + 第N卷/第N章.md`
  → `全息地图.json / 卷分片/*.json` 仅保留兼容投影价值

3-Drafting
  → 以 `3-Drafting/第N卷/第N章.md` 作为当前章唯一正文根文件
  → 根技能直接读取三层 planning + 全局卡 + 风格卡 + north_star + 项目 CONTEXT
  → 实际正文创作固定走 `scripts/write_chapter_via_doubao.py -> doubao-seed-2.0-pro`
  → 若前序章已完成，可额外加载其正文做增强校准
  → 并把章节数据写回 state/index
  → 同步推进 `STATE.json.workflow_runtime`

4-Review
  → 新后台隔离团队做客观检验，决定是否 PASS

review
  → 汇总聚合评估，落库 review_metrics / checkpoints

5-Loopback
  → 仅对 PASS volume 写 validated actualization
  → 更新 Cards.current_state/history
  → 更新 planning actualization sidecars
  → 更新 MAP.actualization compat projection
  → 刷新 writer/planning/query projection

query / resume
  → 作为 5-Loopback 的卫星技能消费上述 truth layers 与 execution truth
```

## 脚本/模块职责速查

### 核心脚本

| 脚本 | 输入 | 输出 |
|------|------|------|
| `init_project.py` | 项目信息 | 生成初始化主工件 + `MEMORY.md` + `STATE.json.workflow_runtime` + 初始化 `index.db` |
| `update_state.py` | 参数 | 原子更新 `STATE.json` 字段（进度/主角/strand_tracker） |
| `status_reporter.py` | 无 | 生成健康报告/伏笔紧急度 |
| `workflow_manager.py` | stage 命令 + chapter | 维护 `STATE.json.workflow_runtime`、恢复检测与 cleanup 备份 |
| `data_modules/migrate_state_to_sqlite.py` | 项目路径 | 迁移旧 `STATE.json` 到 SQLite |

### data_modules 模块

| 模块 | 职责 |
|------|------|
| `state_manager.py` | 实体状态管理（精简 `STATE.json` + SQLite 同步） |
| `sql_state_manager.py` | SQLite 状态管理（替代 JSON 写入） |
| `index_manager.py` | SQLite 索引管理（实体/别名/关系/状态变化/章节/场景） |
| `entity_linker.py` | 别名注册与消歧 |
| `rag_adapter.py` | 向量嵌入与语义检索 |
| `style_sampler.py` | 风格样本提取与管理 |
| `api_client.py` | LLM API 调用封装 |
| `config.py` | 配置管理 |

## 每章数据链

```
1. Context Agent 组装创作任务书
   → 先读取 `2-Planning/整体规划.md + 第V卷/卷规划.md + 第V卷/第N章.md`（规划真源）
   → 读取 `STATE.json`（精简版：进度/配置）
   → SQL 查询 index.db（核心实体/按需实体）
   → RAG 检索（相关场景）

2. `3-Drafting` chapter-native 豆包正文创作
   → 锁当前章 planning / global-style / north-star / project CONTEXT / previous chapter
   → 生成完整章节 Markdown 文件
   → 写回 `3-Drafting/第N卷/第N章.md`
   → 兼容 runtime 若启用，可额外同步写入 `第V卷.写作日志.yaml`

3. inline validation hooks
   → 每个 drafting step 写回后，立即运行 registry 声明的即时审计
   → 通过后才允许继续下一个工序

4. 隔离终验
   → `4-Review` 组装 `validation_fact_pack`
   → 并发 6 个维度子技能
   → 聚合为 `4-Review/第V卷.validation.json`

5. review / 审查落盘
   → `review/` 生成业务报告
   → 落库 `review_metrics`
   → 回写 `STATE.json.review_checkpoints`

6. Data Agent / runtime 数据链
   → AI 实体提取（替代 XML 标签解析）
   → 实体消歧（置信度策略）
   → 写入 index.db（实体/别名/状态变化/关系）
   → 更新 `STATE.json`（进度/主角快照 + chapter_meta）
   → 写入 summaries/chNNNN.md（章节摘要）
   → 向量嵌入 (RAG)
   → 风格样本评估

7. 通过 `5-Loopback` 做 PASS-only actualization
   → 写 `Cards.current_state/history`
   → 写 `整体规划.actualization.json / 卷规划.actualization.json / 第N章.actualization.json`
   → 兼容项目再写 `content.holomap_slice.actualization`
   → 并回刷 `content.holomap.actualization` summary/index
   → 写 `5-Loopback/第V卷.loopback.json`
   → 刷新 query / writer / planning projection

8. 如需清理中断工件，由 `workflow_manager.py cleanup` 生成恢复备份后再执行安全清理
```

> `update_state.py` 用于手动/脚本化更新 `progress`/`protagonist_state`/`strand_tracker` 等字段；主流程通常由 Data Agent 在处理数据链时同步推进进度。

## 规划真源优先级

1. `2-Planning/整体规划.md`
2. `2-Planning/第V卷/卷规划.md`
3. `2-Planning/第V卷/第N章.md`
4. `1-Cards/**/*.json`
5. `STATE.json`
6. `2-Planning/legacy/`（仅 legacy fallback）

说明：
- 涉及章节编排、任务、线索、伏笔、冲突落点的问题，默认先查三层规划文档。
- `2-Planning/legacy/` 仍可作为兼容旧项目的回退来源，但不再是下游默认入口。

## Query Truth Layers（查询时必须区分）

| truth_layer | 回答什么问题 | 主来源 | 注意事项 |
|---|---|---|---|
| planning truth | 原计划如何编排、哪章承载什么 | `2-Planning/整体规划.md` + `2-Planning/第V卷/卷规划.md` + `2-Planning/第V卷/第N章.md` | compat 项目才回退到 `全息地图 + 卷分片` |
| drafting truth | 当前章正文写成什么样、当前章采用了哪些写作约束 | `3-Drafting/第N卷/第N章.md` | 不再回退到旧 `chapter-root.md` |
| object truth | 对象长期定义、当前默认状态、历史变化 | `1-Cards/**/*.json` | 优先区分 `core / current_state / history` |
| runtime snapshot | 当前进度、主角快照、strand tracker、review checkpoints | `STATE.json` | 是快照，不是完整证据库 |
| execution truth | 当前 run、stage 进度、resume marker、事件链 | `STATE.json.workflow_runtime.execution_state + task_log` | `workflow_state` 只是兼容断点，不是全阶段真源 |
| indexed evidence | 实体别名、状态变化、关系、章节出场、评分趋势 | `.webnovel/index.db` | 适合做精确检索与证据补充 |
| validated actualization | 哪些 planned nodes 已在 PASS 后被正式兑现 | `2-Planning/整体规划.actualization.json` + `2-Planning/第V卷/卷规划.actualization.json` + `2-Planning/第V卷/第N章.actualization.json` + `5-Loopback/*.loopback.json`；compat 项目再补 `holomap actualization` | 没有 PASS 证据时不能冒充 actual |
| quality truth | 最近质量趋势、风险字段、阅读力 | `index.db.review_metrics` + `reading_power` | 由 `4-Review + review` 生成 |

固定判定：

- 问“原计划” -> planning truth
- 问“现在怎样” -> object truth / runtime snapshot
- 问“已经发生了吗” -> validated actualization
- 问“当前跑到哪 / 最近哪个 run 卡住” -> execution truth
- 问“证据是什么” -> indexed evidence

## `STATE.json` 精简结构

```json
{
  "project_info": {"title": "", "genre": ""},
  "progress": {"current_chapter": N, "total_words": W, "current_volume": 1},
  "protagonist_state": {
    "name": "",
    "power": {"realm": "", "layer": 1, "bottleneck": ""},
    "location": {"current": "", "last_chapter": 0},
    "golden_finger": {"name": "", "level": 1, "skills": []}
  },
  "strand_tracker": {
    "last_quest_chapter": 0,
    "last_fire_chapter": 0,
    "last_constellation_chapter": 0,
    "current_dominant": "quest",
    "chapters_since_switch": 0,
    "history": []
  },
  "relationships": {},
  "plot_threads": {"active_threads": [], "foreshadowing": []},
  "world_settings": {},
  "disambiguation_warnings": [],
  "disambiguation_pending": [],
  "review_checkpoints": [],
  "chapter_meta": {},
  "_migrated_to_sqlite": true
}
```

## workflow_runtime 内联结构

`STATE.json.workflow_runtime` 固定承载三块执行态：

- `workflow_state`
  - 当前 run 的兼容断点与 history
- `execution_state`
  - 全阶段 run registry / stage_progress / latest_resume_point / governance_index
- `task_log`
  - 追加式事件证据链

> **当前结构说明**: entities_v3、alias_index、state_changes、structured_relationships 已迁移到 index.db，不再存储在 `STATE.json` 中。

> **查询注意**: `STATE.json` 仍然保留 `review_checkpoints`、`chapter_meta`、`strand_tracker` 等快照字段，但它不是 `Cards`、`MAP.actualization` 或 `index.db` 的替代品。

## `STATE.json.workflow_runtime.execution_state` 结构（全阶段执行状态）

```json
{
  "schema_version": "1.0",
  "active_run_id": null,
  "run_sequence": 0,
  "latest_resume_point": null,
  "stage_progress": {
    "0-init": {"status": "idle", "latest_run_id": null, "current_step": null},
    "3-drafting": {"status": "idle", "latest_run_id": null, "current_step": null},
    "5-loopback": {"status": "idle", "latest_run_id": null, "current_step": null}
  },
  "runs": [],
  "artifacts_index": {}
}
```

- `STATE.json.workflow_runtime.workflow_state` 负责“当前 run 的断点与兼容 history”。
- `STATE.json.workflow_runtime.execution_state` 负责“全阶段 run 注册表、stage_progress、resume marker”。
- `STATE.json.workflow_runtime.task_log` 负责“追加式事件证据链”，适合追踪心跳、失败、清理与人工诊断。

## index.db 表结构

```sql
-- 实体表
CREATE TABLE entities (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,           -- 角色/地点/物品/势力/招式
    canonical_name TEXT NOT NULL,
    tier TEXT DEFAULT '装饰',     -- 核心/重要/次要/装饰
    desc TEXT,
    current_json TEXT,            -- JSON: {realm, location, ...}
    first_appearance INTEGER,
    last_appearance INTEGER,
    is_protagonist INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0
);

-- 别名表（一对多）
CREATE TABLE aliases (
    alias TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    PRIMARY KEY (alias, entity_id, entity_type)
);

-- 状态变化表
CREATE TABLE state_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL,
    field TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    reason TEXT,
    chapter INTEGER NOT NULL
);

-- 关系表
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity TEXT NOT NULL,
    to_entity TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    chapter INTEGER NOT NULL,
    UNIQUE(from_entity, to_entity, type)
);

-- 原有表（保留）
CREATE TABLE chapters (...);
CREATE TABLE scenes (...);
CREATE TABLE appearances (...);
```

## Data Agent AI 提取流程

当前主流程不再要求 XML 标签，由 Data Agent 智能提取：

1. **实体识别**: 从正文语义识别角色/地点/物品/势力
2. **实体匹配**: 优先匹配已有实体（通过 alias_index）
3. **消歧处理**:
   - 置信度 > 0.8: 自动采用
   - 置信度 0.5-0.8: 采用但记录 warning
   - 置信度 < 0.5: 标记待人工确认
4. **状态变化识别**: 境界突破/位置移动/关系变化
5. **写入存储**: 直接写入 index.db（实体/别名/关系/状态变化）

## 伏笔字段规范

| 字段 | 规范值 | 兼容值（历史） |
|------|--------|---------------|
| status | `未回收` / `已回收` | 待回收/进行中/active/pending |

**推荐字段**: content, status, planted_chapter, target_chapter, tier

## alias_index 格式（一对多）

```json
{
  "林天": [{"type": "角色", "id": "lintian"}],
  "天云宗": [
    {"type": "地点", "id": "loc_tianyunzong"},
    {"type": "势力", "id": "faction_tianyunzong"}
  ]
}
```

同一别名可映射到多个实体，消歧时根据 type 或上下文判断。

</instructions>

<examples>

<example>
<input>查询当前进度</input>
<output>
```bash
cat "$PROJECT_ROOT/STATE.json" | jq '.progress'
# 输出: { "current_chapter": 45, "total_words": 135000 }
```
</output>
</example>

<example>
<input>查询实体（SQL）</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-entity --id "xiaoyan"
# 输出: {"id": "xiaoyan", "type": "角色", "canonical_name": "萧炎", ...}

python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-core-entities
# 输出: 所有核心实体（主角 + tier=核心/重要）
```
</output>
</example>

<example>
<input>按别名查找实体（一对多）</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "天云宗"
# 输出: [{"id": "loc_tianyunzong", "type": "地点"}, {"id": "faction_tianyunzong", "type": "势力"}]
```
</output>
</example>

<example>
<input>查询状态变化</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "xiaoyan" --limit 10
# 输出: [{entity_id, field, old_value, new_value, reason, chapter}, ...]
```
</output>
</example>

<example>
<input>查询关系</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationships --entity "xiaoyan"
# 输出: [{from_entity, to_entity, type, description, chapter}, ...]
```
</output>
</example>

<example>
<input>检查伏笔紧急度</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus urgency
```
</output>
</example>

<example>
<input>查询实体出场记录</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index entity-appearances --entity "lintian"
```
</output>
</example>

<example>
<input>迁移旧 `STATE.json` 到 SQLite</input>
<output>
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" migrate -- --backup
# 自动备份 `STATE.json`，迁移数据到 index.db，精简 `STATE.json`
```
</output>
</example>

</examples>

<errors>
❌ 伏笔状态写成"待回收" → ✅ 使用规范值"未回收"
❌ 手工更新忘记加 planted_chapter → ✅ 脚本已自动补全
❌ 归档路径混淆 → ✅ 固定为 `.webnovel/archive/*.json`
❌ alias_index 期望单对象 → ✅ 当前结构使用数组格式（一对多）
❌ 期望 XML 标签提取 → ✅ 当前主流程由 Data Agent AI 自动提取
❌ 使用旧版 data_modules.state_manager schema → ✅ 统一使用 entities_v3 结构
❌ 仍从 `STATE.json` 读取 entities_v3 → ✅ 改用 SQL 查询 index.db
❌ 仍写入 `STATE.json` 大数据 → ✅ 改用 SQLite 增量写入
❌ 让 `STATE.json` 持续膨胀 → ✅ 运行迁移脚本: `python "${SCRIPTS_DIR}/story.py" migrate`
</errors>
