# aigc 3-美学/分镜风格

`分镜风格` 负责为 AIGC 影片项目制定分镜层级的节奏、景别流转、镜头组合、连接语法、信息密度和 AI 视频下游可执行边界。它只处理分镜组织风格，不写具体分镜正文、镜头编号、剧情动作、资产设计或摄影参数。

## Directory Tree

```text
分镜风格/
├── agents/openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/2-编剧/第N集.md`、整季 `2-编剧/`、`3-美学/画面基调/全局风格协议.md`、摄影风格协议、用户文本、参考图或参考视频。
- 输出：`projects/aigc/<项目名>/3-美学/分镜风格/分镜风格协议.md`。
- 报告：正式写回时同步生成 `projects/aigc/<项目名>/3-美学/分镜风格/执行报告.md`。
- 默认 prompt：中文 80-130 字，约 100 字；禁止具体分镜正文、镜头编号、剧情动作、资产设计、摄影参数和参考内容照搬。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `agents/openai.yaml` 只提供产品入口元数据。
- `test-prompts.json` 用于 dry-run、审计或回归验证。
- 核心分镜组织判断和提示词蒸馏由 LLM 完成，脚本只做机械辅助。
