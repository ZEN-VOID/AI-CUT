# Changelog

## 2026-06-09

- 同步新版 LibTV 项目空间 / 画布分层口径：产品层项目空间由 `projectSpaceId` / `folderId` 表达，可包含多个画布；CLI legacy `projectUuid` / `uuid` / `-p --project` 指具体画布 UUID。
- 更新 `commands/project.md`，补充 `--folder-id`、`update`、`delete/rm` 和 `projectSpaceId/folderId` 字段说明。
- 同步 `node`、`group`、`upload`、`script`、`image` 和示例文档中的 `-p/--project` 说明，避免把项目空间 ID 误传为画布 UUID。
