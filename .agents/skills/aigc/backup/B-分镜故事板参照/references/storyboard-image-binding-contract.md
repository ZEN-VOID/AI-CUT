# Storyboard Image Binding Contract

本文件定义 step2：检查 `projects/aigc/<项目名>/7-图像/B-分镜故事板` 中是否存在对应分镜组 ID 的图像，并把真实路径写入 LibTV YAML。

## Source Roots

固定候选根：

```text
projects/aigc/<项目名>/7-图像/B-分镜故事板/第N集/
projects/aigc/<项目名>/7-图像/B-分镜故事板/第N集/images/
```

## Match Key

- 只以 `group_id` 作为默认匹配键，例如 `1-1-1`。
- 优先匹配 `images/<group_id>.<ext>`。
- 次级匹配同集目录下 `<group_id>.<ext>`。
- 允许扩展名：`png`、`jpg`、`jpeg`、`webp`。
- 不使用角色名、场景名、正文关键词或模糊语义猜测图片。

## Binding Policy

- 命中唯一真实文件时，写入 YAML：

```yaml
reference_images:
  - path: "projects/aigc/<项目名>/7-图像/B-分镜故事板/第1集/images/1-1-1.png"
    role: "storyboard_sheet"
    marker: "@图1"
    source: "7-图像/B-分镜故事板"
reference_status: "found"
```

- 未命中时，写入：

```yaml
reference_images: []
reference_status: "missing_optional"
```

- 多个同优先级候选命中时，标记 `ambiguous` 并阻断该组提交，不得随机选择。
- 所有路径必须真实存在，且位于当前项目根内。
- 参照图只作为 storyboard visual reference；不得反向改写 `5-分组` 的剧情和镜头事实。
- B 路线真实提交给 LibTV 的 `imageList` 只允许 1 张故事板总参照，且必然不超过 9 张；若异常出现多张候选，必须唯一裁决或阻断，不得把多张候选塞入 `imageList`。
- `marker: "@图1"` 只用于 manifest / submit plan 可读映射；`prompt.md` 与远端提交的 canonical 绑定必须落在 final fenced YAML 的 `故事板参照` 对象中，字段至少包含 `name: 故事板总参照`、`role: storyboard_sheet`、`reference_index: 1`、真实 `uploaded_url` 和可选 `image_token`。draft prompt 不提前写这些槽位字段。
- 远端 `*-libtv-submission.txt` 不得把本地 marker 投影为人工 `参照图1` 编号，也不得另起故事板参照说明段；只能复用 final source-first YAML 中的 `故事板参照.reference_index / uploaded_url / image_token` 绑定。

## Review Notes

- 缺图不是失败，只是该组走 `libtv_session_text_only`。
- 有图时默认走 `libtv_session_with_uploaded_references`，远端 `【直接生成请求】` 必须说明 final `故事板参照.reference_index / uploaded_url / image_token` 是分镜故事板视觉参照，不是首帧。
- 若用户显式要求“没有故事板图就跳过视频生成”，可把 `missing_optional` 改为 `skipped_by_user_policy`。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 故事板图候选是否只从 `7-图像/B-分镜故事板/第N集/` 与 `images/` 两个固定根读取？ | `GATE-SBVID-05` | `FAIL-SBVID-REF` | `N4-REF-BIND` | reference manifest 记录 search roots、episode dir、images dir |
| 匹配键是否只使用 `group_id`，且优先 `images/<group_id>.<ext>`、其次同集目录 `<group_id>.<ext>`，没有用角色名、场景名或语义猜图？ | `GATE-SBVID-05` | `FAIL-SBVID-REF` | `N4-REF-BIND` | candidate list 记录 exact match priority 与 rejected fuzzy evidence |
| 绑定图片是否为真实存在的 `png/jpg/jpeg/webp` 文件，并且路径位于当前项目根内？ | `GATE-SBVID-05` | `FAIL-SBVID-REF` | `N4-REF-BIND` | file existence proof、project-root-relative path、extension |
| 未命中故事板图时是否写 `reference_images: []` 与 `reference_status: missing_optional`，没有伪造占位路径或空 URL？ | `GATE-SBVID-05` | `FAIL-SBVID-REF` | `N4-REF-BIND` / `N5-YAML` | reference manifest、batch YAML 显示空引用和 missing reason |
| 多个同优先级候选是否标记 `ambiguous` 并阻断该组提交，而不是随机选择或全部塞入 `imageList`？ | `GATE-SBVID-05` | `FAIL-SBVID-REF` | `N4-REF-BIND` | candidate list、blocked group record、rework entry |
| 参照图是否只作为 storyboard visual reference，没有反向改写 `5-分组` 的剧情、镜头、对白或场景事实？ | `GATE-SBVID-11` | `FAIL-SBVID-FIDELITY` | `N5-YAML` / `N6-REVIEW` | prompt/source 对照、report 中无 reverse rewrite |
| B 路线有图时远端 `imageList` 是否只含 1 张故事板总参照且小于等于 9，异常多候选必须先唯一裁决？ | `GATE-SBVID-06` | `FAIL-SBVID-LIBTV` | `N5-YAML` / `N7-DISPATCH` | batch YAML、submission text、remote params `imageList` |
| `marker: "@图1"` 是否仅用于 manifest / submit plan 可读映射，没有被投影成人工 `参照图1` 编号？ | `GATE-SBVID-09` | `FAIL-SBVID-LIBTV` | `N5-YAML` / `N7-DISPATCH` | manifest 与 submission text 对照，远端提交不含人工 `参照图N` |
| canonical 绑定是否只在 final fenced YAML 的 `故事板参照` 对象中写 `name / role / reference_index / uploaded_url / image_token`，draft 不提前写槽位？ | `GATE-SBVID-08` | `FAIL-SBVID-PROMPT` | `N5-YAML` / `N7-DISPATCH` | draft prompt、final YAML、slot ledger |
| 有故事板图时，远端请求是否说明该图是分镜故事板视觉参照而不是首帧；无图时是否自然降级 `text2video` 或按用户策略跳过？ | `GATE-SBVID-06` | `FAIL-SBVID-LIBTV` | `N5-YAML` / `N7-DISPATCH` | submission text、command_type、skipped_by_user_policy record |
| 缺图、多候选、排除原因等本地说明是否只留在 manifest / report，没有进入远端 `libtv-submission.txt` 污染 prompt？ | `GATE-SBVID-09` | `FAIL-SBVID-LIBTV` | `N5-YAML` / `N6-REVIEW` | manifest / report 含说明，远端提交不含缺图或未入预算文案 |
