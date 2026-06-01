# 网文类型包索引

本目录保存 `story-drafting-gpt-native` 的网文题材固定上下文包。执行时先加载本索引，再按 `north_star.yaml.genre_contract`、章级 planning 与用户请求选择一个或多个具体题材目录。

## Runtime Selection Rule

- 未能识别更窄题材时，加载本索引作为网文默认边界，并报告具体题材缺口。
- 能识别题材时，加载对应 `types/网文/<题材>/` 中的 Markdown 文件；若同一题材目录存在多个文件，全部作为该题材固定上下文。
- 起草、续写、重写、局部修复和 review 返工都必须保留原项目题材包，不得因为修复模式改写题材真源。

## Default Anchors

`types/type-map.md` 使用若干真实存在的题材文件作为 validator anchor；运行时仍以具体项目命中的题材目录为准。
