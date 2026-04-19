# 2-Global Shared I/O Contract

本文件是 `aigc/2-Global` 的输入输出、命名与汇流写回单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` | 当前集导演前置工作的主输入；正文内部带三段式 `分镜组ID` 标题 `【x-x-x】`，且每组正文需要完整整理入 shared root |
| 可选 | `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md` | 当前集分组决议、组序与 handoff 摘要 |
| 必需 | `projects/aigc/<项目名>/0-Init/north_star.yaml` | 项目级目标与风格方向 |
| 必需 | `projects/aigc/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段高层 handoff |
| 可选 | `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml` | 预设、锁轴、保真模式证据 |
| 可选 | `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md` | 当前集逐集剧本主稿 |
| 可选 | `projects/aigc/<项目名>/2-Global/*.md` | 已有全局文档，供增量 patch 使用 |
| 可选 | `projects/aigc/<项目名>/3-Detail/第N集.json` | 已有 shared episode root；供 `group_design` seed 增量 patch 使用 |
| 可选 | `projects/aigc/<项目名>/team.yaml` | 项目级顾问团真源；若 `enabled == true`，既供 `全局风格` 链提取 team 风格锚点，也供 stage-end 监制会审 runtime 使用 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/aigc/<项目名>/2-Global/全局风格.md` | 项目级风格底座 |
| canonical | `projects/aigc/<项目名>/2-Global/导演意图.md` | 按集、按组组织的导演构思主稿 |
| canonical | `projects/aigc/<项目名>/2-Global/全集类型元素.md` | 项目级类型总则 |
| canonical | `projects/aigc/<项目名>/2-Global/分组类型元素.md` | 按集、按组组织的类型化导演协议 |
| canonical | `projects/aigc/<项目名>/3-Detail/第N集.json` | shared episode root；当前阶段写 `分镜组ID / 总时长 / 剧本正文 / 组间设计 / 分镜切换 / 分镜明细=[]` 的分镜组壳与相关 metadata；`正文切分参考[] / 分镜明细[].正文回指` 由 `3-Detail` 后续补齐 |
| internal | `global_style_plan / type_guidance_plan / director_intent_plan` | 三条内部能力链的思行计划 |
| internal | `group_design_seed_plan / group_design_seed_patch / episode_seed_patch` | Markdown 字段提取、组壳整理与 shared root 写回侧车 |
| internal | `switching_rationale_note` | former `镜花/1-切换` fixed-shot-count 接受逻辑的阶段内化说明 |
| internal | `style_note / type_note / director_note / convergence_report` | 取舍、阻塞与汇流审计侧车 |
| internal | `writeback_patch_set` | 父 skill 最终写回前的统一 patch 集 |
| internal | `supervision_runtime_decision / supervision_reviewer_list / supervision_report / supervision_patch_set / supervision_refine_note` | 输出相关真源文件首次落盘后的 `监制 subagents` 会审、汇流与最小 patch 侧车 |

## Naming Contract

- `input_lock_note`
- `invariant_brief`
- `branch_scope_plan`
- `global_style_plan`
- `global_style_patch`
- `style_note`
- `style_report`
- `type_guidance_plan`
- `type_guidance_patch`
- `type_note`
- `type_report`
- `director_intent_plan`
- `director_intent_patch`
- `director_note`
- `director_report`
- `group_design_seed_plan`
- `group_design_seed_patch`
- `episode_seed_patch`
- `switching_rationale_note`
- `constraint_bridge_note`
- `convergence_report`
- `writeback_patch_set`
- `supervision_runtime_decision`
- `supervision_reviewer_list`
- `supervision_report`
- `supervision_patch_set`
- `supervision_refine_note`
- `handoff_note`

## Hard Rules

1. 本阶段只存在父 skill 一个 canonical writeback owner。
2. `全局风格.md` 的项目级总则必须保持稳定，且其最终字段默认必须是无污染底层摄影风格协议：只描述媒介属性、摄影参照锚点、渲染技术栈、摄影级总体属性与可执行摄影构词，优先使用 AIGC 工具易读的具象词组；重点应放在照明质感、反差策略、颗粒纯度、皮肤层次、反射控制、暗部可读性与可拍空间光比这些能统摄全局的摄影属性，不再要求“空间/时间处理”“整体画面气压”这类抽象汇总词，也不固定景别，不直接写具体颜色、材质、构图、镜头操作、剧情母题总结或工具参数；若 `team.yaml.enabled == true`，则应优先把已启用 team 成员转写为“参照 XXX 的 XXX”式摄影锚点，并补出 AIGC 工具可执行构词；若在 Markdown 中补充 `Midjourney` 等工具的投影组织建议，也只能作为 canonical core prefix 的派生排布，不得改写字段语义。`全集类型元素.md` 只写项目级类型总则，`分组类型元素.md` 必须按 `第N集 -> 【x-x-x】` 组织组级类型判断；三者都不得被 episode 细节污染。
3. `导演意图.md` 必须按 `## 第N集 -> ### 【x-x-x】` 组织，父 skill 只更新命中章节。
4. `2-Global` 必须把 `组间设计` 与完整 `剧本正文` 写入 `projects/aigc/<项目名>/3-Detail/第N集.json` 的分镜组壳，但不得在本阶段发明 shot-level `分镜明细[]`、`正文切分参考[]` 或 `分镜明细[].正文回指`。
5. `2-Global` 必须在同一份 shared root 中直接写入 `分镜切换` 固定数字，供 `3-Detail` 后续直接接受与落镜。
6. former `镜花/1-切换` 的 fixed-shot-count 接受逻辑已内化到 `2-Global`；本阶段应留下 `switching_rationale_note` 解释为何是该镜数，并显式包含 `rhythm_density_profile`（媒介形态、平台形态、类型任务、密度下限、例外原因），但不得在 shared root 发明 shot-level `时间段`。
7. `分镜组列表[].剧本正文` 必须完整整理自 `1-Planning/3-分组/第N集.md` 的命中组正文，只去掉重复的组号标题，不得二次摘要或净化。
8. `3-Detail` 必须在继承整组 `剧本正文` 后补出 `正文切分参考[]` 与 `分镜明细[].正文回指` 作为正式桥接层；`2-Global` 只交组级完整正文，不提前切段。
9. `组间设计.全局风格 / 类型元素 / 导演意图` 必须直接提取自 Markdown 中的同名字段；写入 JSON 时只允许剥离字段标题与空白。`组间设计.出场角色及穿搭` 为组级服装摘要槽，格式建议 `角色名-服装简述`。
10. `组间设计.全局风格 / 类型元素 / 导演意图` 的默认字数窗固定为 `220 / 50 / 100` 个字符以内；`出场角色及穿搭` 在 `2-Global` 阶段允许先留空字符串，待 `3-Detail` 回填。
11. 不再允许 `subagent_brief_*`、`context_packet_*`、`agents_plan_*` 这类外置导演组命名语义继续作为本阶段真源。
12. 新输出不得再生成 `2-Global/类型元素.md`、`2-Global/全局风格/`、`2-Global/类型元素/`、`2-Global/设计元素/` 等旧兼容载体；旧项目中已经存在的同名文件只允许作为迁移输入 fallback。
13. 若 `team.yaml.enabled == true` 且当前阶段命中 `roles.supervision`，`supervision_*` 命名必须作为 stage-end runtime 侧车；它们只能服务于已落盘 canonical 文件的会审与 refine，不得扩写成第二套输出真源。
14. `roles.supervision.source_skill_refs` 只可作为 reviewer 匹配提示，不得直接充当 reviewer skill；会审 reviewer 的最终真源仍应落在 `.agents/skills/team/**/SKILL.md`。
