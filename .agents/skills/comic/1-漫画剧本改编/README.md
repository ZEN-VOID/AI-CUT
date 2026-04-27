# 漫画剧本改编

`comic-script-adaptation` 把文本、图片、视频、新闻或热搜素材改编为按组落盘的漫画剧本真源，供 `2-九刀流漫画提示词` 逐组消费。

## Directory Tree

```text
1-漫画剧本改编/
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

1. 读取 `SKILL.md + CONTEXT.md`。
2. 读取 `types/type-map.md` 并加载命中的来源、改编姿态和输出模式类型包。
3. 按 `steps/adaptation-workflow.md` 完成来源归一、事实边界、剧情发动机、分组、正文与验收。
4. 若素材含对白、旁白、音效、系统提示或规则文字，叠加 `types/projection/directing-field-bridge.md`，并读取 `references/directing-field-projection-bridge.md`。
5. 使用 `templates/grouped-manga-script.template.md` 或 `templates/output-template.md` 组织交付。
6. 运行 validator：

```bash
python3 .agents/skills/comic/1-漫画剧本改编/scripts/validate_grouped_manga_script.py <第N组.md>
python3 .agents/skills/comic/1-漫画剧本改编/scripts/validate_grouped_manga_script.py <stage-1-output-dir>
```

## Output

默认落点：

```text
projects/comic/<项目名>/1-漫画剧本改编/第N组.md
```

`第N组.md` 是唯一 canonical creative truth；不得再用整篇 prose、桥接包或 JSON 与它竞争主真源。
