# lesson

`$lesson` 是课程课件开发工作流的系统级主入口，用于协调 `projects/lesson/<项目名>/` 下的课程、课件、培训、lesson/courseware 项目。目标交付形态是 DOC、PPT、HTML，但三端应从共享课程内容模型投影，不各自形成主稿。

## Directory Tree

```text
lesson/
├── agents/
│   └── openai.yaml
├── _shared/                         # reserved non-executable shared support carrier
├── 0-初始化/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 1-课程定位/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 2-资料吸收与知识建模/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 3-目标与评价蓝图/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 4-教学策略与课程架构/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 5-课时内容开发/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 6-活动练习与测评开发/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 7-视觉媒体与交互设计/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── 8-多端交付生成/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   ├── test-prompts.json
│   ├── doc/
│   │   ├── agents/
│   │   ├── CHANGELOG.md
│   │   ├── CONTEXT.md
│   │   ├── README.md
│   │   ├── SKILL.md
│   │   └── test-prompts.json
│   ├── html/
│   │   ├── agents/
│   │   ├── CHANGELOG.md
│   │   ├── CONTEXT.md
│   │   ├── README.md
│   │   ├── SKILL.md
│   │   └── test-prompts.json
│   └── ppt/
│       ├── agents/
│       ├── CHANGELOG.md
│       ├── CONTEXT.md
│       ├── README.md
│       ├── SKILL.md
│       └── test-prompts.json
├── benchmark/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── learn/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── query/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── repair/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── resume/
│   ├── agents/
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Main Workflow

```text
0-初始化
→ 1-课程定位
→ 2-资料吸收与知识建模
→ 3-目标与评价蓝图
→ 4-教学策略与课程架构
→ 5-课时内容开发
→ 6-活动练习与测评开发
→ 7-视觉媒体与交互设计
→ 8-多端交付生成
```

## Project Runtime

Canonical project root:

```text
projects/lesson/<项目名>/
```

Expected initialized project scaffold:

```text
projects/lesson/<项目名>/
├── 0-初始化/
├── 1-课程定位/
├── 2-资料吸收与知识建模/
├── 3-目标与评价蓝图/
├── 4-教学策略与课程架构/
├── 5-课时内容开发/
├── 6-活动练习与测评开发/
├── 7-视觉媒体与交互设计/
├── 8-多端交付生成/
│   ├── doc/
│   ├── html/
│   └── ppt/
├── assets/
├── content-model/
├── sources/
├── CONTEXT/
│   └── README.md
└── MEMORY.md
```

Stage directories are the canonical truth for each numbered stage. `content-model/` is a shared index, handoff, and derived projection container for cross-stage consumption and DOC/PPT/HTML delivery; it must not become a parallel replacement for stage canonical files.

## Upstream Loading Summary

The authoritative matrix is in root `SKILL.md` under `Upstream Loading Matrix`.

| stage | required upstream |
| --- | --- |
| `1-课程定位` | user/project brief, project `MEMORY.md`, related project `CONTEXT/`, source evidence |
| `2-资料吸收与知识建模` | `1-课程定位/course-positioning.md`, especially section 11 handoff |
| `3-目标与评价蓝图` | `1-课程定位/course-positioning.md` + stage 2 canonical files and `downstream-handoff.md` |
| `4-教学策略与课程架构` | stage 1 positioning + stage 2 knowledge outputs + stage 3 objective/evaluation outputs and handoffs |
| `5-课时内容开发` | stage 1 positioning + stage 2 knowledge evidence + stage 3 objectives + stage 4 architecture and handoffs |
| `6-活动练习与测评开发` | stage 1 positioning + stage 2 evidence backstop + stage 3 objectives + stage 4 architecture + stage 5 content and handoffs |
| `7-视觉媒体与交互设计` | stage 1 positioning + stage 3 objectives + stage 4 architecture + stage 5 content + stage 6 assessment and handoffs |
| `8-多端交付生成` | stage 1 positioning + `content-model/` + stage 3-7 canonical outputs and handoffs |

Rules:

- `downstream-handoff.md` is not optional status decoration; it is the upstream state gate for later stages.
- A stage directory existing is not enough to treat that stage as complete.
- Missing key upstream must route to the owning stage, enter `repair/`, or remain draft-only with visible assumptions.

## Content Model Ownership

| carrier | owning writer | consumer |
| --- | --- | --- |
| `content-model/modules/` | `4-教学策略与课程架构` | `5/6/7/8` |
| `content-model/lessons/` | `5-课时内容开发` | `6/7/8` |
| `content-model/assessments/` | `6-活动练习与测评开发` | `7/8` |
| `content-model/delivery-map.*` | `8-多端交付生成` | `8/doc`, `8/ppt`, `8/html` |

Only the owning writer may refresh its partition. Conflicts between `content-model/` and stage canonical files resolve in favor of the stage canonical files.

## Skill Tree Inventory

| group | directories | status | route behavior |
| --- | --- | --- | --- |
| Root router | `SKILL.md`, `CONTEXT.md`, `README.md`, `CHANGELOG.md` | active | Selects one stage, leaf, or satellite; does not author course content |
| Main stages | `0-初始化` through `8-多端交付生成` | active | Numeric stages run in declared order when the full workflow is requested |
| Delivery leaves | `8-多端交付生成/doc`, `ppt`, `html` | active | Selected by explicit DOC/PPT/HTML intent or by the `8` parent stage |
| Satellites | `query`, `resume`, `repair`, `learn`, `benchmark` | active | Side channels; not part of the default 0-8 serial chain |
| Shared support | `_shared` | reserved empty carrier | Non-executable; only usable when a consuming skill explicitly authorizes a file |

## Routing Summary

| Request | Route |
| --- | --- |
| 初始化课程/课件/培训项目 | `0-初始化` |
| 明确推进某阶段 | corresponding numbered stage |
| 生成 DOC / Word / 讲义 | `8-多端交付生成/doc` |
| 生成 PPT / slides / 授课演示 | `8-多端交付生成/ppt` |
| 生成 HTML / 网页课件 / 交互课件 | `8-多端交付生成/html` |
| 查询项目事实或产物 | `query/` |
| 恢复中断或补齐缺口 | `resume/` |
| 修复阶段产物或三端漂移 | `repair/` |
| 吸收外部方法或参考课件 | `learn/` |
| 对照竞品或优秀课程 | `benchmark/` |

`review/` 不作为根层独立卫星入口；阶段验收由各阶段 `SKILL.md` 的 gate 承担。

## Current Development Status

- Root router: active; directory index, runtime namespace, stage route, upstream loading matrix, content-model ownership, satellite route, and shared support boundary are synchronized.
- `0-初始化`: initialized and validated.
- `1-课程定位`: initialized; supports quick mode and dialog questionnaire mode, outputs `course-positioning.md`.
- `2-资料吸收与知识建模`: initialized; supports deep research, source inventory, evidence audit, knowledge modeling, case/misconception library, dependency mapping, and downstream handoff.
- `3-目标与评价蓝图`: initialized and validated; outputs objective, evidence, rubric, and alignment blueprints.
- `4-教学策略与课程架构`: initialized and validated; outputs course architecture, module map, pacing, lesson sequence, and may refresh `content-model/modules/` indexes.
- `5-课时内容开发`: initialized and validated; outputs lesson scripts, learner materials, examples, content handoff, and may refresh `content-model/lessons/` indexes.
- `6-活动练习与测评开发`: initialized and validated; outputs activity, practice, question, rubric, answer, assessment packages, and may refresh `content-model/assessments/` indexes.
- `7-视觉媒体与交互设计`: initialized and validated; outputs visual system, media briefs, diagram plan, interaction plan, and accessibility constraints.
- `8-多端交付生成`: initialized and validated with `doc/`, `ppt/`, and `html/` leaves; reads stage 1 and stage 3-7 handoffs, audits `content-model/`, and outputs delivery plans, manifests, delivery maps, and selected DOC/PPT/HTML projections.
- `query/`: initialized and validated; read-only evidence-backed project fact, route, artifact, and validation distinction query.
- `resume/`: initialized and validated; reconstructs project evidence and returns one safe next entry or blocker.
- `repair/`: initialized and validated; source-first repair routing for stage outputs, content-model drift, and DOC/PPT/HTML inconsistencies.
- `learn/`: initialized and validated; absorbs external teaching methods, references, course standards, and project experience into evidence-backed learning packets or narrow improvements.
- `benchmark/`: initialized and validated; compares against reference courses, competitors, teaching standards, and quality rubrics without copying source content or rewriting stage truth.
- `_shared/`: reserved empty shared support directory; not a stage, satellite, module, or default context source.

## Validation

Root router:

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson --mode delivery
```

Initialized stage:

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/0-初始化 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/0-初始化 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/1-课程定位 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/1-课程定位 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/2-资料吸收与知识建模 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/2-资料吸收与知识建模 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/3-目标与评价蓝图 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/3-目标与评价蓝图 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/4-教学策略与课程架构 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/4-教学策略与课程架构 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/5-课时内容开发 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/5-课时内容开发 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/6-活动练习与测评开发 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/6-活动练习与测评开发 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/7-视觉媒体与交互设计 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/7-视觉媒体与交互设计 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成/doc --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成/doc --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成/ppt --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成/ppt --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成/html --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成/html --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/query --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/query --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/resume --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/resume --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/repair --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/repair --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/learn --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/learn --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/benchmark --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/benchmark --mode delivery
```
