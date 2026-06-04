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

## Repair Playbook

1. 先确认用户要“控制画布/建节点”还是“执行生成/下载/审片”。
2. 画布控制默认走 `libTV画布流`。
3. 删除远端视频节点属于破坏性操作，必须有用户明确授权。

## Reusable Heuristics

- 现行稳定做法是：本地 YAML 先显式编号 `图片N 主体名 UUID`，再让视频节点 `imageList/mixedList` 与 `图片N` 保持一致。
- 单靠 `--left-add` 不能稳定改变 LibTV 远端 `data.params.imageList`；最终必须查询远端节点参数。
