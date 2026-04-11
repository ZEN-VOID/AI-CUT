# 漫画 VSM 策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SB-COMIC-01 | 输入 | 分镜组结构是否完整 | `ready/incomplete` | 检查 `分镜组ID/剧本正文/组间设计/分镜明细` | P0 |
| V-SB-COMIC-02 | prompt 内容块 | `comic_page_group` 内容块是否完整 | `ready/partial` | 检查组级字段、镜级顺序与漫画硬门槛是否齐全 | P1 |
| V-SB-COMIC-03 | 输出要求 | 本轮只要 JSON 还是 JSON+manifest | `json_only/full_trace` | 结合用户目标与父级要求 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SB-COMIC-01 | `V-SB-COMIC-01=incomplete` | 1.0 | 互斥全部生成路由 | 无 |
| C-SB-COMIC-02 | `V-SB-COMIC-02=ready` | 0.95 | 互斥 C-SB-COMIC-03 | 可并发 C-SB-COMIC-04 |
| C-SB-COMIC-03 | `V-SB-COMIC-02=partial` | 0.90 | 互斥 C-SB-COMIC-02 | 可并发 C-SB-COMIC-04 |
| C-SB-COMIC-04 | `V-SB-COMIC-03=full_trace` | 0.90 | 无 | 可并发 C-SB-COMIC-02/C-SB-COMIC-03 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SB-COMIC-01 | S-COMIC-BACKTRACK | 停止并报告上游缺口 | 不伪造缺失组或镜头事实 | S-COMIC-PAUSE | 上游缺口持续存在 |
| C-SB-COMIC-02 | S-COMIC-MAINLINE | 用完整 `comic_page_group` 填充共享模板 | 固定前缀、漫画硬门槛、组级字段和镜级顺序全部成立 | S-COMIC-PAUSE | 模板字段被局部删改 |
| C-SB-COMIC-03 | S-COMIC-PARTIAL | 保守填充已有内容，不虚构缺失字段 | 输出仍可回链真实上游内容 | S-COMIC-PAUSE | 缺口影响后续生成消费 |
| C-SB-COMIC-04 | S-COMIC-FULL-TRACE | 输出 JSON + manifest | 两文件互相可追溯 | S-COMIC-MAINLINE | 本轮只要求 `json_only` |

## 路由与回退卡

- 默认判定顺序：`shared group list -> comic_page_group 内容完整度 -> 输出模式`
- unknown 默认路由：仍按 `json_only` 执行，但必须显式说明哪些字段保守留空
- 停止条件：无法从 shared schema 确认分镜组结构，或共享模板字段骨架被破坏
