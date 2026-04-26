# aigc 6-图像 / A-分镜画面

从 `projects/aigc/<项目名>/4-分组/` 提取镜级分镜，生成四段式 `分镜ID` 的英文生图 prompt，绑定 `5-设计/*/3-生成` 中的主体图片，并按需调用 `.agents/skills/cli/imagegen` 批量生成分镜画面。

## Directory Tree

```text
A-分镜画面/
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
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

```text
使用 $aigc-image-storyboard-frame，为 projects/aigc/诡校-测试版/4-分组/第1集.md 生成第1集全部分镜画面 prompt，并绑定已有角色、场景、道具参照图。
```

输出根路径固定为：

```text
projects/aigc/[项目名]/6-图像/A-分镜画面
```

逐集产物可在该根路径下使用 `第N集/` 子目录组织。
