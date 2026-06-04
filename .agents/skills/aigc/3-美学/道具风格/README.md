# aigc 3-美学/道具风格

`道具风格` 负责为 AIGC 影片项目确立道具层面的视觉风格协议。它从剧本、画面基调、参考图/视频和项目资料中提取文化元素、形制、质感、材料倾向、工艺痕迹、使用痕迹、尺度语言、符号系统和制作边界。

它只处理道具视觉风格层级，不写具体道具清单、剧情用途、单个物件设定或生成请求。

## Directory Tree

```text
道具风格/
├── agents/openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/2-编剧/第N集.md`、整季 `2-编剧/`、`3-美学/画面基调/全局风格协议.md`、项目设定、用户文本、参考图或参考视频。
- 输出：`projects/aigc/<项目名>/3-美学/道具风格/道具风格协议.md`。
- 报告：正式写回时同步生成 `projects/aigc/<项目名>/3-美学/道具风格/执行报告.md`。
- 默认 prompt：中文约 100 字，禁止具体道具清单、剧情用途、单件设定、生成请求和参考照搬污染。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `agents/openai.yaml` 只提供产品入口元数据。
- `test-prompts.json` 用于 dry-run、审计或回归验证。
- 核心审美判断、文化研究和提示词蒸馏由 LLM 完成，脚本只做机械辅助。
