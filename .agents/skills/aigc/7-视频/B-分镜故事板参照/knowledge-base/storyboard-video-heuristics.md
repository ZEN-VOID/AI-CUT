# Storyboard Video Heuristics

本文件保存 `B-分镜故事板参照` 可复用经验。强制合同以 `SKILL.md` 与 `references/` 为准。

## Heuristics

- 分镜组视频最容易漂移的是“把组正文重写成短视频广告语”；本技能应优先保留 `4-分组` 的完整内容。
- 多格故事板图对视频模型最有价值的是画面连续性、构图节奏和角色位置，不是首帧精确复制。
- `multimodal2video` 比 `image2video` 更适合“故事板 sheet 参照 + 完整文本提示词”的组合。
- 缺故事板图时用 `text2video` 是正常降级；报告清楚即可，不要为了凑参照去绑定主体图或旧资产图。
- 批量视频任务的真实交付状态通常不是“本轮全部完成”，而是 `submitted / querying / downloaded / failed` 的可继续队列。
- 并发执行的重点是每组 job 独立，不是让多个进程同时维护同一份报告。
