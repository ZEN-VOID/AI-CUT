# CHANGELOG.md

本文件记录 `aigc/1-Planning` 的结构性改动与迁移索引，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-PLANNING-GROUPING-STAGE-LOCAL-OWNERSHIP`
  - 将 `3-分组` 升格为真正的 stage-local parent skill，并把 `规划组/team.md` 收回 shared dispatch plane 定位；同时新增 quantizer 作为本阶段计算真源。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
    - `.codex/agents/aigc/规划组/team.md`
    - `.codex/agents/aigc/规划组/分组.md`

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-DIRECT-LEAF`
  - 将 `1-分集` 从“规划组单 subagent 投影”收敛为 direct leaf skill，删除孤立的 `.codex/agents/aigc/规划组/分集.md`，并同步修正父 skill、team、入口元数据与 audit。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`
    - `.codex/agents/aigc/规划组/team.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-AGENTS-PLAN-SHIFT`
  - 将 `1-Planning` 系列从“硬性 thinking sidecar”收敛为“subagents 返回 `agents plan`，skills 负责执行与按需留痕”，并同步修正 shared I/O、入口元数据、leaf 合同与 `规划组` team。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.codex/agents/aigc/规划组/team.md`

- `Case-20260412-AIGC-PLANNING-SUBAGENT-EXECUTION-BOUNDARY`
  - 将“subagents 负责思考与 plan，skill 负责统筹与执行”的硬规则同步到 `1-Planning` 父级、已完成 leaf skills 的经验层与入口元数据，避免入口摘要与主合同再度分叉。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/agents/openai.yaml`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/agents/openai.yaml`
    - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/agents/openai.yaml`
    - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/3-分组/agents/openai.yaml`

- `Case-20260412-AIGC-PLANNING-ANCHOR-RESTORE`
  - 为 `.agents/skills/aigc/1-Planning` 建立父级 `SKILL.md / CONTEXT.md`，修复规划组 team 与 registry 对不存在 `1-规划` 路径的断链引用。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/CONTEXT.md`
    - `.codex/agents/aigc/规划组/team.md`
    - `.codex/registry/skills.yaml`
- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-LEAF`
  - 参照 `AIGC-ZEN-VOID` 的 `1-故事分集`，在 DREAMER runtime 下补齐 `1-分集` 的 leaf 合同、经验层与机读模板。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/templates/episode-split-plan.template.json`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
- `Case-20260412-AIGC-PLANNING-GROUPING-LEAF`
  - 参照 `AIGC-ZEN-VOID` 的 `3-拍摄段落`，在 DREAMER runtime 下补齐 `3-分组` 的 leaf 合同、模板、manifest 与校验链，并同步收口父 skill / shared I/O。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/3-分组/templates/grouping-output.template.md`
    - `.agents/skills/aigc/1-Planning/3-分组/skill_manifest.json`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
- `Case-20260412-AIGC-PLANNING-SPLIT-REPORT-COMPACTION`
  - 按当前规划阶段收口口径，把 `1-分集` 的逐集执行报告降级为最多一份全剧集 `执行报告.md`，避免证据侧车按集爆炸。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/CONTEXT.md`
- `Case-20260412-AIGC-PLANNING-SCRIPT-SINGLE-PACKAGE`
  - 参照 `AIGC-ZEN-VOID` 的 `2-对白·独白·旁白`，在 DREAMER `1-Planning` 下补齐 `2-剧本` 单技能包合同，并把 `标准剧 / 解说剧` 收敛为包内 subagents 路由。
  - 同步修正 `1-分集 -> 2-剧本` 的共享 I/O：`1-分集` 只写逐集原文真源，`2-剧本` 才写 canonical 主稿。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/scripts/validate_script_output.py`
    - `.agents/skills/aigc/1-Planning/_shared/IO_CONTRACT.md`
    - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
