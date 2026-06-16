# Review Contract: aigc 5-导演

本文件展开 `SKILL.md#Review Gate Binding`，只用于候选导演批注稿审查和修复回接。

## Review Gates

| gate_id | pass_condition | fail_code | rework_target |
| --- | --- | --- | --- |
| `GATE-DIR-01-SOURCE-LOCK` | 剧本、美学上下文、导演锚点和输出模式唯一 | `FAIL-DIR-SOURCE-LOCK` | `N1-DIR-INTAKE` |
| `GATE-DIR-02-CONTEXT-UNDERSTANDING` | 报告能说明题材、情节、人物关系和画面基调如何影响批注 | `FAIL-DIR-CONTEXT-SHALLOW` | `N2-DIR-UNDERSTAND` |
| `GATE-DIR-03-STYLE-EVIDENCE` | 导演画像有来源、可执行维度和禁用误读 | `FAIL-DIR-STYLE-SHALLOW` | `N3-DIR-STYLE` |
| `GATE-DIR-04-POINT-COVERAGE` | 全部命中画面点均有批注或明确 N/A | `FAIL-DIR-POINT-COVERAGE` | `N4-DIR-POINT-MAP` |
| `GATE-DIR-05-INLINE-FORMAT` | 批注格式固定为 `（导演批注：XXX）`，并紧贴对应画面点 | `FAIL-DIR-FORMAT` | `N5-DIR-INJECT` |
| `GATE-DIR-06-SCRIPT-FAITHFULNESS` | 原剧本文字、字段、对白、顺序和剧情事实未被改写 | `FAIL-DIR-SCRIPT-DRIFT` | `R2-DIR-SYNC-REPAIR` |
| `GATE-DIR-07-POINT-BINDING` | 每条批注能回指具体画面点 | `FAIL-DIR-GENERIC-ANNOTATION` | `N5-DIR-INJECT` |
| `GATE-DIR-08-DIRECTOR-VOICE` | 批注体现指名导演或推定导演锚点的执导意识 | `FAIL-DIR-VOICE-MISSING` | `N3-DIR-STYLE` |
| `GATE-DIR-09-STAGE-BOUNDARY` | 未生成摄影时间段、图像 prompt、视频参数或完整演员表演稿 | `FAIL-DIR-STAGE-OVERREACH` | `N5-DIR-INJECT` |
| `GATE-DIR-10-SOURCE-ATTRIBUTION` | 知识库、预训练推断和网络资料来源被区分记录 | `FAIL-DIR-SOURCE-ATTRIBUTION` | `N3-DIR-STYLE` / `N7-DIR-WRITEBACK-CLOSE` |
| `GATE-DIR-11-DENSITY` | 批注长度、密度和重复度不破坏剧本可读性 | `FAIL-DIR-DENSITY` | `N5-DIR-INJECT` |
| `GATE-DIR-12-REPORT-EVIDENCE` | 正式写回报告含来源、覆盖、绑定、review、repair 和 N/A | `FAIL-DIR-REPORT-MISSING` | `N7-DIR-WRITEBACK-CLOSE` |
| `GATE-DIR-13-EPISODE-SPINE` | 已建立整集导演意图规划和视觉主轴，逐点批注不是散点影评 | `FAIL-DIR-EPISODE-SPINE` | `N2-DIR-UNDERSTAND` |
| `GATE-DIR-14-DIRECTORIAL-SUBSTANCE` | 批注有戏剧问题、人物压力、观众位置、可演可拍取舍和上游回指 | `FAIL-DIR-SUBSTANCE-SHALLOW` | `N2-DIR-UNDERSTAND` / `N5-DIR-INJECT` |
| `GATE-DIR-15-INFORMATION-ASYMMETRY` | 信息差进入批注意图，观众/角色已知未知、揭示/隐藏边界清楚 | `FAIL-DIR-INFORMATION-ASYMMETRY` | `N2-DIR-UNDERSTAND` / `N5-DIR-INJECT` |
| `GATE-DIR-16-SCENE-RHYTHM` | 场景节奏、信息密度、节奏类型和转出方式影响批注密度与取舍 | `FAIL-DIR-SCENE-RHYTHM` | `N2-DIR-UNDERSTAND` / `N5-DIR-INJECT` |
| `GATE-DIR-17-ANTICLIMAX-STRATEGY` | 高点已判断满足、延迟、打断、假兑现、惨胜或反向兑现策略，或有 N/A 理由 | `FAIL-DIR-ANTICLIMAX-STRATEGY` | `N2-DIR-UNDERSTAND` / `N5-DIR-INJECT` |
| `GATE-DIR-18-PERFORMANCE-HANDOFF` | 关键批注能被表演技能包和演员转成具体、显式、可画面化的表演方式 | `FAIL-DIR-PERFORMANCE-HANDOFF` | `N4-DIR-POINT-MAP` / `N5-DIR-INJECT` |
| `GATE-DIR-19-AUTHORSHIP-INTEGRITY` | 批注由 LLM 基于当前剧情、画面点、导演意图和风格证据逐条判断，不是脚本/映射表/模板批量生成 | `FAIL-DIR-SCRIPTED-PROJECTION` | `R1-DIR-REWORK` -> `N2-DIR-UNDERSTAND` -> `N5-DIR-INJECT` |
| `GATE-DIR-20-UPSTREAM-CONTEXT` | `4-编剧` 与 `2-美学` 上下文明确投影为导演批注决策，并记录 source anchor、local decision 和 preservation check | `FAIL-DIR-UPSTREAM-CONTEXT` | `N1-DIR-INTAKE` / `N2-DIR-UNDERSTAND` / `N5-DIR-INJECT` |
| `GATE-DIR-21-UPSTREAM-DIRECTION` | `Director Direction Inheritance Matrix` 说明剧本、美学、导演风格来源和项目记忆如何分别引导导演意图、节奏、信息差和表演交接 | `FAIL-DIR-UPSTREAM-DIRECTION-MATRIX` | `N2-DIR-UNDERSTAND` / `N3-DIR-STYLE` / `N5-DIR-INJECT` |

