# Context: aigc 12-图像

本文件是 `12-图像` 父级入口的经验层知识库。调用同目录 `SKILL.md` 时必须同时加载本文件。

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
| frame image | 用户要单镜生图 prompt、四段式分镜 ID、或每组多张单独分镜画面 | 路由到 `分镜画面` |
| storyboard sheet | 用户要组级多格故事板、拼图、contact sheet 或多 panel 画面 | 路由到 `分镜故事板`，缺失时报告未配置 |
| video reference | 用户要视频首帧、运动或连续性参照 | 转入视频阶段 |
| legacy grouping test | 用户允许旧版分组稿测试 | 可读取 `5-分组`，但报告必须标记 legacy adapter，不得冒充新版 `10-分组` canonical |
| aspect ratio default | 用户未指定画面比例 | 父级传递或审查 `aspect_ratio=16:9`；只有显式要求才写 override |
| multi-image contact sheet | 分镜画面路线的一次多图返回单张网格/contact sheet | 标记 `FAIL-IMG-STAGE-MULTI-IMAGE-SHAPE`，不得判成功；转 provider handoff 修复或明确 fallback 只是拓扑例外 |

## Repair Playbook

1. 先判断用户要的是单镜画面、故事板，还是视频参照。
2. 父级只做路由，不直接生成 prompt 正文。
3. 若叶子技能缺失，报告配置缺口，不临时伪造叶子合同。
4. 当前 `.agents` 叶子目录是 `分镜画面/` 与 `分镜故事板/`；`A-分镜画面` / `B-分镜故事板` 仅作为业务路线名或项目输出目录名使用。
5. 未指定比例时默认 `16:9`；用户显式要求 `9:16`、`1:1` 或其他比例时才向叶子传 `aspect_ratio_override`。
6. 若用户要求实际生图，先确认 provider 能返回多张单独文件。内置多图若返回 contact sheet，不满足 `分镜画面` 路线，不能因为视觉上包含多个画面就判通过。

## Reusable Heuristics

- “分镜画面”通常是镜级单帧或分镜组内多张单独图，应走 `分镜画面`。
- “分镜故事板”“多格 storyboard”“contact sheet”通常是组级板，应走 `分镜故事板`。
- 图像阶段与视频阶段的分界在是否需要运动、首尾帧或时序连续性。
- `## x-y-z~x-y-z` 连接件默认不属于 `12-图像` 的生图范围；遇到连接件时跳过，不生成连接件单帧、故事板或参照图。
- 2026-06-04 实测：对 `projects/aigc/TMBR/5-分组/第1集.md` 的 `1-1-1` 组使用完整组级多图 prompt，内置图像工具返回一张 8 宫格/contact sheet，而不是 8 张独立图片；随后逐张 fallback 生成了 8 张可用 16:9 单图。该结果证明父级必须区分“可用图片结果”和“合格的一次多图拓扑”，不能把 fallback 当作叶子目标完全通过。
- 本次实测产物落在 `reports/aigc-frame-image-dry-run-20260604/TMBR-第1集-1-1-1/`：`failed/multi-image-contact-sheet-failed.png` 是失败证据，`images/1-1-1-1.png` 到 `images/1-1-1-8.png` 是单图 fallback 结果。
