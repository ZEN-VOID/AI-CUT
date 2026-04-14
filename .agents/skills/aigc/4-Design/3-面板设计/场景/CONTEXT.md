# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-面板设计/场景` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc` 根技能与 `4-Design/2-主体设计/场景` 上游技能之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-面板` 跳过 `2-设计` 直接拼场景 prompt | 输入真源层 | 强制回到 `场景设计.json` 与 `panel_handoff` | 在 `SKILL.md` 与脚本中固化 `2-设计` 为第一输入根 | 不再从导演 JSON 直接生 panel |
| 面板 carrier 只有单个 `layout.json`，没有 episode 级聚合真源 | 输出治理层 | 补回 `场景面板.json` 作为 machine-first canonical carrier | 在单一 `SKILL.md` 的输出合同中固定 episode + per-scene 双层同源结构 | `场景面板.json` 与逐场景 layout 一一可回链 |
| negative constraints 在场景设计有记录，面板阶段丢失 | handoff 合同层 | 将 `reverse_taboos` 与模板 negative prompt 汇总进 `negative_prompt` | 在脚本里固定 negative 合成函数 | per-scene layout 不再遗漏禁区 |
| 面板阶段越权做图片生成 | 阶段边界层 | 停在 panel carrier 落盘，不调用生图 | 在 `SKILL.md`、脚本 CLI 与输出契约中固定 JSON-only 边界 | 运行后只生成 JSON |
| identity badge 漂移，导致场景面板无法稳定追溯 | 命名合同层 | 固定 `<scene_key> + <scene_name>` identity badge | 在模板与脚本中统一 badge 生成规则 | 每个 layout 都有稳定 badge |
| `SKILL.md` 与 `references/*.md` 并行演化，导致 scene panel 合同出现第二真源 | 真源治理层 | 把字段表、流程、判型、输出合同全部收回单一 `SKILL.md` | 对该技能固定 `inline-full-spec`，删除旧 reference 规范文件 | 技能目录内不再存在会继续演化的平行规范源 |
| 连续批量任务里场景设计图没有自动成为 panel 生图参照 | SMART bridge 层 | 在 packet 写稳后按 `continuous-batch` 扫描 `2-设计/第N集/` 图像并桥接 `nano-banana/general` | 用共享 bridge 脚本统一 continuity ref 扫描和 request sidecar | request sidecar 中出现正确的场景 continuity refs |

## Repair Playbook

1. 先查 `2-设计/场景设计.json` 是否存在且 `scene_designs[]` 完整。
2. 再查每个场景是否具备 `scene_key / final_scene_prompt / panel_handoff`。
3. 再查模板是否保持 `16:9 + 3x3 + prompt_segments` 结构。
4. 然后检查 `场景面板.json` 与 `<scene_key>-layout.json` 是否同源。
5. 最后确认运行结果停在 JSON，而不是越权进入出图。

## Reusable Heuristics

- 场景面板最稳的上游不是导演 JSON，而是已经被 `2-设计` 收束过的 `final_scene_prompt + panel_handoff`。
- 只要 `panel_handoff` 已经存在，`3-面板` 就不应该重新解释世界观和空间逻辑，而应该把它们整理成更稳定的展示布局 prompt。
- `场景面板.json` 负责 machine-first 批量消费，逐场景 `*-layout.json` 负责局部追溯与下游 handoff；两者必须同源，不能各自生长。
- 面板阶段最容易越权到“直接生图”，但当前仓的真边界是 `4-Design` 负责 carrier，`5-Image` 负责图像生成。
- 当一个叶子技能的复杂度主要来自判型、写回和汇流，而不是来自跨文件规则族时，`inline-full-spec` 往往比 `SKILL + references` 更稳，因为读者在一个文档里就能完成定位、判断和执行。
- 场景面板的高质量不来自“写更多文案”，而来自逐节点锁定：输入体检、design_state 判型、主 prompt 收束、negative 合成、双层 carrier 同源写回。
- 场景面板若启用自动生图，应该先把 `prompt / negative_prompt / panel_handoff` 固化进 packet，再让 SMART bridge 决定是 I2I 还是 T2I，而不是在模型调用前临时重组。
