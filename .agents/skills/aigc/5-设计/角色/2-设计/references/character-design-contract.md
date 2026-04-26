# Character Design Contract

本文件展开 `角色/2-设计` 的业务细则。入口、路由和最终输出路径仍以同目录 `SKILL.md` 为准。

## Upstream Consumption

- Canonical input: `projects/aigc/<项目名>/5-设计/角色/1-清单/角色清单.md`。
- Required columns: `名称`、`首次登场`、`原文描述（关键词式）`。
- 本技能只能为清单中存在的角色主体生成设计稿。
- 若清单存在同名冲突、疑似漏项或角色归并错误，输出执行报告提出上游修复建议，不直接修改清单。

## Project Context Consumption

`north_star.yaml`:

- 抽取全局风格提示词、主题、时代/地域、影像气质、禁区和视觉约束。
- 若字段命名不统一，由 LLM 根据语义识别，但必须在执行报告中说明使用了哪些字段。
- 不得虚构不存在的全局风格提示词；缺失时写明“未提供明确全局风格提示词”，并从 north star 的主题描述中提炼临时工作口径。

`team.yaml`:

- 只消费与导演、美术、服装、摄影、角色设计、表演、动漫/漫画视觉相关的成员或大师上下文。
- 大师上下文是监制视角，不是文风模仿许可；输出应吸收其设计判断，而不是堆人名。
- 多个大师建议冲突时，以用户请求、项目 north star 和角色功能为裁决依据。

## LLM-First Creative Authorship

- 研究考据、物语、解构、服装设计、摄影描述和提示词必须由 LLM 直接完成。
- 脚本不得生成创作正文，不得把字段模板扩写成设计稿，不得根据关键词拼接英文 prompt。
- 脚本允许执行：读取上游清单、列检查、路径创建、文件存在检查、prompt 字符数统计、空字段报告、manifest 汇总。

## Web Search Allowance

网络搜索只在以下条件下允许：

- 用户明确要求考据，或角色涉及冷门历史、地域、民族服饰、职业制服、宗教/礼仪、器物、医学、军事、法律、真实地点等容易误写的信息。
- 搜索用于支持 `研究考据`，不能替代 LLM 对角色设计的综合判断。
- 搜索结果必须保留来源名称、访问日期或链接摘要；若来源不确定，写为“参考线索”而非事实。
- 搜索不得泄露项目未公开内容，不得把外部版权文本长段复制进设计稿。

## Required Content Blocks

每份设计稿必须包含以下块：

1. `名称 / 首次登场 / 原文描述复述`
2. `研究考据`
3. `物语`
4. `解构`
5. `提示词设计`

`解构` 固定子字段：

- `Identity & Story Pressure`
- `Visual Drivers`
- `Detailed Character Design`
- `Detailed Costume Design`
- `Cinematography`

`提示词设计`:

- 使用英文。
- 引用或融合全局风格提示词。
- 明确包含服装风格。
- 明确包含 `full-body costume fitting photo`、`solid color background` 和 `no scene environment`。
- 控制在 2000 字符内。
- 不包含 markdown 表格、中文解释或多版本堆叠。

## Fixed Visual Constraint

- 角色设计稿默认是纯色背景全身定妆照，用于锁定角色身体、服装、比例和可重复识别点。
- 不得让角色置身于剧情场景、建筑空间、街景、室内陈设、自然环境或复杂背景。
- `Cinematography` 必须写作棚拍式角色设计参考：full body、solid color background、neutral design lighting。
- 如果项目上下文需要表达角色所属场景，只能在研究/物语中说明，不得让最终画面进入该场景。

## Non-Goals

- 不生成最终图片。
- 不创建场景、道具、分镜或视频提示词。
- 不修改 registry、父级 skill、上游清单或其他 worker 负责的技能包。
- 不把单角色设计稿变成项目百科。
- 不输出环境肖像、剧情剧照、场景内角色照或半身头像作为默认主图口径。
