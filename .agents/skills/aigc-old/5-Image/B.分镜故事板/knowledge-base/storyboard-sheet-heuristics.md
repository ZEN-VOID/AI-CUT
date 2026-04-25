# Storyboard Sheet Heuristics

## Stable Heuristics

- 组级 storyboard 的消费单位是 `分镜组ID`，不是单个 `分镜ID`。
- 多格故事板 prompt 必须保留组内镜头顺序，否则后续生图会得到漂亮但不可追溯的拼贴图。
- `source_shot_ids` 是后续参照绑定、视频首帧参照与审查回链的关键字段，不应被省略。
- 参照绑定时优先角色与主空间；泛词道具很容易造成过量绑定。
- provider handoff 的完成只代表提交包稳定，不代表图像已经生成。

## Common Failure Signals

- request JSON 中 `source_shot_ids` 只有一个元素。
- prompt 只写整组剧情，没有按镜头展开。
- `reference_images` 因 prompt 全文泛扫绑定了一批弱相关资产。
- `submit-plan.json` 的 `provider` 仍是 `dual_mode`。
- 输出图片路径写入 `Assets/`，但 submit 包目录没有 canonical 结果。

## Recovery Pattern

1. 回到 `S1` 确认对象是组级。
2. 回到 `S2` 重建组级设计块和多镜融写列。
3. 回到 `S5` 保守绑定强证据引用。
4. 回到 `S7` 锁唯一 provider。
5. 回到 `S9` 写清跳过链、执行链和返工入口。
