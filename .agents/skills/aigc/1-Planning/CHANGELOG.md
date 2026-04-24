# CHANGELOG.md

本文件记录 `aigc/1-Planning` 的结构性改动与迁移索引，不参与默认预加载。

## 2026-04-24

- `Case-20260424-AIGC-PLANNING-SKILL2-FUSION`
  - 按 Skill 2.0 规范将原 `1-分集`、`2-格式`、`3-分组` 三个 sibling skill 包融合为 `.agents/skills/aigc/1-Planning` 单一 Skill 2.0 包。
  - 原三包 `SKILL.md` 细则完整迁入 `references/episode-splitter-contract.md`、`references/script-format-contract.md`、`references/grouping-contract.md`，并补充融合后的 mode owner 说明。
  - 原三包 `CONTEXT.md` 经验层迁入 `knowledge-base/`；原 `_shared/IO_CONTRACT.md` 晋升为 `references/planning-io-contract.md`。
  - 原脚本与模板统一迁入父级 `scripts/`、`templates/`，产品入口收敛到 `$aigc-planning`。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/references/legacy-migration-matrix.md`
    - `.agents/skills/aigc/1-Planning/steps/planning-workflow.md`
    - `.agents/skills/aigc/1-Planning/types/planning-type-map.md`
    - `.agents/skills/aigc/1-Planning/review/planning-review-contract.md`
    - `reports/skill-upgrade-aigc-1-planning-20260424.md`

## 2026-04-12

- `Case-20260412-AIGC-PLANNING-GROUPING-ZXY-SINGLE-SKILL`
  - 将 `3-分组` 从“stage-local parent skill + shared 分组 specialist”收敛为知行合一单技能直达执行真源，并同步删除 `规划组/team.md` 中的 `分组` 角色及审计脚本中的对应硬依赖。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/references/grouping-contract.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-GROUPING-STAGE-LOCAL-OWNERSHIP`
  - 将 `3-分组` 升格为真正的 stage-local parent skill，并把 `规划组/team.md` 收回 shared dispatch plane 定位；同时新增 quantizer 作为本阶段计算真源。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/references/grouping-contract.md`
    - `.agents/skills/aigc/1-Planning/scripts/grouping_quantizer.py`

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-DIRECT-LEAF`
  - 将 `1-分集` 从“规划组单 subagent 投影”收敛为 direct leaf skill，删除孤立的旧分集 subagent 载体，并同步修正父 skill、入口元数据与 audit。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-Planning/references/legacy-episode-splitter-openai.yaml`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-AGENTS-PLAN-SHIFT`
  - 将 `1-Planning` 系列从“硬性 thinking sidecar”收敛为“subagents 返回 `agents plan`，skills 负责执行与按需留痕”，并同步修正 shared I/O、入口元数据、leaf 合同与 `规划组` team。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-Planning/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-Planning/references/script-format-contract.md`
    - `.agents/skills/aigc/1-Planning/references/grouping-contract.md`

- `Case-20260412-AIGC-PLANNING-SUBAGENT-EXECUTION-BOUNDARY`
  - 将“subagents 负责思考与 plan，skill 负责统筹与执行”的硬规则同步到 `1-Planning` 父级、已完成 leaf skills 的经验层与入口元数据，避免入口摘要与主合同再度分叉。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/agents/openai.yaml`
    - `.agents/skills/aigc/1-Planning/knowledge-base/episode-splitter-heuristics.md`
    - `.agents/skills/aigc/1-Planning/references/legacy-episode-splitter-openai.yaml`
    - `.agents/skills/aigc/1-Planning/knowledge-base/script-format-heuristics.md`
    - `.agents/skills/aigc/1-Planning/references/legacy-script-format-openai.yaml`
    - `.agents/skills/aigc/1-Planning/knowledge-base/grouping-heuristics.md`
    - `.agents/skills/aigc/1-Planning/references/legacy-grouping-openai.yaml`

- `Case-20260412-AIGC-PLANNING-ANCHOR-RESTORE`
  - 为 `.agents/skills/aigc/1-Planning` 建立父级 `SKILL.md / CONTEXT.md`，修复规划组 team 与 registry 对不存在 `1-规划` 路径的断链引用。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.codex/registry/skills.yaml`
- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-LEAF`
  - 参照 `AIGC-ZEN-VOID` 的 `1-故事分集`，在 DREAMER runtime 下补齐 `1-分集` 的 leaf 合同、经验层与机读模板。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-Planning/knowledge-base/episode-splitter-heuristics.md`
    - `.agents/skills/aigc/1-Planning/templates/episode-split-plan.template.json`
    - `.agents/skills/aigc/1-Planning/references/planning-io-contract.md`
- `Case-20260412-AIGC-PLANNING-GROUPING-LEAF`
  - 参照 `AIGC-ZEN-VOID` 的 `3-拍摄段落`，在 DREAMER runtime 下补齐 `3-分组` 的 leaf 合同、模板、manifest 与校验链，并同步收口父 skill / shared I/O。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/references/grouping-contract.md`
    - `.agents/skills/aigc/1-Planning/knowledge-base/grouping-heuristics.md`
    - `.agents/skills/aigc/1-Planning/templates/grouping-output.template.md`
    - `.agents/skills/aigc/1-Planning/skill_manifest.json`
    - `.agents/skills/aigc/1-Planning/references/planning-io-contract.md`
- `Case-20260412-AIGC-PLANNING-SPLIT-REPORT-COMPACTION`
  - 按当前规划阶段收口口径，把 `1-分集` 的逐集执行报告降级为最多一份全剧集 `执行报告.md`，避免证据侧车按集爆炸。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-Planning/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-Planning/knowledge-base/episode-splitter-heuristics.md`
- `Case-20260412-AIGC-PLANNING-SCRIPT-SINGLE-PACKAGE`
  - 参照 `AIGC-ZEN-VOID` 的 `2-对白·独白·旁白`，在 DREAMER `1-Planning` 下补齐 `2-格式` 单技能包合同，并把 `标准剧 / 解说剧` 收敛为包内 subagents 路由。
  - 同步修正 `1-分集 -> 2-格式` 的共享 I/O：`1-分集` 只写逐集原文真源，`2-格式` 才写 canonical 主稿。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/references/script-format-contract.md`
    - `.agents/skills/aigc/1-Planning/knowledge-base/script-format-heuristics.md`
    - `.agents/skills/aigc/1-Planning/scripts/validate_script_output.py`
    - `.agents/skills/aigc/1-Planning/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-Planning/references/episode-splitter-contract.md`
