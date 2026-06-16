# aigc 2-美学/场景风格

`场景风格` 负责为 AIGC 影片项目提取场景层级视觉协议，研究空间尺度/秩序、空间光影、色彩/明度纪律、氛围介质/粒子层、生态/人工系统组织、环境层次、时代质地和场景视觉统一性。它不写具体场景清单、地点设计、单镜头构图或生成请求。

## Directory Tree

```text
场景风格/
├── agents/openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/1-分集/`、项目设定、`2-美学/画面基调/全局风格协议.md`、用户文本、参考图或参考视频。
- 输出：单集任务写入 `projects/aigc/<项目名>/2-美学/第N集/场景风格/场景风格协议.md`；整季/项目基线写入 `projects/aigc/<项目名>/2-美学/场景风格/场景风格协议.md`。
- 报告：正式写回时在同一输出目录同步生成 `执行报告.md`。
- 默认 prompt：中文约 100 字，禁止具体地点、场景清单、构图摄影、运镜、生成请求和单图参数污染。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `agents/openai.yaml` 只提供产品入口元数据。
- `test-prompts.json` 用于 dry-run、审计或回归验证。
- 核心场景风格判断和提示词蒸馏由 LLM 完成，脚本只做机械辅助。
