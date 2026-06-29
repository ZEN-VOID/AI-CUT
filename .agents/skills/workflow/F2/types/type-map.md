# F2 Type Map

本文件只展开 F2 类型路由的判型提示。规范路由真源仍是 `SKILL.md` 的 `Type Routing Matrix`。

## Package Index

| package | path | purpose | load_when |
| --- | --- | --- | --- |
| `default` | `types/default/default.md` | 展开 F2 默认 route 判型、降级和审计提示 | 路由复杂、audit、repair 或 dry-run evaluation |

## Default Package Rule

- 未命中特定 repair/audit/plan 信号但明确使用 `$F2` 时，优先判断是否满足 `full_hyperframes_edit`。
- 若缺主时钟但用户没有授权生成 TTS，降级为 `plan_only` 或请求补充音频。
- F2 普通任务默认收束到 `full_hyperframes_edit` 并完成 final MP4；可预览工程只是 render 前置门。
- F2 普通任务默认输出比例为 `16:9`、画布 `1920x1080`；竖屏素材或参考片不能自动改写默认比例。
- F2 普通任务若包含台词字幕，final 前必须运行 `scripts/validate_dialogue_sync.py --strict-final`；validator fail 时 route 回 `repair_dialogue_timing`，不能继续 C7 pass。
- 只有用户明确指定竖屏/短视频平台规格、明确给出其他尺寸，或项目真源已锁定非 16:9 时，才允许非 16:9，并必须在 intake/report 写明依据。
- 只有用户明确禁止渲染、只要工程预览，或 render 依赖阻断时，才停在 `hyperframes_project_build`，并必须报告 no-render 豁免。
- 若用户只要求审查或定位错误，进入 `audit_existing`，除非用户明确要求写回修复。

## Loading Flow

1. 先由 `SKILL.md` 的 `Type Routing Matrix` 决定候选 route。
2. 若多个 route 同时命中，读取 `types/default/default.md` 做判型展开。
3. 判型结果必须回写 `f2_intake.json` 或执行报告。
4. 本文件不得新增 `SKILL.md` 未声明的 route。

## Route Expansion

| type_id | user_signal | canonical_route | required_minimum | notes |
| --- | --- | --- | --- | --- |
| `TYPE-F2-INIT` | 初始化 F2、新建 F2 工作区 | `project_initialization` | project name or output root | 只建/说明工程骨架，不进入 render |
| `TYPE-F2-PLAN` | 只做方案、PRP、storyboard、不要渲染 | `plan_only` | content truth or objective | 输出计划和报告，不写 final |
| `TYPE-F2-FULL` | 命中 F2 且未明确禁止渲染；成片、final MP4、渲染、完整自动剪辑 | `full_hyperframes_edit` | content + audio clock + source media/generation authorization | 必须走 preview 后 render，completion gate 到 C7；未指定时默认 16:9、1920x1080；台词字幕必须有 dialogue sync validator pass |
| `TYPE-F2-PROJECT` | 明确可预览工程、先不出片、禁止渲染，或 render 依赖阻断 | `hyperframes_project_build` | content + source media/generation authorization | completion gate 到 C6，必须报告 no-render 豁免 |
| `TYPE-F2-TIMING` | 字幕/旁白不对、cue 错位 | `repair_dialogue_timing` | existing project or transcript/audio/source | 优先修 dialogue clock，并以 validator pass 作为回流证据 |
| `TYPE-F2-VISUAL` | 画面不贴、大字报/PiP/转场/安全区问题 | `repair_visual_composition` | existing project or source plan/assets | 优先修 evidence/plan/composition |
| `TYPE-F2-AUDIT` | 审查、为什么黑屏、为什么 render fail | `audit_existing` | existing project/final/log | 不默认写回 |
| `TYPE-F2-EVIDENCE` | 只整理素材、理解视频、建立片段证据 | `asset_evidence_only` | source media | 不生成 final |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| Does a type row contradict the main Type Routing Matrix? | Any route not present in `SKILL.md` fails | `FAIL-TYPE-MAP-DRIFT` | `Type Routing Matrix` | type row and main route |
| Is the selected route supported by minimum input? | Missing minimum input without downgrade fails | `FAIL-INPUT-MINIMUM` | `N1-INTAKE` | intake decision |
| Does ordinary F2 output default to 16:9 when no other ratio is specified? | Non-16:9 without explicit user/project evidence fails | `FAIL-ASPECT-RATIO` | `N1-INTAKE` / `N6-HYPERFRAMES-AUTHOR` / `N8-RENDER-VERIFY` | intake aspect and ffprobe dimensions |
| Does dialogue caption sync have mechanical validation? | Missing/failing `dialogue_sync_validation.json` on final route fails | `FAIL-DIALOGUE-CLOCK` | `N4-DIALOGUE-CLOCK` | validator JSON |
