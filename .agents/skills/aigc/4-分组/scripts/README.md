# Scripts

`4-分组/scripts` 只承载机械辅助：

- 读取 Markdown 分组稿。
- 估算每组纯分镜剧本正文字数，并累计 `分镜N（约X秒）` 的组内显式时长。
- 检查分镜组 ID、必填标题、全局风格固定前置词、组底 YAML 字段、纯分镜剧本正文字数、组内显式时长累计、组间连接件结构、连接件三项 north_star 风格行、连接方法、变化过程、主体运动、运镜设计、透视适应和避免元素字段；连接方法只做非空与“不得只填抽象分类名”的机械检查，旧端点字段 `起点尾帧：` / `目标首帧：` 与旧 `连接件提示：` 为 error。
- 输出校验报告；结构错误和单组显式时长累计超过 18 秒均为 error，低于 850 字或低于约 10 秒的组为 warning，必须交给语义 review 判断是否存在短场景例外或是否需要回填。

脚本不得生成分组边界、组间连接件、角色/场景/道具创作判断或 canonical 分组正文。遇到缺失内容或单组超过 18 秒时，应报错并要求 LLM 或人工回到主创环节修复。validator 只能拦截格式、缺项、连接件三项风格行缺失、连接方法裸分类名、端点字段残留、旧 `连接件提示：`、单组超时和明显结构错误，不能替代分组边界、3-4 秒连接件语义、内部方法论选择、主体运动/运镜描述质量和非尾钩判断。

## Commands

```bash
python3 .agents/skills/aigc/4-分组/scripts/validate_storyboard_groups.py projects/aigc/<项目名>/4-分组/第N集.md
python3 .agents/skills/aigc/4-分组/scripts/validate_storyboard_groups.py projects/aigc/<项目名>/4-分组/
```
