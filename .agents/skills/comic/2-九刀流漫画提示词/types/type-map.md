# Type Package Map

`types/` 保存九刀流漫画提示词的漫画题材类型包。每次调用技能时，先根据上游 `type_stack_ref`、用户题材词或剧情 tone 选择一个或多个题材包，再把命中包作为固定上下文加载；来源模式、连续性模式和 handoff 模式归 `steps/source-routing-and-handoff.md`。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | compatible_modes |
| --- | --- | --- | --- | --- | --- | --- |
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

1. 若上游 `type_stack_ref.secondary[]`、用户题材词或 tone 命中 `types/漫画/<题材>/meta.yaml` 的目录名/aliases，则叠加对应漫画题材包。
2. 如果输入没有明确题材，默认不加载漫画题材包；不得凭空套用题材语法。
3. 来源、连续性和下游交接 mode 的选择不在本文件处理，统一读取 `steps/source-routing-and-handoff.md`。

## Loading Flow

1. `N1-INTAKE` 收集用户输入、项目路径、上游文件、输出目标和下游阶段。
2. 读取 `steps/source-routing-and-handoff.md`，选择来源、continuity 和 handoff mode。
3. 读取本 `types/type-map.md`，选择命中的漫画题材类型包。
4. 加载命中题材包的 `context_files` 作为固定上下文。
5. `steps/nine-blade-workflow.md` 消费 mode 与题材上下文，选择来源前奏、切组、continuity 和 handoff 分支。
6. 需要补充风格、版式、文字或提示词经验时，再检索 `knowledge-base/comic-prompt-heuristics.md`。
7. `review/review-contract.md` 按命中 mode 和题材包检查输出。

## Anti-Patterns

- 不要把 `第N组.md` 拼回整篇再产出唯一整集 JSON。
- 不要把 raw source fallback 输出成第二份 canonical group plan。
- 不要在多集项目里覆盖旧 `nine_blade_comic_prompts.json`。
- 不要让动画 handoff 只剩一条页级大 prompt；必须保留 `panels[]`。
