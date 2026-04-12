# CHANGELOG.md

本文件承载 `aigc/0-Init` 的派生变更史与详细迁移线索，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-12

- `Case-20260412-AIGC-INIT-RUNTIME-MAPPING-CLARIFICATION`
  - 将 `0-Init` 和 shared runtime layout 里的“active 子路径骨架”明确定义为项目 runtime 预建目录，而不是技能树执行入口目录。
  - 为 `5-Image / 6-Video` 新增“技能树路径 -> runtime 落盘路径”的显式映射，并说明为什么 `5-Image/2-图像生成` 暂不在默认预建列表、为什么 `6-Video/2-视频生成` 在 runtime 里落成 `生成任务/`。
  - 证据路径：
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
- `Case-20260412-AIGC-INIT-SINGLE-SKILL-ABSORPTION`
  - 将 `0-Init` 从“父 skill + 初始组外置合同”回收为真正的单技能真源。
  - 把模式路由、主创会诊、快速成案、自主问答、充分性审计全部吸收到父 `SKILL.md` 的内部能力合同与节点网络中。
  - 同轮删除 `.codex/agents/aigc/初始组/*.md`，并调整 `scripts/aigc_skill_audit.py`，改为拦截 `0-Init` 回指外置初始组合同。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
    - `.agents/skills/aigc/0-Init/agents/openai.yaml`
    - `scripts/aigc_skill_audit.py`
- `Case-20260412-AIGC-INIT-RUNTIME-SKELETON-SYNC`
  - 将 `0-Init` 的初始化目录结构从“阶段根目录预建”升级为“阶段根目录 + active 子路径骨架”。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
    - `scripts/aigc_skill_audit.py`

## 2026-04-11

- `Case-20260411-AIGC-INIT-TEMPLATE-PATH-REPAIR`
  - 将 `north-star.template.yaml` 与 `init-handoff.template.yaml` 的规范引用统一收敛到 `.agents/skills/aigc/0-Init/templates/`。
- `Case-20260411-AIGC-INIT-NEXT-STEP-SYNC`
  - 将 `north_star.stage_entry_contract.stage_priority_order` 设为唯一阶段入口来源，并要求 `project_state.yaml` 与 `route-plan.yaml` 只做项目态投影。

## 2026-04-10

- `Case-20260410-AIGC-INIT-PARTIAL-STORY-SOURCE-GATE`
  - 将 `story-source-manifest` 从单一正式分集门拆成“可增量进入 + 可整季完成”两层 gate。
- `Case-20260410-AIGC-INIT-STORY-DIR-RENAME`
  - 将项目级故事正文目录统一收敛为 `projects/<项目名>/Story/`。
- `Case-20260410-AIGC-INIT-RUNTIME-ROOT-PRECREATE`
  - 在初始化阶段预建 `0-Init / Story / 1-Planning / 2-Global / 3-Detail / 4-Design / 5-Image / 6-Video / 7-Cut` 这些项目根 runtime 目录。
- `Case-20260410-AIGC-INIT-MODE-CARD-GATE`
  - 增加“模式先锁定再起草”的前置 gate，禁止仅凭项目名或一句题眼自动替用户选择快速模式。

## 2026-04-09

- `Case-20260409-AIGC-INIT-MULTI-MODE`
  - 为 `0-Init` 建立基于当前影视技能链的多模式初始化合同，并以 `north_star.yaml` 作为主输出物。
- `Case-20260409-AIGC-INIT-TEAM-MANIFEST`
  - 将主创会诊模式从顾问路径列表升级为 `team.yaml` 团队真源，并固化 `策划 / 监制 / 评审` 三角色的作用矩阵。
- `Case-20260409-AIGC-INIT-TEAM-ROOT-PROMOTION`
  - 将 `team.yaml` 从 `0-Init/` 提升到 `projects/<项目名>/team.yaml`。
- `Case-20260409-AIGC-INIT-FAST-MINIMAL-BRIEF`
  - 确认快速模式可以接受极简 brief，但不等于可以跳过模式选择 gate。
- `Case-20260409-AIGC-INIT-ADAPTATION-PACING-GATE`
  - 在初始化阶段明确 `original_adherence` 与节奏重排授权。
