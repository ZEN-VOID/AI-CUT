# 06R-分镜优化

`06R-分镜优化` 承接 `06-智能分镜` 的 JSON 产物，对 frame、group、bridge、原 `6-分组` 规则同步、资产/风格引用、生成 payload 和 schema/index 做自然语言驱动的二次优化与修复。

## Canonical Input

`output/[项目名]/06-智能分镜/`

优先读取：

1. `manifest.json`
2. `分镜总表.json`
3. `镜头列表.json`
4. `生产组索引.json`
5. `桥接连接件.json`
6. `分镜报告.json`
7. `episodes/`
8. `frames/`

## Canonical Output

`output/[项目名]/06R-分镜优化/`

主要输出：

- `分镜优化补丁.json`
- `分镜优化报告.json`
- `manifest.json`

按需输出：

- `storyboard.optimized.json`
- `shot-list.optimized.json`
- `group-index.optimized.json`
- `bridge-connectors.optimized.json`
- `conflict-decision-request.json`

## Boundary

- 不重新执行 `06-智能分镜`。
- 不改写 `03` 剧情、对白或场景顺序。
- 不新增没有 `03/04/05/06` 证据的角色、场景、道具或风格事实。
- 不简化原 `6-分组` 的 group/bridge/statistics 规则。
- 不直接生成图片或视频。
- 脚本只做机械校验和落盘辅助，分镜优化判断必须由 LLM 完成。

## Files

```text
06R-分镜优化/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```
