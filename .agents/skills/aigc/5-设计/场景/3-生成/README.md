# aigc-scene-generation

Skill 2.0 package for `aigc/5-设计/场景/3-生成`.

## Purpose

`$aigc-scene-generation` consumes upstream scene design documents from:

```text
projects/aigc/<项目名>/5-设计/场景/2-设计/
```

It generates:

- `主体名称-主图` image and prompt JSON.
- `主体名称-多视图` image and prompt JSON.

The skill only calls `$imagegen` from existing design documents. It does not redesign scene subjects or modify upstream design files.

## Directory Tree

```text
3-生成/
├── references/
│   └── scene-generation-contract.md
├── scripts/
│   └── README.md
├── templates/
│   ├── output-template.md
│   ├── scene-main-image-prompt.json
│   └── scene-multiview-prompt.json
├── review/
│   └── review-contract.md
├── steps/
│   └── scene-generation-workflow.md
├── knowledge-base/
│   └── scene-generation-heuristics.md
├── types/
│   └── scene-generation-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

Use `$aigc-scene-generation` with a project path and one or more upstream scene design documents.

Required runtime output path:

```text
projects/aigc/<项目名>/5-设计/场景/3-生成/
```

Default flow:

1. Generate `主体名称-主图` from the upstream design prompt.
2. Generate `主体名称-多视图` from the multi-view template, using the main image as reference.
3. Persist each image and same-name JSON prompt record under the project output path.

## Visual / Review Anchors

- `SKILL.md` contains the top-level Mermaid routing maps required by the Skill 2.0 workshop contract.
- `steps/scene-generation-workflow.md` owns the detailed node graph, sequence diagram, branch matrix and failure loop.
- `review/review-contract.md` owns reviewer dispatch, local downgrade fields and the final verdict schema.
