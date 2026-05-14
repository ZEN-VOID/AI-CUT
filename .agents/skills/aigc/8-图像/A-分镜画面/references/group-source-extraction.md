# Group Source Extraction Contract

本文件定义 step1：以 `projects/aigc/<项目名>/6-分组` 为主要信息来源，获取每个分镜内容，并理清其关联剧情桥段信息。

## Source Priority

1. `projects/aigc/<项目名>/6-分组/第N集.md` 是镜级 prompt 的剧情与镜头主要真源。
2. `projects/aigc/<项目名>/0-初始化/north_star.yaml` 只提供风格直引，不替代分镜内容。
3. `7-设计/*/3-生成` 只提供主体参照候选，不改写剧情。
4. `5-摄影` 仅在用户要求上溯修复 `6-分组` 时读取。

## Frame Landing ID Mapping

`6-分组` 中的标题 `## x-y-z` 表示三段式分镜组 ID：

- `x`: episode number
- `y`: scene number
- `z`: group number inside the scene

本技能生成的是 `分镜帧 / storyboard frame`，不是上游视频运镜单元的一对一翻译。组内 `分镜1`、`分镜2` 等标签是 `6-分组` 阶段围绕视频运镜中心形成的处理结果，只能作为 frame landing 的证据之一，不得直接等同于本阶段的 `shot_id`。

四段式 ID 的最后一段表示当前三段式分镜组内经判断识别后的第 `N` 个 frame landing：

```text
x-y-z-N
```

例如 `## 1-1-1` 中一个上游 `分镜1` 若包含“开场构图 -> 道具插入 -> 角色反应”三个都必须独立成帧的视觉落点，可映射为 `1-1-1-1`、`1-1-1-2`、`1-1-1-3`，并在索引中记录它们共同来自同一个 `source_camera_unit: 分镜1`。

## Frame Landing Decision

每个普通分镜组必须先做 frame landing 判断，再写 prompt。判断输入包括：场景标题、环境描写、角色动作、对白画面、旁白画面、道具特写、群像画面、心理反应、音效画面、组底 YAML、以及 `分镜明细`。禁止只扫描 `分镜N` 标签后机械生成。

常见 frame landing 类型：

| frame_landing_type | 触发证据 | 输出意图 |
| --- | --- | --- |
| `opening_composition` | 运镜开始处已有明确景别、主体和空间锚点 | 锁定当前视频分镜最初的可生成构图状态 |
| `decisive_action` | 递出、抓住、踩住、站直、停笔、收脚、按停等动作结果 | 捕捉动作意义最清楚的一帧 |
| `reaction_frame` | 眼神变化、笑意收住、屏息、强笑、皱眉、泪光等 | 捕捉情绪判断和关系变化 |
| `prop_or_evidence_insert` | 账本、朱笔、征发牌、木屑、鱼骨、玉箫、酒碗等成为画面支配物 | 让物证、道具或材料承载叙事 |
| `environment_pressure` | 雾墙、黑岸、门窗闭合、潮线、空屋、火堆熄低等 | 让空间和天气承担压力 |
| `group_blocking` | 群像、火圈、酒舍众人、织坊女眷等空间关系是重点 | 锁定多人站位与群体反应 |

同一个上游 `分镜N` 可产生 0、1 或多个 frame landing；多个上游字段也可合并为一个 frame landing。判断标准是：这一帧是否承担独立的画面构图、主体空间、主体运动、叙事信息或视觉证据。若只是同一运镜的过渡过程且不提供新的可生成画面信息，应合并而非单独成帧。

## Connector Ignore Rule

- `## x-y-z~x-y-z` 是 `6-分组` 的组间连接件标题，不是三段式分镜组，也不映射四段式 `shot_id`。
- `8-图像/A-分镜画面` 默认完全忽略连接件：不进入 `story_beat`、`shot_detail`、`bridge_context`、英文 prompt、reference manifest、imagegen plan 或生成图片。
- 普通分镜组的抽取边界必须在下一个普通分镜组标题 `## x-y-z`、连接件标题 `## x-y-z~x-y-z` 或文件结尾前结束；连接件块本身跳过。
- 未来若需要连接件视频或连接件画面，由单独手动视频连接 skill 处理；本技能不得临时接管连接件生成。

## Extraction Fields

每个镜级条目至少提取：

| field | source | requirement |
| --- | --- | --- |
| `shot_id` | group id + frame landing serial | 四段式，稳定唯一；最后一段不是上游 `分镜N` 的直接编号 |
| `source_group_id` | `## x-y-z` | 可回指原分镜组 |
| `source_episode_path` | `6-分组/第N集.md` | 可回读 |
| `source_camera_units` | 一个或多个上游 `分镜N` / 字段名 | 只作为证据，不是 ID 真源 |
| `frame_landing_type` | landing 判断 | opening_composition / decisive_action / reaction_frame / prop_or_evidence_insert / environment_pressure / group_blocking 等 |
| `frame_landing_reason` | LLM 判断 | 为什么这个落点需要独立成帧 |
| `bridge_context` | 组内前后句 | 不读取组间连接件；只保留同组内连续性线索 |
| `story_beat` | 当前画面字段、动作、对白画面或环境描写 | 保留核心剧情桥段 |
| `shot_detail` | frame landing 消费的上游分镜明细片段 | 不机械粘贴；只保留当前落点需要的信息 |
| `characters` | 组底 YAML + 当前镜文本 | 精确主体优先 |
| `scene` | 场景标题 + 组底 YAML | 单一主场景优先 |
| `props` | 组底 YAML + 当前镜文本 | 重要叙事道具优先 |

## Bridge Context Rule

- 前后相邻的 `组间连接件` 默认不用于理解镜头开始前或结束后的视觉状态。
- 连接件不得作为当前镜头的连续性证据，不得反向改写当前分镜正文。
- prompt 只能吸收和当前镜头直接相关的桥段信息；不得把前后镜头的动作合并成同一张图。

## Evidence Gate

step1 完成后必须能生成 `shot-index.json` 或等价表格，证明：

- 每个 `shot_id` 唯一。
- 每个 `shot_id` 有源文件、源组、`source_camera_units`、`frame_landing_type` 与 `frame_landing_reason`。
- 每个 `shot_id` 有可读的剧情桥段与分镜明细摘要。
- 上游 `分镜N` 没有被直接当成镜级 ID 真源；一对多、多对一或跳过关系均已在索引中显式记录。
- 连接件块已被识别并忽略，没有生成 `shot_id` 或图片任务。
- 未能解析的组、镜头或 YAML 统计必须进入 report。
