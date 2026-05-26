# Review Contract

## Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-01` | 是否有可观察证据、时间码、截图或明确描述 | `FAIL-SBS-EVIDENCE` | 回到 `N1-INTAKE` 补证 |
| `GATE-SBS-02` | 镜头边界是否能复查 | `FAIL-SBS-SHOT-MAP` | 回到 `N2-SHOT-MAP` |
| `GATE-SBS-03` | 分析是否覆盖任务相关 craft 维度 | `FAIL-SBS-OBSERVATION` | 回到 `N3-OBSERVE` |
| `GATE-SBS-04` | 临摹原则是否脱离具体表达 | `FAIL-SBS-IMITATION` | 回到 `N4-PRINCIPLE` |
| `GATE-SBS-05` | `全局风格解析.md` 是否完整包含叙事/类型承诺/视觉母题/年代质感/情绪曲线/路由/媒介/美学/节奏/审计/提示词候选，默认无污染且不直接改写 north star / style contract | `FAIL-SBS-STYLE-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-06` | `编剧风格解析.md` 是否完整包含潜台词层/情绪脉冲/声音叙事/副线编织，无摄影越权 | `FAIL-SBS-DIRECTING-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-07` | `摄影风格解析.md` 是否完整包含视点/焦深语义/光源叙事/运动/切点/长镜头结构，能转成 `分镜明细：` | `FAIL-SBS-CINE-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-08` | `设计风格解析.md` 是否完整包含角色色调材质/空间叙事/道具层级/世界观视觉语法，按角色/场景/道具拆分且遵守画面合同 | `FAIL-SBS-DESIGN-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-09` | `分镜脚本.md` 是否含 Numbers 示例 19 列、顺序一致、每镜一行、提示词编排合规 | `FAIL-SBS-STORYBOARD-SCRIPT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-10` | 是否存在版权表达复制、项目不适配或 AIGC 不可执行风险 | `FAIL-SBS-RIGHTS` | 回到 `N4-PRINCIPLE` 或阻断 |
| `GATE-SBS-11` | 输出是否含 `思考过程`、路径统一、阶段解析与分镜脚本可消费 | `FAIL-SBS-OUTPUT` | 回到 `N7-WRITE` |

## Verdict

- `pass`: 所有 gate 通过，可作为 AIGC 阶段附加上下文。
- `needs_rework`: 有局部字段、证据或桥接问题，必须直接修复后复审。
- `blocked`: 素材不可见、版权边界无法处理、或用户要求具体复制。
