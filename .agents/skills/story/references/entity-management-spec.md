# 实体管理规范

> 适用范围：角色 / 场景 / 物品 / 势力 / 关系 / 知识状态等可演化对象

## 核心结论

`story2026` 的实体管理不是“全都放进 index.db”。

最新系统固定为三层分工：

1. `Cards`
   - 对象真源
   - 保存 `core / current_state / history`
2. `story_map.actualization`
   - 计划执行态真源
   - 保存 episode、线索、伏笔、任务、promise 等规划节点实际推进到哪里
3. `index.db`
   - 检索与观测层
   - 保存实体索引、别名、出场、关系、状态变化、审查指标等 runtime-friendly 数据

## Truth Ownership

| 层 | 负责回答的问题 | 默认写入方 |
|---|---|---|
| `Cards.core` | 对象长期定义是什么 | `1-Cards` |
| `Cards.current_state` | 对象现在怎样了 | `1-Cards` / `5-Loopback` |
| `Cards.history` | 哪一集验证过哪些持续变化 | `5-Loopback` |
| `story_map.actualization` | 规划节点实际推进到哪了 | `5-Loopback` |
| `index.db` | 最近出场、别名、关系、趋势、查询加速 | Data Agent / CLI |

硬规则：

- `index.db` 不是 Cards 的替代品。
- `story_map.actualization` 不是对象卡的替代品。
- `planned_*` 不得被执行态静默覆盖。

## Runtime Storage

### `index.db` 负责的内容

- `entities`
- `aliases`
- `state_changes`
- `relationships`
- `chapters`
- `scenes`
- `review_metrics`
- `chapter_reading_power`

### `state.json` 负责的内容

- 当前进度
- 主角运行态快照
- strand tracker
- 告警 / pending 列表

## Write Ownership by Stage

| 阶段 | 允许写什么 | 不允许写什么 |
|---|---|---|
| `1-Cards` | 建立对象卡 `core/current_state/history` 骨架 | 写入 episode actualization |
| `3-Drafting` | 产出正文；允许 Data Agent 做 runtime 索引提取 | 未经验证直接改对象真源 |
| `4-Validation` | 只做隔离评估和聚合 | 直接写 Cards / MAP |
| `5-Loopback` | 把 `PASS` 结果写回 `Cards.current_state/history` 与 `story_map.actualization` | 覆盖 `Cards.core` 或 `planned_*` |

## 实体提取与消歧

当前主流程：

1. 正文写纯文本，不强制 XML 标签。
2. Data Agent 从正文提取实体、别名、关系、状态变化。
3. 置信度处理：
   - `> 0.8`：自动采用
   - `0.5 - 0.8`：采用并记录 warning
   - `< 0.5`：标记待人工确认

别名规则：

- alias 可一对多。
- 遇到歧义时，优先使用稳定 `id`，其次补 `type`。

## 查询接口

```bash
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-entity --id "xiaoyan"
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "萧炎"
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "xiaoyan"
python "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationships --entity "xiaoyan"
```

## 手动标注（可选）

- XML/标签体系只作为手工排障工具保留。
- 正式主流程默认依赖 Data Agent 自动提取，不再要求作者在正文里埋标签。

## 维护约束

- 若新增实体类或关系类，先判断它属于 `Cards`、`story_map.actualization` 还是 `index.db`。
- 若一个字段回答的是“对象现在怎样了”，优先落 `Cards.current_state/history`。
- 若一个字段回答的是“规划节点走到哪了”，优先落 `story_map.actualization`。
