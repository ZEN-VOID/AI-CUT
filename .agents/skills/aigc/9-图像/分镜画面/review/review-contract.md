# Review Contract

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 `.agents/skills/cli/imagegen` 分镜画面任务 |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、未生成或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照、数量映射或生成结果的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-GROUP-SOURCE` | 每个目标普通 `group_id` 直接引用或可审计消费 `8-分组` 完整组稿；连接件不进入任务 | `FAIL-FRAME-GROUP-SOURCE` | `references/group-source-extraction.md` |
| `G2-SHOT-MAP` | 组内普通 `分镜N` 与 `x-y-z-N` 一一映射；`shot_count >= 1`；无任意拆分、合并、跳过或新增 | `FAIL-FRAME-SHOT-MAP` | `references/group-source-extraction.md` |
| `G3-PROJECT-STYLE` | project_style_context 风格字段来自 `2-美学`、`MEMORY.md` 或项目 `CONTEXT/` 的直引或 N/A 说明，未摘要改写为第二风格真源 | `FAIL-FRAME-PROMPT` | `references/prompt-assembly-contract.md` |
| `G4-REF` | YAML 对应角色、场景、道具主体图绑定保守准确；多视图优先；生成前已 `view_image` 或缺失原因明确 | `FAIL-FRAME-REF` | `references/reference-slot-binding.md` |
| `G5-PROMPT` | prompt 含任务执行词前缀，要求生成 `shot_count` 张单独图片，并禁止 storyboard sheet / collage / grid / multi-panel / variants | `FAIL-FRAME-PROMPT` | `references/prompt-assembly-contract.md` |
| `G5A-CONSISTENCY` | 每个 Image section 完整还原对应分镜点画面状态；同组角色、场景、服装、光影、色调、道具和空间关系一致 | `FAIL-FRAME-CONSISTENCY` | `references/prompt-assembly-contract.md` / `references/spatial-continuity-contract.md` |
| `G5C-UPSTREAM-DIRECTION` | 报告包含 `Image Upstream Visual Direction Matrix`，说明上游美学、主体、分组稿、已有图像和项目约束如何导向 prompt、参照保真、比例/输出和 handoff；上游电影风格没有覆盖单独分镜画面目标 | `FAIL-FRAME-UPSTREAM-DIRECTION` | `../../_shared/upstream-context-application-contract.md` |
| `G6-PLAN` | `imagegen-plan.json` 每个普通组只有一个 group imagegen package；每个 `shot_id` 有独立 task spec；`expected_image_count == shot_count` | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G7-HANDOFF` | `.agents/skills/cli/imagegen` 依赖、内置 `image_gen` 路由、批量并发上限、参照可见化、输出覆盖和项目持久化策略合规 | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G8-RESULT-MAP` | 返回图片数量等于 `shot_count`，且每张是单独图片，按 `shot_id_order` 保存为 `images/<shot_id>.png` | `FAIL-FRAME-RESULT-MAP` | `references/imagegen-handoff.md` |
| `G9-REPORT` | 执行报告列出 generated / skipped / failed、Reference Execution Matrix、Rule Evidence Map、N/A Justification、Repair Log 与返工入口 | `FAIL-FRAME-REPORT` | `templates/output-template.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-GROUP-SOURCE
    - G2-SHOT-MAP
    - G3-PROJECT-STYLE
    - G4-REF
    - G5-PROMPT
    - G5A-CONSISTENCY
    - G5C-UPSTREAM-DIRECTION
    - G6-PLAN
    - G7-HANDOFF
    - G8-RESULT-MAP
    - G9-REPORT
  todos: []
```
