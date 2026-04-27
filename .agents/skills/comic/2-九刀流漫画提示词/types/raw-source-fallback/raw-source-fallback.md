# Type Package: raw-source-fallback

## Purpose

用于用户只提供 raw source、没有 `第N组.md` 的兼容场景。此包只允许本轮内部做最小整形与临时切组，不创建第二套长期 canonical 真源。

## Fixed Context

- 先判定 `scene-led / explainer-led / compare`。
- `scene-led` 保留场景动作和对白块。
- `explainer-led` 将摘要压成顺时序事件单元，补人物、场景、转场和视觉动作。
- `compare` 只在输入模糊时双路比较，最终只保留一份 canonical handoff。

## Grouping Rule

- 约 1000 字原文为一个 9 pages 组单元。
- 不满 1000 字的一组直出。
- 长文尾组 300 字以内并入上一组，700 字以上可独立成组，301-699 字默认并入上一组，除非存在明确 scene/hook 边界。
- 自然边界优先于机械字数。

## Review Gate

- 临时 group 不得丢失关键角色、场景、转场、高潮或余波。
- raw source fallback 完成后，后续执行仍按 group 单位进入九刀主流程。
