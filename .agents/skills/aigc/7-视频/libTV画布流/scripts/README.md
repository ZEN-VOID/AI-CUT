# Scripts

本目录仅保存本技能的机械辅助脚本和说明。不得复制、不改写 `.agents/skills/cli/libTV/scripts/` 官方脚本。

## Official Scripts

使用以下官方脚本：

```bash
.agents/skills/cli/libTV/scripts/create_session.py
.agents/skills/cli/libTV/scripts/query_session.py
.agents/skills/cli/libTV/scripts/change_project.py
.agents/skills/cli/libTV/scripts/upload_file.py
.agents/skills/cli/libTV/scripts/download_results.py
```

本技能远端调用优先通过本地 wrapper 加载仓库根 `.env` 后转调用官方脚本：

```bash
python3 .agents/skills/aigc/7-视频/libTV画布流/scripts/run_libtv_with_env.py create_session.py "把全部工作流和结果都放在画布上。..."
python3 .agents/skills/aigc/7-视频/libTV画布流/scripts/run_libtv_with_env.py query_session.py SESSION_ID --project-id PROJECT_UUID
python3 .agents/skills/aigc/7-视频/libTV画布流/scripts/run_libtv_with_env.py upload_file.py /path/to/ref.png
```

`run_libtv_with_env.py` 的职责只限于：

- 定位仓库根。
- 读取 `.env` 并补齐 `LIBTV_ACCESS_KEY`。
- 校验目标脚本属于官方 libTV scripts allowlist。
- 原样转调用官方脚本和参数。

## Boundary

- 脚本只能做机械读取、上传、查询、下载、校验和计划投影。
- 不得让脚本生成分镜组创作正文。
- 默认不下载，除非用户显式要求。
- wrapper 不得绕过官方脚本，也不得改写官方 API 逻辑。
