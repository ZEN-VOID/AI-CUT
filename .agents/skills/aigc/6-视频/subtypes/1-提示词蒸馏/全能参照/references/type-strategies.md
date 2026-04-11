# 全能参照 类型策略细则

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VID-SUBJ-01 | 输入 | 分镜组结构是否完整 | `ready/incomplete` | 检查 `分镜组ID/剧本正文/组间设计/分镜明细` | P0 |
| V-VID-SUBJ-02 | 字数预算 | 非固定字段压缩压力 | `normal/tight/underflow` | 估算固定块后剩余字数 | P1 |
| V-VID-SUBJ-03 | 输出要求 | 本轮只要 JSON 还是 JSON+manifest | `json_only/full_trace` | 结合用户目标 | P1 |

## Case To Strategy Map

| case_id | 触发谓词 | 主策略 | 通过标准 | fallback |
| --- | --- | --- | --- | --- |
| C-VID-SUBJ-01 | `V-VID-SUBJ-01=incomplete` | 停止并报告上游缺口 | 不伪造缺失字段 | 回 `2-组间/3-明细` |
| C-VID-SUBJ-02 | `V-VID-SUBJ-02=normal` | 用自然语句压缩非固定字段 | `prompt_char_count` 落在 1800-2000 | 无 |
| C-VID-SUBJ-03 | `V-VID-SUBJ-02=tight` | 把非固定字段压成短语/关键词串 | 固定块不动，整体仍尽量靠近目标窗 | 无 |
| C-VID-SUBJ-04 | `V-VID-SUBJ-02=underflow` | 保守保真，不虚构扩写 | 允许低于 1800，但 manifest 备注原因 | 无 |
| C-VID-SUBJ-05 | `V-VID-SUBJ-03=full_trace` | 输出 JSON + manifest | 两文件互相可追溯 | `json_only` |
