# aigc 3-美学/摄影风格

`摄影风格` 负责为 AIGC 影片项目确立构图秩序、景别体系、机位关系、镜头运动、运动连招、镜头连续性和可继承摄影提示词。它只处理摄影层协议，不写剧情、角色、道具、场景设计或单镜头正文。

## Directory Tree

```text
摄影风格/
├── agents/openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/2-编剧/第N集.md`、整季 `2-编剧/`、`3-美学/画面基调/全局风格协议.md`、项目设定、用户文本、参考图或参考视频。
- 输出：`projects/aigc/<项目名>/3-美学/摄影风格/摄影风格协议.md`。
- 报告：正式写回时同步生成 `projects/aigc/<项目名>/3-美学/摄影风格/执行报告.md`。
- 默认 prompt：中文约 100 字，禁止剧情、角色、道具、场景和单镜头正文污染。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `agents/openai.yaml` 只提供产品入口元数据。
- `test-prompts.json` 用于 dry-run、审计或回归验证。
- 核心摄影判断和提示词蒸馏由 LLM 完成，脚本只做机械辅助。
