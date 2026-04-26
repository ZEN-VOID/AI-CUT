# photoGPT

`photoGPT` 是 imagegen 专属的多模板提示词强化器：先判定图像编辑类型和子类型，再读取对应模板，把用户指令转为可执行 prompt plan，并交给 `.agents/skills/cli/imagegen` 执行。

## Directory Tree

```text
photoGPT/
├── references/
│   └── prompt-enhancement-contract.md
├── scripts/
│   └── README.md
├── templates/
│   ├── output-template.md.template
│   ├── 多视图/
│   │   ├── README.md
│   │   ├── 场景/TEMPLATE.md
│   │   ├── 道具/TEMPLATE.md
│   │   ├── 服装/TEMPLATE.md
│   │   └── 角色/TEMPLATE.md
│   ├── 多图融合/
│   │   ├── README.md
│   │   ├── 电商广告/TEMPLATE.md
│   │   └── 分镜构图/TEMPLATE.md
│   ├── 风格化/
│   │   ├── README.md
│   │   ├── 风格迁移/TEMPLATE.md
│   │   └── 滤镜/TEMPLATE.md
│   ├── 修图/
│   │   ├── README.md
│   │   ├── 高清/TEMPLATE.md
│   │   └── 美颜美体/TEMPLATE.md
│   └── 元素替换/
│       ├── README.md
│       ├── 换背景/TEMPLATE.md
│       ├── 换角色/TEMPLATE.md
│       ├── 换脸/TEMPLATE.md
│       └── 换装/TEMPLATE.md
├── review/
│   └── review-contract.md
├── steps/
│   └── execution-workflow.md
├── knowledge-base/
│   └── photoGPT-heuristics.md
├── types/
│   └── type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

1. 读取 `SKILL.md + CONTEXT.md`。
2. 读取 `types/type-map.md` 判定 `edit_family` / `edit_subtype`。
3. 读取对应 `templates/<类型>/<子类型>/TEMPLATE.md` 和 `references/prompt-enhancement-contract.md`。
4. 输出 prompt plan；若输入齐备，调用 `.agents/skills/cli/imagegen`。

## Supported Families

- `多视图`: 场景、道具、服装、角色
- `多图融合`: 电商广告、分镜构图
- `风格化`: 风格迁移、滤镜
- `修图`: 高清、美颜美体
- `元素替换`: 换背景、换角色、换脸、换装
