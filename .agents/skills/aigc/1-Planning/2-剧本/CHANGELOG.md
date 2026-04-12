# CHANGELOG.md

本文件记录 `aigc/1-Planning/2-剧本` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-PLANNING-SCRIPT-EXECUTION-BOUNDARY`
  - 将“变体 subagents 负责思考与 patch，`2-剧本` skill 负责主稿写回、validator 与执行报告”的边界同步到经验层与入口元数据。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/agents/openai.yaml`

- `Case-20260412-AIGC-PLANNING-SCRIPT-SINGLE-PACKAGE`
  - 参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白`，在 DREAMER `1-Planning` 下建立单一 `2-剧本` 技能包。
  - 按用户要求取消本地 `标准剧 / 解说剧` 子技能目录，改由规划组 subagents 路由。
  - 证据路径：
    - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/CONTEXT.md`
    - `.agents/skills/aigc/1-Planning/2-剧本/scripts/validate_script_output.py`
    - `.codex/agents/aigc/规划组/标准剧.md`
    - `.codex/agents/aigc/规划组/解说剧.md`
