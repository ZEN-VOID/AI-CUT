# Context: aigc-image-storyboard-floor-plan

本文件是 `分镜平面图` 的经验层知识库，不是过程日志。它用于沉淀从 `8-分组` 生成组级多 panel 顶视图平面图时的类型判断、修复打法和可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-floor-plan-specific
last_checked_at: 2026-06-10
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-FLOOR-01` | 成图像故事板画面或透视场景 | diagram standard drift | 重写为顶视图建筑平面图 prompt，删除透视/镜头画面词 | Review Gate 固化 `G3-DIAGRAM-STANDARD` | 图中有平面边界、出入口、墙体/锚点，无写实人物和透视场景 |
| `TM-FLOOR-02` | 角色被画成写实人物或黑白小人 | icon legend drift | 重建 `character_icon_legend`，用彩色圆形/三角/方形/菱形等表示角色 | 模板固定角色图例字段 | 每个角色有颜色、形状、黑色名称标签 |
| `TM-FLOOR-03` | 颜色进入角色服装、背景或气氛渲染 | annotation color drift | 恢复黑白底图，将颜色限制到标注层和角色几何图标 | prompt 负向原子固定 color rendering forbidden | review note 确认颜色未用于渲染 |
| `TM-FLOOR-04` | 蓝色箭头表示角色运动或红色箭头表示摄影机 | annotation semantic drift | 按红=身体运动、蓝=摄影机运动重建图例 | review gate 固定颜色语义 | annotation legend 与每 panel 标注一致 |
| `TM-FLOOR-05` | panel 机械等同原始 `分镜N`，空间变化被漏掉 | panel planning drift | 由 LLM 根据位置、动作、机位和视觉节拍重建 `floor_plan_panels` | `N3-PANEL-PLAN` 固化 source span 证据 | 每 panel 有空间目标和源 span |
| `TM-FLOOR-06` | 下一组角色/摄影机/道具位置无解释跳变 | continuity drift | 对照前一张 accepted sheet 补 unchanged anchors、changed positions、movement logic | `N5-CONTINUITY` 固化连续性门 | continuity verdict 为 initial/consistent 或 failed with rework |
| `TM-FLOOR-07` | 源文本没有明确方位时被画成确定空间事实 | overconfident inference | 记录 `spatial_inference_basis` 和保守假设，避免伪造 | Quant fallback evidence 固化不确定性表达 | report 中列出保守推断依据 |
| `TM-FLOOR-08` | prompt 看似完整但空间裁决是模板套句 | scripted projection | 标记脚本化投影失败，回到完整组稿逐组重写 | LLM-first 门禁阻断脚本主创 | 每组能指出本组独有源锚点 |
| `TM-FLOOR-09` | 流程停在 `imagegen-plan.json`，没有实际生成分镜平面图图片 | imagegen plan mistaken as output | 回到 `N7-IMAGEGEN`，加载并调用 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`，补 `imagegen_called` 与项目内图片路径 | SKILL、review、template 和 type map 固化 plan-only 不可 pass | `floor-plan-sheets/<分镜组ID>.png` 存在，report 记录 imagegen_called |
| `TM-FLOOR-10` | 上游上下文只列入报告，没有说明如何影响空间理解、panel、图例、动线/机位或连续性 | upstream visual direction missing | 补 `Image Upstream Visual Direction Matrix`，把美学、主体、分组稿、前序平面图和项目上下文落到空间裁决和保守推断边界 | review gate 固化 `G2A-UPSTREAM-DIRECTION`，共享上游合同授权加载 | report 中有 source anchor、spatial decision、panel/output anchor、boundary check |

## Repair Playbook

1. 先判断失败属于源追溯、panel 结构、图面标准、角色图例、颜色标注、空间连续性、imagegen handoff 还是报告闭环。
2. 若 `group_id` 不唯一、组正文截断或连接件误入，回到 `N2-SOURCE-LOCK`。
3. 若 panel 结构像故事板画面或只按 `分镜N` 顺序切格，回到 `N3-PANEL-PLAN`，按空间位置、角色状态、摄影机变化和动作路径重新裁决。
4. 若成图不是顶视图建筑平面图，回到 `N4-DIAGRAM-SPEC`，明确黑白平面底图、墙体/边界/出入口、无透视/无场景插画。
5. 若角色图标不稳定，同集重新生成统一 `character_icon_legend`，不要按每组临时换颜色或形状。
6. 若颜色语义混乱，恢复红/蓝/绿/橙/紫/黑图例，不适用的颜色写 `none`，不要发明源文本没有的运动或机位。
7. 若连续性失败，先对照上一组 accepted sheet，列出不变锚点和变化路径，再重画当前组；必要时回查前一组是否本身不可靠。
8. 若 source 中缺方位信息，允许保守推断，但必须记录依据和不确定性，不得把猜测包装为源事实。
9. 若 imagegen 失败，保留 prompt、plan 和 manifest，记录可重试入口，不回滚已成功组。
10. `第N集-imagegen-plan.json` 只是调用载体；没有 `.agents/skills/cli/imagegen` 调用证据和 `floor-plan-sheets/<分镜组ID>.png` 时，不得把任务判为完成。
11. 整集/多组批量平面图出图默认遵循 `.agents/skills/cli/imagegen` 的 subagents 并发 fan-out，最大并发 10；主线程逐一执行只在用户显式要求时使用。
12. 平面图的上游导向矩阵必须区分“空间事实”“保守推断”“视觉风格禁用边界”。如果 source 没有明确方位，只能记录 `spatial_inference_basis`，不能把猜测写成确定站位。

## Reusable Heuristics

- `分镜平面图` 的核心对象是空间关系，不是镜头画面。越像建筑平面图，越接近目标；越像电影画面，越偏离目标。
- 分镜组内的 floor-plan panels 应围绕角色/摄影机/道具位置变化切分，而不是围绕美术构图切分。
- 彩色几何角色图标比小人轮廓更稳定；同一集内角色颜色和形状应保持一致。
- 摄影机可以用蓝色 camera marker、方向箭头和视野锥表达；蓝色不应用来表示角色运动。
- 红色角色动线可以是实线或虚线箭头，但必须对应源文本里的实际身体移动；无移动时写 none。
- 绿色构图标记适合表达取景边界、构图线或区域框，不应替代摄影机方向。
- 橙色灯光方向只有源文本或上游分组已给出时才使用；没有明确灯光方向时写 none。
- 紫色强调适合标出声音、情绪压力或叙事焦点，但不能改变空间事实。
- 上下组连续性最好以同一场景固定锚点为基准：门、窗、桌椅、道路转角、墙体、楼梯、关键道具等。
- 当角色从上一组位置移动到当前组位置时，平面图应说明路径变化；如果叙事发生跳切，也要记录 `jump_cut_or_time_gap`，不要强行画连续路径。
- imagegen plan 是执行载体，不是分镜平面图产物；完成态必须包含 `imagegen_called` 和项目内持久化图片路径。
- imagegen 批量执行形态也是完成证据；报告应记录 subagents parallel / max_concurrency 或用户显式要求的 main-thread serial。
