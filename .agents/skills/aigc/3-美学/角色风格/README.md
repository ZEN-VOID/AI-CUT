# aigc 3-美学/角色风格

`角色风格` 负责为 AIGC 影片项目确立角色层视觉风格协议，覆盖形象、气质、妆容、发型、服装结构、体态、年龄质感和表演外观边界。它只处理角色视觉风格层级，不写具体角色卡、具体人物姓名、剧情动作、场景或镜头。

## Directory Tree

```text
角色风格/
├── agents/openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/2-编剧/第N集.md`、整季 `2-编剧/`、`3-美学/画面基调/全局风格协议.md`、项目设定、用户文本、参考图或参考视频。
- 输出：单集任务写入 `projects/aigc/<项目名>/3-美学/第N集/角色风格/角色风格协议.md`；整季/项目基线写入 `projects/aigc/<项目名>/3-美学/角色风格/角色风格协议.md`。
- 报告：正式写回时在同一输出目录同步生成 `执行报告.md`。
- 默认 prompt：中文约 100 字，允许 80-130 字；禁止具体角色卡、姓名、剧情动作、场景、镜头和参考人物复制。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `agents/openai.yaml` 只提供产品入口元数据。
- `test-prompts.json` 用于 dry-run、审计或回归验证。
- 核心角色审美判断和提示词蒸馏由 LLM 完成，脚本只做机械辅助。
