# Scripts

本目录只保存 `1-Planning` 融合包的机械辅助脚本。

- `validate_script_output.py`：校验 `script_format` mode 输出；业务显示名为 `2-剧本`。
- `grouping_quantizer.py`：计算 `grouping` mode authoritative 量化字段。
- `postprocess_grouping_output.py`：应用尾钩借焰、渲染报告并调用分组 validator。
- `render_grouping_report.py`：按模板回写 `3-分组/执行报告.md`。
- `validate_grouping_output.py`：校验 grouped script 与执行报告一致性。

脚本不得替代 LLM 生成核心创作正文、剧本策略或组界判断。
