# Review Contract

## Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-01` | 是否有可观察证据、时间码、截图或明确描述 | `FAIL-SBS-EVIDENCE` | 回到 `N1-INTAKE` 补证 |
| `GATE-SBS-02` | 镜头边界是否能复查 | `FAIL-SBS-SHOT-MAP` | 回到 `N2-SHOT-MAP` |
| `GATE-SBS-03` | 分析是否覆盖任务相关 craft 维度 | `FAIL-SBS-OBSERVATION` | 回到 `N3-OBSERVE` |
| `GATE-SBS-04` | 临摹原则是否脱离具体表达 | `FAIL-SBS-IMITATION` | 回到 `N4-PRINCIPLE` |
| `GATE-SBS-05` | `画面风格解析.md` 是否对齐 `north_star.yaml` 风格字段且不直接改写 north star | `FAIL-SBS-STYLE-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-06` | `编导解析.md` 是否无摄影越权 | `FAIL-SBS-DIRECTING-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-07` | `摄影解析.md` 是否能转成自然中文 `分镜明细：` | `FAIL-SBS-CINE-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-08` | `设计解析.md` 是否按角色/场景/道具拆分且遵守画面合同 | `FAIL-SBS-DESIGN-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-09` | 是否存在版权表达复制、项目不适配或 AIGC 不可执行风险 | `FAIL-SBS-RIGHTS` | 回到 `N4-PRINCIPLE` 或阻断 |
| `GATE-SBS-10` | 输出是否含 `思考过程`、路径稳定、阶段解析可消费 | `FAIL-SBS-OUTPUT` | 回到 `N7-WRITE` |

## Verdict

- `pass`: 所有 gate 通过，可作为 AIGC 阶段附加上下文。
- `needs_rework`: 有局部字段、证据或桥接问题，必须直接修复后复审。
- `blocked`: 素材不可见、版权边界无法处理、或用户要求具体复制。
