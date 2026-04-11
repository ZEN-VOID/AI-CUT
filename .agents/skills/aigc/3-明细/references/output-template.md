# aigc 3-明细 / Output Template

本文件承载 `aigc 3-明细` 的输出写位、模板与 canonical write contract。

## Canonical Output Slots

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- 阶段索引：`projects/<项目名>/编导/detail-stage-index.json`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 运行时布局真源：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- bootstrap 模板真源：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- schema 真源：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 子路径证据目录：
  - `projects/<项目名>/编导/evidence/1-分镜表现/`
  - `projects/<项目名>/编导/evidence/2-角色表现/`
  - `projects/<项目名>/编导/evidence/3-运镜手法/`
  - `projects/<项目名>/编导/evidence/4-场景氛围/`
  - `projects/<项目名>/编导/evidence/5-摄影美学/`
  - `projects/<项目名>/编导/evidence/6-转场特效/`

## Shared Director Schema Consumption

- `3-明细` 默认消费的是已存在的 `projects/<项目名>/编导/第N集.json`，不是自建空文件。
- 若上游 `2-组间/导演意图` 或阶段中间件需要结构化 JSON，唯一共享字段壳为 `.agents/skills/aigc/_shared/director_episode_output.schema.json`。
- `3-明细` 不得私造另一套 episode/group/shot JSON 命名；结构化消费时，默认读取 `final_output.main_content.分镜组列表[]`。
- 读取前必须先检查 `metadata.source_profile`；若存在 storyboard 预设保护模式，则本阶段只允许“preserve and extend”式 patch。
- 每个组级对象的共享固定顺序为：`分镜组ID -> 总时长 -> 剧本正文 -> 组间设计 -> 分镜明细`。
- 每个镜级对象的共享固定顺序为：`分镜ID -> 时间段 -> 场景及方位 -> 角色及站位 -> 道具及状态 -> 分镜表现 -> 角色表现 -> 运镜手法 -> 场景氛围 -> 摄影美学 -> 转场特效(可选)`。
- 当前阶段 patch-in-place 的重点是把各子路径判断压回共享 `分镜明细[]` 语义，而不是将其重写成另一份独立 shot contract。

## Source Profile Consumption

`metadata.source_profile` 的默认消费方式如下：

| 字段 | `3-明细` 默认理解 |
| --- | --- |
| `source_type = storyboard_script` | 当前集已有镜头/分镜层预设，不再把全部镜头逻辑视为待生成空白位 |
| `preset_retention_mode = preserve_and_extend` | 可补质感、角色、氛围、摄影与细节，不可推翻预设轴 |
| `preset_retention_mode = preserve_only` | 仅补最小必要缺口，避免任何结构性重排 |
| `locked_preset_axes[]` | 命中这些轴时，不得改写对应边界、顺序或母题 |

## 镜级字段责任总览

| 子路径 | patch 目标 | 最低固定语义 | 本地 sidecar |
| --- | --- | --- | --- |
| `1-分镜表现` | `final_output.main_content.分镜组列表[].分镜明细[].分镜表现` | 组内静态镜头组织与镜头分配 | `projects/<项目名>/编导/evidence/1-分镜表现/` |
| `2-角色表现` | `final_output.main_content.分镜组列表[].分镜明细[].角色表现` | 角色动作、身体冲突、对手关系或内心泄漏 | `projects/<项目名>/编导/evidence/2-角色表现/` |
| `3-运镜手法` | `final_output.main_content.分镜组列表[].分镜明细[].运镜手法` | 观看路径、运动节奏与落点 | `projects/<项目名>/编导/evidence/3-运镜手法/` |
| `4-场景氛围` | `final_output.main_content.分镜组列表[].分镜明细[].场景氛围` | 空间压力、温度、空气与环境信号 | `projects/<项目名>/编导/evidence/4-场景氛围/` |
| `5-摄影美学` | `final_output.main_content.分镜组列表[].分镜明细[].摄影美学` | 光影、色彩与捕捉策略 | `projects/<项目名>/编导/evidence/5-摄影美学/` |
| `6-转场特效` | `final_output.main_content.分镜组列表[].分镜明细[].转场特效` | 必要镜间桥接与后效包装 | `projects/<项目名>/编导/evidence/6-转场特效/` |

## Canonical Write Contract

- 本技能不定义第二正文或平行真稿，只允许沿共享终稿或阶段真源 `patch-in-place`。
- 每次输出都必须先读整份 `projects/<项目名>/编导/第N集.json`，再定向 patch 本子路径负责字段。
- 执行报告、CHANGELOG、validation-report 等辅助输出只承担证据与验收职责，不与主真源竞争。
