# aigc 9-图像 / 分镜画面

从 `projects/aigc/<项目名>/8-分组/` 提取普通分镜组，按每个 `## x-y-z` 的完整组稿组织 `.agents/skills/cli/imagegen` 组级多图任务：一个分镜组形成一个 group imagegen package，按组内 `分镜N` 数量生成同等数量的单独图片，并按四段式 `x-y-z-N` 持久化。

关键口径：

- 直接引用对应分镜组完整内容作为 prompt 基础。
- 多图不是故事板拼图、九宫格、contact sheet 或多 panel。
- `image_count == 组内普通 分镜N 数量`。
- YAML 中对应角色、场景、道具主体图作为参照图，多视图优先。
- 同一组多图必须保持角色、服装、场景、光影、色调、材质、空间锚点和道具一致。
- 批量出图遵循 `.agents/skills/cli/imagegen`：默认 subagents 并发，最大并发 10；用户明确要求时可主线程逐一执行。

## Directory Tree

```text
分镜画面/
├── references/
├── scripts/
├── templates/
├── review/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

```text
使用 $aigc-image-storyboard-frame，为 projects/aigc/诡校-测试版/8-分组/第1集.md 的 1-1-1 分镜组生成 imagegen 多图 prompt，并按组内分镜数生成多张单独分镜画面。
```

输出根路径固定为：

```text
projects/aigc/<项目名>/9-图像/分镜画面
```
