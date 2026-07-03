# MiniMax Voice Slots

本文件记录当前仓库常用的 MiniMax 自定义声音。真实 API Key 保存在仓库根目录 `.env`，不要写入本文件。

## Active Voice Cloning Slots

MiniMax API 当前对这些官网克隆声音返回的 `voice_name` 为空；官网显示名称需要人工从控制台补充。

| official_name | voice_id | type | source | created_time | status | usage | notes |
|---|---|---|---|---|---|---|---|
| 贝因女声2 | `moss_audio_9e8695bb-6f8d-11f1-938c-a6f6fa6b2a0c` | `voice_cloning` | MiniMax web clone | 2026-06-24 | active | TBD | API `voice_name` is empty. |
| 贝因女声1 | `moss_audio_644a5ef6-6f8d-11f1-83ef-8afcbb8b5b5c` | `voice_cloning` | MiniMax web clone | 2026-06-24 | active | TBD | API `voice_name` is empty. |
| 贝因男声2 | `moss_audio_ba1bbbae-6f8d-11f1-ba6a-025474e1e406` | `voice_cloning` | MiniMax web clone | 2026-06-24 | active | TBD | API `voice_name` is empty; verified with TTS output at `/Volumes/AIGC/AI-CUT/projects/output/minimax-tests/moss_audio_test.mp3`. |

## Check Current Remote Voices

```bash
set -a
. /Volumes/AIGC/AI-CUT/.env
set +a

curl -sS --request POST \
  --url https://api.minimax.io/v1/get_voice \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"voice_type":"voice_cloning"}'
```

## Use A Voice

```bash
cd /Volumes/AIGC/AI-CUT/.agents/skills/cli/mmx-cli

./node_modules/.bin/mmx speech synthesize \
  --text "这里是要生成的文字。" \
  --voice moss_audio_ba1bbbae-6f8d-11f1-ba6a-025474e1e406 \
  --model speech-2.8-hd \
  --out /Volumes/AIGC/AI-CUT/projects/output/minimax-voice-test.mp3 \
  --region=global
```

## Delete A Retired Voice

删除后该 `voice_id` 不能复用。删除前先确认没有项目仍在依赖它。

```bash
set -a
. /Volumes/AIGC/AI-CUT/.env
set +a

curl --request POST \
  --url https://api.minimax.io/v1/delete_voice \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "voice_type": "voice_cloning",
    "voice_id": "VOICE_ID_TO_DELETE"
  }'
```
