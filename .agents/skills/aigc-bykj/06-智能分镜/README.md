# 06-智能分镜

`06-智能分镜` 是 BYKJ AIGC 工作流的 JSON-first 分镜阶段。它整合原 AIGC `5-摄影` 的镜头/摄影细部模块，以及 `6-分组` 的生产分组、定场镜头、组间连接件和统计模块。

注意：本阶段同步原 AIGC `6-分组` 的输出规则，不同步旧输出路径。canonical 输出仍为 `output/[项目名]/06-智能分镜/`，但 group、bridge、statistics 的内容字段、顺序约束、禁止项、计数边界和 review 口径必须与原 `6-分组` 等价。

## Canonical Input

优先读取：

- `output/[项目名]/03-智能分集/`
- `output/[项目名]/04R-全局优化/`，不存在时回退 `04-全局预设/`
- `output/[项目名]/05R-资产优化/`，不存在时回退 `05-资产提取/`

## Canonical Output

`output/[项目名]/06-智能分镜/`

主要输出：

- `分镜总表.json`
- `镜头列表.json`
- `生产组索引.json`
- `桥接连接件.json`
- `分镜报告.json`
- `manifest.json`

按需输出：

- `episodes/storyboard-episode-N.json`
- `frames/frame-index.json`
- `conflict-decision-request.json`

## Boundary

- 不写回旧 `projects/aigc/<项目名>/5-摄影/` 或 `6-分组/`。
- 不简化原 `6-分组` 的 group/bridge/statistics 规则；JSON 字段必须完整承载原规则。
- 不改写剧情、对白、场景顺序。
- 不新增没有上游证据的角色、场景、道具。
- 不直接生成图片或视频。
- 脚本只做机械校验和落盘辅助，分镜与连接件主创必须由 LLM 完成。

## Files

```text
06-智能分镜/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```
