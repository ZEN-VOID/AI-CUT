# Request Package

用于默认执行、生成、提交或主流程请求。调用时作为基础固定上下文加载。

## Fixed Context

- 优先读取本技能的 Input Contract、Mode Selection 和 Output Contract。
- 保持 provider、路径、输出命名和完成门禁不漂移。
- 只在需要补充经验时检索 `knowledge-base/`。
