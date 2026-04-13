# CHANGELOG.md

本文件记录 `aigc/2-Global` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-GLOBAL-STAGE-BOOTSTRAP`
  - 新建 `2-Global` 父 skill、经验层、shared I/O、三份输出模板与 `agents/openai.yaml`。
  - 同步把仓内显式旧路径 `.agents/skills/aigc/2-组间/*` 切换到 `.agents/skills/aigc/2-Global/*`。

- `Case-20260412-AIGC-GLOBAL-ZHI-XING-INTERNALIZATION`
  - 将 `2-Global` 从“父 skill + 导演组外置 contracts”重构为知行合一的单技能并发链。
  - 把 `全局风格 / 类型元素 / 导演意图` 三条能力链全部内收进 `SKILL.md`，不再依赖外置导演组 contracts 作为执行真源。
  - 重写 `SKILL.md`、`CONTEXT.md`、`_shared/IO_CONTRACT.md`、三个模板、`agents/openai.yaml`、根 `aigc/SKILL.md` 与 `scripts/aigc_skill_audit.py`，同步删除旧导演组 contracts。
