# 九刀流漫画提示词 Review Contract

本文件定义 `comic-nine-blade-prompts` 的质量门禁。业务主真源仍归 `SKILL.md` 与创作输出；review 只给出通过、返工或风险结论。

## Default Provider

- 默认辅助 provider：`code-reviewer`。
- 用途：检查 Skill 2.0 结构、JSON 合同、脚本边界、类型包加载、提示词质量门禁。
- 当前上层策略若阻断真实 subagent/reviewer 调度，降级为本地 checklist，并在最终报告说明：阻断层级、原计划 provider、实际降级路径、未真实启动的 reviewer。

## Review Scope

| dimension | checks |
| --- | --- |
| `structure` | canonical 分区、`SKILL.md + CONTEXT.md`、`README.md`、`CHANGELOG.md`、`agents/openai.yaml` 是否齐全 |
| `dynamic_reference` | `SKILL.md` 是否只保留入口、路由、关键门禁和 Output Contract，是否引用真实分区 |
| `modes` | `steps/source-routing-and-handoff.md` 是否能选择 grouped/raw/multi-episode/poster-aware mode，并提供对应合同 |
| `types` | `types/type-map.md` 是否只选择漫画题材类型包，并加载具体包文件 |
| `steps` | `steps/nine-blade-workflow.md` 是否包含前奏、切组、九刀主流程、三支路汇流和失败回路 |
| `schema` | JSON 是否符合 `templates/nine-blade-comic-prompts.schema.json` |
| `semantic` | 9 页是否连续、非拼图、非变体、角色/场景/风格稳定 |
| `layout_text` | 版式是否多样、每页多格、文字槽是否四类齐备且可读 |
| `scripts` | `scripts/validate_nine_blade_prompt_json.py` 是否只做机械校验，不替代 LLM 主创 |
| `handoff` | 是否可被 3 号生图和 4 号剧集海报阶段消费 |

## Review Checklist

- `generation_contract.hard_constraints` 包含 9 separate pages、no collage、no variations、multiple panels、character/scene consistency、bottom-right digits-only page numbers。
- `main_character_lock.anchor_prompt` 有角色名、身份/物种、体型轮廓、脸部特征、服装、材质/色彩、consistent face/costume/silhouette/color palette。
- 多人页 `active_character_ids` 回指角色锁，且 `positive_prompt` 点名至少两名出场 recurring characters。
- `scene_continuity_bible.scene_locks[]` 至少一个具名场景锁；每页 `scene_id` 回指该锁，prompt 注入场景名。
- 每页 `positive_prompt` 前段重复 `global style anchor`，并含 `forbidden style shifts` 或等价语义。
- 9 页至少 5 个不同 `layout_id`，动态版式不少于 3 类。
- `comic_text_system` 四类齐备；九页整体至少覆盖 dialogue、narration、inner_monologue、sfx 各一次。
- 每个 text slot 的 `speaker_id / placement / bubble_style / inside_panel` 与类型规则一致。
- `page_number_overlay.text` 为 `"1"` 到 `"9"`，位置 `bottom-right`，prompt 写明 digits only。
- 若需要动画，`pages[].panels[]` 可逐格展开为 shot plan。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给 3/4 号技能 |
| `pass_with_followups` | 可交付，但存在非阻断优化项 |
| `needs_rework` | 有阻断问题，必须按 failure routing 返工 |
| `blocked` | 缺失输入、上游真源或权限导致无法执行 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: structure | dynamic_reference | types | steps | schema | semantic | layout_text | scripts | handoff
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Required Commands

```bash
python3 .agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py <json_path>
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/comic/2-九刀流漫画提示词
```
