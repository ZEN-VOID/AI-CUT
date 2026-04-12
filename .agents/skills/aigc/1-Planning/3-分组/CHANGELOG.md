# CHANGELOG.md

本文件记录 `aigc/1-Planning/3-分组` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-PLANNING-GROUPING-ZXY-SINGLE-SKILL`
  - 按 `skill-知行合一` 将 `3-分组` 重写为单技能思行网络真源，并把旧 `规划组/分组.md` 的边界判断、回退升级、质量检查与输入输出合同吸收回本地 `SKILL.md`；同步删除 planning team 中的 `分组` 角色与 audit 依赖。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-GROUPING-SUBAGENT-GOVERNANCE-RESET`
  - 将 `3-分组` 从“leaf 合同 + 一个分组 agent 附注”重构为 stage-local parent skill，明确 shared planning team 只负责调度与 handoff matrix，`分组` specialist 只负责 `patch / note / report`。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/SKILL.md`

- `Case-20260412-AIGC-PLANNING-GROUPING-QUANTIZER-SOURCE-LAYER`
  - 新增 `grouping_quantizer.py`，把 `effective_text_chars / duration mapping / mixed-source recompute` 提升为脚本真源；同步让 validator 直接消费 quantizer 结果。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/grouping_quantizer.py`
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/postprocess_grouping_output.py`
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`

- `Case-20260412-AIGC-PLANNING-GROUPING-AGENTS-PLAN`
  - 将 `3-分组` 从“强制 thinking sidecar”改为“可选 `agents plan` 证据”，并同步后处理与校验链到新的 agents-plan 口径。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/3-分组/skill_manifest.json`
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/postprocess_grouping_output.py`
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`

- `Case-20260412-AIGC-PLANNING-GROUPING-EXECUTION-BOUNDARY`
  - 将“分组 agent 负责 group plan，`3-分组` skill 负责 thinking sidecar、主稿、sidecar 与 validate 落盘”的边界同步到经验层与入口元数据。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/3-分组/agents/openai.yaml`

- `Case-20260412-AIGC-PLANNING-GROUPING-MIGRATION`
  - 参照 `AIGC-ZEN-VOID` 的 `3-拍摄段落`，补齐 `3-分组` 的 leaf skill 合同、经验层、模板、manifest 与校验脚本，同时改写到 DREAMER 的 `projects/<项目名>/1-Planning/...` runtime。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
    - `.agents/skills/aigc/1-Planning/3-分组/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/3-分组/skill_manifest.json`
    - `.agents/skills/aigc/1-Planning/3-分组/templates/grouping-output.template.md`
    - `.agents/skills/aigc/1-Planning/3-分组/scripts/validate_grouping_output.py`
