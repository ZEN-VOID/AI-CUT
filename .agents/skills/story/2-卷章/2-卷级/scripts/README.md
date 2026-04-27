# Scripts

本目录保留 `2-卷级` 的机械辅助入口。当前技能没有专属生成脚本；核心规划内容必须由 LLM 直接完成。

## Allowed Script Roles

- 结构校验。
- 路径存在性检查。
- Markdown 标题或模板完整性检查。
- 只读 dry-run 报告。

## Disallowed Script Roles

- 自动生成卷级故事大纲、章划分、六拍内容、任务线或审美判断。
- 用模板灌字替代 LLM 主创。

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章/2-卷级
python3 scripts/skill_context_audit.py --strict
```
