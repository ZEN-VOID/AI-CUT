# C-主体参照

`C-主体参照` 是 `8-视频` 阶段的组级主体参照视频生成入口。它从 `projects/aigc/<项目名>/5-分组` 读取分镜组原文，按组底 YAML 绑定主体参照，并以分镜组为单位调用 $libTV skill scripts。

## Directory Tree

```text
C-主体参照/
├── references/
│   ├── libtv-handoff.md
│   ├── group-source-extraction.md
│   ├── reference-slot-binding.md
│   └── video-prompt-assembly-contract.md
├── scripts/
│   └── README.md
├── templates/
│   ├── libtv-submit-plan.template.json
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── subject-reference-video-workflow.md
├── knowledge-base/
│   └── video-subject-reference-heuristics.md
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

使用 `$aigc-video-subject-reference` 处理 `projects/aigc/<项目名>/5-分组/第N集.md`，输出到：

```text
projects/aigc/<项目名>/8-视频/C-主体参照/第N集/
```

默认步骤：

1. 从 `5-分组` 提取每个分镜组完整正文和底部 YAML。
2. 按 YAML 的角色、场景、道具查找多视图或主图参照。
3. 生成 LibTV `libtv_session_with_uploaded_references` 或 `libtv_session_text_only` 提交计划，并按需批量提交。
