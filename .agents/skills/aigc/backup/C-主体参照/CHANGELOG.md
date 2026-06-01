# Changelog

## 2026-05-11

- 将主体参照上传策略改为同一 LibTV `projectUuid/projectID` 内优先复用同名 active uploaded URL；本地路径和指纹降为可选审计证据。
- 固化图片调整/更换时的 `explicit_replace` 规则：只有用户显式要求替换、更新或重新上传，才重新解析本地图片并上传新 URL。

## 2026-05-10

- 将 C 主体参照视频时长从固定 15 秒改为组级估算投影：读取 `5-分组` 当前组 `时长估算`，按 4-15 秒范围 clamp 后写入 LibTV submit plan 和远端提交。

## 2026-05-05

- 将默认视频基础规格收束为 720P、15 秒、16:9；用户显式指定时才覆盖。
- 将主体名称多候选策略改为先窗口图像上下文自动识图消歧，无法唯一匹配时才进入 `ambiguous` 阻断。

## 2026-04-30

- 将 LibTV 视频生成默认路由改为以 `.agents/skills/cli/libTV` 后端默认路由为中心。

## 2026-04-26

- 初始化 `8-视频/C-主体参照` Skill 2.0 包。
- 固化 `5-分组` 作为视频 prompt 主源，组底 YAML 作为主体参照唯一默认基准。
- 增加 $libTV skill scripts handoff、后台并发批量提交、queue ledger 和项目内输出合同。
