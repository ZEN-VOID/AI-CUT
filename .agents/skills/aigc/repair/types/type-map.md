# Type Map

## Package Index

| package_id | path | selection signal | relation | loaded_for |
| --- | --- | --- | --- | --- |
| `scope.stage-output` | `types/scope/stage-output.md` | 阶段文本产物、分集、编剧、导演、表演、摄影、分组 | stackable | source rule review |
| `scope.asset-continuity` | `types/scope/asset-continuity.md` | 场景、角色、道具、参照图、资产 alias 或引用不一致 | stackable | impact map |
| `scope.generated-media` | `types/scope/generated-media.md` | 图像、storyboard、视频、MP4、生成报告或审片缺陷 | stackable | asset route |
| `scope.visual-style` | `types/scope/visual-style.md` | 视觉主轴、氛围、镜头语言、光影、风格一致性 | stackable | polish / inspire |
| `scope.narrative-fact` | `types/scope/narrative-fact.md` | 剧情事实、对白、顺序、角色状态、空间时间线 | stackable | source owner |
| `operation.plan-only` | `types/operation/plan-only.md` | 只要影响范围、修复计划或报告，不授权写回 | mutually-exclusive operation | repair plan |
| `operation.execute` | `types/operation/execute.md` | 用户要求执行、改掉、同步修、写回或重做 | mutually-exclusive operation | writeback |
| `acceptance.review-gate` | `types/acceptance/review-gate.md` | 需要验收、关闭 finding、code-reviewer 或 review | stackable | final gate |

## Default Package Rule

- 默认加载 `scope.stage-output` 与 `acceptance.review-gate`。
- 若目标涉及事实、对白、顺序或角色状态，加载 `scope.narrative-fact`。
- 若目标涉及场景、角色、道具、参照图或 asset alias，加载 `scope.asset-continuity`。
- 若目标涉及图像、视频、storyboard、MP4 或生成报告，加载 `scope.generated-media`。
- 若目标涉及中文润色、视觉氛围、镜头表达或创意激发，加载 `scope.visual-style`。
- 未授权写回时选择 `operation.plan-only`；用户明确要求执行时选择 `operation.execute`。
- operation 包互斥；scope 和 acceptance 包可叠加。

## Loading Flow

1. 读取用户请求、项目根、目标路径和 review finding。
2. 选择 scope 包，先定位 stage output，再叠加对象、资产、生成媒体或风格包。
3. 选择 operation 包，决定只出 plan 还是写回。
4. 选择 acceptance 包，确定验收深度。
5. 将命中包作为固定上下文交给 `steps/repair-workflow.md`。
