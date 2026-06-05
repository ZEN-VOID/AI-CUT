# CHANGELOG

## 2026-06-05

- Implemented `6-活动练习与测评开发` as `lesson-assessment-development`, a Skill 2.0 runtime-spine stage package.
- Defined upstream dependencies on `3-目标与评价蓝图`, `4-教学策略与课程架构`, and `5-课时内容开发`.
- Fixed canonical outputs as:
  - `activity-exercise-package.md`
  - `question-bank.yaml`
  - `scoring-rubrics.md`
  - `answer-explanations.md`
  - `assessment-package.md`
  - `downstream-handoff.md`
- Added LLM-first creative authorship rules that prohibit script or template generation, batch insertion, regex phrasing, and mapping projection for activity, question, explanation, rubric, or scoring content.
- Added `SKILL.md`, `CONTEXT.md`, `README.md`, `agents/openai.yaml`, and `test-prompts.json` without enabling optional modules.
