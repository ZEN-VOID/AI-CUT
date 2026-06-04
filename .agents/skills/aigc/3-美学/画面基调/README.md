# aigc 3-美学/画面基调

`画面基调` 负责为 AIGC 影片项目确立全局视觉媒介、渲染管线、美学范式、大师参照和可继承风格提示词。它只处理底层风格协议，不写角色、场景、道具、构图、焦段、运镜或具体画面内容。

## Directory Tree

```text
画面基调/
├── agents/openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/2-编剧/第N集.md`、整季 `2-编剧/`、项目设定、用户文本、参考图或参考视频。
- 输出：`projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md`。
- 报告：正式写回时同步生成 `projects/aigc/<项目名>/3-美学/画面基调/执行报告.md`。
- 默认 prompt：中文 200-300 字，禁止具体颜色、材质、构图、摄影/运镜和具象内容污染。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `agents/openai.yaml` 只提供产品入口元数据。
- `test-prompts.json` 用于 dry-run、审计或回归验证。
- 核心审美判断和提示词蒸馏由 LLM 完成，脚本只做机械辅助。
