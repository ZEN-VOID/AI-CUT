# Output Template

## Output Contract Alignment

本文件是 `1-Planning` 模板层的对齐索引，不直接生成项目产物。实际业务模板见同目录 `episode-split-plan.template.json`、`grouping-output.template.md` 与 `grouping-report.template.md`。

| marker | rule |
| --- | --- |
| Required output | 只允许回指 `SKILL.md` `Output Contract` 中声明的 `OUTPUT-*`。 |
| Output format | Markdown 正文、Markdown 报告与 JSON 索引必须分别匹配对应 output_id。 |
| Output path | 模板内声明的 `output_path` 必须等于对应 canonical 输出位置。 |
| Naming convention | 逐集正文文件使用 `第N集.md`；分集、格式、分组报告均使用各自子目录下唯一 `执行报告.md`；分组标题使用三段式 `分镜组ID`。 |
| Completion gate | 模板只是结构骨架；输出仍必须通过 validator 或 review gate 后才可宣布完成。 |

## Template Registry

| template | output_id | Output path | Output format |
| --- | --- | --- | --- |
| `episode-split-plan.template.json` | `OUTPUT-SPLIT-PLAN` | `projects/aigc/<项目名>/1-Planning/episode-split-plan.json` | JSON 机读索引 |
| `script-format-report.template.md` | `OUTPUT-SCRIPT-REPORT` | `projects/aigc/<项目名>/1-Planning/2-格式/执行报告.md` | Markdown 执行报告 |
| `grouping-output.template.md` | `OUTPUT-GROUPED-SCRIPT` | `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` | Markdown grouped script |
| `grouping-report.template.md` | `OUTPUT-GROUPING-REPORT` | `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md` | Markdown 执行报告 |
