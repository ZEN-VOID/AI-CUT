# Type Package: arbitrary-text

适用于用户指定的任意小说、剧本、Markdown、纯文本或贴入文本。

## Fixed Context

- 先记录 `source_path` 或 `source_inline`，不要把任意来源伪装成项目 stage truth。
- 若用户没有指定输出路径，默认写入 source 相邻的 `3-运动/` 子目录。
- 任意来源可能没有标准场景标题或字段，需要用段落、行号或自定义 unit id 作为 `source_anchor`。

## Output Bias

- 文件名默认 `<source_stem>-运动强化.md`。
- 报告必须列出任意来源模式、source 证据和输出路径。
