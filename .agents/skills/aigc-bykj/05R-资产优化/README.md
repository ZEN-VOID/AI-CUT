# 05R-资产优化

`05R-资产优化` 承接 `05-资产提取` 的 JSON 资产产物，对角色、场景、道具及其 `design_spec` 做自然语言驱动的二次优化、schema 修复、跨资产一致性修复和 prompt 约束修复。

## Canonical Input

`output/[项目名]/05-资产提取/`

优先读取：

1. `manifest.json`
2. `资产清单.json`
3. `角色提取/角色清单.json`
4. `场景提取/场景清单.json`
5. `道具提取/道具清单.json`
6. `*提取报告.json`

## Canonical Output

`output/[项目名]/05R-资产优化/`

主要输出：

- `资产优化补丁.json`
- `资产优化报告.json`
- `manifest.json`

按需输出：

- `optimized-资产清单.json`
- `characters.optimized.json`
- `scenes.optimized.json`
- `props.optimized.json`
- `conflict-decision-request.json`

## Boundary

- 不重新执行 `05-资产提取`。
- 不新增没有 `05` 或 `02` 证据的角色、场景、道具。
- 不改写 `02` 剧本事实。
- 不生成图片、分镜或视频任务。
- 不默认写入旧 AIGC 7-设计 Markdown runtime。

## Files

```text
05R-资产优化/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```
