# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 8006
current_lines: 170
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-08T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 2-Planning 当成 8 个独立子技能包 | source contract | 回到 `2-Planning/SKILL.md` 明确单技能治理与 references 边界 | 在 workflow/docs/helper 中统一使用单技能入口与 module 名称 | 不再出现独立 skill id 调度 8 个 step |
| planning 文件写进旧目录路径而不是并列文件 | path contract | 改写到 `Planning/*.json` canonical 路径 | 用 `planning_paths.py` 统一 canonical + legacy fallback | 新写入路径全部落在 `Planning/1-*.json` 至 `Planning/8-*.json` |
| 多个 planning 文件同时漂移，只修 holomap | rollback discipline | 回滚到最早失稳模块重新起链 | 固化“最早失稳模块优先”而非“最显眼失败模块优先” | 下游不再重复出现同类漂移 |
| holomap 变成摘要页，失去导航与编组能力 | holomap contract | 先修 `chapter_boards / cross_thread_indexes / three-axis` | 在 `references/holomap/module-spec.md` 固定六问底盘与三轴合同 | 任一章都能看出事件、冲突、任务、线索、伏笔与代价 |
| module 细则留在经验档案里，无法被主技能稳定调用 | reference routing | 把模块要点提炼进 `references/*/module-spec.md`，局部故障沉淀到同目录 `CONTEXT.md` | 主技能先判 step，再加载 `module-spec.md`，局部异常再读模块 `CONTEXT.md`，最后读模板 | 任一 step 都能解释该读哪个模块合同与局部经验 |
| `genre-selection` 仍试图依赖 stage 私有套路库，而不是共享题材根目录 | genre asset routing | 在 `references/genre-selection/module-spec.md` 中显式读取 `templates/genres/README.md` 与对应题材模板 | 固化“题材知识归 shared templates，planning references 只保留 step 合同”的分层 | Step 1 可以解释自己为什么读共享题材模板，而不是要求复制 trope 文档 |
| 章节体量与角色/线索/伏笔密度不匹配 | chapter density contract | 回修 `2-章节规划` 的 density contract | 把密度规则固定在 Step 2，后序只读取不重发明 | holomap 能回指密度目标已被承接 |
| query/write/resume 继续默认找旧 holomap 路径 | downstream data-flow | 改为优先读取 `Planning/8-全息地图.json` | 在脚本 helper 中集中处理 canonical + legacy fallback | 下游报告中明确显示 canonical planning source |
| 初始化已生成 `TEAM.toml`，但 `2-Planning` 执行时不读取 `策划` 布阵 | stage team governance | 在 `2-Planning/SKILL.md` 把 `TEAM.toml` 升级为必读输入，并要求有策划 AGENTS 时必须伴随后台多 subagents 会诊 | 将“策划团队参与 planning 决策并落盘”写成根技能硬规则，而不是初始化提示语 | 执行 `2-Planning` 时能明确区分“无策划组单跑”与“有策划组并行会诊后落盘” |

### 类型化处理偏好

| symptom_shape | preferred_owner | why |
| --- | --- | --- |
| 题材、冲突、任务、线索同时跑偏 | `1-题材选型` 或 `3-故事大纲` | 这是上游方向盘漂移，不是四个模块同时失手 |
| holomap 只有摘要没有编组 | `8-全息地图` + `2-章节规划` | 一个管节点组织，一个管章节容器 |
| drafting 找不到稳定章节挂点 | `2-章节规划` | 章节容器不稳时，下游一定发虚 |
| 只剩“知道答案”，没有发现过程 | `6-线索设计` | 证据链断了 |
| 回收无力、回照无力 | `7-伏笔设计` | 这是长期记忆系统问题 |

## Repair Playbook

1. 先问这是主技能路由问题、module 细则问题，还是具体 planning 文件问题。
2. 若多个后续文件一起失真，先锁定最早失稳模块，再从那里重新起链。
3. 若只是路径失配，优先修 helper 和 canonical path 合同，不先改内容。
4. 若 holomap 发虚，先检查 `chapter_boards / cross_thread_indexes / lifecycle_lexicon`。
5. 若 module 失真，先看 `references/*/module-spec.md` 是否还能解释当前 step；若是局部故障，再读同目录 `CONTEXT.md`，最后看模板字段是否对齐。
6. 收尾验证顺序固定为：
   - `Planning/1-题材选型.json`
   - `Planning/2-章节规划.json`
   - `Planning/3-故事大纲.json`
   - `Planning/4-7*.json`
   - `Planning/8-全息地图.json`
   - 下游 holomap-first 消费是否成立

### 诊断信号

- 如果你无法一句话说清“当前这步只裁决什么”，说明 module 边界还没锁稳。
- 如果后序文件比前序更像真源，说明单技能治理已经失效。
- 如果 holomap 不能回答“这一章为什么必须这样排”，说明至少有一个上游文件还没真的站住。
- 如果脚本只能读旧目录路径，说明 source-layer 重构还没闭环。

## Reusable Heuristics

### 编排治理启发式

- `2-Planning` 的杠杆点不在“多写一份文件”，而在“每份文件只裁决自己那层的真问题”。
- 1-7 份文件可以并列存在，但不能并列争真源；真源只能是第 8 份 holomap。
- 真正稳定的 holomap 不是“信息量最大”，而是“下游不需要重新临场拼 chapter board”。
- 与其问“哪份文件最难看”，不如先问“哪份文件最早开始不再承接上游”。

### 模块判断启发式

- 题材是方向盘，章节是容器，故事大纲是脊柱，冲突/任务/线索/伏笔是四条长线，holomap 是编组真源。
- 章节密度合同必须由 Step 2 统一裁决，否则后面一定一边写一边膨胀。
- 线索解决“当前如何发现”，伏笔解决“未来如何回照”，两者不要互相冒充。
- actualization 只能写进 holomap 的执行态容器，不能覆盖 planned state。
- 当 Step 1 需要题材工法时，优先去 `templates/genres/` 取共享知识，不要在 `2-Planning/references/` 里养第二份 trope 库。

### 路径迁移启发式

- 目录结构简化后，最容易漏的是下游脚本与测试，而不是主技能文档本身。
- 对 canonical path 做升级时，最好同时提供 legacy read fallback，这样迁移成本最低、回归面也最小。
- 把路径规则集中到单一 helper，比在 8 个脚本里分散硬编码更稳。
- 对阶段级大 skill 来说，frontmatter `description` 必须写成 `Use when...` 式触发条件；一旦改成流程摘要，模型更容易停在摘要层而不继续读正文合同。
