# Group Source Extraction Contract

本文件定义 `N2-GROUP-SOURCE` 与 `N3-SHOT-POINT-MAP`：从 `projects/aigc/<项目名>/10-分组/第N集.md` 中锁定对应普通分镜组的完整内容，并把组内 `分镜N` 点位映射为四段式 `shot_id`。

## Source Priority

1. `projects/aigc/<项目名>/10-分组/第N集.md` 是分镜画面生成的剧情、镜头、声音和组内连续性主真源。
2. 对每个目标 `## x-y-z`，必须直接引用或完整保存该组从标题到下一个标题前的全部正文，作为 `group_full_content`。
3. 项目 `MEMORY.md` 与相关 `CONTEXT/` 只提供项目级风格边界，不替代组稿内容；legacy `north_star.yaml` 仅在旧项目已存在且本轮需要回读时作为辅助证据。
4. `11-主体/*/3-生成` 只提供主体参照图候选，不改写剧情或分镜点。
5. `8-摄影`、`9-光影` 仅在用户显式要求上溯修复 `10-分组` 时读取。

## Group Block Rules

- 普通分镜组标题格式为 `## x-y-z`。
- 连接件标题格式为 `## x-y-z~x-y-z`；连接件默认完全忽略，不进入 prompt、manifest、plan 或生成图片。
- 目标组的完整正文必须保留：场景标题、全局风格、画面风格、全部 `分镜N`、对白/音效/旁白、组底 YAML、角色/场景/道具统计和其他上游已写入的生产信息。
- 不得用“组摘要”“当前镜摘要”或只摘取 `分镜N` 单行替代完整组稿基础。

## Shot Point ID Mapping

本技能现在按 `10-分组` 内已经形成的普通 `分镜N` 点位生成图片。四段式 ID 的最后一段必须与组内普通分镜点的源顺序一一对应：

```text
group_id: 1-2-3
source shot labels: 分镜1, 分镜2, 分镜3
shot_id_order: 1-2-3-1, 1-2-3-2, 1-2-3-3
image_count: 3
```

规则：

- 每个普通 `分镜N` 生成 1 张独立图片。
- `shot_count` 等于该组普通 `分镜N` 数量。
- `imagegen-plan.json` 的 `n` 必须等于 `shot_count`。
- 不得由 LLM 任意拆分、合并、跳过或新增 `分镜N` 点位。
- 若源稿确实存在空分镜、重复编号或无法解析的分镜点，必须进入 report 和 repair，不得静默修正。

## Extraction Fields

`group-index.json` 至少包含：

| field | requirement |
| --- | --- |
| `episode_id` | 集号 |
| `source_episode_path` | `10-分组/第N集.md` 路径 |
| `group_id` | 三段式普通组 ID |
| `group_heading` | 原始标题行 |
| `group_full_content` | 对应组完整正文或可审计的全文块引用 |
| `group_full_content_hash` | 可选，便于证明 prompt 依据未漂移 |
| `shot_points[]` | 按源顺序列出每个 `分镜N` |
| `shot_points[].shot_id` | 四段式 ID |
| `shot_points[].source_shot_label` | 例如 `分镜1` |
| `shot_points[].source_shot_text` | 该分镜点正文 |
| `shot_count` | 普通 `分镜N` 数量 |
| `skipped_connectors[]` | 被跳过的连接件标题 |
| `yaml_subjects` | 组底 YAML 中角色、场景、道具 |

## Evidence Gate

完成后必须证明：

- 每个目标普通组有完整 `group_full_content`。
- 每个 `shot_id` 唯一且可回指 `group_id + source_shot_label`。
- `shot_count >= 1`。
- `shot_count` 与后续 prompt 的 Image section 数、plan 的 `n`、result 的返回图片数一致。
- 连接件没有进入任何图片任务。
- 未解析的组、重复分镜、空分镜或 YAML 问题进入执行报告。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否把 `10-分组/第N集.md` 的目标普通组完整正文作为 prompt 基础，而不是摘要或单镜片段？ | `G1-GROUP-SOURCE` | `FAIL-FRAME-GROUP-SOURCE` | `N2-GROUP-SOURCE` | `group-index.json` 记录 `group_full_content` 或全文块引用、源路径、起止行/hash。 |
| 是否按普通 `分镜N` 源顺序建立 `x-y-z-N`，且没有 LLM 自行拆分、合并或新增点位？ | `G2-SHOT-MAP` | `FAIL-FRAME-SHOT-MAP` | `N3-SHOT-POINT-MAP` | `shot_points[]` 包含 `source_shot_label`、`source_shot_text`、`shot_id`；`shot_count` 明确。 |
| 连接件是否被识别并跳过，未进入 prompt、manifest、plan 或图片任务？ | `G2-SHOT-MAP` | `FAIL-FRAME-SHOT-MAP` | `N2-GROUP-SOURCE` | `skipped_connectors[]` 与 plan task 列表可对照，连接件任务数为 0。 |
| `shot_count` 是否与 prompt sections、plan.n、result returned_count 保持一致？ | `G8-RESULT-MAP` | `FAIL-FRAME-RESULT-MAP` | `N3-SHOT-POINT-MAP` / `N9-PERSIST-MAP` | report 记录 `shot_count`, `prompt_image_section_count`, `plan.n`, `returned_count`。 |
