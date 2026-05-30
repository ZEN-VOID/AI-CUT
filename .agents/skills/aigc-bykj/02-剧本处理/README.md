# 02-剧本处理

BYKJ AIGC 工作流的整合型剧本处理阶段。

## Purpose

本阶段把用户指定的任意小说或剧本处理为一份同时具备编剧、导演、表演能力的 canonical 稿件。

核心输出固定为：

```text
output/[项目名]/02-剧本处理/
├── 剧本处理稿.json
├── 执行报告.json
└── manifest.json
```

批量模式可额外生成：

```text
output/[项目名]/02-剧本处理/episodes/第N集.json
```

## Files

- `SKILL.md`：唯一执行真源，承载输入、流程、字段、门禁、输出合同。
- `CONTEXT.md`：经验层，记录失效模式和修复启发。
- `agents/openai.yaml`：产品侧入口元数据。

## Boundary

本阶段吸收 `aigc/2-编剧`、`aigc/3-导演`、`aigc/4-表演` 的核心能力，但不继承三套分阶段输出目录。所有 BYKJ `02` canonical 输出只落在 `output/[项目名]/02-剧本处理/`。
