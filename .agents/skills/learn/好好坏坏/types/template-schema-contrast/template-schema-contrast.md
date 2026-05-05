# Template Schema Contrast

用于分析好/坏示例在输出字段、命名、路径、schema、模板和下游可消费性上的差异。

## Fixed Checks

- 好示例是否满足固定字段、JSON/YAML/Markdown schema、命名规范或路径规范。
- 坏示例是否丢字段、错层级、路径漂移、破坏机器可读结构或混入无法消费的说明文字。
- `templates/output-template.md` 是否与目标 `SKILL.md` Output Contract 五字段一致。
- 脚本是否只做格式投影和校验，没有生成核心判断正文。

## Patch Bias

- 模板字段问题优先修 `templates/`。
- 输出路径和命名规范必须同步目标 `SKILL.md` Output Contract。
- 机器可读校验可落 `scripts/`，但脚本不得替代 LLM 判断。