## Review Procedure

1. 抽取原剧本和候选批注稿的字段结构，确认未改原字段顺序。
2. 统计画面点数量、批注数量、N/A 数量和覆盖率。
3. 抽样或全量检查批注是否紧贴对应画面点。
4. 检查批注是否有当前画面绑定信息；泛化句返回 `FAIL-DIR-GENERIC-ANNOTATION`。
5. 检查导演风格是否来自已记录来源；来源缺失返回 `FAIL-DIR-SOURCE-ATTRIBUTION`。
6. 检查是否有 `Episode Director Intent Plan`、`Episode Visual Spine`、`Director Substance Plan`、`Information Asymmetry Map`、`Scene Rhythm Profile`、`Anticlimax Strategy Map` 与 `Performance Handoff Map` 或 N/A 理由。
7. 抽查批注是否消费上述规划证据，而不是只重复导演风格词。
8. 抽查关键心理、对白、动作和表演画面点：批注必须至少给出一种演员可执行外化动作，例如视线、呼吸、停顿、手部、身体距离、重心、声线、话前/话后反应或道具/空间接触；缺失返回 `FAIL-DIR-PERFORMANCE-HANDOFF`。
9. 检查执行报告是否有 `Upstream Context Application Map` 与 `Director Direction Inheritance Matrix`；若只列输入或只说“已参考”，返回 `FAIL-DIR-UPSTREAM-CONTEXT` 或 `FAIL-DIR-UPSTREAM-DIRECTION-MATRIX`。
10. 检查越权术语：时间段、镜头参数、prompt、生成模型参数、视频节点参数，以及替下游写成完整演员表演稿。
11. 输出 `pass / needs_rework / blocked` verdict，并列出 fail code、证据和返工目标。
