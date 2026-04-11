# 2-组间阶段输出契约总表

## 阶段级交付

- 阶段运行时根：`projects/<项目名>/编导/`
- 统一根文件：`projects/<项目名>/编导/第N集.json`
- 阶段验证报告：`projects/<项目名>/编导/validation-report.md`
- 运行时布局真源：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- shared schema 真源：`.agents/skills/aigc/_shared/director_episode_output.schema.json`

## 父级真源责任

1. `1-分集` 负责首次创建空的 `projects/<项目名>/编导/第N集.json`。
2. `2-组间` 每次执行前都要完整读取现存 `第N集.json` 作为上下文，而不是只读单个组。
3. `2-组间` 只 patch 组级字段，不创建第二份 episode/group 真源。
4. `3-明细` 继续在同一根文件上 patch 镜级字段。

## 组级字段责任总览

| 子路径 | patch 目标 | 最低固定语义 | 本地 sidecar | 结构化投影 |
| --- | --- | --- | --- | --- |
| `全局风格` | `final_output.main_content.分镜组列表[].组间设计.全局风格` | 所有分镜组一致继承的风格底座 | `projects/<项目名>/编导/thinking/全局风格.md` | shared schema 同一根文件 |
| `类型元素` | `final_output.main_content.分镜组列表[].组间设计.类型元素` | 全组共享约束 + 分组激活/偏置 | `projects/<项目名>/编导/thinking/类型元素.md` | shared schema 同一根文件 |
| `导演意图` | `final_output.main_content.分镜组列表[].组间设计.导演意图` | 按分镜组展开的导演设计 | `projects/<项目名>/编导/thinking/导演意图-第N集.md` | shared schema 同一根文件 |

## Shared JSON Projection

- 结构化 JSON 真源统一收口到 `.agents/skills/aigc/_shared/director_episode_output.schema.json`。
- 该 schema 不是平行第二正文，而是 `projects/<项目名>/编导/第N集.json` 的固定结构合同，顶层固定为 `metadata / thinking_chain / final_output`。
- bootstrap 空文件模板统一来自 `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`。
- `final_output.main_content.分镜组列表[]` 是 `2-组间 -> 3-明细` 的共享组级壳；`3-明细` 若做结构化消费，必须继承这一壳，不得私造另一套 group/shot 字段名。
- `分镜组列表[]` 内部固定顺序为：`分镜组ID -> 总时长 -> 剧本正文 -> 组间设计 -> 分镜明细`。
- `分镜明细[]` 内部固定顺序为：`分镜ID -> 时间段 -> 场景及方位 -> 角色及站位 -> 道具及状态 -> 分镜表现 -> 角色表现 -> 运镜手法 -> 场景氛围 -> 摄影美学 -> 转场特效(可选)`。

## 根技能输出责任

1. 给出唯一主路由，而不是同时扩写三个子技能产物。
2. 固定阶段边界与 canonical landing。
3. 每次执行都先加载整份 `projects/<项目名>/编导/第N集.json`，再做字段级 patch。
4. 在阶段级 `validation-report.md` 中沉淀顾问团意见与验收结论。
5. 若需要节奏蓝图，引用 `1-规划/4-节奏` 作为上游真源，不在组间阶段平行重写。
6. 明确唯一下一阶段入口：`3-明细`。
