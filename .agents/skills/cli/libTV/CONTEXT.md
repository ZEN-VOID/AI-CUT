# Context: libTV

本文件是 `.agents/skills/cli/libTV` 的经验层知识库。它用于沉淀 LibTV / LibLib.tv Agent-IM 调用中的可复用经验，不重定义 `SKILL.md` 的入口合同。

## Type Map

| type_id | 触发症状 | 可能根因 | 立即修复 | 预防检查 |
| --- | --- | --- | --- | --- |
| `TM-LIBTV-01` | 用户要求 LibTV/LibLib.tv 生成图片或视频 | 路由识别 | 进入生成会话路径 | 用户明确提到 LibTV 时不要改走通用 imagegen |
| `TM-LIBTV-02` | 用户提供本地图片/视频并要求编辑、参考生成或图生视频 | 参考文件交接 | 先上传文件，拿到 OSS URL 后再创建会话 | 提交给 LibTV 的消息只包含 OSS URL，不包含本地路径 |
| `TM-LIBTV-03` | 用户给出 `sessionId` 或要求查看进度/下载 | 会话操作 | 使用查询或下载脚本，不新建会话 | 只有用户要求查询/下载时才执行对应操作 |
| `TM-LIBTV-04` | 提交内容比用户原始需求更华丽或更复杂 | 本地 prompt 越权 | 去掉本地扩写，只保留用户原文、OSS URL 和必要操作性指令 | 最终汇报说明已保持原文传话 |
| `TM-LIBTV-05` | 脚本无法运行并提示缺凭证 | 环境变量缺失 | 停止 API 调用，要求配置 `LIBTV_ACCESS_KEY` | 实时调用前先检查凭证 |
| `TM-LIBTV-06` | 用户希望或流程要求工作流在画布上可见 | 画布操作性指令缺失 | 在新建会话消息开头加入 `把全部工作流和结果都放在画布上。` | 完成汇报包含画布指令状态和 `projectUrl` |
| `TM-LIBTV-07` | 画布链接过早展示 | 输出时机错误 | 生成过程中只说正在生成中，完成后再给 `projectUrl` | 输出合同区分过程中与完成时 |
| `TM-LIBTV-08` | 生成完成但没有本地文件 | 下载环节失败或未执行 | 若用户/合同要求本地文件，运行 `download_results.py` | 完成门禁检查本地文件列表 |

## Repair Playbook

1. 路由不确定时，先判断是生成、编辑/参考、还是 session 操作。
2. 有本地文件时，先确认文件存在且是图片或视频，再调用 `upload_file.py`。
3. 上传成功后，只把返回的 OSS URL 附到用户原始描述中，不把本地路径发给 LibTV。
4. 新建生成或编辑任务时，把 `把全部工作流和结果都放在画布上。` 作为独立操作性指令放在消息开头。
5. 本地 Agent 不扩写、不润色、不翻译、不拆分用户的创作需求，除非用户明确要求做这些转换。
6. API 失败时，先查 `LIBTV_ACCESS_KEY`，再查 `OPENAPI_IM_BASE` / `IM_BASE_URL` 和脚本 stderr。
7. 生成过程中不要提前给用户 `projectUrl`；完成后同时给结果链接、本地文件列表和项目画布链接。
8. 若以后恢复 `steps/`、`review/` 等分区，必须同步更新 `SKILL.md` 的 `Reference Loading Guide`。

## Reusable Heuristics

- LibTV 技能最大的风险不是命令行参数，而是本地 Agent 在提交前越权改写创作需求。
- 画布指令是操作性约束，不是创意增强词；它可以追加到消息里，但不能替代用户原文。
- `projectUuid` 是画布地址的关键真源；`projectUrl` 可由 `https://www.liblib.tv/canvas?projectId=` + `projectUuid` 拼接。
- 文件名前缀只用于本地归档，不应泄漏进创作描述。
- 本地路径只服务上传脚本；LibTV 会话消息应使用 OSS URL。
- 当用户只问进度或下载时，不要创建新会话。
- `.env` 中可存在 `LIBTV_ACCESS_KEY` 供本地使用，但不得提交密钥。
