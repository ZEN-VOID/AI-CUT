# 2-Global I/O Contract

本文件是 `aigc/2-Global` 的输入输出、命名与汇流写回单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` | 当前集导演前置工作的主输入；正文内部带三段式 `分镜组ID` 标题 `【x-x-x】`，且每组正文需要完整整理入 episode seed root |
| 可选 | `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md` | 当前集分组决议、组序与 handoff 摘要 |
| 必需 | `projects/aigc/<项目名>/0-Init/north_star.yaml` | 项目级目标与风格方向 |
| 必需 | `projects/aigc/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段高层 handoff |
| 可选 | `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml` | 预设、锁轴、保真模式证据 |
| 可选 | `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md` | 当前集逐集剧本主稿 |
| 可选 | `projects/aigc/<项目名>/2-Global/第N集.json` | 已有当前集 seed root；供增量 patch 使用 |
| 可选 | `projects/aigc/<项目名>/team.yaml` | 项目级顾问团真源；若 `enabled == true`，当前只供前置风格/类型 advisory 与角色归属解释使用 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| creative | `projects/aigc/<项目名>/2-Global/第N集.json` | `2-Global` 专属按集 seed root；当前阶段写 `meta + project_global + groups[].global`，不写 shot-level 明细 |
| governance | `projects/aigc/<项目名>/2-Global/validation-report.md` | 阶段验收、阻塞、根因上溯与 closure；不是创作业务输出物 |
| internal | `global_style_plan / type_bible_plan / group_type_plan / director_intent_plan` | 四条内部能力链的思行计划 |
| internal | `episode_seed_patch / writeback_patch_set / convergence_report` | 模板填充、汇流审计与最终写回侧车 |
| internal | `advisory_runtime_note / advisory_member_list / advisory_synthesis` | 当前仅记录前置 `监制` advisory 的命中情况与综合摘要；不再承载落盘后 refine |
| removed | `projects/aigc/<项目名>/2-Global/{全局风格,全集类型元素,分组类型元素,导演意图}.md` | 新执行不得生成或更新；历史项目中仅视为 legacy artifacts |

## Naming Contract

- `input_lock_note`
- `invariant_brief`
- `global_style_plan`
- `type_bible_plan`
- `group_type_plan`
- `director_intent_plan`
- `episode_seed_patch`
- `convergence_report`
- `writeback_patch_set`
- `advisory_runtime_note`
- `advisory_member_list`
- `advisory_synthesis`
- `handoff_note`

## Hard Rules

1. 本阶段只存在父 skill 一个 canonical writeback owner。
2. `projects/aigc/<项目名>/2-Global/第N集.json` 是本阶段唯一创作业务真源；`.agents/skills/aigc/2-Global/templates/episode-root.template.json` 只是填写模板。
3. `第N集.json` 必须同步维护 `meta.剧名 / 集数 / 组数 / 总时长`、`project_global.全局风格 / 全集类型元素` 与 `groups[].分镜组ID / global.剧本正文 / global.*`。
4. `groups[].global.剧本正文` 必须完整整理自 `1-Planning/3-分组/第N集.md` 的命中组正文，只去掉重复组号标题，不得二次摘要或净化。
5. `groups[].global.全局风格 / 类型元素 / 导演意图` 必须由当前阶段直接定稿写入 JSON，不允许先写 Markdown 再抽取；其中 `全局风格` 在真人古装影视项目中默认遵循高清电影级真实摄影语法、物理照明、真实材质、克制镜头、真实动作反馈与反动画化禁区，`导演意图` 必须具备观看策略、执行抓手和禁用方向，不得退化成剧情摘句。
6. 本阶段的 episode seed root 只负责组级结构化 handoff，不得在本阶段发明 `分镜切换`、`正文切分参考[]`、`分镜明细[]`、`正文回指` 或任何 shot-level 字段。
7. 新执行不得生成 Markdown 输出；若历史迁移任务确需派生，必须从已确认 JSON 派生，不得出现“Markdown 先写、JSON 后补”的逆序。
8. `3-Detail` 后续若需要更细分的 shot-level root，应在自己的 `_shared` 下定义并维护独立模板，不得反向要求 `2-Global` 沿用 detail root 结构。
9. 若 `team.yaml.enabled == true` 且当前阶段命中 `roles.supervision`，只允许把 advisory 记录为前置侧车；不得再借 `team.yaml` 触发落盘后的 `监制 refine`。
