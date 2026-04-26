# deepseek

DeepSeek 官方 API 的 repo-local provider skill，固定模型为 `deepseek-v4-pro`。

## 入口

- `SKILL.md`：技能主合同与路由门禁
- `CONTEXT.md`：经验层与排错策略
- `references/api.md`：DeepSeek API 摘要
- `scripts/deepseek_chat.py`：机械调用、解析与落盘脚本
- `agents/openai.yaml`：产品侧入口元数据

## 最小调用

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --prompt "Hello!" \
  --dry-run --print-payload
```
