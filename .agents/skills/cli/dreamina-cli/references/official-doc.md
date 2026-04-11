# Dreamina CLI Official Notes

本文件整理官方资料与本机 `dreamina -h` 实测帮助信息，供 `dreamina-cli` 技能按需加载。

当前核验基线：
- 核验日期：`2026-04-03`
- 本机官方 CLI build：`4946b9d`
- build time：`2026-03-31T07:24:44Z`

## 1. 快速上手

安装命令：

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

推荐最小自检顺序：

```bash
dreamina --help
dreamina login
dreamina user_credit
```

## 2. 登录路径

### 2.1 浏览器登录

```bash
dreamina login
```

- 会尝试拉起默认浏览器并等待本地登录态写入。
- 如果机器无法正常打开浏览器，CLI 会提示 manual import 方案。

### 2.2 调试登录

```bash
dreamina login --debug
```

- 用于回调地址异常、浏览器未拉起、登录过程卡住等情况。
- 会打印额外调试信息，便于定位问题。

### 2.3 Headless 登录

```bash
dreamina login --headless
```

- 更适合 agent、远程环境或不方便操作图形浏览器的场景。
- 官方帮助说明在 Linux 上需要可用的 `google-chrome` 或 `google-chrome-stable`。

### 2.4 重新登录

```bash
dreamina relogin
dreamina relogin --headless
dreamina relogin --debug
```

- `relogin` 会先清掉已有本地凭证，再发起新登录流程。

### 2.5 手动导入登录态

```bash
dreamina import_login_response --file /tmp/dreamina-login.json
cat /tmp/dreamina-login.json | dreamina import_login_response
```

- 适用于另一台机器完成浏览器授权，再把完整 JSON 导回当前环境。
- 官方明确建议：不要依赖聊天窗口粘贴超长 JSON，优先本地文件或 stdin pipe。

## 3. 登录成功自检

```bash
dreamina user_credit
```

返回值为 JSON，常见字段包括：
- `vip_credit`
- `gift_credit`
- `purchase_credit`
- `total_credit`

如果 `dreamina user_credit` 失败，不要继续测试生成命令，先回到登录或环境排障。

## 4. 核心生成命令

所有生成命令本质上都是异步任务。加上 `--poll=<秒数>` 时，CLI 会每秒查询一次，最多等待指定秒数。

- 在等待时间内完成：直接输出最终结果
- 超时仍未完成：先返回 querying 状态，需要后续再用 `query_result`

### 4.1 文生图

```bash
dreamina text2image \
  --prompt="一只戴墨镜的橘猫" \
  --ratio=1:1 \
  --resolution_type=2k \
  --poll=30
```

实测帮助要点：
- `--model_version` 支持 `3.0, 3.1, 4.0, 4.1, 4.5, 4.6, 5.0, lab`
- `3.x` 支持 `1k` 或 `2k`
- `4.x / 5.0 / lab` 支持 `2k` 或 `4k`

### 4.2 文生视频

```bash
dreamina text2video \
  --prompt="镜头推进，一只橘猫从沙发上跳下来" \
  --duration=5 \
  --ratio=16:9 \
  --video_resolution=720p \
  --poll=30
```

实测帮助要点：
- `--model_version` 仅支持 `seedance2.0, seedance2.0fast`
- 默认 `model_version` 是 `seedance2.0fast`
- `duration` 范围为 `4-15`
- `video_resolution` 当前只有 `720p`
- 部分高安全风险模型可能要求先在 Web 端完成合规确认

### 4.3 图生图

```bash
dreamina image2image \
  --images ./input.png \
  --prompt="改成水彩风格" \
  --resolution_type=2k \
  --poll=30
```

实测帮助要点：
- `--images` 需要本地图片路径，可传一个或多个
- `1k` 不支持

### 4.4 图生视频

```bash
dreamina image2video \
  --image ./first_frame.png \
  --prompt="镜头慢慢推近" \
  --duration=5 \
  --poll=30
```

实测帮助要点：
- `--image` 需要单个本地首帧路径
- `--model_version` 支持 `3.0, 3.0fast, 3.0pro, 3.0_fast, 3.0_pro, 3.5pro, 3.5_pro, seedance2.0, seedance2.0fast`
- 比例由输入图片推断，不单独传 `--ratio`

