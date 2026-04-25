# CHANGELOG.md

本文件记录 `aigc/2-Global` 的结构性改动，不参与默认预加载。

## 2026-04-24

- `Case-20260424-AIGC-GLOBAL-SHARED-RETIREMENT`
  - 按 Skill 2.0 canonical 目录口径，回收 `2-Global/_shared/` 内部非标准分区。
  - 将 `_shared/episode_root.json` 迁为 `templates/episode-root.template.json`，明确它只是按集 JSON 填写模板，不是项目运行时输出名。
  - 将 `_shared/IO_CONTRACT.md` 与 `_shared/branch-output-contract.md` 迁为 `references/io-contract.md` 与 `references/writeback-contract.md`，同步更新 `SKILL.md`、README、CONTEXT、review、共享 handoff 与审计脚本引用。
  - 补充 `templates/output-template.md` 作为 Skill 2.0 结构校验索引，并在模板说明中明确它不是业务输出内容模板。

- `Case-20260424-AIGC-GLOBAL-TEMPLATES-DEMOTION`
  - 删除 `templates/全局风格.template.md`、`templates/全集类型元素.template.md`、`templates/导演意图.template.md`，避免被误读为新链路业务输出内容模板。
  - 新增 `templates/README.md`，明确 `templates/` 不再承载 2-Global creative output template；唯一填写模板是 `templates/episode-root.template.json`。
  - 同步更新 `SKILL.md`、README、TODO 与 `scripts/aigc_skill_audit.py`，让旧 Markdown 模板重现时触发审计失败。

- `Case-20260424-AIGC-GLOBAL-SKILL-INPUT-OUTPUT-SPINE`
  - 将 `SKILL.md` 重写为 input/output 首尾合同：主文件只保留必需输入、可选输入、禁止输入、按集 JSON 输出、治理侧车、字段门禁与目录导引。
  - 将项目运行时 creative 输出从固定 `episode_root.json` 收束为 `projects/aigc/<项目名>/2-Global/第N集.json`；`templates/episode-root.template.json` 保留为模板名。
  - 同步更新 `references/io-contract.md`、`references/writeback-contract.md`、`_shared/group_design_seed_contract.md`、`_shared/project-runtime-layout.md`、入口元数据与审计脚本，避免固定根文件与按集文件双真源。

- `Case-20260424-AIGC-GLOBAL-GROUP-TYPE-PROJECTION-REMOVAL`
  - 依据 `templates/episode-root.template.json` 的新输出模板基准，移除独立 `分组类型元素.md / 分组类型元素.template.md` 载体。
  - 保留组级类型能力链，但唯一落点收束为 `groups[].global.类型元素`，避免文件级投影与 JSON 字段形成双真源。
  - 同步更新 `SKILL.md`、I/O 合同、branch 输出合同、compat 投影规则、`全集类型元素` 与 `导演意图` 模板、README、TODO 和仓库审计脚本。

- `Case-20260424-AIGC-GLOBAL-SKILL20-STYLE-BEST-PRACTICE`
  - 按 `skill-工作车间` 的 `incremental_upgrade` 路径补齐 Skill 2.0 最小分区：`README.md`、`review/`、`steps/`、`types/`、`knowledge-base/`。
  - 新增 `references/全局风格词最佳实践.md`，将真人版古装影视写实摄影基线明确接入 `project_global.全局风格` 与 `groups[].global.全局风格`。
  - 新增 `steps/全局风格词生成流程.md`、`types/type-map.md`、`review/review-contract.md` 与 `knowledge-base/global-style-heuristics.md`，将风格词生成、分型改写、审计门和经验层拆到稳定 owner。
  - 更新 `SKILL.md`、字段映射、思行网络、I/O 合同、`全局风格.template.md`、`CONTEXT.md` 与 `agents/openai.yaml`，把旧模板中的动画/国漫并列示例回收为非默认路径，避免污染真人古装写实风格。

## 2026-04-23

- `Case-20260423-AIGC-GLOBAL-ZHI-XING-SKELETON-UPGRADE`
  - 按 `skill-知行合一` 口径，把 `2-Global/SKILL.md` 升级为 `单技能知行合一 + skeleton-first` 主合同。
  - 新增 `Mode Selection`、`Single-Skill Positioning`、`Thinking-Action Node Contract` 与 4 张 Mermaid，把线性说明收束为 `N1-N7` 思行网络。
  - 新建 `references/思行网络.md`、`references/字段与验收映射.md`、`references/增量写回与兼容投影.md`，将字段表、patch 细则与 compat 规则下沉出主合同。
  - 同步更新 `CONTEXT.md` 与 `agents/openai.yaml`，让入口摘要、经验层与新骨架保持一致。

## 2026-04-15

- `Case-20260415-AIGC-GLOBAL-ROOT-FILE-CANONICALIZATION`
  - 将 `2-Global` canonical 输出从目录化旧结构收束为根层四文件：`全局风格.md`、`导演意图.md`、`全集类型元素.md`、`分组类型元素.md`。
  - 拆分原 `类型元素.template.md` 为 `全集类型元素.template.md` 与 `分组类型元素.template.md`，并同步 `SKILL.md`、`IO_CONTRACT.md`、`agents/openai.yaml`、bootstrap skeleton、审计脚本和下游读取 fallback。
  - 将旧 `2-Global/类型元素.md` 和 `全局风格/类型元素/设计元素` 子目录降级为旧项目迁移 fallback，禁止新输出继续生成。

- `Case-20260415-AIGC-GLOBAL-THINKING-ACTION-NODE-ENRICHMENT`
  - 将思行网络从“三链并发”细化为“全局风格、全集类型、分组类型、导演意图预解构/定稿”四输出面。
  - 新增 `N3B-TYPE-BIBLE`、`N3C-GROUP-TYPE-PROTOCOL`、`N3D-DIRECTOR-PREP` 的依赖关系：`全集类型 -> 分组类型 -> 约束汇流 -> 导演意图定稿`。
  - 将类型细化步骤拆成 `TB*` 与 `GT*` 两套表，并在四个模板中加入思行节点对照槽位。

## 2026-04-12

- `Case-20260412-AIGC-GLOBAL-STAGE-BOOTSTRAP`
  - 新建 `2-Global` 父 skill、经验层、shared I/O、三份输出模板与 `agents/openai.yaml`。
  - 同步把仓内显式旧路径 `.agents/skills/aigc/2-组间/*` 切换到 `.agents/skills/aigc/2-Global/*`。

- `Case-20260412-AIGC-GLOBAL-ZHI-XING-INTERNALIZATION`
  - 将 `2-Global` 从“父 skill + 导演组外置 contracts”重构为知行合一的单技能并发链。
  - 把 `全局风格 / 类型元素 / 导演意图` 三条能力链全部内收进 `SKILL.md`，不再依赖外置导演组 contracts 作为执行真源。
  - 重写 `SKILL.md`、`CONTEXT.md`、`references/io-contract.md`、三个模板、`agents/openai.yaml`、根 `aigc/SKILL.md` 与 `scripts/aigc_skill_audit.py`，同步删除旧导演组 contracts。
