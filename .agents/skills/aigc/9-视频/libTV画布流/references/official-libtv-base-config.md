# Official LibTV Base Config

本文件保存从 `.agents/skills/cli/libTV` 继承而来的官方基本配置与调用逻辑索引。它是本技能的下游调用边界，不改写官方脚本。

## Official Source

- Skill: `.agents/skills/cli/libTV/SKILL.md`
- Context: `.agents/skills/cli/libTV/CONTEXT.md`
- Scripts:
  - `.agents/skills/cli/libTV/scripts/create_session.py`
  - `.agents/skills/cli/libTV/scripts/query_session.py`
  - `.agents/skills/cli/libTV/scripts/change_project.py`
  - `.agents/skills/cli/libTV/scripts/upload_file.py`
  - `.agents/skills/cli/libTV/scripts/download_results.py`

## Required Environment

```bash
export LIBTV_ACCESS_KEY="your-access-key"
```

在本仓库执行时，`LIBTV_ACCESS_KEY` 默认配置在仓库根 `.env` 中。本技能优先通过 wrapper 自动加载 `.env` 后再转调用官方脚本：

```bash
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py create_session.py "把全部工作流和结果都放在画布上。..."
```

wrapper 只负责定位仓库根、读取 `.env`、校验 `LIBTV_ACCESS_KEY` 并以同一参数调用 `.agents/skills/cli/libTV/scripts/` 下的官方脚本；不得复制、修改或替代官方脚本逻辑。

若直接调用官方脚本，则必须先执行等价环境加载：

```bash
set -a
source .env >/dev/null 2>&1
set +a
```

若 `.env` 缺失或没有有效 `LIBTV_ACCESS_KEY`，应阻断远端调用并报告配置缺口。

Optional:

```bash
export OPENAPI_IM_BASE="https://im.liblib.tv"
export IM_BASE_URL="https://im.liblib.tv"
```

## Preserved Official Calls

```bash
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py create_session.py "把全部工作流和结果都放在画布上。..."
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py create_session.py "追加消息" --session-id SESSION_ID
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py query_session.py SESSION_ID --project-id PROJECT_UUID
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py change_project.py
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py upload_file.py /path/to/ref.png
python3 .agents/skills/aigc/9-视频/libTV画布流/scripts/run_libtv_with_env.py download_results.py SESSION_ID --output-dir OUTPUT_DIR --filename FILE
```

这些命令等价于加载 `.env` 后调用官方脚本；官方脚本路径、参数语义、API 逻辑和输出格式仍以 `.agents/skills/cli/libTV` 为准。

## Canvas Instruction

新建生成或编辑任务时，消息开头必须保留独立操作性指令：

```text
把全部工作流和结果都放在画布上。
```

## AIGC Canvas Flow Override

本技能仅覆盖默认交付策略，不改变官方命令逻辑：

- 官方 CLI 支持下载；本技能默认不自动下载。
- 官方 CLI 支持上传本地文件；本技能主体参照流默认先复用画布上已规范命名、已上传的素材节点。
- 官方 CLI 负责 session 和 projectUrl；本技能只把项目、分镜组、主体绑定表和参数投影成传给 Agent IM 的消息。
