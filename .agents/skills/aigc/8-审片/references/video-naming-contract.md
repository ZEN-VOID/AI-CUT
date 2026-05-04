# Video Naming Contract

## Canonical Names

- 单个分镜组视频：`<group_id>.mp4`
- 同组变体：`<group_id>-<variant>.mp4`
- `group_id` 使用三段式：`episode-scene-group`，例如 `1-3-1`
- `variant` 使用小写英文字母：`a`、`b`、`c`

Examples:

```text
1-3-1.mp4
1-3-1-a.mp4
1-3-1-b.mp4
```

## Extension Rule

`.mp4` 是视频审片 canonical 扩展名。`.mp3` 只表示音频或扩展名异常；若用户把视频变体写成 `.mp3`，审片时必须标注 `extension_drift`，不得把它当成通过命名规范的视频素材。

## Search Order

1. 用户直接提供的视频路径。
2. `projects/aigc/<项目名>/7-视频/**/<group_id>.mp4`
3. `projects/aigc/<项目名>/7-视频/**/<group_id>-*.mp4`
4. 若只给 episode，搜索 `第N集/` 下的规范文件。

## 7-视频 Handoff

`7-视频` 生成或下载素材时必须把 sessionId、remote task id、provider id 写入 queue / results / report，不写进 canonical 视频文件名。需要保留多个候选时，使用 `-a`、`-b`、`-c` 变体后缀。
