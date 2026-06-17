# aigc 9-光影

> 退役备份：本目录仅保留旧 AIGC 独立光影链路的审计和追溯价值，不再作为正式 `projects/aigc/<项目名>/9-光影/` 生成阶段。可复用核心已收束到 `.agents/skills/aigc/7-摄影/references/cinematic-light-in-camera-contract.md`，作为摄影观看纪律进入 `camera_light_plan`、`lighting_design_type_map`、`shadow_design_map`、`narrative_light_function_map`、`camera_light_alignment_map` 和 `light_continuity_map`。

正式光影强化不再以光源、受光、色温和介质观察为主轴；应优先落到布光类型/光型、阴影组织、叙事美学功能和主体可读性控制，光源可信只作为 source motivation boundary。

`9-光影` 将 `projects/aigc/<项目名>/7-摄影/第N集.md` 或用户指定分镜/摄影稿升级为逐分镜电影光影美学稿。

## Directory Tree

```text
9-光影/
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── README.md
├── references/
│   ├── aesthetic-light-inheritance-contract.md
│   ├── ai-video-light-handoff-contract.md
│   ├── cinematic-light-language-contract.md
│   ├── dynamic-light-source-contract.md
│   ├── light-continuity-contract.md
│   └── source-incremental-light-injection-contract.md
├── knowledge-base/
│   ├── aigc-video-lighting-vocabulary.md
│   └── cinematic-lighting-top10.md
└── scripts/
    └── README.md
```

## Runtime

- 默认 source：`projects/aigc/<项目名>/7-摄影/第N集.md`
- 指定 source：用户显式指定文稿或粘贴文本时优先
- 必读上下文：`2-美学/画面基调/全局风格协议.md`、当前集优先的 `2-美学/第N集/场景风格/场景风格协议.md` 与 `2-美学/第N集/摄影风格/摄影风格协议.md`，缺失时回退项目级对应风格协议
- 默认工具标准：未指定其他下游视频工具时，以 `Seedance 2.0` 作为 AIGC 光影可实现性与稳定性审查标尺
- 输出：`projects/aigc/<项目名>/9-光影/第N集.md`
- 报告：`projects/aigc/<项目名>/9-光影/执行报告.md`

## Output Shape

```text
分镜1（N-N秒）：原有内容（包含摄影）。光影美学描述。
分镜2（N-N秒）：原有内容（包含摄影）。光影美学描述。
```

只追加光影句，不改原分镜、摄影、剧情、对白、秒数或编号。
