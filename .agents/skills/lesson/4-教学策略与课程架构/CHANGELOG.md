# CHANGELOG

## 2026-06-05

- Implemented `4-教学策略与课程架构` as `lesson-course-architecture`, a Skill 2.0 runtime-spine stage package.
- Added the default upstream dependencies on `1-课程定位`, `2-资料吸收与知识建模`, and `3-目标与评价蓝图`.
- Defined teaching-strategy-first execution: upstream anchor, architecture scope, strategy matrix, module blueprint, session sequence, cognitive-load review, writeback, review, and downstream handoff.
- Fixed canonical outputs as:
  - `course-outline.md`
  - `teaching-strategy-and-load-plan.md`
  - `downstream-handoff.md`
- Added LLM-first creative authorship rules forbidding scripts, templates, regex, or mapping projection from generating course architecture正文.
- Added `SKILL.md`, `CONTEXT.md`, `README.md`, `agents/openai.yaml`, and `test-prompts.json`.
