# 首帧参照 类型策略细则

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VID-FFR-01 | 输入 | 目标分镜结构是否完整 | `ready/incomplete` | 检查 `分镜组ID/剧本正文/组间设计/目标分镜明细` | P0 |
| V-VID-FFR-02 | 桥段判定 | `剧本正文` 与目标分镜的对应清晰度 | `single_shot/direct_match/ambiguous` | 结合组内分镜数、时间段与动作状态 | P0 |
| V-VID-FFR-03 | 字数预算 | 非固定字段压缩压力 | `normal/tight/underflow` | 估算剧情桥段 + 全局风格后剩余字数 | P1 |

## Case To Strategy Map

| case_id | 触发谓词 | 主策略 | 通过标准 | fallback |
| --- | --- | --- | --- | --- |
| C-VID-FFR-01 | `V-VID-FFR-01=incomplete` | 停止并报告上游缺口 | 不伪造缺失字段 | 回 `2-组间/3-明细` |
| C-VID-FFR-02 | `V-VID-FFR-02=single_shot` | 直接使用整段 `剧本正文` 作为剧情桥段 | 桥段与目标分镜天然一一对应 | 无 |
| C-VID-FFR-03 | `V-VID-FFR-02=direct_match` | 提取与目标分镜直接对应的剧情桥段 | 不引入无关分镜事实 | 无 |
| C-VID-FFR-04 | `V-VID-FFR-02=ambiguous` | 保守压缩到目标分镜可见的最小剧情事实 | 不虚构过渡；manifest 备注原因 | `single_shot` |
| C-VID-FFR-05 | `V-VID-FFR-03=normal` | 用自然语句压缩非固定字段 | `prompt_char_count` 落在 800-1200 | 无 |
| C-VID-FFR-06 | `V-VID-FFR-03=tight` | 把非固定字段压成短语/关键词串 | 固定块不动，整体仍尽量靠近目标窗 | 无 |
| C-VID-FFR-07 | `V-VID-FFR-03=underflow` | 保守保真，不虚构扩写 | 允许低于 800，但 manifest 备注原因 | 无 |
