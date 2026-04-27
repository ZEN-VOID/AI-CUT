# 九刀流漫画提示词输出模板

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 每个 page-group 一份 `nine_blade_comic_prompts.v1` JSON，必要时附同名前缀思考摘要 |
| Output format | JSON 根对象字段按 `templates/nine-blade-comic-prompts.schema.json` 与本模板骨架填写 |
| Output path | 单集写入 `projects/comic/[项目名]/2-九刀流漫画提示词/page-group-XX-nine_blade_comic_prompts.json`；多集写入 `第N集-page-group-XX-nine_blade_comic_prompts.json` |
| Naming convention | group 使用两位序号；多集加 `第N集-` 前缀；schema/任务 ID 保持 ASCII 安全 |
| Completion gate | JSON 校验脚本通过，人工 review 确认非拼图、非变体、9 页多格、continuity 和页码正确 |

## JSON Skeleton

优先复制 `templates/nine-blade-template.json`，再由 LLM 填写具体创作内容。最小根字段：

```json
{
  "schema_version": "nine_blade_comic_prompts.v1",
  "page_group": {},
  "continuity_context": {},
  "generation_contract": {},
  "type_stack_ref": {},
  "type_pack_context": {},
  "main_character_lock": {},
  "scene_continuity_bible": {},
  "style_bible": {},
  "character_locks": [],
  "comic_text_system": {},
  "story_beat_map": [],
  "pages": [],
  "global_negative_prompt": ""
}
```

## Thought Summary Skeleton

```markdown
# page-group-XX 思考过程摘要

## Source And Grouping

- source: `第N组.md` / raw fallback
- group span:
- rhythm rationale:

## Nine Blades

| page | role | source fragment | layout_id | text slots |
| --- | --- | --- | --- | --- |
| 1 | 开场钩子 |  |  |  |

## Continuity

- main character lock:
- recurring characters:
- scene locks:
- cross-group inheritance:

## Risks

- schema:
- style drift:
- layout/text:
- downstream animation:
```
