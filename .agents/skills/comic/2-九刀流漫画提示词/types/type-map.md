# Type Package Map

`types/` 保存九刀流漫画提示词的固定上下文类型包。每次调用技能时，先根据输入选择一个或多个包，再把命中包作为固定上下文加载；`knowledge-base/` 只做按需经验检索。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `grouped-script` | `types/grouped-script/` | 已存在 `第N组.md`、上游 1 号阶段已完成分组、用户明确要求按组跑九刀 | stackable | `types/grouped-script/grouped-script.md` | none | none |
| `raw-source-fallback` | `types/raw-source-fallback/` | 只有 raw source，没有 `第N组.md` 或 stage-1 产物 | stackable | `types/raw-source-fallback/raw-source-fallback.md` | none | none |
| `multi-episode-continuity` | `types/multi-episode-continuity/` | 用户提到第 2 集/第 3 集、目录已有其他集 JSON、需要保持前集角色和风格 | stackable | `types/multi-episode-continuity/multi-episode-continuity.md` | none | none |
| `poster-aware-handoff` | `types/poster-aware-handoff/` | 下游 4 号剧集海报需要把 panels、角色、场景和风格锚点提炼为海报高光候选 | stackable | `types/poster-aware-handoff/poster-aware-handoff.md` | none | none |
| `漫画/体育竞技` | `types/漫画/体育竞技/` | 体育竞技、运动、球类、训练、对手、逆转 | stackable | `types/漫画/体育竞技/体育竞技.md`, `types/漫画/体育竞技/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/历史武侠` | `types/漫画/历史武侠/` | 武侠、江湖、侠义、门派、古风武侠 | stackable | `types/漫画/历史武侠/历史武侠.md`, `types/漫画/历史武侠/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/喜剧` | `types/漫画/喜剧/` | 喜剧、搞笑、颜艺、包袱、反应、节奏停顿 | stackable | `types/漫画/喜剧/*.md`, `types/漫画/喜剧/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/少年战斗冒险` | `types/漫画/少年战斗冒险/` | 少年战斗、热血、冒险、中二、命名战斗、宿敌、宣言 | stackable | `types/漫画/少年战斗冒险/*.md`, `types/漫画/少年战斗冒险/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/恐怖怪谈` | `types/漫画/恐怖怪谈/` | 恐怖、怪谈、惊悚、灵异、空间异常 | stackable | `types/漫画/恐怖怪谈/*.md`, `types/漫画/恐怖怪谈/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/情感关系剧` | `types/漫画/情感关系剧/` | 狗血、虐恋、豪门拉扯、高情绪、关系翻转 | stackable | `types/漫画/情感关系剧/*.md`, `types/漫画/情感关系剧/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/推理悬疑` | `types/漫画/推理悬疑/` | 推理、悬疑、侦探、线索机关、翻页悬念 | stackable | `types/漫画/推理悬疑/*.md`, `types/漫画/推理悬疑/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/日常治愈` | `types/漫画/日常治愈/` | 日常、治愈、温馨、生活切片、小事成章 | stackable | `types/漫画/日常治愈/日常治愈.md`, `types/漫画/日常治愈/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/社会职场` | `types/漫画/社会职场/` | 职场、现实、行业剧、社会派、制度压力 | stackable | `types/漫画/社会职场/社会职场.md`, `types/漫画/社会职场/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/科幻机甲` | `types/漫画/科幻机甲/` | 科幻、机甲、赛博、未来战争、人机关系 | stackable | `types/漫画/科幻机甲/科幻机甲.md`, `types/漫画/科幻机甲/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/青春恋爱` | `types/漫画/青春恋爱/` | 青春恋爱、甜宠、校园、心动、暧昧 | stackable | `types/漫画/青春恋爱/*.md`, `types/漫画/青春恋爱/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |
| `漫画/黑暗奇幻` | `types/漫画/黑暗奇幻/` | 黑暗奇幻、灾厄、诅咒、献祭、深渊 | stackable | `types/漫画/黑暗奇幻/*.md`, `types/漫画/黑暗奇幻/meta.yaml` | none | `grouped-script` or `raw-source-fallback` |

## Default Package Rule

1. 若 `projects/comic/[项目名]/1-漫画剧本改编/第*.组.md` 存在，默认加载 `grouped-script`。
2. 若用户只给 raw source，加载 `raw-source-fallback`；一旦临时切出 group，后续仍按 group 单位执行。
3. 若检测到多集命名、前序 `第N集-page-group-*` 或用户要求延续前集视觉 DNA，叠加 `multi-episode-continuity`。
4. 若用户提到剧集海报、海报高光、4 号阶段或海报生图，叠加 `poster-aware-handoff`。
5. 若上游 `type_stack_ref.secondary[]`、用户题材词或 tone 命中 `types/漫画/<题材>/meta.yaml` 的目录名/aliases，则叠加对应漫画题材包。
6. 如果输入没有明确题材，默认只加载模式包；不得凭空套用漫画题材包。
7. 如果输入没有明确模式，默认 `grouped-script`；缺少分组文件时回退 `raw-source-fallback`。

## Loading Flow

1. `N1-INTAKE` 收集用户输入、项目路径、上游文件、输出目标和下游阶段。
2. 读取本 `types/type-map.md`，选择命中的类型包。
3. 加载命中包的 `context_files` 作为固定上下文。
4. `steps/nine-blade-workflow.md` 消费类型上下文，选择来源前奏、切组、continuity 和 handoff 分支。
5. 需要补充风格、版式、文字或提示词经验时，再检索 `knowledge-base/comic-prompt-heuristics.md`。
6. `review/review-contract.md` 按命中类型包检查输出。

## Anti-Patterns

- 不要把 `第N组.md` 拼回整篇再产出唯一整集 JSON。
- 不要把 raw source fallback 输出成第二份 canonical group plan。
- 不要在多集项目里覆盖旧 `nine_blade_comic_prompts.json`。
- 不要让动画 handoff 只剩一条页级大 prompt；必须保留 `panels[]`。
