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
2. `projects/aigc/<项目名>/8-视频/**/<group_id>.mp4`
3. `projects/aigc/<项目名>/8-视频/**/<group_id>-*.mp4`
4. 若只给 episode，搜索 `第N集/` 下的规范文件。

## 8-视频 Handoff

`8-视频` 生成或下载素材时必须把 sessionId、remote task id、provider id 写入 queue / results / report，不写进 canonical 视频文件名。需要保留多个候选时，使用 `-a`、`-b`、`-c` 变体后缀。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 视频文件名是否使用 canonical `group_id.mp4` 或 `group_id-variant.mp4`，且 `group_id` 是三段式 `episode-scene-group`？ | `GATE-REVIEW-13` | `FAIL-REVIEW-NAMING` | `steps/video-review-workflow.md#N1 Intake` + `references/video-naming-contract.md#Canonical Names` | 审片报告记录 `video_path`、解析出的 `group_id`、`variant` 和 `naming_status`；不规范时记录 `naming_drift`。 |
| 同组多候选是否只使用小写字母 `a`、`b`、`c` 作为 variant，而没有把 sessionId、remote task id 或 provider id 塞进 canonical 文件名？ | `GATE-REVIEW-13` | `FAIL-REVIEW-NAMING` | `references/video-naming-contract.md#Canonical Names` + `references/video-naming-contract.md#8-视频 Handoff` | 报告列出候选文件与 variant 解析；外部 id 只能回指 queue / results / report 证据。 |
| `.mp4` 是否作为视频审片 canonical 扩展名；`.mp3` 或其他扩展是否被标注为 `extension_drift`，且没有被当作通过命名规范的视频素材？ | `GATE-REVIEW-13` | `FAIL-REVIEW-NAMING` | `references/video-naming-contract.md#Extension Rule` + `steps/video-review-workflow.md#N7-VERIFY` | 报告记录扩展名、素材类型判断和 `extension_drift`；若用户要求审音频，verdict 不得写成视频成片命名通过。 |
| 搜索候选时是否按直接路径、`8-视频/**/<group_id>.mp4`、`8-视频/**/<group_id>-*.mp4`、`第N集/` 规范文件的顺序定位，避免先凭画面猜 group？ | `GATE-REVIEW-13` | `FAIL-REVIEW-NAMING` | `references/video-naming-contract.md#Search Order` + `steps/video-review-workflow.md#N1 Intake` | 报告或工作记录写明搜索路径、命中候选和唯一性；无法唯一定位时阻断或最小澄清。 |
| 从命名进入 `5-分组` 前，是否能稳定锁定 project root、episode、group_id 和 variant，并把命名漂移带入后续审片而非静默忽略？ | `GATE-REVIEW-13` | `FAIL-REVIEW-NAMING` | `steps/video-review-workflow.md#N1 Intake` + `steps/video-review-workflow.md#N7-VERIFY` | `input lock` 证据包含 project root、episode、group_id、variant、naming_drift / extension_drift；最终 verify 复查命名状态。 |
