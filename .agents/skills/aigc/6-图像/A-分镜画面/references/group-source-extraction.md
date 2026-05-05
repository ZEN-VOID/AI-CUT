# Group Source Extraction Contract

本文件定义 step1：以 `projects/aigc/<项目名>/4-分组` 为主要信息来源，获取每个分镜内容，并理清其关联剧情桥段信息。

## Source Priority

1. `projects/aigc/<项目名>/4-分组/第N集.md` 是镜级 prompt 的剧情与镜头主要真源。
2. `projects/aigc/<项目名>/0-初始化/north_star.yaml` 只提供风格直引，不替代分镜内容。
3. `5-设计/*/3-生成` 只提供主体参照候选，不改写剧情。
4. `3-摄影` 仅在用户要求上溯修复 `4-分组` 时读取。

## Shot ID Mapping

`4-分组` 中的标题 `## x-y-z` 表示三段式分镜组 ID：

- `x`: episode number
- `y`: scene number
- `z`: group number inside the scene

组内每个 `分镜N` 映射为四段式镜级 ID：

```text
x-y-z-N
```

例如 `## 1-1-1` 中的 `分镜2` 映射为 `1-1-1-2`。

## Connector Ignore Rule

- `## x-y-z~x-y-z` 是 `4-分组` 的组间连接件标题，不是三段式分镜组，也不映射四段式 `shot_id`。
- `6-图像/A-分镜画面` 默认完全忽略连接件：不进入 `story_beat`、`shot_detail`、`bridge_context`、英文 prompt、reference manifest、imagegen plan 或生成图片。
- 普通分镜组的抽取边界必须在下一个普通分镜组标题 `## x-y-z`、连接件标题 `## x-y-z~x-y-z` 或文件结尾前结束；连接件块本身跳过。
- 未来若需要连接件视频或连接件画面，由单独手动视频连接 skill 处理；本技能不得临时接管连接件生成。

## Extraction Fields

每个镜级条目至少提取：

| field | source | requirement |
| --- | --- | --- |
| `shot_id` | group id + `分镜N` | 四段式，稳定唯一 |
| `source_group_id` | `## x-y-z` | 可回指原分镜组 |
| `source_episode_path` | `4-分组/第N集.md` | 可回读 |
| `bridge_context` | 组内前后句 | 不读取组间连接件；只保留同组内连续性线索 |
| `story_beat` | 当前画面字段、动作、对白画面或环境描写 | 保留核心剧情桥段 |
| `shot_detail` | 当前 `分镜N` 对应分镜明细 | 不改写，可压缩为 prompt 所需信息 |
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
- 每个 `shot_id` 有源文件、源组、源 `分镜N`。
- 每个 `shot_id` 有可读的剧情桥段与分镜明细摘要。
- 连接件块已被识别并忽略，没有生成 `shot_id` 或图片任务。
- 未能解析的组、镜头或 YAML 统计必须进入 report。
