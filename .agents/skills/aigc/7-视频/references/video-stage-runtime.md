# Video Stage Runtime

当前视频阶段 canonical runtime：

```text
projects/aigc/<项目名>/7-视频/
```

## Child Runtime Roots

```text
projects/aigc/<项目名>/7-视频/A-分镜画面参照/
projects/aigc/<项目名>/7-视频/B-分镜故事板参照/
projects/aigc/<项目名>/7-视频/C-主体参照/
```

## Legacy Boundary

- `.agents/skills/aigc/6-Video/` 和 `projects/aigc/<项目名>/6-Video/` 只作为旧链路兼容回读。
- 新提交、队列、下载和执行报告不得默认写入 `6-Video`。
- 从旧路径迁移时必须记录 source path 与 target path。