### 4.5 多模态视频

```bash
dreamina multimodal2video \
  --image ./ref-1.png \
  --image ./ref-2.png \
  --prompt="@图1 为角色身份锚点，@图2 为场景锚点；保持一致性" \
  --model_version=seedance2.0 \
  --duration=5 \
  --ratio=16:9 \
  --video_resolution=720p \
  --poll=30
```

实测帮助要点：
- `--model_version` 仅支持 `seedance2.0, seedance2.0fast`
- 当前这是 CLI 暴露的最强多模态视频入口
- 至少需要一个 `--image` 或 `--video`
- 图片输入上限为 `<=9`

### 4.6 多帧故事视频

```bash
dreamina multiframe2video \
  --images ./a.png,./b.png,./c.png \
  --transition-prompt="从A过渡到B" \
  --transition-prompt="从B过渡到C" \
  --poll=30
```

实测帮助要点：
- 不提供 `--model_version` 切换
- 不提供 `--video_resolution` 覆盖
- 更适合多帧叙事过渡，不适合通用多参考图锁定

## 4.x 视频模型矩阵速查

| 子命令 | 当前官方暴露的 `model_version` | 备注 |
| --- | --- | --- |
| `dreamina text2video` | `seedance2.0`, `seedance2.0fast` | 默认 `seedance2.0fast` |
| `dreamina multimodal2video` | `seedance2.0`, `seedance2.0fast` | 仅 Seedance 2.0 家族 |
| `dreamina image2video` | `3.0`, `3.0fast`, `3.0pro`, `3.0_fast`, `3.0_pro`, `3.5pro`, `3.5_pro`, `seedance2.0`, `seedance2.0fast` | 视频模型面最宽 |
| `dreamina multiframe2video` | 无 `--model_version` | 不支持模型切换 |

结论：
- 当前官方 CLI 没有在这些视频子命令中暴露 `seedance1.5pro`
- 如果目标是 `3.5pro`，应优先走 `dreamina image2video`

## 5. 异步结果与历史记录

### 5.1 查询单个任务

```bash
dreamina query_result --submit_id=<your_submit_id>
dreamina query_result --submit_id=<your_submit_id> --download_dir=./downloads
```

### 5.2 查看任务历史

```bash
dreamina list_task
dreamina list_task --gen_status=success
dreamina list_task --submit_id=<your_submit_id>
```

实测帮助要点：
- `list_task` 还支持 `--gen_task_type`、`--limit`、`--offset`

## 6. FAQ 摘要

### Q1. 登录成功后还是提示无权限或失败？

先检查两件事：
1. `~/.dreamina_cli/config.toml` 是否存在且内容正常
2. `dreamina user_credit` 是否成功返回 JSON

### Q2. 浏览器登录卡住怎么办？

优先重试：

```bash
dreamina login --debug
```

### Q3. `--poll` 超时了怎么办？

记下 `submit_id`，稍后执行：

```bash
dreamina query_result --submit_id=<your_submit_id>
```

### Q4. 怎么切换账号？

```bash
dreamina relogin
```

### Q5. 怎么清掉本地登录信息？

```bash
dreamina logout
```

注意：
- `logout` 只清凭证
- 不会删除 `config.toml`
- 不会删除 `tasks.db`

## 7. 本地文件语义

Dreamina CLI 会在用户主目录维护这些关键文件：

- `~/.dreamina_cli/config.toml`
  - 环境配置文件，决定请求发往哪里
- `~/.dreamina_cli/credential.json`
  - 本地登录凭证
- `~/.dreamina_cli/tasks.db`
  - 本地任务记录数据库
- `~/.dreamina_cli/logs/`
  - 运行日志目录

推荐排障顺序：
1. `config.toml`
2. `credential.json`
3. `tasks.db`
4. `logs/`

## 8. 真实二进制优先原则

若官方文档与当前本机二进制存在细小差异，优先以：

```bash
dreamina <subcommand> -h
```

为准，再回写技能或排障结论。
