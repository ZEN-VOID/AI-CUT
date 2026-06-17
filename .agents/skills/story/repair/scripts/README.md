# Scripts

`story-repair` 本级暂不提供主创脚本。脚本只能承担机械辅助：

- `rg` / path discovery / old-term distribution checks
- structured diff and changed-file listing
- schema or report validation
- invoking shared story helpers such as `../scripts/workflow_manager.py`

禁止脚本直接生成小说正文、设定正文、规划正文、repair creative truth 或审美判断。

创作型修复硬标准：

- 不能用脚本做批量生成、批量插入、正则套句或映射投影。
- 必须从上到下逐条理解目标对象，并只把 LLM 判断后的结果按照指定要求落盘。
- 若脚本、模板或正则产物看似可用，仍必须废弃，回到 owning stage 的 LLM-first 节点。
