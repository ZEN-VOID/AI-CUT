# aigc flash

`flash` 是 `.agents/skills/aigc` 的聊天窗口 mini prompt 技能。它把一个短故事源、分镜组、参照图、参照视频或首尾帧任务，快速压缩串联 AIGC `2-编剧` 到 `10-分组` 的核心判断，只在当前聊天窗口输出统一视频提示词。

## Directory Tree

```text
flash/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

1. 加载 `SKILL.md + CONTEXT.md`。
2. 锁定输入类型：文字故事、图生视频、首尾帧、参考视频、混合参照、prompt repair 或 review。
3. 默认目标时长为 `11.5秒`，用户指定时长优先。
4. 多模态任务先做证据分级，再写 prompt；不可见素材不得强推断。
5. 输出唯一 `Flash Prompt Pack` 到当前聊天窗口。

## Boundary

- 不保存文档。
- 不写项目 canonical 文件。
- 不执行正式 2-10 阶段。
- 不调用视频或图像 provider。
- 不复制参考素材具体表达。
