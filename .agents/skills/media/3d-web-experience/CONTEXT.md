# CONTEXT.md

## Purpose & Loading Contract

- 本文件是该技能的经验上下文知识库（不是执行日志）。
- 技能每次被调用时，应自动预加载同目录 `CONTEXT.md`，用于策略选择、避坑与修复分支决策。
- 若 `SKILL.md` 与 `CONTEXT.md` 发生冲突，优先级遵循：用户显式请求 > AGENT.md / 元规则 > SKILL.md > CONTEXT.md。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对当前技能上下文做定向压缩与结构整理。
  - critical: 先归档旧案例，再继续大规模追加。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 3D 方案过重导致加载或交互退化 | SKILL 合同层 | 回退到更轻的 3D 栈或减少模型复杂度 | 在选型前先判断业务目标、设备预算和降级方案 | 检查首屏加载、FPS 和移动端体验 |
| 模型资源未优化导致场景卡顿 | 规则应用层 | 压缩 GLB、简化材质和纹理、减少 draw calls | 在资产接入前加入模型体积和多边形预算 | 复查包体、内存占用和渲染流畅度 |
| 成功沉淀可复用 3D 场景骨架 | CONTEXT 经验层 | 提炼为场景分层与交互边界 heuristic | 在跨 2+ 3D 页面验证后晋升到 `SKILL.md` | 不同内容类型下仍能保持可维护性 |

## Repair Playbook

1. 识别症状：确认问题是选型不当、模型过重、交互复杂度过高还是移动端退化不足。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修正 3D 栈选择、模型预算和降级契约。
4. 再修局部：调整材质、灯光、相机、交互和滚动联动逻辑。
5. 沉淀经验：把高复用的场景组织方式和预算规则写回知识库。
6. 验证闭环：桌面端和移动端都检查加载、可操作性和电量/发热表现。

## Reusable Heuristics

- 先回答“3D 为这个页面增加了什么”，再决定用 Spline、R3F 还是 Three.js 原生。
- Web 3D 的第一原则通常不是更炫，而是更轻、更稳、更易交互。
- 模型、纹理、灯光和滚动联动要一起看预算，单独优化其中一项通常不够。
