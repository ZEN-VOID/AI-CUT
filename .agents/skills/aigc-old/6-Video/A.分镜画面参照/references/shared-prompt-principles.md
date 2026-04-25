# Shared Prompt Principles

本文件承接 `6-Video/_shared/image-to-video-prompt-principles.md` 的共享取向，并在融合包内固定为本地可读引用。

## Principles

1. 只消费 `3-Detail/<episode>.json` 的现有事实，不虚构角色、场景、动作、道具、光线或镜头信息。
2. 优先消费 branch-owned canonical 字段；legacy projection 只作 fallback。
3. 文本应更像“给视频模型的画面与运动指令”，不是字段抄录。
4. 推荐语义顺序：
   - 剧情/桥段锚点
   - 主体识别与服装锚点
   - 风格与世界观锚点
   - 镜头起势：分镜构图、运镜手法、速度、视角、镜头类型兼容
   - 主体动作与空间关系
   - 状态与环境
   - 视觉组织
   - 可选转场
5. 默认使用可朗读自然句；只有预算紧张时才局部短语化。
6. 压缩优先级：先压 legacy/fallback，再压非关键视觉修饰，最后才影响分镜构图、运动表现、角色表现。

## Governance

- 若共享原则需要更新，应优先同步父级 `_shared/image-to-video-prompt-principles.md`，再回写本文件。
- 若只是本融合包局部策略变化，只改 `prompt-distillation-contract.md` 或 workflow 节点。
