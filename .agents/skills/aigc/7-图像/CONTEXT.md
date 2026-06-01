# Context: aigc 7-图像

本文件是 `7-图像` 父级入口的经验层知识库。调用同目录 `SKILL.md` 时必须同时加载本文件。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 12000
hard_limit_chars: 24000
status: ok
last_checked_at: 2026-04-26
```

## Type Map

| type | symptom | repair |
| --- | --- | --- |
| frame image | 用户要单镜生图 prompt 或四段式分镜 ID | 路由到 `A-分镜画面` |
| storyboard sheet | 用户要组级多格故事板 | 路由到 `B-分镜故事板`，缺失时报告未配置 |
| video reference | 用户要视频首帧、运动或连续性参照 | 转入视频阶段 |

## Repair Playbook

1. 先判断用户要的是单镜画面、故事板，还是视频参照。
2. 父级只做路由，不直接生成 prompt 正文。
3. 若叶子技能缺失，报告配置缺口，不临时伪造叶子合同。

## Reusable Heuristics

- “分镜画面”通常是镜级单帧，应走 `A-分镜画面`。
- “分镜故事板”“多格 storyboard”通常是组级板，应走 `B-分镜故事板`。
- 图像阶段与视频阶段的分界在是否需要运动、首尾帧或时序连续性。
- `## x-y-z~x-y-z` 连接件默认不属于 `7-图像` 的生图范围；遇到连接件时跳过，不生成连接件单帧、故事板或参照图。
