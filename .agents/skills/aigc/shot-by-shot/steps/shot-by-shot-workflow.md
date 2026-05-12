# Shot-by-Shot Workflow

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定素材、项目和目标阶段 | 用户请求、视频/截图/时间码、项目上下文 | 判定素材类型、证据等级、目标对接包 | `source_profile` | `N2-SHOT-MAP` | 素材可观察或已标注补证需求 |
| `N2-SHOT-MAP` | 建立逐镜边界 | `source_profile` | 编号镜头、记录时间码、入口/出口和可见事件 | `shot_boundary_map` | `N3-OBSERVE` | 不用剧情段落冒充镜头 |
| `N3-OBSERVE` | 并行拆解 craft 维度 | `shot_boundary_map`、分析方法 | 拆导演、表演、摄影、剪辑、声音、美术、AIGC 可行性 | `craft_observation_matrix` | `N4-PRINCIPLE` | 每条结论有证据锚点 |
| `N4-PRINCIPLE` | 抽象临摹原则 | `craft_observation_matrix`、权利边界 | 区分可迁移原则和禁止复制表达 | `imitation_principle_map`、`forbidden_copy_ledger` | `N5-BRIDGE` | 原片具体表达不得进入建议 |
| `N5-BRIDGE` | 投影阶段对接解析 | `imitation_principle_map`、全局风格/2/3/5/分镜脚本合同 | 生成 `全局风格解析.md`、`编剧风格解析.md`、`摄影风格解析.md`、`设计风格解析.md`、`分镜脚本.md` | `stage_bridge_analysis_docs`、`storyboard_script_table` | `N6-REVIEW` | 字段不越权，可被 owning stage 和分镜生产消费 |
| `N6-REVIEW` | 验收与直接修复 | 全部候选输出 | 执行证据、边界、阶段、AIGC 可行性 review | `review_verdict` | `N7-WRITE` 或责任节点 | 阻断项已修复或明确阻断 |
| `N7-WRITE` | 写回唯一拉片包 | 通过 review 的候选包 | 写主报告、`分镜脚本.md`、项目 `CONTEXT/` 四份解析和执行报告 | output paths | done | 路径稳定，报告含 `思考过程` |

## Workflow Notes

- `N3-OBSERVE` 可以并行分析多个维度，但必须在 `N4-PRINCIPLE` 汇流为唯一临摹原则口径。
- `N5-BRIDGE` 是阶段适配门，不是内容改写门；正式主创仍由全局风格 owning stage、`2-编导`、`3-摄影` 或 `5-设计` 执行；`分镜脚本.md` 只承接表格式输出，不改变上游主真源。
- `N6-REVIEW` 发现“照搬风险”时，回到 `N4-PRINCIPLE`；发现“阶段字段越权”时，回到 `N5-BRIDGE`。
