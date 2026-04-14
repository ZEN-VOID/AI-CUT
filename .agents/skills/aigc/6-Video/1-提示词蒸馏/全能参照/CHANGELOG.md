# CHANGELOG.md

本文件承载 `aigc/6-Video/1-提示词蒸馏/全能参照` 的结构性迁移记录，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-14

- `Case-20260414-AIGC-VIDEO-OMNIREF-I2V-STYLE-GOVERNANCE`
  - 新增 `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md` 作为组级与帧级叶子共享的 `图生视频` 句法原则真源。
  - 重写 `prompt-assembly-spec.md` 的组级桥接句与镜级句法顺序，使其更偏“主体锚点 -> 镜头起势 -> 可见动作 -> 环境光感 -> 视觉焦点”的 `image-to-video` 组织方式，但内容来源仍保持当前 `3-Detail` 字段。
  - 同步更新 `6-Video/SKILL.md`、共享文本模板、`SKILL.md` / `CONTEXT.md` / `agents/openai.yaml` 的回指口径，避免兄弟叶子再次各自演化 prompt 风格。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md`
    - `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`
    - `.agents/skills/aigc/6-Video/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/prompt-assembly-spec.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`

- `Case-20260414-AIGC-VIDEO-OMNIREF-PROMPT-ASSEMBLY-SPEC`
  - 新增 `prompt-assembly-spec.md` 作为 `全能参照` 的句法真源，显式收束组级桥接句、镜级 `P1/P2/P3` 槽位、`tight/ultra` 压缩落点与 `转场特效` 可选挂句。
  - `generate_episode_packets.py` 改为解析并消费 spec，不再把句法字符串散落硬编码在 `build_group_bridge / build_camera_sentence / build_shot_text` 等函数里。
  - 同步把共享 `video-generation-input.template.json` 的 `source_file` 示例更新为 `projects/aigc/<项目名>/...`，修复模板层与执行层的命名空间漂移。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/prompt-assembly-spec.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/scripts/generate_episode_packets.py`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`

- `Case-20260414-AIGC-VIDEO-OMNIREF-DETAIL-HANDOFF-GATE`
  - 将 `全能参照` 与父级 `6-Video` 的输入门同步到重构后的 `3-Detail` shared-root 合同：只消费 `metadata.document_phase=ready`，并显式校验每组 `分镜切换 == len(分镜明细[])`。
  - 同步把同口径校验下沉到 `generate_episode_packets.py`，避免脚本层绕过技能合同误吃 `bootstrapped/detail_in_progress` 或 merge 未稳定的 episode root。
  - 同步刷新 `CONTEXT.md` 与 `agents/openai.yaml`，把 `ready gate + 分镜切换对齐门` 固化为入口记忆和默认提示。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/scripts/generate_episode_packets.py`

## 2026-04-12

- `Case-20260412-AIGC-VIDEO-SUBJECT-SINGLE-SOURCE-CONTRACT`
  - 将 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/output-template.md`、`references/type-strategies.md` 全量回收到 `SKILL.md`，把 `SKILL.md` 升格为子技能唯一规范真源。
  - 同步补建 `agents/openai.yaml` 与 `CHANGELOG.md`，并把经验层引用改到 `SKILL.md` / shared templates。
  - 将旧写法 `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/` 统一收敛为当前 canonical 路径 `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/`。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`

- `Case-20260412-AIGC-VIDEO-SUBJECT-ZXY-REFACTOR`
  - 在不改变现有输入、输出、模板、字段、字数窗与禁止项的前提下，将 `全能参照` 重写为知行合一式单技能思行网络。
  - 新增 `业务需求分析合同 / 总输入合同 / 拓扑合同 / N0-N8 思行节点 / 汇流门 / 一次性输出门`，并显式声明 `复杂链路的骨架 / 细则分层: false`。
  - 新增执行闭环要求：最终结案除三件套外，必须包含 `思考过程 + 关键证据 + 风险/例外`。
  - 同步刷新 `CONTEXT.md` 的 Type Map、Heuristics 与案例记录，并更新 `agents/openai.yaml` 的入口描述。
  - 证据路径：
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
    - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`
