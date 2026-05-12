# Type Map

## Package Index

| package | path | selection signal | relation |
| --- | --- | --- | --- |
| `subject_reference_flow` | `types/subject-reference-flow.md` | 默认；主体参照图、角色/场景/道具参照、`4-分组` 分镜组出视频 | default |
| `storyboard_reference_flow` | `types/storyboard-reference-flow.md` | 用户显式指定分镜参照流、storyboard reference flow、用分镜图/故事板图参照出视频 | explicit-only |

## Default Package Rule

- 未显式指定路线时，必须加载 `subject_reference_flow`。
- 用户显式指定 `storyboard_reference_flow` 时，加载该包并返回占位执行说明；不得临时借主体参照流伪造分镜参照流。
- 查询、下载、修复任务应根据既有工件所属路线补加载对应类型包；无法判断时先阻断。

## LibTV Seedance 2.0 Standard `modeType`

下表来自 LibTV/Seedance 2.0 `create_generation_task` 工具 metadata。执行视频生成时，`modeType` 必须显式传入下列标准称谓之一；不得只写中文口径、业务别名或本技能内部 `generation_mode`。

| standard `modeType` | 标准称谓 | 媒体数量约束 | 适用场景 | 本技能默认 |
| --- | --- | --- | --- | --- |
| `text2video` | 文生视频 | 只要求 `prompt` | 纯文本生成，无参考图/视频/音频 | 禁止作为主体参照流默认值 |
| `singleImage2video` | 单图生视频 | 1 张图片 | 单张首帧或单主体图驱动视频 | 仅用户显式指定单图生视频时使用 |
| `frames2video` | 首尾帧/关键帧生视频 | 1-2 张图片 | 首帧、尾帧或两关键帧过渡 | 仅用户显式指定首尾帧时使用 |
| `image2video` | 多图参考生视频 | 1-9 张图片 | 仅图片参考，不混入视频/音频参考 | 可显式选择 |
| `audio2video` | 音频驱动/音频参考生视频 | 0-3 个音频 | 音频驱动或音频参考视频 | 仅用户显式指定音频参考时使用 |
| `mixed2video` | 混合/全能参考生视频 | 1-15 个媒体；配置含最多 9 图、3 视频、3 音频 | 多主体、多图或图/视频/音频混合参考 | `subject_reference_flow` 默认 |

ModeType rules:

- `subject_reference_flow` 有任何可用主体参照图时，默认 `modeType=mixed2video`。
- 如果用户明确要求“多图参考但不使用混合/全能参考”，可显式使用 `modeType=image2video`。
- 如果用户明确要求单图、首尾帧、音频参考或纯文生，必须使用对应标准 `modeType` 原文。
- 用户指定 `modeType` 时，submit plan、queue record、manifest 和远端 prompt 都必须记录相同标准值。
- 任何别名都必须在提交前归一为标准 `modeType`；无法唯一归一时阻断，不得提交。
- `text2video` fallback 默认禁止；只有用户当前轮显式授权无参考图继续时才可使用，并必须记录 `text2video_fallback_authorized=true`。

## Loading Flow

1. 读取用户请求、项目路径、集号、分镜组 ID 和已有工件路径。
2. 若出现“分镜参照流 / storyboard reference flow / 用分镜图参照”，选择 `storyboard_reference_flow`。
3. 否则选择 `subject_reference_flow`。
4. 把选中类型包作为固定上下文加载，再进入 `steps/libtv-canvas-workflow.md`。

## Review Gate Mapping

| package | gate |
| --- | --- |
| `subject_reference_flow` | 主体绑定表、标准 `modeType`、时长 clamp、默认规格、画布素材命名、官方 LibTV handoff |
| `storyboard_reference_flow` | placeholder gate：不得提交远端生成任务 |
