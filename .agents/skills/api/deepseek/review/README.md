# review

本分区承载 DeepSeek provider skill 的质量评估与验收门禁。

当前最小门禁：

- `--dry-run --print-payload` 能生成合法 payload。
- `scripts/deepseek_chat.py --help` 能正常输出。
- 控制台与报告不得泄露 `DEEPSEEK_API_KEY`。
- 默认输出目录保持 `output/影片/[项目名]/5-API/llm/deepseek/`。
