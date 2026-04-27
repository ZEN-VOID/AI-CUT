# comic-episode-poster

为漫画项目当前剧集生成 `comic_episode_poster_design.v1` 海报设计 JSON，并在用户要求生图时把已校验 prompt 交给 `.agents/skills/cli/imagegen`。

## Directory Tree

```text
4-剧集海报/
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
2. 按 `types/type-map.md` 选择类型包。
3. 回读 `projects/comic/<项目名>/1-漫画剧本改编/` 与 `2-九刀流漫画提示词/`。
4. 生成 `projects/comic/<项目名>/4-剧集海报/第N集-剧集海报.json`。
5. 运行：

```bash
python3 .agents/skills/comic/4-剧集海报/scripts/validate_episode_poster_json.py path/to/第N集-剧集海报.json
```

若用户要求生成海报图，先完成 JSON 校验，再加载 `.agents/skills/cli/imagegen` 执行。
