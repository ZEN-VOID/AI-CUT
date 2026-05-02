# Review Contract

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 imagegen |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、跳过或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照或生成结果的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `shot_id` 可回指 `4-分组` 源组与 `分镜N` | `FAIL-FRAME-ID` | `references/group-source-extraction.md` |
| `G2-NORTHSTAR` | 三项 north_star 字段为直引，未摘要、未翻译、未改写 | `FAIL-FRAME-PROMPT` | `references/prompt-assembly-contract.md` |
| `G3-PROMPT` | 英文 prompt 为单镜、核心内容未改写、<= 1300 English words，且完整 prompt 设计体系进入英文 prompt 本体 | `FAIL-FRAME-PROMPT` | `references/prompt-assembly-contract.md` |
| `G3D-PROMPT-DESIGN-SYSTEM` | 英文 prompt 必须包含或等价覆盖：frame identity、source truth、continuity、primary anchor、support anchors、spatial blocking、camera/composition、focus target、scene reference style lock、materials/atmosphere、avoid constraints；不得只写镜头摘要或把体系停留在 `Spatial Continuity Plan` 字段 | `FAIL-FRAME-PROMPT-SYSTEM` | `references/prompt-assembly-contract.md` |
| `G3C-SCENE-VISUAL-STYLE-LOCK` | 若场景参照图存在，prompt 组织前必须已 `view_image` 并记录 `scene_visual_style_lock_status: visible_in_conversation_context`；prompt 块必须包含固定提示词“画面风格，光影，色调和氛围与场景参照图保持一致。”；英文 prompt 必须包含等价约束 `Match the scene reference image's visual style, lighting, color palette, and atmosphere.`；报告/manifest 必须记录从场景图提炼的光影、色调、氛围和材质信息 | `FAIL-FRAME-SCENE-STYLE` | `references/prompt-assembly-contract.md` |
| `G3A-PREV-FRAME-CONTINUITY` | 同场景非首镜若上一分镜已有本地生成图，当前 prompt 组织前必须已 `view_image` 上一图并记录 `previous_frame_context_status: visible_in_conversation_context`；当前 prompt 必须保持站位、走位、朝向、遮挡、关键道具相对位置和镜头轴线的逻辑一致；无上一图、上一镜未生成、不同场景或场景首镜必须记录对应原因 | `FAIL-FRAME-CONTINUITY` | `references/prompt-assembly-contract.md` |
| `G3B-3D-SPATIAL-CONTINUITY` | 同场景分镜必须包含 `Spatial Continuity Plan`：候选锚点、主锚点、辅助锚点、空间轴线、角色起点/终点/移动轨迹、身体朝向、视线、遮挡、道具相对位置和镜头轴线；不得只复用平面背景；正反打必须说明相对背景面、line of action、screen direction 和 eyeline match；追逐、进出门、围站、绕物、上下楼、遮挡、交接、队列、换机位等桥段必须有对应锚定模式 | `FAIL-FRAME-SPATIAL` | `references/spatial-continuity-contract.md` |
| `G3E-SHOT-ANCHOR-PROJECTION` | `Primary anchor` / `Support anchors` 必须从当前四段式分镜的单镜真相投影得到，并在 `Spatial Continuity Plan` 中记录 `shot_anchor_projection_status` 与 `source_frame_anchor_evidence`；蒙太奇、插入镜、道具特写、转场镜头、路线图、远景建立镜头或同组临时换地点画面不得直接沿用分组主场景默认锚点；只有当前单镜画面确实由分组主场景锚点支配构图时，才允许 `inherited_scene_anchor_with_reason` | `FAIL-FRAME-SHOT-ANCHOR` | `references/spatial-continuity-contract.md` |
| `G4-SLOTS` | Characters / Scene / Props 只绑定存在图片；同一主体有多视图时必须优先绑定多视图，只有缺多视图时才用主图 | `FAIL-FRAME-REF` | `references/reference-slot-binding.md` |
| `G4A-PROMPT-PACKAGE-FIRST` | `episode_batch_generate` 与 `shot_batch_generate` 在任何 imagegen 调用前，必须已落盘覆盖指定范围全部 `shot_id` 的 `第N集-分镜画面-prompts.md`、`reference-manifest.json` 与 `imagegen-plan.json`；plan 记录 `prompt_package_status: complete_before_imagegen`，不得边生图边补写后续 prompt | `FAIL-FRAME-IMAGEGEN` | `steps/frame-image-workflow.md` |
| `G5-HANDOFF` | imagegen mode 合法，未未经许可切 CLI/API fallback | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G6-PERSIST` | 生成图片或计划输出位于项目目录，不只在 `$CODEX_HOME` | `FAIL-FRAME-IMAGEGEN` | `.agents/skills/cli/imagegen/references/output-persistence.md` |
| `G7-REF-INPUT` | 若绑定本地参照图，生成前必须逐张 `view_image` 且 results/report 记录 `reference_input_status: visible_in_conversation_context`；确无绑定图片时记录 `no_reference_images_bound` | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G8-SERIAL-BATCH` | `episode_batch_generate` 与 `shot_batch_generate` 必须按 `shot_id` 严格串行逐镜执行；plan/result 记录 `execution_order` / `serial_index` / `previous_shot_status`；不得并发、后台并行、分片并跑、边生图边补写 prompt 或跳过前镜结果 | `FAIL-FRAME-IMAGEGEN` | `references/imagegen-handoff.md` |
| `G9-REPORT` | 执行报告列出 generated / skipped / failed 与返工入口 | `FAIL-FRAME-REPORT` | `templates/output-template.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-NORTHSTAR
    - G3-PROMPT
    - G3D-PROMPT-DESIGN-SYSTEM
    - G3C-SCENE-VISUAL-STYLE-LOCK
    - G3A-PREV-FRAME-CONTINUITY
    - G3B-3D-SPATIAL-CONTINUITY
    - G3E-SHOT-ANCHOR-PROJECTION
    - G4-SLOTS
    - G4A-PROMPT-PACKAGE-FIRST
    - G5-HANDOFF
    - G6-PERSIST
    - G7-REF-INPUT
    - G8-SERIAL-BATCH
    - G9-REPORT
  todos: []
```
