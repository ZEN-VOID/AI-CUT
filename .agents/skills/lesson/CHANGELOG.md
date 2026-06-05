# CHANGELOG

## 2026-06-05

- Added root `agents/openai.yaml` so the lesson router now satisfies the Skill 2.0 core layout at root level as well as in child packages.
- Added root metadata field/pass boundaries to keep `agents/openai.yaml` as product entry metadata rather than a runtime rule source.
- Added root `Upstream Loading Matrix` to make per-stage required upstream files, handoff gates, missing policies, truth boundaries, and content-model touchpoints explicit.
- Added root `Content Model Governance Contract` covering `content-model/modules/`, `lessons/`, `assessments/`, and `delivery-map.*` ownership.
- Synchronized stages `1` through `8` with the root upstream policy: `1/course-positioning.md` is a global positioning anchor, `downstream-handoff.md` is a required status gate, and missing upstream must route to the owning stage, `repair/`, or draft-only mode.
- Assigned content-model write ownership: stage `4` may refresh `modules/`, stage `5` may refresh `lessons/`, stage `6` may refresh `assessments/`, and stage `8` may write only derived delivery maps and manifests.
- Added `LESSON-TM-12`, `LESSON-TM-13`, and `Case-005` to root `CONTEXT.md` for upstream handoff bypass and content-model ownership drift prevention.
- Synchronized root documentation with the latest `.agents/skills/lesson` directory structure: active 0-8 stages, `8/doc|ppt|html` delivery leaves, `query|resume|repair|learn|benchmark` satellites, and `_shared/` as a reserved non-executable support carrier.
- Added root `_shared/` boundary language to `SKILL.md`, including field mapping, pass gate, root-cause repair handling, and context writeback rules.
- Added root `Type Routing Matrix`, `Thinking-Action Node Map`, `Module Trigger Matrix`, and `Convergence Contract` so the router remains a readable Skill 2.0 runtime spine rather than a pure directory index.
- Added README skill tree inventory and updated root router status from initialized to active.
- Added `LESSON-TM-10`, `LESSON-TM-11`, and `Case-004` to root `CONTEXT.md` for shared support boundary drift prevention and nested-skill smoke interpretation.
- Implemented `3-目标与评价蓝图` as a Skill 2.0 runtime-spine stage package.
- Implemented `4-教学策略与课程架构` as a Skill 2.0 runtime-spine stage package.
- Implemented `5-课时内容开发` as a Skill 2.0 runtime-spine stage package.
- Implemented `6-活动练习与测评开发` as a Skill 2.0 runtime-spine stage package.
- Implemented `7-视觉媒体与交互设计` as a Skill 2.0 runtime-spine stage package.
- Implemented `8-多端交付生成` as a Skill 2.0 runtime-spine parent package with `doc/`, `ppt/`, and `html/` delivery leaves.
- Updated root route status from scaffolded to active for stages `3` through `8` and the three delivery leaves.
- Clarified root content-model governance: stage canonical files remain stage truth; `content-model/` is a shared index, handoff, and derived projection container, not a second course manuscript.
- Implemented root satellites `query/`, `resume/`, `repair/`, `learn/`, and `benchmark/` as Skill 2.0 runtime-spine packages.
- Synchronized root README and reference loading guide so satellite packages are marked active instead of placeholders.
- Implemented `2-资料吸收与知识建模` as `lesson-knowledge-modeling`, a Skill 2.0 runtime-spine stage package.
- Added deep research, source inventory, evidence audit, knowledge modeling, evidence/case library, misconception mapping, dependency mapping, and downstream handoff contracts.
- Fixed stage outputs as `projects/lesson/<项目名>/2-资料吸收与知识建模/research-source-inventory.md`, `knowledge-model.md`, `evidence-and-case-library.md`, and `downstream-handoff.md`.
- Declared project `MEMORY.md` writeback boundaries for durable context provided during the research stage.
- Implemented `1-课程定位` as `lesson-positioning`, a Skill 2.0 runtime-spine stage package.
- Added quick mode and dialog questionnaire mode for course positioning inputs.
- Fixed the stage output as `projects/lesson/<项目名>/1-课程定位/course-positioning.md`.
- Initialized the `lesson` root router for courseware and lesson projects.
- Fixed canonical project runtime as `projects/lesson/<项目名>/`.
- Documented the 0-8 main workflow:
  `0-初始化 -> 1-课程定位 -> 2-资料吸收与知识建模 -> 3-目标与评价蓝图 -> 4-教学策略与课程架构 -> 5-课时内容开发 -> 6-活动练习与测评开发 -> 7-视觉媒体与交互设计 -> 8-多端交付生成`.
- Declared DOC/PPT/HTML delivery leaves under `8-多端交付生成/doc|ppt|html`.
- Declared root satellite boundaries for `query/`, `resume/`, `repair/`, `learn/`, and `benchmark/`.
- Explicitly kept `review/` out of the root satellite set; review gates belong inside each stage package.
- Added root `SKILL.md`, `CONTEXT.md`, `README.md`, and `CHANGELOG.md` as continuing-development context for the lesson workflow.
