# Type Map: D-主板混合参照

本文件定义 `D-主板混合参照` 的任务分型和 route。

## Mode Selection

| mode | input signal | required context | output |
| --- | --- | --- | --- |
| `prompt_only` | 只要提示词、manifest、submit plan，不执行 Dreamina | `4-分组`、故事板目录、设计生成目录 | prompt、reference manifest、submit plan |
| `single_group_generate` | 单个三段式 `group_id` + 要生成视频 | 单组正文、YAML、故事板/主体参照 | 单组 plan、queue、结果 |
| `episode_batch_generate` | 第 N 集整集批量 | 全集分组、全集故事板、设计资产 | 逐组 plan、queue、报告 |
| `group_batch_generate` | 多个三段式 `group_id` | 指定组集合 | 多组 plan、queue、报告 |
| `multi_episode_batch_generate` | 多集 | 每集独立输入与输出根 | 分集 plan、queue、报告 |
| `query_or_download` | submit_id、queue ledger、结果下载 | 既有 D 输出目录 | 更新状态或下载 |
| `repair` | prompt/manifest/plan/queue 漂移 | 现有 D 产物与源输入 | 修复后的产物 |
| `review_only` | 只检查，不提交 | 现有 D 产物 | review verdict |

## Reroute Signals

| signal | route |
| --- | --- |
| 只需要镜级分镜画面图、多张 shot image 或四段式 `分镜ID@路径` | `7-视频/A-分镜画面参照` |
| 只需要组级故事板图作为参照 | `7-视频/B-分镜故事板参照` |
| 只需要角色、场景、道具主体参照 | `7-视频/C-主体参照` |
| 需要同时使用故事板总参照和主体后缀参照 | 留在 `7-视频/D-主板混合参照` |
| 需要生成故事板图本体 | `6-图像/B-分镜故事板` |
| 需要生成角色/场景/道具设计图本体 | `5-设计/*/3-生成` |

## Type Package Loading

## Package Index

| package | load when | context files |
| --- | --- | --- |
| `hybrid_reference_default` | 默认所有 D 任务 | `references/hybrid-prompt-assembly-contract.md`, `references/hybrid-reference-binding.md` |
| `batch_execution` | 需要提交、查询或下载 Dreamina | `references/dreamina-handoff.md`, `.agents/skills/cli/dreamina-cli/SKILL.md`, `.agents/skills/cli/dreamina-cli/CONTEXT.md` |
| `repair_review` | 修复或审查既有产物 | `review/review-contract.md`, `CONTEXT.md` |

## Default Package Rule

默认加载 `types/hybrid-reference-default.md`。当任务进入提交、查询或下载时，额外加载 `batch_execution` 对应上下文；当任务是修复或审查时，额外加载 `repair_review` 对应上下文。

## Loading Flow

1. 先根据用户输入和现有产物锁定 `mode`。
2. 加载默认包 `types/hybrid-reference-default.md`。
3. 若 `mode` 涉及 Dreamina 执行、查询或下载，加载 `references/dreamina-handoff.md` 与 dreamina-cli 技能对。
4. 若 `mode` 是 `repair` 或 `review_only`，加载 `review/review-contract.md`。
5. 把选中的类型包交给 `steps/hybrid-reference-video-workflow.md` 消费。

## Completion Gate

1. mode 与处理范围明确。
2. D 任务必须同时尝试故事板总参照和 YAML 主体参照绑定。
3. 若任一参照缺失，manifest 和报告必须说明缺失原因。
4. 输出路径位于项目内 `7-视频/D-主板混合参照`。
