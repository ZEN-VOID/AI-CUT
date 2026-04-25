# Shared Prompt Principles

本文件只记录 `B.分镜故事板参照` 对共享 `图生视频` 句法原则的本地承接方式。

## Shared Source

跨视频叶子的共享原则以 `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md` 为准。

本包只补组级故事板 specialization：

- 先锁住分镜组整体气质，再按组内镜头顺序展开可见动作。
- 故事板或漫画引用只作为视觉连续性锚点，不得反向改写 `3-Detail` 的剧情和镜头事实。
- 多镜组 prompt 要保留镜头切换节奏；不要把整组写成一个没有分镜边界的连续场景描述。
- 引用图顺序以“故事板/漫画 -> 角色 -> 服装”为默认优先级；provider-specific 解析下沉到 `generation-handoff`。

## Local Anti-Patterns

- 只写整组气氛，不写逐镜动作。
- 为迎合故事板图片而改写上游 `剧本正文`。
- 把 `reference_images` 当作 provider 私有字段，提前写死为 URL 或 CLI 参数。
- 把 `第N集.txt` 当唯一真源，漏掉 JSON request packet。
