# 2-Planning Legacy References Note

`2-Planning/references/*` 已在本轮重构中退役。

当前 canonical 结构：

| 旧模块 | 新子技能包 | 本地模板 |
| --- | --- | --- |
| `genre-selection` | [`../1-题材选型/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/1-题材选型/SKILL.md) | [`../1-题材选型/templates/genre-selection.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/1-题材选型/templates/genre-selection.template.json) |
| `chapter-planning` | [`../2-章节规划/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/2-章节规划/SKILL.md) | [`../2-章节规划/templates/chapter-planning.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/2-章节规划/templates/chapter-planning.template.json) |
| `story-outline` | [`../3-故事大纲/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/3-故事大纲/SKILL.md) | [`../3-故事大纲/templates/story-outline.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/3-故事大纲/templates/story-outline.template.json) |
| `conflict-design` | [`../4-冲突设计/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/4-冲突设计/SKILL.md) | [`../4-冲突设计/templates/conflict-design.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/4-冲突设计/templates/conflict-design.template.json) |
| `mission-design` | [`../5-任务设计/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/5-任务设计/SKILL.md) | [`../5-任务设计/templates/mission-design.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/5-任务设计/templates/mission-design.template.json) |
| `clue-design` | [`../6-线索设计/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/6-线索设计/SKILL.md) | [`../6-线索设计/templates/clue-design.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/6-线索设计/templates/clue-design.template.json) |
| `foreshadow-design` | [`../7-伏笔设计/SKILL.md`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/7-伏笔设计/SKILL.md) | [`../7-伏笔设计/templates/foreshadow-design.template.json`](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/story/2-Planning/7-伏笔设计/templates/foreshadow-design.template.json) |

`Planning/全息地图.json` 不再对应独立子技能。

它是 `1-7` 子技能串行 progressive commit 后，自然长出的 shared story_map root；父层只负责 normalize / validate。
