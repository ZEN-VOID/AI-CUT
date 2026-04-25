# 2-Global Type Map

本文件保存 `aigc/2-Global` 的类型变量和分型策略。默认只在项目风格类型不明、与真人古装基线冲突，或用户要求改写媒介风格时加载。

## Style Type Profile

| type_id | 触发信号 | 默认策略 | 必读规则 | review gate |
| --- | --- | --- | --- | --- |
| `live_action_costume` | 古装、真人、影视、写实、电影级、真实摄影 | 使用 `references/全局风格词最佳实践.md` 的推荐基线 | `references/全局风格词最佳实践.md` | `review/review-contract.md#global-style-review-gate` |
| `live_action_non_costume` | 真人、现代、年代、都市、纪实，但非古装 | 保留真实摄影、物理光影、真实材质、克制镜头和反动画化禁区，改写服饰/时代语汇 | `references/全局风格词最佳实践.md` | `global_style` 不得保留错误时代标签 |
| `stylized_animation_exception` | 用户或项目源层明确要求动画、漫画、国漫、赛璐璐 | 不套用真人古装推荐基线；另行建立动画风格基线，并明确这是源层例外 | 项目 `north_star / init_handoff` | 不得把真人写实禁区误当动画项目禁区 |
| `legacy_projection_only` | 旧项目迁移需要读取历史 Markdown | 不重新判型，只复述 JSON 已确认字段 | `references/增量写回与兼容投影.md` | legacy 文件不得新增业务事实 |

## Decision Rule

1. 若用户显式给出真人古装影视风格参考，优先判为 `live_action_costume`。
2. 若 `north_star / init_handoff / MEMORY.md` 与用户参考冲突，按用户显式请求优先，但在 `validation-report.md` 记录冲突与采纳原因。
3. 若项目并非古装但仍是真人影视，保留真实摄影与反动画化骨架，替换古装相关词。
4. 若项目明确是动画或漫画，不要把真人古装基线硬套为输出；只把“避免污染、字段可继承、物理或风格逻辑自洽”的方法迁移过去。
