# CHANGELOG

## 2026-05-11

- 将执行后 canonical 解析输出调整为 `全局风格解析.md`、`编剧风格解析.md`、`摄影风格解析.md`、`设计风格解析.md` 与 `分镜脚本.md`。
- 新增五份解析细则：全局风格参照 `global-style-director` 字段逻辑，编剧/摄影/设计分别绑定 2/3/5 阶段边界，分镜脚本固定参照 `input/苍穹裂缝·战神降维.numbers` 的 19 列字段和内容编排方式。
- 同步更新输出模板、review gate、workflow、validator 与 README；旧 `画面风格解析.md`、`编导解析.md`、`摄影解析.md`、`设计解析.md` 仅保留为 legacy mirror 语义。

## 2026-05-04

- 初始化 `.agents/skills/aigc/shot-by-shot` Skill 2.0 包。
- 明确其为 AIGC 根下临摹型卫星技能，服务 `0-初始化`、`2-编导`、`3-摄影` 与 `5-设计`，不替代主链阶段 canonical 写回。
- 建立逐镜证据、解析维度、临摹原则、禁止照搬清单、`画面风格解析.md`、`编导解析.md`、`摄影解析.md` 与 `设计解析.md` 的项目 `CONTEXT/` 输出合同。
- 按 `$skill-知行合一` 要求建立思行网络、Mermaid 拓扑、Field Master、Thought Pass Map、Pass Table 与 `思考过程` 输出槽位。
- 源层同步阶段解析落点：阶段可消费文档归入 `projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/`。
