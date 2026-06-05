# Context: AIGC 13-画布

本文件是 `13-画布` 阶段父入口经验层，不是叶子执行规范。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 12000
hard_limit_chars: 24000
status: ok
```

## Type Map

| situation | signal | handling |
| --- | --- | --- |
| 默认 LibTV 画布视频 | 用户说“根据 10-分组生成视频节点”、“创建画布项目”、“上传主体参照图” | 路由 `libTV画布流` |
| 只审查视频结果 | 用户给出 mp4 或要求审片 | 转交 `14-审片` |
| LibTV prompt 伪差异 | 多个视频节点 prompt 只替换主体名、`{{Image N}}` 或分组 ID，句架来自脚本模板 | 标记 `FAIL-CANVAS-SCRIPTED-PROMPT`，回叶子检查是否直接消费完整分镜组正文 |
| 同一分镜组重生成 | 用户说“针对已生成过的分镜组重新生成一组”或同一画布已有同组节点 | 路由 `libTV画布流`，默认创建新的 `video_node_instance_id`，不得因 `source_group_id` 已存在而跳过 |

## Repair Playbook

1. 先确认用户要“控制画布/建节点”还是“执行生成/下载/审片”。
2. 画布控制默认走 `libTV画布流`。
3. 删除远端视频节点属于破坏性操作，必须有用户明确授权。
4. 画布父级不审美主创，但仍要阻断模板化 prompt 伪差异；脚本可写映射和节点参数，不可批量生成视频 prompt 正文。
5. 同一画布同一分镜组允许多实例共存；父级只路由，不把“分镜组 ID 已存在”解释为完成。

## Reusable Heuristics

- 现行稳定做法是：本地 YAML 先显式编号 `图片N 主体名 UUID`，提交 LibTV prompt 时主体行重排为 `图片N 主体名 {{Image N}} UUID`，再让视频节点 `imageList/mixedList` 与 `图片N` 保持一致。
- 单靠 `--left-add` 不能稳定改变 LibTV 远端 `data.params.imageList`；最终必须查询远端节点参数。
- `{{Image N}}` 顺序正确只是结构 gate；若 prompt 主体不是完整分镜组正文，而是脚本用少量锚点拼出的短句，不能因为顺序正确就判完成。
- `source_group_id` 是来源锚点，`video_node_instance_id` 才是画布节点和证据文件的唯一键；重生成默认递增批次，二修默认递增修订。
