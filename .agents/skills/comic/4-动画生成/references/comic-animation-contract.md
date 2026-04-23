# 漫画动画生成合同

本文件补充 `.agents/skills/comic/4-动画生成/SKILL.md` 的细则，不构成第二真源。

## 1. Prompt 真源与兼容原则

- 固定前缀必须原样作为每页 `video_prompt` 的开头。
- 4 号阶段默认消费 LLM 已直出的 `comic_page_animation_prompts.v1`，不再把脚本编 `video_prompt` 当默认主链。
- 若项目仍处于 legacy 兼容窗口，脚本只允许在显式开启 `--allow-legacy-script-authorship` 时，基于 2 号已有页级信息做受控投影。
- 4 号阶段不重新发明剧情；无论是默认路径还是兼容路径，都只能继承 2 号已经存在的页级事实与结构锚点。
- `panels[]` 默认按 `右到左、上到下` 的阅读顺序编成 `shot_plan[]`。
- 保真不等于冻结整页。应保住剧情顺序、角色身份、道具、中文文字、页码、风格 DNA 和关键构图逻辑，但必须把“静止漫画页”翻译成“有景深、有表演、有环境运动的动画电影镜头”。
- 必须显式反对：`slideshow / PPT animation / simple pan-zoom / Ken Burns / motion poster / paper cut-out drift`。
- 每页 prompt 要先保真，再谈动态化：
  - 保真：角色、服装、场景、版式、中文文字、页码和风格 DNA 不漂。
  - 动态化：角色动作更自然、镜头更平滑、环境更有生命力。

## 2. 页级 Prompt 结构

推荐句序：

1. 固定前缀
2. 当前页角色和页面职责
3. 把当前页当成 storyboard truth，而不是 frozen poster
4. 当前页 `positive_prompt` 摘要
5. `layout` 摘要
6. `shot_plan` 逐条展开
7. 景深、环境运动、角色表演和转场要求
8. 文字与页码保真要求
9. 禁止项

## 3. Shot Plan 原则

- 默认 `一个格子一个分镜`。
- 若页面有 `3` 个 panel，就默认编成 `3` 个 shot。
- 每个 shot 最少应包含：
  - `source_panel_id`
  - `shot`
  - `action`
  - `camera_motion`
  - `subject_motion`
- `camera_motion` 不能长期停留在“轻微推镜 + 平移”层；应尽量使用有动机的推进、景深穿越、rack focus、foreground wipe、parallax、crane/glide 等真实镜头语言。
- `subject_motion` 不能只写“slight motion”；应尽量给出身体重心、头部转向、视线变化、手部动作、服装/头发/雨水等 secondary motion。
- `text_slots` 不是纯装饰。若 panel 中有对白、旁白或 SFX，应在 `text_handling` 里明确“保留位置与可读性，不做文字形变”。

## 4. 图片匹配原则

- 优先匹配 `page01..page09`
- 回退匹配 `group_slug-page01..page09`
- 不允许按图像内容猜图，因为这会引入第二套不可审计真源

## 5. 与 man-tui sora 的边界

- 4 号阶段可以调用 `man-tui/video/sora`，但不重写其三段异步合同。
- `man-tui sora` 的职责是：创建任务、轮询状态、下载结果。
- `man-tui sora` 的图生视频参考图只能使用公网 URL；4 号阶段若只有本地 `page01..page09`，默认只能完成编译与 dry-run。
- 4 号的默认职责是：消费动画 prompt 真源、匹配页图、组织逐页执行与组级汇总报告。
