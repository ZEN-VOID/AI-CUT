# photoGPT

`photoGPT` 是 `gpt-image-2` 专属的多模板提示词强化器：先判定图像编辑类型和子类型，再读取对应模板，把用户指令转为可执行 prompt plan，并交给 `.agents/skills/cli/imagegen` 的 `gpt-image-2` 路径执行。

## Directory Tree

```text
photoGPT/
├── references/
│   └── prompt-enhancement-contract.md
├── scripts/
│   └── README.md
├── templates/
│   ├── output-template.json
│   ├── 多视图/
│   │   ├── README.md
│   │   ├── 场景/TEMPLATE.json
│   │   ├── 道具/TEMPLATE.json
│   │   ├── 服装/TEMPLATE.json
│   │   └── 角色/TEMPLATE.json
│   ├── 多镜头/
│   │   ├── README.md
│   │   └── 九宫格/TEMPLATE.json
│   ├── 多图融合/
│   │   ├── README.md
│   │   ├── 电商广告/TEMPLATE.json
│   │   └── 分镜构图/TEMPLATE.json
│   ├── 风格化/
│   │   ├── README.md
│   │   ├── 风格迁移/TEMPLATE.json
│   │   └── 滤镜/TEMPLATE.json
│   ├── 修图/
│   │   ├── README.md
│   │   ├── 高清/TEMPLATE.json
│   │   └── 美颜美体/TEMPLATE.json
│   └── 元素替换/
│       ├── README.md
│       ├── 换背景/TEMPLATE.json
│       ├── 换角色/TEMPLATE.json
│       ├── 换脸/TEMPLATE.json
│       └── 换装/TEMPLATE.json
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── photoGPT-heuristics.md
├── types/
│   └── type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

1. 读取 `SKILL.md + CONTEXT.md`。
2. 读取 `types/type-map.md` 判定 `edit_family` / `edit_subtype`。
3. 读取对应 `templates/<类型>/<子类型>/TEMPLATE.json` 和 `references/prompt-enhancement-contract.md`。
4. 由 LLM 直接生成 prompt plan；脚本只能校验、保存或转发。
5. 若输入齐备，只调用 `.agents/skills/cli/imagegen` 的 `gpt-image-2` 路径；否则输出 prompt-only / blocked。

## Runtime Spine

- `SKILL.md` 是唯一执行主合同，包含业务画像、类型路由、节点表、Mermaid 拓扑、模块授权、触发表、汇流门、注意力协议、检查点和输出合同。
- `types/`、`templates/`、`references/`、`review/`、`scripts/` 和 `knowledge-base/` 只在 `SKILL.md` 授权时参与执行，不维护第二节点真源。
- 本包不再使用 `steps/`；旧 workflow 节点已迁回 `SKILL.md`。

## Supported Families

- `多视图`: 场景、道具、服装、角色
- `多镜头`: 九宫格
- `多图融合`: 电商广告、分镜构图
- `风格化`: 风格迁移、滤镜
- `修图`: 高清、美颜美体
- `元素替换`: 换背景、换角色、换脸、换装
