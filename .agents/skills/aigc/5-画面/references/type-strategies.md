# 5-画面 VSM 策略台

## 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VIS-ROOT-01 | 类型 | 用户需要的是组级故事板、单帧还是漫画页 | `sheet/frame/comic/ambiguous` | 读取任务目标与交付词 | P0 |
| V-VIS-ROOT-02 | 输入 | 现有共享导演数据、锚点或既有画面文件是否足以支撑本轮执行 | `ready/partial/missing` | 读取 `编导/第N集.json`、已有 manifest、历史图片 | P0 |
| V-VIS-ROOT-03 | 一致性 | `4-主体`、参考图或历史出图是否可用于一致性锚定 | `available/partial/missing` | 检查 `projects/<项目名>/主体/` 与 `projects/<项目名>/画面/` | P1 |
| V-VIS-ROOT-04 | 交付 | 本轮主要目标是 prompt 组合、直接出图还是二者兼有 | `prompt_only/generate/mixed` | 结合用户目标与当前文件状态 | P1 |

## 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-VIS-ROOT-01 | `V-VIS-ROOT-02=missing` | 1.0 | 互斥全部产物路由 | 无 |
| C-VIS-ROOT-02 | `V-VIS-ROOT-01=ambiguous` | 0.95 | 无 | 可并发 C-VIS-ROOT-06 |
| C-VIS-ROOT-03 | `V-VIS-ROOT-01=frame` | 0.95 | 互斥 C-VIS-ROOT-04/C-VIS-ROOT-05 | 可并发 C-VIS-ROOT-06 |
| C-VIS-ROOT-04 | `V-VIS-ROOT-01=sheet` | 0.95 | 互斥 C-VIS-ROOT-03/C-VIS-ROOT-05 | 可并发 C-VIS-ROOT-06 |
| C-VIS-ROOT-05 | `V-VIS-ROOT-01=comic` | 0.95 | 互斥 C-VIS-ROOT-03/C-VIS-ROOT-04 | 可并发 C-VIS-ROOT-06 |
| C-VIS-ROOT-06 | `V-VIS-ROOT-03=missing` | 0.90 | 无 | 可并发全部产物路由 |

## 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-VIS-ROOT-01 | S-VIS-BACKTRACK | 停止进入本阶段并回退到 `2-组间 / 3-明细` 补齐共享导演数据或既有文件 | 不得在无共享分镜数据时继续生成画面产物 | S-VIS-PAUSE | 无法补齐上游锚点 |
| C-VIS-ROOT-02 | S-VIS-DEFAULT-SHEET | 以 `分镜故事板` 作为默认主入口 | 只输出一个主入口 | S-VIS-PAUSE | 用户后续补充明确改为单帧或漫画 |
| C-VIS-ROOT-03 | S-VIS-TO-FRAME | 直接路由到 `分镜帧` | 单一 `分镜ID` 可唯一锁定 | S-VIS-DEFAULT-SHEET | 单帧目标描述不够明确 |
| C-VIS-ROOT-04 | S-VIS-TO-SHEET | 直接路由到 `分镜故事板` | 组级边界稳定 | S-VIS-PAUSE | 组级边界不清楚 |
| C-VIS-ROOT-05 | S-VIS-TO-COMIC | 直接路由到 `漫画` | 页级改编目标明确且保持组边界 | S-VIS-DEFAULT-SHEET | 任务只是在要普通故事板 |
| C-VIS-ROOT-06 | S-VIS-SOFT-ANCHOR | 允许一致性资产不足时保守执行，但必须显式说明锚点不足 | 不虚构主体细节、不伪造历史图像连续性 | S-VIS-PAUSE | 任务明确要求强一致性 |

## 路由与回退卡

- 默认判定顺序：`共享导演数据是否就绪 -> 任务目标类型 -> 一致性锚点是否可用 -> 交付模式`
- 默认主入口：`分镜故事板`
- sibling 关系：`分镜故事板` 为 `T1-mainline`；`分镜帧` 与 `漫画` 为 `T2-branch`
- unknown 默认路由：优先 `分镜故事板`，但必须显式标注“本轮按模糊需求保守进入主入口”
- 停止条件：上游无合法 `分镜组列表[] / 分镜明细[]`，或请求同时要求多个互斥产物却未给优先级
