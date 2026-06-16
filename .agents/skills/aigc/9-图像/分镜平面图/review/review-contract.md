# Review Contract

本 review gate 只裁决 `分镜平面图` 的 prompt、manifest、imagegen 计划、成图和项目持久化，不改写 `8-分组` 主真源。

`imagegen plan` 不是完成态；必须能证明已按 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md` 执行生成，并有项目内图片路径。

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，目标组已生成并持久化 floor plan sheet 图片 |
| `pass_with_todo` | 目标组已生成并持久化图片，但存在明确记录的缺失参照、低风险不确定方位或可后续优化项 |
| `needs_rework` | 存在会污染空间事实、图面标准、连续性或生成结果的问题，必须返工 |
| `failed` | 输入缺口不可恢复，或同一失败超过重试上限；必须保留失败原因和返工入口 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `group_id` 可回指 `8-分组` 源标题、组正文和 YAML，且连接件未进入生图任务 | `FAIL-FLOOR-PLAN-PANELS` | `N2-SOURCE-LOCK` |
| `G2-PANEL-PLAN` | 每个 `floor_plan_panel` 有 source span、空间目标、角色/道具/摄影机状态，且不是机械等同 `分镜N` | `FAIL-FLOOR-PLAN-PANELS` | `N3-PANEL-PLAN` |
| `G2A-UPSTREAM-DIRECTION` | 报告包含 `Image Upstream Visual Direction Matrix`，说明上游美学、主体、分组稿、前序平面图和项目上下文如何导向空间理解、panel、图例、动线/机位、连续性和 prompt；上游视觉风格没有覆盖平面图标准 | `FAIL-FLOOR-UPSTREAM-DIRECTION` | `../../_shared/upstream-context-application-contract.md` |
| `G3-DIAGRAM-STANDARD` | prompt、plan 和成图均为顶视图黑白建筑平面图标准；不得是透视分镜画面、场景插画、气氛图或电影 still | `FAIL-FLOOR-DIAGRAM-STANDARD` | `N4-DIAGRAM-SPEC` / `N7-IMAGEGEN` |
| `G4-ICON-LEGEND` | 角色使用同集一致的彩色几何图标，并有黑色角色名标签；名称与组底 YAML 一致 | `FAIL-FLOOR-ICON-LEGEND` | `N4-DIAGRAM-SPEC` |
| `G5-ANNOTATION-COLOR` | 标注颜色语义正确：红=身体运动、蓝=摄影机、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑=文字；颜色未用于渲染 | `FAIL-FLOOR-ANNOTATION-COLOR` | `N4-DIAGRAM-SPEC` / `N6-PROMPT-PAYLOAD` |
| `G6-CONTINUITY` | 同一集相邻目标组记录 unchanged anchors、changed positions、movement logic、camera transition 和 narrative spatial rationale | `FAIL-FLOOR-CONTINUITY` | `N5-CONTINUITY` |
| `G7-IMAGEGEN` | 已加载并调用 `.agents/skills/cli/imagegen`；imagegen plan 一组一任务，默认 4K，批量执行符合最大并发 10，输出项目内路径，不走 CLI/API/provider 专属控制，不静默覆盖，不得以 plan-only 通过 | `FAIL-FLOOR-IMAGEGEN` | `N6-PROMPT-PAYLOAD` / `N7-IMAGEGEN` |
| `G8-REPORT` | 执行报告列出 generated / skipped / failed、review verdict、continuity verdict、缺参照和返工入口 | `FAIL-FLOOR-REPORT` | `N9-CLOSE` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 目标组是否可追溯，且没有把连接件当成生图任务？ | `G1-SOURCE` | `FAIL-FLOOR-PLAN-PANELS` | `N2-SOURCE-LOCK` | floor-plan-index.json 的 source heading、source span、YAML subjects |
| floor plan panels 是否按空间变化裁决，并能回指源文本？ | `G2-PANEL-PLAN` | `FAIL-FLOOR-PLAN-PANELS` | `N3-PANEL-PLAN` | panel source map 和 spatial goal |
| 上游上下文是否明确导向平面图空间裁决，并记录保守假设边界？ | `G2A-UPSTREAM-DIRECTION` | `FAIL-FLOOR-UPSTREAM-DIRECTION` | `N2-SOURCE-LOCK` / `N3-PANEL-PLAN` / `N5-CONTINUITY` | `Image Upstream Visual Direction Matrix`、source spatial comprehension、continuity manifest |
| 成图是否符合顶视图黑白建筑平面图标准？ | `G3-DIAGRAM-STANDARD` | `FAIL-FLOOR-DIAGRAM-STANDARD` | `N4-DIAGRAM-SPEC` / `N7-IMAGEGEN` | generated image path、review screenshot note、negative prompt atoms |
| 角色图例是否同集一致，并以彩色几何图标加黑色角色名呈现？ | `G4-ICON-LEGEND` | `FAIL-FLOOR-ICON-LEGEND` | `N4-DIAGRAM-SPEC` | character_icon_legend 与 panel labels |
| 颜色标注语义是否正确且未污染渲染层？ | `G5-ANNOTATION-COLOR` | `FAIL-FLOOR-ANNOTATION-COLOR` | `N4-DIAGRAM-SPEC` / `N6-PROMPT-PAYLOAD` | annotation legend、negative prompt atoms、review note |
| 上下组空间变化是否合理并与叙事扣合？ | `G6-CONTINUITY` | `FAIL-FLOOR-CONTINUITY` | `N5-CONTINUITY` | spatial-continuity-manifest.json |
| 生成计划、调用证据和结果是否位于项目内并满足一组一任务？ | `G7-IMAGEGEN` | `FAIL-FLOOR-IMAGEGEN` | `N7-IMAGEGEN` | imagegen-plan.json、imagegen-results.json、imagegen_called evidence、output existence check |
| 执行报告是否可审计且含返工入口？ | `G8-REPORT` | `FAIL-FLOOR-REPORT` | `N9-CLOSE` | 执行报告.md |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-PANEL-PLAN
    - G2A-UPSTREAM-DIRECTION
    - G3-DIAGRAM-STANDARD
    - G4-ICON-LEGEND
    - G5-ANNOTATION-COLOR
    - G6-CONTINUITY
    - G7-IMAGEGEN
    - G8-REPORT
  todos: []
```
