# aigc 12-图像 / A-分镜画面

从 `projects/aigc/<项目名>/10-分组/` 提取普通分镜组，按每个 `## x-y-z` 的完整组稿组织 GPT-IMAGE-2 组级多图任务：一个分镜组一次调用，生成组内 `分镜N` 数量相同的多张单独图片，并按四段式 `x-y-z-N` 持久化。

关键口径：

- 直接引用对应分镜组完整内容作为 prompt 基础。
- 多图不是故事板拼图、九宫格、contact sheet 或多 panel。
- `image_count == 组内普通 分镜N 数量`。
- YAML 中对应角色、场景、道具主体图作为参照图，多视图优先。
- 同一组多图必须保持角色、服装、场景、光影、色调、材质、空间锚点和道具一致。
- 若 provider 单次多图上限不足，默认阻断并报告，不静默拆组。

## Directory Tree

```text
A-分镜画面/
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
使用 $aigc-image-storyboard-frame，为 projects/aigc/诡校-测试版/10-分组/第1集.md 的 1-1-1 分镜组生成 GPT-IMAGE-2 多图 prompt，并按组内分镜数一次生成多张单独分镜画面。
```

输出根路径固定为：

```text
projects/aigc/<项目名>/12-图像/A-分镜画面
```
