# CHANGELOG.md

本文件记录 `aigc/6-Video/3-视频生成` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-VIDEO-GENERATION-SINGLE-SOURCE-UPLIFT`
  - 将 `3-视频生成` 从“主合同摘要 + references 细则”升格为单一 `SKILL.md` 规范真源。
  - 同步补齐 `CONTEXT.md`、`agents/openai.yaml` 与目录说明，并将 `providers/README.md` 降级为非规范性槽位注释。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/3-视频生成/SKILL.md`
    - `.agents/skills/aigc/6-Video/3-视频生成/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/3-视频生成/agents/openai.yaml`
    - `.agents/skills/aigc/6-Video/3-视频生成/providers/README.md`

- `Case-20260412-AIGC-VIDEO-GENERATION-PATH-NORMALIZATION`
  - 将本叶子的当前路径口径统一收敛到 `.agents/skills/aigc/6-Video/3-视频生成/`，清理旧 `2-视频生成` / `subtypes/2-视频生成` 回指。
  - 同轮移除旧 `references/*.md` 载体，避免继续演化为第二真源。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/SKILL.md`
    - `.agents/skills/aigc/6-Video/CONTEXT.md`
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/CHANGELOG.md`
