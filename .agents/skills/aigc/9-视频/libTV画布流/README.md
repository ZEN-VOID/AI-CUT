# AIGC 9-视频 / libTV画布流

## 目录树

```text
libTV画布流/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## 快速说明

- 默认路线：主体参照流。
- 输入真源：`projects/aigc/<项目名>/6-分组/第N集.md`。
- 主体绑定：使用 `主体绑定表` 固定 `yaml_name -> node_key -> URL`。
- 调用层：通过本技能 `.env` wrapper 转调用 `.agents/skills/cli/libTV` 官方脚本，不改官方逻辑。
- 证据链：项目级 active registry + 组级 manifest / submit plan / queue record / 执行报告。
- 交付策略：生成物默认沉淀在 LibTV 画布；显式要求时才下载。

## 快速入口

```text
使用 $aigc-video-libtv-canvas-flow，为 projects/aigc/<项目名>/6-分组/第N集.md 生成 LibTV 画布视频任务。
```
