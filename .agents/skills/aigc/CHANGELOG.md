# CHANGELOG.md

本文件承载 `aigc` 根技能的派生变更史与详细 rollout 记录，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-11

- `Case-20260411-AIGC-ROOT-VIDEO-SUBMIT-STATUS-SYNC`
  - 将根技能中 `6-视频` 的阶段状态同步扩展为包含真实叶子 `2-视频生成` 可执行，并把 provider 占位目录收敛到 `providers/`。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/6-Video/SKILL.md`
    - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
    - `scripts/aigc_skill_audit.py`

## 2026-04-12

- `Case-20260412-AIGC-ROOT-INIT-RUNTIME-SKELETON-SYNC`
  - 将根技能对 `0-Init` 的说明同步为“按 shared runtime layout 预建阶段根目录与 active child skeleton”，并补入 `projects/<项目名>/故事/` 项目根目录，避免根入口继续停留在旧的根目录口径。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `Case-20260412-AIGC-ROOT-VIDEO-GENERATION-SINGLE-SOURCE-SYNC`
  - 将根技能与 `6-Video` 父级中的 `3-视频生成` / `subtypes/3-视频生成` 旧口径收敛到真实路径 `.agents/skills/aigc/6-Video/2-视频生成/`。
  - 同步反映 `2-视频生成` 已从“主合同摘要 + references 细则”升格为单一 `SKILL.md` 规范真源。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/6-Video/SKILL.md`
    - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
    - `.agents/skills/aigc/6-Video/2-视频生成/CHANGELOG.md`
- `Case-20260411-AIGC-ROOT-BENCHMARK-SUITE-BOOTSTRAP`
  - 为根 suite 新增 `benchmark-suite.yaml`，覆盖 baseline、boundary、stress、adversarial 与 regression 五类评测任务。
  - 证据路径：
    - `.agents/skills/aigc/benchmark-suite.yaml`
    - `.agents/skills/aigc/SKILL.md`
- `Case-20260411-AIGC-INIT-CONTRACT`
  - 将 `0-Init` 在根技能中的阶段状态从“预留中”升级为“已建合同，脚本待补”，完成根入口与初始化合同的第一次对齐。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/0-Init/SKILL.md`

## 2026-04-10

- `Case-20260410-AIGC-ROOT-RUNTIME-DIR-NONNUMERIC`
  - 将根技能的 canonical stage landing 从带号 runtime 目录收敛为 `规划 / 主体 / 画面`，要求目录名回查 shared layout。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `Case-20260410-AIGC-ROOT-VISUAL-STAGE-RENAME`
  - 将 runtime 口径统一收敛到 `projects/<项目名>/5-Image/`，避免继续把视觉阶段写成历史命名。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/5-画面/SKILL.md`
- `Case-20260410-AIGC-ROOT-VIDEO-STAGE-ACTIVATE`
  - 将 `6-视频` 从 `shelved` 收敛为部分可执行阶段，并要求根入口、registry 与 route carrier 同步更新。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.codex/registry/skills.yaml`
    - `.codex/registry/routes.yaml`
- `Case-20260410-AIGC-RUNTIME-MAPPING-RECONCILIATION`
  - 将 shared runtime layout、根技能、`1-规划`、`0-Init` 与审计脚本统一到同一套 runtime mapping，修复 `设定/画面`、`Init/1-规划` 两套并行口径。
  - 证据路径：
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
    - `.agents/skills/aigc/1-Planning/SKILL.md`
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `scripts/aigc_skill_audit.py`
- `Case-20260410-AIGC-ROOT-VIDEO-FIRST-FRAME-STATUS-SYNC`
  - 将根技能中 `6-视频` 的可执行子路径说明同步扩展为 `全能参照 + 首帧参照`。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`

## 2026-04-09

- `Case-20260409-AIGC-ROOT-PLANNING-STATUS-SYNC`
  - 将根入口中的 `1-规划` 从“已建骨架”同步更新为“已建阶段合同，子路径持续补全中”。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/1-Planning/SKILL.md`
- `Case-20260409-AIGC-ROOT-DIRECTING-STATUS-SYNC`
  - 将根入口中的 `2-组间` 状态同步为“阶段合同已建、四个子路径可执行”。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/2-Global/SKILL.md`
- `Case-20260409-AIGC-ROOT-SCRIPT-STATUS-SYNC`
  - 将根入口中的 `3-明细` 同步为“阶段合同已建，`2-角色表现` 父子路由已补齐，其余子路径持续补全”。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/3-明细/SKILL.md`
- `Case-20260409-AIGC-ROOT-SCRIPT-CAMERA-STATUS-SYNC`
  - 根入口将 `3-运镜手法` 纳入 `3-明细` 当前可路由子路径。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.codex/agents/aigc/制作组/运镜手法.md`
- `Case-20260409-AIGC-ROOT-SCRIPT-ATMOSPHERE-STATUS-SYNC`
  - 根入口将 `4-场景氛围` 纳入 `3-明细` 当前可路由子路径。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.codex/agents/aigc/制作组/场景氛围.md`
- `Case-20260409-AIGC-ROOT-SCRIPT-CINEMATOGRAPHY-STATUS-SYNC`
  - 根入口将 `5-摄影美学` 纳入 `3-明细` 当前可路由子路径。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.codex/agents/aigc/制作组/摄影美学.md`
- `Case-20260409-AIGC-ROOT-SCRIPT-TRANSITION-STATUS-SYNC`
  - 根入口将 `6-转场特效` 纳入 `3-明细` 当前可路由子路径。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.codex/agents/aigc/制作组/转场特效.md`
- `Case-20260409-AIGC-ROOT-STORYBOARD-STATUS-SYNC`
  - 根入口将 `5-画面` 子路径 `分镜故事板 / 分镜帧 / 漫画` 收口为已知可执行入口。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/5-画面/SKILL.md`
- `Case-20260409-AIGC-ROOT-SUBJECT-STATUS-SYNC`
  - 将根入口中的 `4-主体` 从“待补”同步为已建父子合同的阶段。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/4-主体/SKILL.md`
- `Case-20260409-AIGC-PROJECT-ROOT-RUNTIME`
  - 将 `projects/<项目名>/` 收口为唯一项目运行时真源，移除隐藏运行时目录作为第二真相。
  - 证据路径：
    - `.agents/skills/aigc/SKILL.md`
    - `.codex/registry/skills.yaml`
    - `.codex/registry/routes.yaml`
    - `scripts/aigc_skill_audit.py`
- `Case-20260409-AIGC-LEAF-ROLLOUT-CLOSURE`
  - 为多个 governed leaf 补齐 `Root-Cause Execution Contract`，并让严格审计跳过 `shelved` 阶段的 leaf 级失败。
  - 证据路径：
    - `.codex/agents/aigc/制作组/动作戏.md`
    - `.codex/agents/aigc/制作组/光影设计.md`
    - `scripts/aigc_skill_audit.py`
- `Case-20260409-AIGC-ROOT-COUNCIL-RUNTIME`
  - 将 `team.yaml` 提升为项目根团队真源，并新增 `_shared/council-runtime/` 共享运行时入口。
  - 证据路径：
    - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
    - `.agents/skills/aigc/SKILL.md`
