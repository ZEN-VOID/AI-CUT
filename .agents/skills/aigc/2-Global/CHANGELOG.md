# CHANGELOG.md

本文件记录 `aigc/2-Global` 的结构性改动，不参与默认预加载。

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
  - 重写 `SKILL.md`、`CONTEXT.md`、`_shared/IO_CONTRACT.md`、三个模板、`agents/openai.yaml`、根 `aigc/SKILL.md` 与 `scripts/aigc_skill_audit.py`，同步删除旧导演组 contracts。
