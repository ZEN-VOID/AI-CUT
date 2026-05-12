# Screenwriter Style Analysis Contract

`编剧风格解析.md` 是 `shot-by-shot` 输出给 `2-编导` 的编剧/戏剧风格 side context。它只提炼戏剧问题、人物压力、场面调度、潜台词行为、叙事节奏和可拍承托，不写机位、景别、焦段、运镜或分镜编号。

## Required Fields

| field | requirement |
| --- | --- |
| `dramatic_question_seed` | 这一段逼角色面对什么选择、代价或不可回避的问题 |
| `audience_position_seed` | 观众知道、误解、等待、担心或被延迟满足的内容 |
| `character_pressure_seed` | 角色目标、阻碍、隐藏信息、外显策略和关系压力 |
| `performance_task_seed` | 可执行身体动作、停顿、视线、呼吸、道具动作 |
| `blocking_power_seed` | 人物站坐、高低、远近、入口、障碍物、权力位置等空间调度 |
| `dialogue_strategy_seed` | 对白密度、沉默、反问、威胁、信息释放或潜台词节奏 |
| `scene_state_delta` | 场景开始与结束时，人物关系、信息权力或局势如何改变 |
| `controlled_enrichment_seed` | 不新增剧情的环境反应、群体反应、声音、道具余波和可拍承托 |
| `do_not_import` | 不得导入参考片台词、剧情、角色关系、标志性动作和具体画面表达 |

## Markdown Shape

`编剧风格解析.md` 至少包含：

1. `## 使用边界`
2. `## 戏剧结构摘要`
3. `## 编剧风格 Seeds`
4. `## 场面调度与表演承托`
5. `## 禁用摄影越权`
6. `## Do Not Import`
