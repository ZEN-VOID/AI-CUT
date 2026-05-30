# 场景提取

从 BYKJ `02-剧本处理` 输出中提取场景资产清单，并为每个 canonical 场景生成 JSON 设计规格。默认直接汇总剧本中的场景标题和 slugline，不重新发明场景名。

默认输入：

```text
output/[项目名]/02-剧本处理/
```

默认输出：

```text
output/[项目名]/05-资产提取/场景提取/
├── 场景清单.json
├── 场景提取报告.json
└── manifest.json
```

核心规则：`source_title` 保留上游原标题；统一索引名写入 `normalized_name`，不得替换原标题。设计规格参考 `aigc/7-设计/场景/2-设计`，但本阶段不默认生成 Markdown 设计稿。
