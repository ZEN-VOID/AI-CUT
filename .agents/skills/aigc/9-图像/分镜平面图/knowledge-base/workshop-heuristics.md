# Floor Plan Heuristics

本文件存放人工维护或稳定沉淀后的分镜平面图经验。自动执行经验优先写入同目录 `CONTEXT.md`，稳定后再晋升到这里或 `SKILL.md`。

## Common Failure Patterns

| pattern | risk | repair |
| --- | --- | --- |
| 把平面图画成故事板 | 角色站位与空间连续性不可审计 | 重写为 top-down architectural floor plan |
| 角色用写实人物 | 图面混入风格和身份渲染问题 | 改成彩色几何图标 + 黑色角色名 |
| 动线颜色语义错 | 下游误判身体运动和摄影机运动 | 固定红=身体，蓝=摄影机 |
| 上下组跳变 | 视频/故事板连续性断裂 | 补 continuity_from_previous |
| 源文本不明确但图面过度确定 | 伪造空间事实 | 写 spatial_inference_basis 和 conservative assumption |

## Practical Notes

- 室内场景优先画墙体、门窗、桌椅、通道、角色站位和摄影机视野锥。
- 室外场景优先画道路、入口、遮挡物、边界线、行进方向和相对距离。
- 有队伍、追逐、对峙时，角色之间的前后/左右/内外关系比装饰细节重要。
- 对话场景也需要摄影机和角色朝向；静止不等于没有空间逻辑。
