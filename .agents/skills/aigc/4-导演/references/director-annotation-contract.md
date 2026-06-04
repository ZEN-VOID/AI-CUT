# Director Annotation Contract

本文件只展开 `SKILL.md` 中已声明的导演批注注入规则，不拥有独立入口、输出路径或完成门。

## Injection Target Contract

命中画面点包括：

- 明确字段：`画面`、`动作画面`、`对白画面`、`音效画面`、`旁白画面`、`系统画面`、`心理反应`、`表演提示`、`环境描写`、`角色动作`、`场面调度`、`群像画面`、`表情特写`、`道具特写`、`独白画面`、`内心独白画面`、`规则显影`、`现实灾难画面`、`转场`。
- 语义等价字段：任何包含可见动作、可听声音承托、信息显影、表演反应、心理外化、系统界面或环境压力的字段。
- 纯对白、纯旁白、纯音效字段本身不默认注入；它们对应的 `对白画面`、`旁白画面`、`音效画面` 必须注入。

## Annotation Content Contract

每条批注应满足：

- 绑定当前画面点，不泛泛评价整集。
- 体现导演对这个画面的理解：观看重点、情绪压力、权力关系、节奏停顿、空间阻隔、声音功能、表演方向或信息揭示方式。
- 面向下游表演技能包和演员可读：关键心理、对白、动作和表演画面点必须包含或强烈暗示至少一种表演外化种子，如视线落点、呼吸变化、停顿、手部动作、身体距离、重心变化、声线收放、话前/话后反应、道具/空间接触。
- 体现指名导演的角色意识，但不模仿口号或硬贴代表作。
- 默认 25-80 个中文字符；复杂高潮、群像或心理高点可到 120 个中文字符。

禁止：

- 改写原剧本。
- 新增剧情事实或替换对白。
- 写成摄影时间段、镜头参数、图像 prompt 或视频生成参数。
- 替下游生成完整演员表演稿；本阶段只提供能被下游扩写的表演种子。
- 每条批注机械重复同一导演风格词。

## Style Source Contract

导演风格来源优先级：

1. 用户明确指定的导演、作品或资料。
2. 本目录 `knowledge-base/` 中已有导演或作品资料。
3. `3-美学/画面基调` 中的导演、摄影师、作品、工作室锚点。
4. 模型已有知识。
5. 网络搜索资料。

若使用第 4 或第 5 类来源，报告必须区分 `pretrained_style_inference` 与 `web_retrieved_source`。网络资料必须记录链接和检索日期。

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 注入点是否只覆盖画面点？ | `GATE-DIR-04-POINT-COVERAGE` | `FAIL-DIR-POINT-COVERAGE` | `N4-DIR-POINT-MAP` | 画面点清单 |
| 批注是否紧贴原画面点并使用固定格式？ | `GATE-DIR-05-INLINE-FORMAT` | `FAIL-DIR-FORMAT` | `N5-DIR-INJECT` | 格式抽样 |
| 批注是否体现导演角色意识且绑定当前画面？ | `GATE-DIR-07-POINT-BINDING` / `GATE-DIR-08-DIRECTOR-VOICE` | `FAIL-DIR-GENERIC-ANNOTATION` / `FAIL-DIR-VOICE-MISSING` | `N3-DIR-STYLE` / `N5-DIR-INJECT` | 批注绑定表 |
| 是否没有越权进入摄影、图像或视频阶段？ | `GATE-DIR-09-STAGE-BOUNDARY` | `FAIL-DIR-STAGE-OVERREACH` | `N5-DIR-INJECT` | 越权术语清单 |
| 关键批注是否能被演员转成具体、显式、画面化的表演？ | `GATE-DIR-18-PERFORMANCE-HANDOFF` | `FAIL-DIR-PERFORMANCE-HANDOFF` | `N4-DIR-POINT-MAP` / `N5-DIR-INJECT` | `performance_handoff_map`、表演动作抽样 |
